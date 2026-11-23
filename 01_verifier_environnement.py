
import sys,os
from pathlib import Path

from dotenv import load_dotenv

# Affiche l'interpréteur Python réellement utilisé.
print("Python utilise :", sys.executable)

# Vérifie si le dossier de l'environnement virtuel est actif.
print("Environnement virtuel actif :", sys.prefix != sys.base_prefix)

# Charge les variables du fichier .env situé à la racine.
racine_projet = Path(__file__).resolve().parent
fichier_env = racine_projet / ".env"

print("Fichier .env présent :", fichier_env.is_file())

load_dotenv(dotenv_path=fichier_env)

print("Configuration de l'environnement vérifiée.")

# Vérifie la présence des clés sans afficher leurs valeurs.
print("Clé Anthropic configurée :", bool(os.getenv("ANTHROPIC_API_KEY")))
print("Clé OpenAI configurée :", bool(os.getenv("OPENAI_API_KEY")))
print("Clé Gemini configurée :", bool(os.getenv("GEMINI_API_KEY")))
