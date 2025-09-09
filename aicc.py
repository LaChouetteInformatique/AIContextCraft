import argparse
import datetime
import os
import ast
import io
import sys
import tokenize
import logging
from pathlib import Path
import yaml
import pathspec
import fnmatch

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

# --- Fonctions de traitement des fichiers ---

# CORRIGÉ : Nouvelle version robuste utilisant 'ast'
def strip_comments_from_code(content, file_path):
    """
    Supprime les commentaires et les docstrings d'un fichier de code.
    Utilise 'ast' pour une suppression robuste en Python.
    """
    file_ext = Path(file_path).suffix
    
    if file_ext == '.py':
        try:
            tree = ast.parse(content)
            class DocstringRemover(ast.NodeTransformer):
                def _remove_docstring(self, node):
                    if not node.body: return
                    first_node = node.body[0]
                    if isinstance(first_node, ast.Expr):
                        if isinstance(getattr(first_node.value, 'value', None), str): # Python 3.8+
                             node.body = node.body[1:]
                        elif isinstance(first_node.value, ast.Str): # Python < 3.8
                             node.body = node.body[1:]

                def visit_Module(self, node):
                    self._remove_docstring(node)
                    self.generic_visit(node)
                    return node

                def visit_FunctionDef(self, node):
                    self._remove_docstring(node)
                    self.generic_visit(node)
                    return node

                visit_AsyncFunctionDef = visit_FunctionDef
                visit_ClassDef = visit_FunctionDef

            transformer = DocstringRemover()
            new_tree = transformer.visit(tree)
            ast.fix_missing_locations(new_tree)
            return ast.unparse(new_tree)

        except (SyntaxError, Exception):
            logging.warning(f"  -> AVERTISSEMENT: Impossible de parser/stripper les commentaires de {file_path}. Fichier inclus tel quel.")
            return content

    elif file_ext in ('.sh', '.bash') or 'Dockerfile' in Path(file_path).name:
        return "\n".join([line for line in content.splitlines() if not line.strip().startswith('#')])
    
    return content

def get_python_headers(content, full_body_filters_patterns):
    try:
        tree = ast.parse(content)
    except Exception as e:
        return f"# ERREUR: Impossible de parser le fichier Python: {e}\n{content}"
    output_lines = []
    def should_keep_full_body(name):
        return any(fnmatch.fnmatch(name, pattern) for pattern in full_body_filters_patterns)
    def format_signature(node, indent=""):
        lines = [f"{indent}@{ast.unparse(decorator)}" for decorator in getattr(node, 'decorator_list', [])]
        prefix = indent
        if isinstance(node, ast.AsyncFunctionDef): prefix += "async def"
        elif isinstance(node, ast.FunctionDef): prefix += "def"
        elif isinstance(node, ast.ClassDef): prefix += "class"
        name = node.name
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = ast.unparse(node.args)
            return_annotation = f" -> {ast.unparse(node.returns)}" if node.returns else ""
            lines.append(f"{prefix} {name}({args}){return_annotation}:")
        elif isinstance(node, ast.ClassDef):
            bases = [ast.unparse(b) for b in node.bases]
            keywords = [f"{k.arg}={ast.unparse(k.value)}" for k in node.keywords]
            lines.append(f"{prefix} {name}({', '.join(bases + keywords)}):")
        return "\n".join(lines)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if should_keep_full_body(node.name):
                output_lines.append(ast.get_source_segment(content, node))
                continue
            output_lines.append(format_signature(node))
            docstring = ast.get_docstring(node)
            if docstring: output_lines.append(f'    """{docstring}"""')
            if isinstance(node, ast.ClassDef):
                has_methods = False
                for method_node in node.body:
                    if isinstance(method_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        has_methods = True
                        output_lines.append("\n" + format_signature(method_node, indent="    "))
                        method_docstring = ast.get_docstring(method_node)
                        if method_docstring: output_lines.append(f'        """{method_docstring}"""')
                        output_lines.append("        pass")
                if not docstring and not has_methods: output_lines.append("    pass")
            else:
                output_lines.append("    pass")
            output_lines.append("")
    return "\n".join(output_lines)

# --- Fonctions utilitaires ---

def setup_logging(log_file_path, verbose):
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO if verbose else logging.WARNING)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

