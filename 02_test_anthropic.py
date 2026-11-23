import anthropic
from dotenv import load_dotenv
from pathlib import Path

# 1. Localiser le fichier .env à la racine du projet.
racine_projet = Path(__file__).resolve().parent
fichier_env = racine_projet / ".env"

# 2. Charger les variables d'environnement.
load_dotenv(dotenv_path=fichier_env)

# 3. Créer le client Anthropic.
# Le SDK récupère automatiquement ANTHROPIC_API_KEY.
client = anthropic.Anthropic()

# 4. Envoyer une requête au modèle.
reponse = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=150,
    system="Tu es un assistant pédagogique. Réponds en français.",
    messages=[
        {
            "role": "user",
            "content": "Explique la notion de token en 3 phrases."
        }
    ],
)

# 5. Afficher la réponse générée.
print("\n--- RÉPONSE DE CLAUDE ---")
for bloc in reponse.content:
    if bloc.type == "text":
        print(bloc.text)

# 6. Afficher les informations sur la consommation.
print("\n--- UTILISATION DES TOKENS ---")
print("Tokens en entrée :", reponse.usage.input_tokens)
print("Tokens en sortie :", reponse.usage.output_tokens)
print("Raison de l'arrêt :", reponse.stop_reason)