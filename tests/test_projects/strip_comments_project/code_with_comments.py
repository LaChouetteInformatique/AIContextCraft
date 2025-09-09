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