def generate_tree(directory, include_spec, exclude_spec):
    tree_lines = [f"Arbre du projet : {directory.resolve()}"]
    def is_path_visible(path):
        relative_p = str(path.relative_to(directory))
        return include_spec.match_file(relative_p) and not exclude_spec.match_file(relative_p)
    paths = sorted([p for p in directory.rglob('*') if is_path_visible(p)])
    last_in_level = {}
    for path in paths:
        relative_path = path.relative_to(directory)
        depth = len(relative_path.parts)
        try:
            siblings = [p for p in sorted(path.parent.iterdir()) if is_path_visible(p)]
            is_last = path.name == siblings[-1].name if siblings else True
        except IndexError: is_last = True
        last_in_level[depth - 1] = is_last
        indent = "".join(["    " if last_in_level.get(i) else "│   " for i in range(depth - 1)])
        connector = "└── " if is_last else "├── "
        tree_lines.append(f"{indent}{connector}{path.name}{'/' if path.is_dir() else ''}")
    return "\n".join(tree_lines)

def format_bytes(size):
    if size < 1024: return f"{size} B"
    for unit in ['KB', 'MB', 'GB', 'TB']:
        size /= 1024.0
        if size < 1024.0: return f"{size:.2f} {unit}"
    return f"{size:.2f} PB"

def get_file_stats(content_str, encoding='utf-8'):
    total_bytes = len(content_str.encode(encoding))
    formatted_size = format_bytes(total_bytes)
    tokens = "N/A"
    if TIKTOKEN_AVAILABLE:
        try:
            encoding_tiktoken = tiktoken.get_encoding("cl100k_base")
            tokens = len(encoding_tiktoken.encode(content_str))
        except Exception: tokens = "Erreur"
    return f"Taille: {formatted_size} ({total_bytes:,} octets), Tokens (estim.): {tokens}"

# --- Fonction principale ---

