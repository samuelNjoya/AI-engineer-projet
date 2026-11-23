python -m venv .venv
gitbash
source .venv/Scripts/activate 
cmd
.venv\Scripts\activate.bat

python -m pip install tiktoken
python -m pip show tiktoken

# enregistrer les bibliothèques Python installées dans ton environnement, avec leurs versions,
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt

# d'autres models
python -m pip install anthropic openai google-genai pydantic fastapi "uvicorn[standard]" python-dotenv

# puis on contnue comme ça 
python -m pip freeze > requirements.txt

Voici à quoi elles serviront :
- anthropic, openai, google-genai : communiquer avec les trois fournisseurs d'IA.
- pydantic : valider et structurer les données.
- fastapi : construire une API web.
- uvicorn[standard] : lancer le serveur de notre future API.
- python-dotenv : charger les variables du fichier .env.
- tiktoken : compter les tokens avec les encodages compatibles d'OpenAI.

https://platform.openai.com/api-keys?utm_source=chatgpt.com
https://aistudio.google.com/api-keys
https://platform.claude.com/create/credits?from=resume


prompt_token_count : tokens d'entrée.



candidates_token_count : tokens de sortie.



thoughts_token_count : tokens associés au raisonnement.



total_token_count : total communiqué par Google.
