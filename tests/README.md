# 🧪 AI Context Craft - Tests

## 🚀 Quick Start (TL;DR)

```bash
# 1. Setup initial (une seule fois)
make setup

# 2. Lancer les tests
make test              # Tests par défaut
make test-quick        # Tests rapides seulement
make test-full         # Tous les tests
make test-basic        # Un groupe spécifique

# 3. Voir les résultats
make report            # Afficher le dernier rapport
make view-results      # Interface web (http://localhost:8080)
```

## 📋 Commandes essentielles

| Commande | Description | Durée |
|----------|-------------|-------|
| `make test` | Lance les tests principaux (basic, config, patterns) | ~2 min |
| `make test-quick` | Tests de smoke rapides | ~30 sec |
| `make test-full` | Suite complète avec tous les scénarios | ~5 min |
| `make pytest` | Lance avec pytest (plus de détails) | ~3 min |
| `make coverage` | Tests avec rapport de couverture | ~3 min |
| `make shell` | Ouvre un shell pour debugger | - |
| `make clean` | Nettoie les résultats de tests | instant |

## 🔍 Lancer des tests spécifiques

```bash
# Par groupe
make test-basic        # Tests de base
make test-config       # Tests de configuration
make test-patterns     # Tests de patterns
make test-edge         # Tests de cas limites
make test-features     # Tests de fonctionnalités

# Avec le runner Python directement
./run-tests.sh test --groups basic config
./run-tests.sh test --groups patterns --verbose

# Avec pytest pour un test précis
docker run --rm -v $(pwd)/tests:/app/tests aicc-test-runner:latest \
    pytest /app/tests/test_aicc_integration.py::TestBasicFunctionality::test_help_command -v
```

---

## 📖 Comment ça marche ?

### Architecture du système de tests

Le système utilise **Python + pytest** dans **Docker** pour garantir la reproductibilité :

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Makefile      │────▶│  run-tests.sh    │────▶│  Docker Runner  │
│  (interface)    │     │   (launcher)     │     │   (Python)      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                           │
                                                           ▼
                                                   ┌───────────────┐
                                                   │ test_runner.py│
                                                   └───────────────┘
                                                           │
                                ┌──────────────────────────┼──────────────────────────┐
                                ▼                          ▼                          ▼
                        ┌──────────────┐          ┌──────────────┐          ┌──────────────┐
                        │ basic.py     │          │ config.py    │          │ patterns.py  │
                        └──────────────┘          └──────────────┘          └──────────────┘
```

### 🐳 Environnement Docker

Deux images Docker sont utilisées :

1. **`aicontextcraft:test`** - Votre application
2. **`aicc-test-runner:latest`** - L'environnement de test Python

```bash
# Construction des images (automatique avec make setup)
docker build -t aicontextcraft:test .
docker build -f tests/Dockerfile.test -t aicc-test-runner:latest .
```

### 🏗️ Structure des tests

```
tests/
├── test_runner.py           # 🎯 Orchestrateur principal
├── test_groups/            # 📦 Groupes de tests modulaires
│   ├── basic.py           # Tests de base (help, version, etc.)
│   ├── config.py          # Tests de configuration YAML
│   ├── patterns.py        # Tests de filtrage de fichiers
│   ├── edge_cases.py      # Tests de cas limites
│   └── features.py        # Tests de fonctionnalités avancées
├── test_aicc_integration.py # 🔧 Tests d'intégration pytest
├── test-project/           # 📁 Projet Lorem Ipsum de test
└── test-results/          # 📊 Résultats et rapports
```

### 🎯 Le projet de test Lorem Ipsum

Un projet complet est créé pour les tests avec :
- **Backend** : Code Python avec classes et modules
- **Frontend** : React/TypeScript avec composants
- **Docs** : Fichiers Markdown
- **Config** : YAML, JSON, Dockerfile
- **Exclusions** : node_modules, venv, .git, etc.

```bash
# Créer/recréer le projet de test
bash tests/test-project-setup.sh
```

### 🔄 Workflow d'un test

1. **Lancement** : `make test-basic`
2. **Orchestration** : `run-tests.sh` prépare l'environnement
3. **Docker** : Lance le container `aicc-test-runner`
4. **Python** : `test_runner.py` charge le module `basic.py`
5. **Exécution** : Chaque test lance votre app dans Docker
6. **Validation** : Vérifie le code de sortie et le contenu
7. **Rapport** : Génère JSON/HTML avec les résultats

### 📝 Anatomie d'un test

```python
def run_tests(tester):
    """Run basic functionality tests"""
    
    tester.run_test(
        name="basic-help",                      # Nom unique
        group="basic",                          # Groupe
        description="Check if help works",      # Description
        command="--help",                       # Commande à tester
        expected_exit_code=0,                   # Code attendu
        validate_output=lambda out: "usage" in out  # Validation custom
    )
