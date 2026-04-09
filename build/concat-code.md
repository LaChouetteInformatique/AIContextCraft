Ce fichier est une concaténation de plusieurs fichiers sources d'un projet.
Date de génération : 2026-04-09 19:57:41
Statistiques du contenu : Taille: 68.07 KB (69,706 octets), Tokens (estim.): 15326

Arbre du projet : /home/lachouette/AIContextCraft
├── .gitignore
├── LICENSE
├── README.md
├── ROADMAP.md
├── aicc.bak.py
├── aicc.py
├── build/
├── config.yaml
├── requirements.txt
└── tests/
    ├── setup_tests.sh
    ├── test_aicc.py
    └── test_projects/
        ├── basic_project/
        │   ├── .gitignore
        │   ├── app/
        │   │   └── main.py
        │   ├── config.yaml
        │   ├── expected_output.txt
        │   └── utils.py
        └── strip_comments_project/
            ├── code_with_comments.py
            └── expected_output.txt

--------------------------------------------------------------------------------
CONTENU DES FICHIERS
--------------------------------------------------------------------------------


================================================================================
--- FICHIER: .gitignore
================================================================================

# ================================================================= #
# AI Context Craft - .gitignore                                     #
# ================================================================= #

# ─────────────────────────────────────────────────────────────────
# Python
# ─────────────────────────────────────────────────────────────────

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual Environments
*venv/
.venv/
env/
.env/
ENV/
env.bak/
venv.bak/
virtualenv/
.virtualenv/

# Distribution / packaging
.Python
build/*
!build/.gitkeep
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# ─────────────────────────────────────────────────────────────────
# Testing & Coverage
# ─────────────────────────────────────────────────────────────────

# Test results (but keep the directory structure)
tests/test-results/*
!tests/test-results/.gitkeep

# Pytest
.pytest_cache/
.tox/
.nox/
.coverage
.coverage.*
htmlcov/
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
junit.xml

# Test outputs
*.log
test-output/
test-reports/

# ─────────────────────────────────────────────────────────────────
# AI Context Craft specific outputs
# ─────────────────────────────────────────────────────────────────

# Generated concatenation files (default pattern)
project_files_*.txt
project_tree_*.txt
concat_*.txt

# Build directory (where outputs go by default)
build/*
!build/.gitkeep

# But allow example outputs for documentation
!examples/sample_output.txt

# ─────────────────────────────────────────────────────────────────
# IDE and Editors
# ─────────────────────────────────────────────────────────────────

# VSCode
.vscode/
*.code-workspace
.history/

# PyCharm
.idea/
*.iml
*.ipr
*.iws

# Sublime Text
*.sublime-project
*.sublime-workspace

# Vim
[._]*.s[a-v][a-z]
[._]*.sw[a-p]
[._]s[a-rt-v][a-z]
[._]ss[a-gi-z]
[._]sw[a-p]
*.un~
Session.vim
.netrwhist
*~

# Emacs
\#*\#
/.emacs.desktop
/.emacs.desktop.lock
*.elc
auto-save-list
tramp
.\#*

# ─────────────────────────────────────────────────────────────────
# Operating System
# ─────────────────────────────────────────────────────────────────

# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon
._*
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk

# Windows
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db
*.stackdump
[Dd]esktop.ini
$RECYCLE.BIN/
*.cab
*.msi
*.msix
*.msm
*.msp
*.lnk

# Linux
.directory
.Trash-*
.nfs*

# ─────────────────────────────────────────────────────────────────
# Environment & Secrets
# ─────────────────────────────────────────────────────────────────

# Environment variables
.env
.env.*
!.env.example
!.env.template

# Secrets
*.key
*.pem
*.cert
secrets/
credentials/

# ─────────────────────────────────────────────────────────────────
# Dependencies
# ─────────────────────────────────────────────────────────────────

# Node (if frontend is added later)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# ─────────────────────────────────────────────────────────────────
# Docker
# ─────────────────────────────────────────────────────────────────

# Docker volumes (local development)
.docker-volumes/

# Temporary Dockerfiles created by tests
tests/.dockerfile.test
*.dockerfile.tmp

# ─────────────────────────────────────────────────────────────────
# Backup and Temporary files
# ─────────────────────────────────────────────────────────────────

# Backups
*.bak
*.backup
*.old
*.orig
*.tmp
*.temp
backup-*.tar.gz

# Temporary files
tmp/
temp/
*.swp
*.swo

/todo.sh

# ─────────────────────────────────────────────────────────────────
# Documentation build
# ─────────────────────────────────────────────────────────────────

# Sphinx documentation
docs/_build/
docs/_static/
docs/_templates/

# MkDocs
site/

# ─────────────────────────────────────────────────────────────────
# Project specific (adjust as needed)
# ─────────────────────────────────────────────────────────────────

# Local configuration overrides (but keep examples)
concat-config.local.yaml
config.local.yaml

# User-specific test configurations
tests/test-config.local.yaml

# Analysis outputs for AI (generated files)
ai-analysis.txt
ai-report.txt
debug.txt
context.txt

# Performance profiling
*.prof
*.stats
.profiling/

/notes/

# ─────────────────────────────────────────────────────────────────
# Keep these files/folders
# ─────────────────────────────────────────────────────────────────

# Keep empty directories with .gitkeep
!**/.gitkeep

