
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# 1. Localiser et charger le fichier .env.
racine_projet = Path(__file__).resolve().parent
fichier_env = racine_projet / ".env"

load_dotenv(dotenv_path=fichier_env)

# 2. Créer le client Gemini.
# Il récupère automatiquement la variable GEMINI_API_KEY.
client = genai.Client()

# 3. Envoyer une question courte au modèle.
reponse = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explique la notion de token en trois phrases, en français.",
)

# 4. Afficher la réponse.
print("\n--- RÉPONSE DE GEMINI ---")
print(reponse.text)

# 5. Afficher les informations sur les tokens.

print("\n--- UTILISATION DES TOKENS ---")

usage = reponse.usage_metadata

if usage is not None:
    entree = usage.prompt_token_count or 0
    sortie = usage.candidates_token_count or 0
    total_api = usage.total_token_count

    print("Tokens en entrée :", entree)
    print("Tokens en sortie :", sortie)
    print("Somme entrée + sortie :", entree + sortie)
    print("Tokens de raisonnement :", usage.thoughts_token_count)
    print("Total communiqué par l'API :", total_api)
    print("Métadonnées complètes :", usage)
else:
    print("Les informations sur les tokens ne sont pas disponibles.")
