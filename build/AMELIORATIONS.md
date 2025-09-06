### **Mode interactif avec preview** 
Une fonctionnalité pour prévisualiser quels fichiers seront inclus avant la concaténation :

```python
# Option --preview ou --dry-run
python main.py . --preview

# Affichage :
📊 Preview mode - No files will be created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files to be included (23 files, ~12,450 tokens):
  ✅ main.py (2.3 KB)
  ✅ utils/config_manager.py (4.1 KB)
  ✅ utils/file_processor.py (3.8 KB)
  ❌ node_modules/... (excluded)
  ❌ venv/... (excluded)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Proceed? [Y/n]:
```

### **Support des templates/profils**
Créer des profils prédéfinis pour différents cas d'usage :

```yaml
# profiles.yaml
profiles:
  python-minimal:
    description: "Python project, code only"
    include: ["**/*.py"]
    exclude: ["tests/**", "**/__pycache__/**"]
    
  fullstack:
    description: "Full-stack web application"
    include: ["**/*.py", "**/*.js", "**/*.jsx", "**/*.css", "**/*.html"]
    exclude: ["node_modules/**", "venv/**", "build/**"]
    
  documentation:
    description: "Documentation and configs only"
    include: ["**/*.md", "**/*.yaml", "**/*.json", "Dockerfile", "Makefile"]
```

Usage : `./run.sh --profile python-minimal`

### **Chunking automatique**
Pour les très gros projets, diviser automatiquement en chunks :

```python
# Option --chunk-size
python main.py . --chunk-size 100000  # tokens max par fichier

# Génère :
# project_chunk_1_of_3.txt
# project_chunk_2_of_3.txt
# project_chunk_3_of_3.txt
```

### **Export en formats multiples**
Support de différents formats de sortie :

```python
--format markdown  # Par défaut
--format json      # Structure JSON
--format xml       # Format XML structuré
```

### **Cache et incrémental**
Pour les gros projets, un système de cache qui ne retraite que les fichiers modifiés :

```python
# Première exécution : crée un cache
./run.sh --cache

# Exécutions suivantes : utilise le cache
./run.sh --cache  # Ne retraite que les fichiers modifiés
```