# Keep example/template files
!.env.example
!concat-config.example.yaml
!tests/test-project/**

# Keep documentation
!*.md
!LICENSE
!requirements*.txt

# Keep CI/CD configurations
!.github/**
!.gitlab-ci.yml
!.travis.yml
================================================================================
--- FICHIER: ROADMAP.md
================================================================================

# **AI Context Craft : Document d'Évolution et Roadmap**

## 1. Vision et Mission

**Vision :** Un outil à la fois simple et puissant pour les développeurs qui préparent des bases de code pour une analyse par des Grands Modèles de Langage (LLM).

**Mission :** Offrir un contrôle granulaire, une performance élevée et des fonctionnalités intelligentes pour créer le contexte le plus pertinent et concis possible, optimisant ainsi l'efficacité des interactions avec l'IA.

## 2. État Actuel (v1.0 - Baseline)

*   **Gestion de la Configuration :** Configuration complète via un fichier `config.yaml`.
*   **Filtrage à Deux Étapes :** Logique puissante d'inclusion prioritaire (`include_patterns`) suivie par une exclusion (`common_filters`, etc.).
*   **Traitement de Code Python Avancé :**
    *   Suppression des commentaires et docstrings basée sur l'AST, garantissant une grande fiabilité (`--strip-comments`).
    *   Extraction des en-têtes et docstrings pour un contexte de haut niveau (`--headers-only`).
*   **Génération d'Arborescence :** Visualisation claire de la structure du projet, respectant les filtres.
*   **Utilitaires :** Logging, gestion des timestamps, calcul de statistiques (taille, tokens), et support du `.gitignore`.

## 3. Architecture Cible (v2.0 - Le Refactoring)

L'objectif principal est de passer d'un script monolithique à une architecture modulaire pour garantir la maintenabilité, la testabilité et l'évolutivité du projet.

#### Structure de Projet Proposée :

```
ai-context-craft/
├── main.py                  # Point d'entrée, orchestrateur principal
├── config.yaml              # Fichier de configuration
|
└── craft/                   # Package contenant la logique métier
    ├── __init__.py
    ├── config_manager.py    # Chargement, validation et fusion de la configuration.
    ├── file_processor.py    # Fonctions de traitement de contenu (strip_comments, get_headers).
    ├── filter_manager.py    # Logique d'assemblage des patterns d'inclusion/exclusion.
    ├── tree_generator.py    # Logique de génération de l'arborescence.
    └── utils.py             # Fonctions utilitaires transverses (logging, stats, etc.).
```

#### Bénéfices :

*   **Principe de Responsabilité Unique :** Chaque module a un rôle clair.
*   **Facilité de Test :** Permet d'écrire des tests unitaires pour chaque composant isolé.
*   **Lisibilité :** `main.py` devient un flux de travail de haut niveau, facile à comprendre.

---

## 4. Backlog des Fonctionnalités

### Catégorie A : Expérience Utilisateur & Améliorations de Base

1.  **A1. Barre de Progression :**
    *   **Quoi :** Afficher une barre de progression (`tqdm`) lors de la concaténation des fichiers.
    *   **Pourquoi :** Fournir un retour visuel sur les projets volumineux et améliorer l'expérience utilisateur.

2.  **A2. Copie vers le Presse-papiers :**
    *   **Quoi :** Ajouter une option `--clipboard` pour copier la sortie directement dans le presse-papiers.
    *   **Pourquoi :** Fluidifier radicalement le workflow de l'utilisateur (Générer -> Coller).

3.  **A3. Gestion Robuste des Encodages :**
    *   **Quoi :** Remplacer `errors='ignore'` par une détection d'encodage (ex: `chardet`) ou, à défaut, logger un avertissement clair en cas d'échec de décodage.
    *   **Pourquoi :** Augmenter la fiabilité sur des projets hétérogènes.

### Catégorie B : Extension des Capacités

1.  **B1. Support Multi-langage pour le `strip-comments` :**
    *   **Quoi :** Étendre la fonction `strip_comments_from_code` pour gérer les commentaires `//`, `/* ... */` (JS, TS, Java, C++, CSS) et `<!-- ... -->` (HTML/XML).
    *   **Pourquoi :** Rendre l'outil universel et indispensable pour tout type de projet.

2.  **B2. Profils de Configuration :**
    *   **Quoi :** Permettre de définir des profils nommés dans `config.yaml` (ex: `frontend`, `backend`) que l'on peut activer via une option CLI (`--profile frontend`). Chaque profil aurait ses propres `include_patterns`.
    *   **Pourquoi :** Simplifier l'utilisation sur des monorepos ou des projets full-stack.

3.  **B3. Fractionnement Automatique de la Sortie :**
    *   **Quoi :** Ajouter une option `--max-tokens <N>` qui divise la sortie en plusieurs fichiers numérotés si le contexte dépasse N tokens.
    *   **Pourquoi :** Gérer les projets trop grands pour la fenêtre de contexte d'un LLM.

### Catégorie C : Contexte "Intelligent" & Intégration Git

1.  **C1. Intégration Git `diff` :**
    *   **Quoi :** Créer une option `--git-diff <branche>` pour ne traiter que les fichiers modifiés ou ajoutés par rapport à une branche de référence (ex: `main`).
    *   **Pourquoi :** **Fonctionnalité majeure.** Idéale pour les revues de code, la génération de descriptions de Pull Request ou le débuggage de nouvelles fonctionnalités.

2.  **C2. Priorisation Intelligente des Tokens :**
    *   **Quoi :** En conjonction avec `--max-tokens`, développer une logique qui, pour rester sous la limite, passe automatiquement certains fichiers en mode `--headers-only` en se basant sur des heuristiques (ex: fichiers les moins récemment modifiés, fichiers dans `tests/`).
    *   **Pourquoi :** Produire le meilleur contexte possible sous une contrainte de taille.

---

## 5. Roadmap Évolutive

### **Phase 0 : Fondation - Le Grand Refactoring (Prérequis)**

*   **Objectif :** Établir une base de code saine pour l'avenir.
*   **Tâches :**
    1.  Créer la nouvelle structure de dossiers (`craft/`).
    2.  Migrer la logique existante dans les modules dédiés (`config_manager.py`, `file_processor.py`, etc.).
    3.  Adapter `main.py` pour qu'il agisse en tant qu'orchestrateur.
    4.  S'assurer que toutes les fonctionnalités existantes fonctionnent parfaitement après le refactoring.

### **Phase 1 : L'Expérience "Pro" (Améliorations UX)**

*   **Objectif :** Rendre l'outil plus agréable et plus rapide à utiliser au quotidien.
*   **Tâches :**
    1.  Implémenter la barre de progression (**A1**).
    2.  Implémenter la copie vers le presse-papiers (**A2**).
    3.  Améliorer la gestion des encodages (**A3**).

### **Phase 2 : L'Outil Universel (Extension des capacités)**

*   **Objectif :** Faire de l'outil un compagnon indispensable pour tous types de projets.
*   **Tâches :**
    1.  Ajouter le support multi-langage pour la suppression des commentaires (**B1**).
    2.  Mettre en place le système de profils de configuration (**B2**).
    3.  Introduire le fractionnement automatique de la sortie par tokens (**B3**).

### **Phase 3 : Le Saut vers l'Intelligence (Intégration Git)**

*   **Objectif :** Transformer l'outil d'un simple "concaténateur" à un véritable "assistant de contexte".
*   **Tâches :**
    1.  Implémenter l'intégration avec `git diff` (**C1**). C'est le jalon principal de cette phase.
    2.  (Optionnel) Commencer à explorer la priorisation intelligente des tokens (**C2**).
================================================================================
--- FICHIER: aicc.bak.py
================================================================================

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
        relative_p = str(path.relative_to(directory)).replace('\\', '/')
        return include_spec.match_file(relative_p) and not exclude_spec.match_file(relative_p)

    # Étape 1 : Obtenir tous les chemins (fichiers ET dossiers) qui correspondent aux filtres
    visible_paths = {p for p in directory.rglob('*') if is_path_visible(p)}

    # Étape 2 (LA CORRECTION CLÉ) : S'assurer que tous les dossiers parents des
    # chemins visibles sont également inclus dans l'ensemble à dessiner.
    paths_for_tree = set(visible_paths)
    for path in visible_paths:
        parent = path.parent
        while parent != directory:
            paths_for_tree.add(parent)
            parent = parent.parent

    # Étape 3 : Trier et dessiner l'arbre comme avant
    paths = sorted(list(paths_for_tree))
    
    last_in_level = {}
    for path in paths:
        relative_path = path.relative_to(directory)
        depth = len(relative_path.parts)
        
        # Pour déterminer si un élément est le dernier, on ne considère que ses "frères"
        # qui sont aussi dans la liste finale à dessiner.
        try:
            siblings_in_tree = [p for p in sorted(path.parent.iterdir()) if p in paths_for_tree]
            is_last = (path == siblings_in_tree[-1]) if siblings_in_tree else True
        except (IndexError, FileNotFoundError):
            is_last = True
        
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

    logging.info("="*50)
    logging.info("CONFIGURATION FINALE DES FILTRES DE DÉBOGAGE")
    logging.info(f"  - PATTERNS D'INCLUSION: {include_patterns}")
    logging.info(f"  - FILTRES D'EXCLUSION (CONTENU): {final_project_filters}")
    logging.info("="*50)

    logging.info("Génération de l'arbre du projet...")
    project_tree = generate_tree(project_path, include_spec, tree_exclude_spec)
    
    print("Concaténation des fichiers...")
    all_files_content = []
    
    logging.info("Étape 1: Sélection des fichiers à inclure...")
    all_potential_files = sorted([p for p in project_path.rglob('*') if p.is_file()])
    included_files = [
        p for p in all_potential_files 
        if include_spec.match_file(str(p.relative_to(project_path)).replace('\\', '/'))
    ]
    logging.info(f"{len(included_files)} fichiers correspondent aux patterns d'inclusion.")

    logging.info("--- LISTE DES FICHIERS PASSANT LE FILTRE D'INCLUSION ---")
    for p in included_files:
        logging.info(f"  [INCLUS] {str(p.relative_to(project_path)).replace('\\', '/')}")
    logging.info("--- FIN DE LA LISTE ---")

    logging.info("Étape 2: Application des filtres d'exclusion...")
    final_file_list = [
        p for p in included_files 
        if not project_exclude_spec.match_file(str(p.relative_to(project_path)).replace('\\', '/'))
    ]
    logging.info(f"{len(final_file_list)} fichiers restants après exclusion.")

    excluded_files_for_log = set(included_files) - set(final_file_list)
    logging.info("--- LISTE DES FICHIERS RETIRÉS PAR LE FILTRE D'EXCLUSION ---")
    if not excluded_files_for_log:
        logging.info("  (Aucun)")
    else:
        for p in sorted(list(excluded_files_for_log)):
             logging.info(f"  [EXCLUS] {str(p.relative_to(project_path)).replace('\\', '/')}")
    logging.info("--- FIN DE LA LISTE ---")

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
================================================================================
--- FICHIER: aicc.py
================================================================================

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
    # Correction pour éviter les handlers dupliqués si la fonction est appelée plusieurs fois
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
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

# <<< MODIFICATION : La fonction generate_tree est maintenant optimisée avec os.walk pour élaguer les dossiers exclus.
def generate_tree(directory, include_spec, exclude_spec):
    tree_lines = [f"Arbre du projet : {directory.resolve()}"]
    
    paths_for_tree = set()

    for root, dirs, files in os.walk(directory, topdown=True):
        root_path = Path(root)
        
        # Logique d'élagage : on retire de la liste `dirs` les dossiers à exclure
        # pour que os.walk ne les visite pas.
        excluded_dirs = []
        for d in dirs:
            dir_path_str = str((root_path / d).relative_to(directory)).replace('\\', '/')
            if exclude_spec.match_file(dir_path_str) or exclude_spec.match_file(dir_path_str + '/'):
                excluded_dirs.append(d)
        
        for d in excluded_dirs:
            dirs.remove(d)

        # On traite les dossiers et fichiers restants
        for name in dirs + files:
            item_path = root_path / name
            relative_p_str = str(item_path.relative_to(directory)).replace('\\', '/')
            if include_spec.match_file(relative_p_str) and not exclude_spec.match_file(relative_p_str):
                paths_for_tree.add(item_path)

    # Assurer que les dossiers parents des chemins visibles sont inclus
    final_paths_for_tree = set(paths_for_tree)
    for path in paths_for_tree:
        parent = path.parent
        while parent and parent != directory:
            final_paths_for_tree.add(parent)
            parent = parent.parent

    # Trier et dessiner l'arbre
    paths = sorted(list(final_paths_for_tree))
    
    last_in_level = {}
    for path in paths:
        if path == directory: continue # Ne pas dessiner la racine elle-même dans l'arbre
        relative_path = path.relative_to(directory)
        depth = len(relative_path.parts)
        
        try:
            siblings_in_tree = [p for p in sorted(path.parent.iterdir()) if p in final_paths_for_tree]
            is_last = (path == siblings_in_tree[-1]) if siblings_in_tree else True
        except (IndexError, FileNotFoundError):
            is_last = True
        
        last_in_level[depth - 1] = is_last
        
        indent = "".join(["    " if last_in_level.get(i) else "│   " for i in range(depth - 1)])
        connector = "└── " if is_last else "├── "
        
        tree_lines.append(f"{indent}{connector}{path.name}{'/' if path.is_dir() else ''}")

    return "\n".join(tree_lines)
# <<< FIN MODIFICATION

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
        except Exception as e:
            # AJOUT : Affiche l'erreur réelle dans la console pour comprendre
            logging.error(f"Erreur Tiktoken : {e}") 
            tokens = "Erreur"
    return f"Taille: {formatted_size} ({total_bytes:,} octets), Tokens (estim.): {tokens}"

# --- Fonction principale ---

def main():
    parser = argparse.ArgumentParser(description="Agrège les fichiers d'un projet en un seul fichier texte pour une IA.")
    # ... (les arguments n'ont pas changé) ...
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
        'include_patterns': ['**/*'],
        'common_filters': ['__pycache__/', '*.pyc', '.git/', '.venv/', 'venv/', 'node_modules/', 'build/', 'dist/', '.idea/', '.vscode/'],
        'project_only_filters': [],
        'tree_only_filters': ['*.md', 'LICENSE', '.gitignore', 'config.yaml'],
        'full_body_filters': ['main', 'run_app', 'settings', 'configure_*']
    }
    
    # ... (la logique de configuration n'a pas changé) ...
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
        if not patterns:
            return []
        return [p for p in patterns if p and p.strip()]

    include_patterns = clean_patterns(config.get('include_patterns') or ['**/*'])
    common_filters = clean_patterns(config.get('common_filters') or [])
    project_only_filters = clean_patterns(config.get('project_only_filters') or [])
    tree_only_filters = clean_patterns(config.get('tree_only_filters') or [])
    full_body_filters = config.get('full_body_filters') or []

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

    logging.info("="*50)
    logging.info("CONFIGURATION FINALE DES FILTRES DE DÉBOGAGE")
    logging.info(f"  - PATTERNS D'INCLUSION: {include_patterns}")
    logging.info(f"  - FILTRES D'EXCLUSION (CONTENU): {final_project_filters}")
    logging.info(f"  - FILTRES D'EXCLUSION (ARBRE): {final_tree_filters}")
    logging.info("="*50)

    logging.info("Génération de l'arbre du projet (version optimisée)...")
    project_tree = generate_tree(project_path, include_spec, tree_exclude_spec)
    
    print("Concaténation des fichiers...")
    all_files_content = []
    
    # <<< MODIFICATION : Remplacement de la recherche de fichiers en deux étapes par une seule boucle optimisée.
    logging.info("Recherche optimisée des fichiers (avec élagage des dossiers exclus)...")
    final_file_list = []
    for root, dirs, files in os.walk(project_path, topdown=True):
        # Élagage des dossiers exclus pour que os.walk ne les visite pas.
        # On modifie la liste `dirs` en place.
        excluded_dirs = []
        for d in dirs:
            # On vérifie le chemin relatif du dossier. ex: 'node_modules/'
            dir_path_str = str((Path(root) / d).relative_to(project_path)).replace('\\', '/')
            if project_exclude_spec.match_file(dir_path_str) or project_exclude_spec.match_file(dir_path_str + '/'):
                excluded_dirs.append(d)
        
        for d in excluded_dirs:
            dirs.remove(d)

        # Traitement des fichiers dans le dossier courant (qui n'est pas exclus)
        for filename in files:
            file_path = Path(root) / filename
            relative_path_str = str(file_path.relative_to(project_path)).replace('\\', '/')
            
            # Un fichier est inclus s'il correspond aux inclusions ET ne correspond PAS aux exclusions.
            if include_spec.match_file(relative_path_str) and not project_exclude_spec.match_file(relative_path_str):
                final_file_list.append(file_path)

    final_file_list.sort() # Trier la liste pour un traitement ordonné
    logging.info(f"{len(final_file_list)} fichiers finaux trouvés après filtrage optimisé.")
    logging.info("--- LISTE DES FICHIERS À TRAITER ---")
    for p in final_file_list:
        logging.info(f"  [INCLUS] {str(p.relative_to(project_path)).replace('\\', '/')}")
    logging.info("--- FIN DE LA LISTE ---")
    # <<< FIN MODIFICATION

    for file_path in final_file_list:
        relative_path_str = str(file_path.relative_to(project_path))
        try:
            with open(file_path, 'r', encoding=args.encoding, errors='ignore') as f: content = f.read()
            logging.info(f"  -> Traitement de : {relative_path_str}")
            
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
================================================================================
--- FICHIER: config.yaml
================================================================================

# Chemin par défaut pour le fichier de sortie.
output_path: "./build/project_context.txt"

# --- SÉLECTION DES FICHIERS ---

# ÉTAPE 1: INCLUSION (prioritaire)
# Seuls les fichiers et dossiers correspondant à ces patterns seront considérés.
# Le pattern '**/*' signifie "tous les fichiers dans tous les sous-dossiers".
# Exemples :
#   - ['src/', 'tests/', 'README.md'] pour ne prendre que le contenu de 'src', 'tests' et le fichier README.
#   - ['*.py', 'requirements.txt'] pour ne prendre que les fichiers Python et le fichier requirements.
include_patterns:
  - '**/*'

# ÉTAPE 2: EXCLUSION
# Parmi les fichiers inclus à l'étape 1, ceux qui correspondent à ces patterns
# seront retirés.

# Filtres communs : s'appliquent PARTOUT (arbre et contenu des fichiers).
# Idéal pour exclure les dépendances, les builds, les caches, etc.
common_filters:
  - "__pycache__/"
  - "*.pyc"
  - ".git/"
  - ".venv/"
  - "venv/"
  - "node_modules/"
  - "build/"
  - "dist/"
  - ".idea/"
  - ".vscode/"

# Filtres spécifiques au contenu : N'exclut que du contenu des fichiers,
# mais le fichier/dossier APPARAÎTRA dans l'arbre.
project_only_filters:
  - ""

# Filtres spécifiques à l'arbre : N'exclut que de l'affichage de l'arbre.
# Le contenu de ces fichiers SERA INCLUS dans la sortie finale.
tree_only_filters:
  - ""
  # - "*.md"
  # - "LICENSE"
  # - ".gitignore"
  # - "config.yaml"

# --- OPTIONS AVANCÉES ---

# Pour l'option --headers-only, les fonctions/classes dont le nom correspond
# à ces patterns seront incluses intégralement.
full_body_filters:
  - "main"
  - "run_app"
  - "settings"
  - "configure_*"
================================================================================
--- FICHIER: requirements.txt
================================================================================

pyyaml
tiktoken
pathspec
pytest
================================================================================
--- FICHIER: tests/setup_tests.sh
================================================================================

#!/usr/bin/env bash

# ================================================================= #
# Script de Génération des Projets de Test pour AI Context Craft    #
#                                                                   #
# Utilisation :                                                     #
#   1. ./setup_tests.sh              : Crée/réinitialise les projets de test.
#   2. ./setup_tests.sh --golden-files : Crée les projets ET génère les
#                                      fichiers "expected_output.txt".
# ================================================================= #

# Arrête le script immédiatement si une commande échoue
set -e

# --- Configuration et Couleurs ---
# Se positionne dans le répertoire du script pour que les chemins relatifs fonctionnent
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."
TEST_PROJECTS_ROOT="$SCRIPT_DIR/test_projects"
AICC_SCRIPT="$PROJECT_ROOT/aicc.py"

# Couleurs pour un affichage plus clair
COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_NC='\033[0m' # No Color

# --- Fonctions de création des projets ---

# Scénario 1 : Un projet simple pour tester la concaténation de base
create_basic_project() {
    local project_dir="$TEST_PROJECTS_ROOT/basic_project"
    echo -e "${COLOR_BLUE}--> Création du projet de test : 'basic_project'${COLOR_NC}"
    
    # Nettoyer l'ancien projet s'il existe
    rm -rf "$project_dir"
    mkdir -p "$project_dir/app"

    # Créer les fichiers avec leur contenu via "here documents"
    cat << 'EOF' > "$project_dir/config.yaml"
# Configuration simple pour le test
include_patterns:
  - '**/*'
common_filters:
  - ".git/"
  - "build/"
tree_only_filters: []
EOF

    cat << 'EOF' > "$project_dir/.gitignore"
# Fichier à ignorer
ignored_file.txt
__pycache__/
EOF

    cat << 'EOF' > "$project_dir/app/main.py"
# main.py
import utils

def main():
    """Ceci est la fonction principale."""
    print("Hello, World!")
    utils.helper()
EOF

    cat << 'EOF' > "$project_dir/utils.py"
# utils.py
def helper():
    # Une fonction utilitaire
    print("Helper function.")
EOF
    echo "    Projet 'basic_project' créé."
}

# Scénario 2 : Un projet pour tester la suppression des commentaires (--strip-comments)
create_strip_comments_project() {
    local project_dir="$TEST_PROJECTS_ROOT/strip_comments_project"
    echo -e "${COLOR_BLUE}--> Création du projet de test : 'strip_comments_project'${COLOR_NC}"

    rm -rf "$project_dir"
    mkdir -p "$project_dir"

    # Fichier Python riche en commentaires et docstrings
    cat << 'EOF' > "$project_dir/code_with_comments.py"
# Ce script est un exemple pour le test.
# Il contient divers types de commentaires.

class MyClass:
    """
    Ceci est une docstring de classe.
    Elle devrait être supprimée.
    """
    def __init__(self, name):
        self.name = name # Commentaire en ligne

    def greet(self):
        """Docstring de méthode."""
        # Affiche un message
        print(f"Hello, {self.name}")

# Fonction de premier niveau
def top_level_function():
    """Une autre docstring à supprimer."""
    return 1 + 1 # Calcul simple
EOF
    echo "    Projet 'strip_comments_project' créé."
}

# --- Fonction pour générer les fichiers "Golden" (attendus) ---

generate_golden_files() {
    echo -e "\n${COLOR_YELLOW}--- Génération des fichiers 'Golden' (expected_output.txt) ---${COLOR_NC}"

    # 1. Pour 'basic_project'
    echo "  -> Génération pour 'basic_project'..."
    local basic_project_dir="$TEST_PROJECTS_ROOT/basic_project"
    local temp_output_basic="/tmp/aicc_basic_output.txt"
    python3 "$AICC_SCRIPT" \
        --project "$basic_project_dir" \
        --output "$temp_output_basic" \
        --no-timestamp \
        --config "$basic_project_dir/config.yaml"

    # Supprime l'en-tête dynamique pour créer un fichier de référence stable
    # Le chemin dans l'arbre sera différent sur chaque machine, donc on le remplace.
    # On saute les 4 premières lignes et on ajoute un en-tête simple et stable.
    {
        echo "Ce fichier est une concaténation de plusieurs fichiers sources d'un projet."
        echo ""
        tail -n +5 "$temp_output_basic" | sed "1s|Arbre du projet :.*|Arbre du projet : [CHEMIN_NORMALISÉ]|"
    } > "$basic_project_dir/expected_output.txt"
    rm "$temp_output_basic"
    echo -e "     ${COLOR_GREEN}Fichier 'expected_output.txt' généré.${COLOR_NC}"


    # 2. Pour 'strip_comments_project'
    echo "  -> Génération pour 'strip_comments_project' (avec --strip-comments)..."
    local strip_project_dir="$TEST_PROJECTS_ROOT/strip_comments_project"
    local temp_output_strip="/tmp/aicc_strip_output.txt"
    python3 "$AICC_SCRIPT" \
        --project "$strip_project_dir" \
        --output "$temp_output_strip" \
        --no-timestamp \
        --strip-comments
    
    {
        echo "Ce fichier est une concaténation de plusieurs fichiers sources d'un projet."
        echo ""
        tail -n +5 "$temp_output_strip" | sed "1s|Arbre du projet :.*|Arbre du projet : [CHEMIN_NORMALISÉ]|"
    } > "$strip_project_dir/expected_output.txt"
    rm "$temp_output_strip"
    echo -e "     ${COLOR_GREEN}Fichier 'expected_output.txt' généré.${COLOR_NC}"

    echo -e "${COLOR_YELLOW}--- Génération terminée ---${COLOR_NC}"
}


# --- Point d'entrée du script ---
main() {
    # Créer le répertoire principal des projets de test s'il n'existe pas
    mkdir -p "$TEST_PROJECTS_ROOT"

    echo -e "${COLOR_GREEN}Initialisation de l'environnement de test...${COLOR_NC}"
    
    # Appeler les fonctions pour créer chaque projet
    create_basic_project
    create_strip_comments_project
    # Ajoutez ici les appels pour vos futurs projets de test
    # create_headers_only_project

    # Vérifier si l'argument --golden-files est passé
    if [[ "$1" == "--golden-files" ]]; then
        generate_golden_files
    else
        echo -e "\n${COLOR_YELLOW}Pour générer/mettre à jour les fichiers 'expected_output.txt', lancez : ./setup_tests.sh --golden-files${COLOR_NC}"
    fi

    echo -e "\n${COLOR_GREEN}✅ Environnement de test prêt !${COLOR_NC}"
}

# Exécuter la fonction principale
main "$@"
================================================================================
--- FICHIER: tests/test_aicc.py
================================================================================

# tests/test_aicc.py

import subprocess
import sys
from pathlib import Path

# Définir les chemins de base pour une meilleure portabilité
# __file__ est le chemin de ce fichier de test
TESTS_DIR = Path(__file__).parent
# On remonte d'un niveau pour avoir la racine du projet
PROJECT_ROOT = TESTS_DIR.parent
# Chemin vers le script principal
AICC_SCRIPT = PROJECT_ROOT / 'aicc.py'

def run_aicc(args, cwd=PROJECT_ROOT):
    """Exécute le script aicc.py avec les arguments fournis via subprocess."""
    command = [sys.executable, str(AICC_SCRIPT)] + args
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding='utf-8',
        cwd=cwd
    )
    return result

def find_content_start(lines):
    """Trouve l'index de la ligne où le contenu réel commence."""
    for i, line in enumerate(lines):
        if line.strip().startswith("Arbre du projet :"):
            return i
    # Si on ne trouve pas l'arbre, on retourne 0 pour comparer tout le fichier (et probablement échouer)
    return 0

def compare_files_robust(generated_path, expected_path):
    """
    Compare deux fichiers de manière robuste.
    1. Ignore tout l'en-tête en trouvant la ligne "Arbre du projet".
    2. Normalise le chemin de l'arbre pour être indépendant de la machine.
    """
    with open(generated_path, 'r', encoding='utf-8') as f_gen, \
         open(expected_path, 'r', encoding='utf-8') as f_exp:
        
        lines_gen = f_gen.read().splitlines()
        lines_exp = f_exp.read().splitlines()

        # Trouver le début du contenu dans chaque fichier
        start_gen = find_content_start(lines_gen)
        start_exp = find_content_start(lines_exp)
        
        # Tronquer les listes pour ne garder que le contenu pertinent
        content_lines_gen = lines_gen[start_gen:]
        content_lines_exp = lines_exp[start_exp:]

        # Normaliser la première ligne (le chemin de l'arbre)
        if content_lines_gen:
            content_lines_gen[0] = "Arbre du projet : [CHEMIN_NORMALISÉ]"
        if content_lines_exp:
            content_lines_exp[0] = "Arbre du projet : [CHEMIN_NORMALISÉ]"

        # Joindre les lignes pour la comparaison finale
        final_content_gen = "\n".join(content_lines_gen)
        final_content_exp = "\n".join(content_lines_exp)
        
        assert final_content_gen == final_content_exp


def test_basic_concatenation(tmp_path):
    """
    Teste la fonctionnalité de base : concaténation simple d'un projet.
    `tmp_path` est une fixture pytest qui fournit un dossier temporaire unique.
    """
    # 1. Définir les chemins pour ce test
    test_project_path = TESTS_DIR / 'test_projects' / 'basic_project'
    output_file = tmp_path / 'output.txt'
    expected_file = test_project_path / 'expected_output.txt'
    
    # 2. Construire la commande
    args = [
        '--project', str(test_project_path),
        '--output', str(output_file),
        '--no-timestamp',
        '--config', str(test_project_path / 'config.yaml')
    ]
    
    # 3. Exécuter le script
    result = run_aicc(args)
    
    # 4. Vérifier les résultats
    assert result.returncode == 0, f"Le script a échoué avec le code {result.returncode}.\nStderr: {result.stderr}"
    assert output_file.exists(), "Le fichier de sortie n'a pas été créé."
    
    # 5. Comparer le contenu du fichier généré avec le fichier attendu
    compare_files_robust(output_file, expected_file)
================================================================================
--- FICHIER: tests/test_projects/basic_project/.gitignore
================================================================================

# Fichier à ignorer
ignored_file.txt
__pycache__/

================================================================================
--- FICHIER: tests/test_projects/basic_project/app/main.py
================================================================================

# main.py
import utils

def main():
    """Ceci est la fonction principale."""
    print("Hello, World!")
    utils.helper()

================================================================================
--- FICHIER: tests/test_projects/basic_project/config.yaml
================================================================================

# Configuration simple pour le test
include_patterns:
  - '**/*'
common_filters:
  - ".git/"
  - "build/"
  - "expected_output.txt"
  - "*.log"
# On laisse les .md dans l'arbre pour ce test
tree_only_filters: []
================================================================================
--- FICHIER: tests/test_projects/basic_project/expected_output.txt
================================================================================

Ce fichier est une concaténation de plusieurs fichiers sources d'un projet.
Date de génération : 2025-09-09 23:59:15
Statistiques du contenu : Taille: 1.56 KB (1,602 octets), Tokens (estim.): 244

Arbre du projet : /home/lachouette/utils/ai-context-craft/tests/test_projects/basic_project
├── .gitignore
├── app/
│   └── main.py
├── config.yaml
└── utils.py

--------------------------------------------------------------------------------
CONTENU DES FICHIERS
--------------------------------------------------------------------------------


================================================================================
--- FICHIER: .gitignore
================================================================================

# Fichier à ignorer
ignored_file.txt
__pycache__/

================================================================================
--- FICHIER: app/main.py
================================================================================

# main.py
import utils

def main():
    """Ceci est la fonction principale."""
    print("Hello, World!")
    utils.helper()

================================================================================
--- FICHIER: config.yaml
================================================================================

# Configuration simple pour le test
include_patterns:
  - '**/*'
common_filters:
  - ".git/"
  - "build/"
  - "expected_output.txt"
  - "*.log"
# On laisse les .md dans l'arbre pour ce test
tree_only_filters: []
================================================================================
--- FICHIER: utils.py
================================================================================

# utils.py
def helper():
    # Une fonction utilitaire
    print("Helper function.")

================================================================================
--- FICHIER: tests/test_projects/basic_project/utils.py
================================================================================

# utils.py
def helper():
    # Une fonction utilitaire
    print("Helper function.")

================================================================================
--- FICHIER: tests/test_projects/strip_comments_project/code_with_comments.py
================================================================================

# Ce script est un exemple pour le test.
# Il contient divers types de commentaires.

class MyClass:
    """
    Ceci est une docstring de classe.
    Elle devrait être supprimée.
    """
    def __init__(self, name):
        self.name = name # Commentaire en ligne

    def greet(self):
        """Docstring de méthode."""
        # Affiche un message
        print(f"Hello, {self.name}")

# Fonction de premier niveau
def top_level_function():
    """Une autre docstring à supprimer."""
    return 1 + 1 # Calcul simple

================================================================================
--- FICHIER: tests/test_projects/strip_comments_project/expected_output.txt
================================================================================

Ce fichier est une concaténation de plusieurs fichiers sources d'un projet.

Arbre du projet : [CHEMIN_NORMALISÉ]
└── code_with_comments.py

--------------------------------------------------------------------------------
CONTENU DES FICHIERS
--------------------------------------------------------------------------------


================================================================================
--- FICHIER: code_with_comments.py
================================================================================

class MyClass:

    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f'Hello, {self.name}')

def top_level_function():
    return 1 + 1