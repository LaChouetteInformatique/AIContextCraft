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