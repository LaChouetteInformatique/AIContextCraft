![Public Domain Dedication](https://img.shields.io/badge/Public%20Domain-CC0%201.0-blue)

# AI Context Craft 🤖

**AI Context Craft** est un outil en ligne de commande puissant et configurable pour agréger des fichiers de code source en un seul fichier texte. Il est conçu pour préparer facilement des contextes de projet complets à fournir aux grands modèles de langage (LLM) comme Gemini, GPT, etc.

## ✨ Fonctionnalités

-   **Concaténation de fichiers** : Combine de manière sélective les fichiers de votre projet en un seul contexte.
-   **Filtrage avancé** : Utilise des patterns de style `.gitignore` pour inclure ou exclure finement des fichiers et des dossiers (grâce à `pathspec`).
-   **Génération d'arborescence** : Inclut automatiquement une représentation en arbre de la structure de votre projet pour donner plus de contexte au LLM.
-   **Modes d'arborescence multiples** :
    -   `--with-tree` : Arbre basé sur les mêmes filtres que la concaténation.
    -   `--with-tree-full` : Arbre complet du projet (avec des exclusions minimales).
    -   `--with-tree-custom` : Arbre basé sur une configuration personnalisée.
-   **Suppression des commentaires** : Option `--strip-comments` pour nettoyer le code et économiser des tokens (grâce à `tree-sitter`).
-   **Configuration flexible** : Gérez vos filtres via un fichier `concat-config.yaml` pour une réutilisation facile.
-   **Validation de configuration** : Une commande pour vérifier que votre configuration est valide.

## 🚀 Installation

Le script d'installation mettra en place un environnement virtuel Python et installera toutes les dépendances nécessaires.

```bash
# Clonez le projet (si ce n'est pas déjà fait)
git clone https://github.com/VOTRE_NOM/ai-context-craft.git
cd ai-context-craft

# Lancez le script d'installation
bash install.sh
```

## 📖 Utilisation

Après l'installation, assurez-vous d'activer l'environnement virtuel avant d'utiliser l'outil.

```bash
source venv/bin/activate
```

### Commandes de base

```bash
# Concaténer les fichiers du répertoire courant (sortie dans build/)
./run.sh

# Traiter un autre répertoire
./run.sh ../mon-autre-projet

# Spécifier un fichier de sortie
./run.sh -o ./output/contexte_projet.txt
```

### Options populaires

```bash
# Inclure une arborescence du projet dans la sortie
./run.sh --with-tree

# Inclure une arborescence plus complète
./run.sh --with-tree-full

# Supprimer tous les commentaires du code
./run.sh --strip-comments

# Combiner les options
./run.sh --with-tree --strip-comments
```

### Générer uniquement l'arborescence

```bash
# Générer l'arborescence seule en utilisant la configuration 'full'
./run.sh --tree-only --tree-mode full -o project-tree.txt
```

### Valider la configuration

Avant de lancer une grosse concaténation, vous pouvez valider votre fichier `concat-config.yaml`.

```bash
./validate_config.py
```

## ⚙️ Configuration (`concat-config.yaml`)

Créez un fichier `concat-config.yaml` à la racine de votre projet pour contrôler précisément quels fichiers sont inclus.

**Exemple de configuration (mode exclusion) :**

```yaml
# Fichier: concat-config.yaml

concat_project_files:
  # En mode 'exclude', tout est inclus sauf ce qui est listé ci-dessous.
  mode: exclude
  exclude:
    # Dossiers complets
    - 'node_modules/'
    - 'build/'
    - 'dist/'
    - '.venv/'
    - '__pycache__/'
    - '.git/'
    # Fichiers par nom ou pattern
    - '*.log'
    - '*.lock'
    - '.env'
    - 'data/*'
```

**Exemple de configuration (mode inclusion) :**

```yaml
# Fichier: concat-config.yaml

concat_project_files:
  # En mode 'include', rien n'est inclus sauf ce qui est listé ci-dessous.
  mode: include
  include:
    - 'src/**/*.py'      # Tous les fichiers Python dans src
    - 'src/**/*.js'       # Tous les fichiers JS dans src
    - 'tests/*.py'        # Les fichiers de test à la racine de tests/
    - 'README.md'         # Le README principal
    - 'requirements.txt'
```


## 📜 Licence

Ce projet est dédié au **domaine public** via la licence [Creative Commons Zero (CC0) 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).

Vous êtes libre de copier, modifier, distribuer et exécuter le travail, même à des fins commerciales, sans demander la permission.


---