```

### 📊 Types de validation

Les tests peuvent valider :
- **Exit code** : Le programme s'est-il terminé correctement ?
- **Output content** : Le contenu est-il présent/absent ?
- **Format** : JSON valide ? XML bien formé ?
- **Performance** : Temps d'exécution acceptable ?

### 🔧 Debugging

```bash
# Shell interactif dans le container de test
make shell

# Dans le shell :
cd /app/tests
python test_runner.py --groups basic --verbose
python -m pdb test_runner.py  # Avec debugger

# Voir les logs d'un test spécifique
cat tests/test-results/output-basic-help.txt
```

### 📈 Monitoring en temps réel

```bash
# Terminal 1 : Lancer les tests
make test-full

# Terminal 2 : Monitor
make monitor

# Terminal 3 : Voir les résultats
make view-results
# Ouvrir http://localhost:8080
```

## 🆕 Ajouter des tests

### 1. Créer un nouveau groupe

```python
# tests/test_groups/security.py
def run_tests(tester):
    """Security tests"""
    
    tester.run_test(
        name="security-no-secrets",
        group="security",
        description="Check no secrets in output",
        command=". --include .env",
        expected_exit_code=0,
        validate_output=lambda out: "SECRET_KEY" not in out
    )
```

### 2. L'enregistrer

```python
# tests/test_groups/__init__.py
from . import basic, config, patterns, edge_cases, features, security

__all__ = ['basic', 'config', 'patterns', 'edge_cases', 'features', 'security']
```

### 3. L'utiliser

```bash
make test-security
# ou
./run-tests.sh test --groups security
```

## 🐛 Résolution de problèmes

### Les tests échouent

```bash
# Voir le dernier rapport
make report

# Examiner un test spécifique
cat tests/test-results/output-[test-name].txt

# Relancer en mode verbose
./run-tests.sh test --groups basic --verbose
```

### Docker ne build pas

```bash
# Nettoyer et reconstruire
make clean-all
make setup
```

### Pas assez de mémoire

```bash
# Limiter les tests parallèles
./run-tests.sh test --quick
```

## 📊 Interprétation des résultats

```
═══════════════════════════════════════
           TEST SUMMARY
═══════════════════════════════════════

Metric          Value
────────────────────────
Total Tests        45
Passed             43  ✅
Failed              2  ❌
Pass Rate       95.6%
Total Duration  67.3s
```

- **Pass Rate > 95%** : Excellent ! 🎉
- **Pass Rate 80-95%** : Acceptable, mais vérifier les échecs
- **Pass Rate < 80%** : Problème à corriger

## 🔗 Intégration CI/CD

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: make ci
```

### GitLab CI

```yaml
test:
  stage: test
  script:
    - make ci-full
```

## 📚 Ressources

- **Pytest** : https://docs.pytest.org/
- **Docker** : https://docs.docker.com/
- **Rich** (output formatting) : https://rich.readthedocs.io/

## 💡 Tips

1. **Tests rapides pendant le dev** : `make test-quick`
2. **Tests complets avant commit** : `make test-full`
3. **Debugger un échec** : `make shell` puis rejouer le test
4. **Voir la couverture** : `make coverage`
5. **Nettoyer régulièrement** : `make clean`

---

*Pour plus de détails techniques, voir le code source dans `tests/test_runner.py`*