def main():
    parser = argparse.ArgumentParser(description="Agrège les fichiers d'un projet en un seul fichier texte pour une IA.")
    parser.add_argument('-c', '--config', type=str, help="Chemin vers le fichier de configuration YAML.")
    parser.add_argument('-p', '--project', type=str, help="Chemin vers le projet cible.")
    parser.add_argument('-o', '--output', type=str, help="Chemin vers le fichier de sortie.")
    parser.add_argument('--no-timestamp', action='store_true', help="Ne pas ajouter de timestamp au nom du fichier de sortie.")
    parser.add_argument('--strip-comments', action='store_true', help="Supprimer les commentaires des fichiers.")
    parser.add_argument('--headers-only', action='store_true', help="Ne conserver que les signatures de fonctions/méthodes.")
    parser.add_argument('--dry-run', action='store_true', help="Simule l'opération sans écrire de fichier.")
    parser.add_argument('--encoding', type=str, default='utf-8', help="Encodage des fichiers (défaut: utf-8).")
    parser.add_argument('--use-gitignore', action='store_true', help="Utilise le .gitignore du projet pour filtrer les fichiers.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Affiche des informations détaillées sur la console.")
    args = parser.parse_args()

    DEFAULT_CONFIG = {
        'output_path': './build/project_context.txt',
        'include_patterns': ['**/*'], # CORRIGÉ : Pattern récursif par défaut
        'common_filters': ['__pycache__/', '*.pyc', '.git/', '.venv/', 'venv/', 'node_modules/', 'build/', 'dist/', '.idea/', '.vscode/'],
        'project_only_filters': [],
        'tree_only_filters': ['*.md', 'LICENSE', '.gitignore', 'config.yaml'],
        'full_body_filters': ['main', 'run_app', 'settings', 'configure_*']
    }

    config = DEFAULT_CONFIG.copy()
    script_dir = Path(__file__).resolve().parent
    config_path = Path(args.config or script_dir / 'config.yaml')

    if config_path.exists():
        try:
            with open(config_path, 'r', encoding=args.encoding) as f:
                config.update(yaml.safe_load(f) or {})
        except yaml.YAMLError as e:
            sys.exit(f"ERREUR: Impossible de parser le fichier de configuration '{config_path}': {e}")

    project_path = Path(args.project or config.get('project_path', '.')).resolve()
    output_path_str = args.output or config.get('output_path')
    
    output_path = Path(output_path_str)
    if not args.no_timestamp:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_path.with_name(f"{output_path.stem}_{timestamp}{output_path.suffix}")

    log_path = output_path.with_suffix('.log')
    setup_logging(log_path, args.verbose)

    if args.dry_run: print("--- MODE DRY RUN ACTIVÉ : AUCUN FICHIER NE SERA ÉCRIT ---")
    if not config_path.exists():
        with open(config_path, 'w', encoding=args.encoding) as f: yaml.dump(DEFAULT_CONFIG, f, sort_keys=False, allow_unicode=True)
        logging.info(f"Fichier de configuration par défaut créé à '{config_path}'")
    else:
        logging.info(f"Configuration chargée et fusionnée depuis '{config_path}'")

    logging.info("Assemblage des filtres...")
    def clean_patterns(patterns):
        if not patterns:  # Gère None et les listes vides
            return []
        return [p for p in patterns if p and p.strip()]

    # On s'assure que même si la clé existe mais est vide (None), on a une liste
    include_patterns = clean_patterns(config.get('include_patterns') or ['**/*'])
    common_filters = clean_patterns(config.get('common_filters') or [])
    project_only_filters = clean_patterns(config.get('project_only_filters') or [])
    tree_only_filters = clean_patterns(config.get('tree_only_filters') or [])
    full_body_filters = config.get('full_body_filters') or [] # Correction ajoutée ici aussi

    final_project_filters = common_filters + project_only_filters
    final_tree_filters = common_filters + tree_only_filters

    output_path_base = Path(output_path_str).stem
    auto_exclude_pattern = f'{output_path_base}*'
    final_project_filters.append(auto_exclude_pattern)
    final_tree_filters.append(auto_exclude_pattern)
    
    if args.use_gitignore:
        gitignore_path = project_path / '.gitignore'
        if gitignore_path.is_file():
            logging.info(f"Utilisation des filtres de {gitignore_path}")
            with open(gitignore_path, 'r', encoding=args.encoding) as f:
                gitignore_patterns = clean_patterns(f.read().splitlines())
                final_project_filters.extend(gitignore_patterns)
                final_tree_filters.extend(gitignore_patterns)

    include_spec = pathspec.PathSpec.from_lines('gitwildmatch', include_patterns)
    project_exclude_spec = pathspec.PathSpec.from_lines('gitwildmatch', final_project_filters)
    tree_exclude_spec = pathspec.PathSpec.from_lines('gitwildmatch', final_tree_filters)

    logging.info("Génération de l'arbre du projet...")
    project_tree = generate_tree(project_path, include_spec, tree_exclude_spec)
    
    print("Concaténation des fichiers...")
    all_files_content = []
    
    logging.info("Étape 1: Sélection des fichiers à inclure...")
    all_potential_files = sorted([p for p in project_path.rglob('*') if p.is_file()])
    included_files = [p for p in all_potential_files if include_spec.match_file(str(p.relative_to(project_path)))]
    logging.info(f"{len(included_files)} fichiers correspondent aux patterns d'inclusion.")

    logging.info("Étape 2: Application des filtres d'exclusion...")
    final_file_list = [p for p in included_files if not project_exclude_spec.match_file(str(p.relative_to(project_path)))]
    logging.info(f"{len(final_file_list)} fichiers restants après exclusion.")

    for file_path in final_file_list:
        relative_path_str = str(file_path.relative_to(project_path))
        try:
            with open(file_path, 'r', encoding=args.encoding, errors='ignore') as f: content = f.read()
            logging.info(f"  -> Traitement de : {relative_path_str}")
            
            # CORRIGÉ : Logique de priorité entre --headers-only et --strip-comments
            if args.headers_only and file_path.suffix == '.py':
                content = get_python_headers(content, full_body_filters)
            elif args.strip_comments:
                content = strip_comments_from_code(content, file_path)
            
            header = f"\n{'='*80}\n--- FICHIER: {relative_path_str}\n{'='*80}\n\n"
            all_files_content.append(header + content)
        except IOError as e:
            logging.error(f"  -> ERREUR: Impossible de lire {relative_path_str}. Erreur: {e}")

    logging.info("Assemblage du fichier de sortie...")
    body_content_str = "".join(all_files_content)
    full_body = project_tree + "\n\n" + "-"*80 + "\nCONTENU DES FICHIERS\n" + "-"*80 + "\n\n" + body_content_str
    
    stats = get_file_stats(full_body, args.encoding)
    
    final_output_str = "".join([
        "Ce fichier est une concaténation de plusieurs fichiers sources d'un projet.\n",
        f"Date de génération : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"Statistiques du contenu : {stats}\n\n",
        full_body
    ])
    
    if not args.dry_run:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding=args.encoding) as f: f.write(final_output_str)
        print("\nOpération terminée.")
        print(f"Fichier de sortie généré : {output_path.resolve()}")
    else:
        print("\nOpération (dry run) terminée.")
        print(f"Le fichier de sortie aurait été : {output_path.resolve()}")

    print(f"Fichier de log généré : {log_path.resolve()}")
    print(f"Statistiques finales : {stats}")

if __name__ == '__main__':
    main()