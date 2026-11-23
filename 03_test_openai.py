
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# 1. Localiser le fichier .env à la racine du projet.
racine_projet = Path(__file__).resolve().parent
fichier_env = racine_projet / ".env"

# 2. Charger les variables d'environnement.
load_dotenv(dotenv_path=fichier_env)

# 3. Créer le client OpenAI.
# Il récupère automatiquement OPENAI_API_KEY depuis l'environnement.
client = OpenAI()

# 4. Envoyer une question au modèle.
reponse = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Tu es un assistant pédagogique. Réponds en français."
        },
        {
            "role": "user",
            "content": "Explique la notion de token en 3 phrases."
        }
    ],
    max_completion_tokens=150,
)

# 5. Afficher la réponse générée.
print("\n--- RÉPONSE D'OPENAI ---")
print(reponse.choices[0].message.content)

# 6. Afficher la consommation de tokens.
print("\n--- UTILISATION DES TOKENS ---")
print("Tokens en entrée :", reponse.usage.prompt_tokens)
print("Tokens en sortie :", reponse.usage.completion_tokens)
print("Total des tokens :", reponse.usage.total_tokens)

# 7. Afficher la raison de fin de génération.
print("Raison de l'arrêt :", reponse.choices[0].finish_reason)
