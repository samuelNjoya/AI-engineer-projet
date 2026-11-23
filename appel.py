"""
Couche d'appel uniforme pour Anthropic, OpenAI et Google.

Expose appeler(messages, system, provider, model, max_tokens, temperature)
qui renvoie un dictionnaire uniforme :
    {
        'texte': str,
        'tokens_in': int,
        'tokens_out': int,
        'duree_s': float,
        'stop': str,
        'provider': str,
        'model': str,
        'cout_usd': float,
    }

Chaque appel est journalisé dans appels.jsonl avec le coût estimé.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Charge les variables du fichier .env dans l'environnement Python.
# Appelé une seule fois au chargement du module.
load_dotenv()


# ---------------------------------------------------------------------------
# Prix par million de tokens (entrée, sortie). Remplace par les prix actuels
# de ton fournisseur avant de calculer un budget réel.
# Les modèles absents de ce dictionnaire auront un coût de 0.0 (non calculé).
# ---------------------------------------------------------------------------
PRIX = {
    'anthropic': {
        'claude-haiku-5-5':   {'in': 1.0,  'out': 5.0},
        'claude-sonnet-5-0':  {'in': 3.0,  'out': 15.0},
    },
    'openai': {
        'gpt-4o-mini':        {'in': 0.15, 'out': 0.60},
        'gpt-4o':             {'in': 2.50, 'out': 10.0},
    },
    'google': {
        'gemini-3.8-flash':   {'in': 0.10, 'out': 0.40},
        'gemini-3.6-flash':   {'in': 0.10, 'out': 0.40},
        'gemini-3.5-flash':   {'in': 0.10, 'out': 0.40},
        'gemini-2.5-pro':     {'in': 1.25, 'out': 5.0},
    },
}

# Chemin du journal d'appels, à la racine du projet
JOURNAL = Path('appels.jsonl')


def _cout(provider, model, tin, tout):
    """
    Calcule le coût en dollars d'un appel.

    Formule : (tokens_in * prix_in + tokens_out * prix_out) / 1_000_000.
    Si le modèle n'est pas dans le dictionnaire PRIX, renvoie 0.0
    (coût non calculé, pas une erreur).
    """
    try:
        p = PRIX[provider][model]
    except KeyError:
        return 0.0
    return (tin * p['in'] + tout * p['out']) / 1_000_000


def _journaliser(ligne):
    """
    Ajoute une ligne JSON au journal d'appels (appels.jsonl).

    Ouvre le fichier en mode append ('a'), écrit la ligne suivie d'un
    retour à la ligne. Le format JSON Lines permet de lire facilement
    le journal ligne par ligne, et d'agréger avec pandas ou une boucle.
    """
    with open(JOURNAL, 'a', encoding='utf-8') as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + '\n')


def _appel_anthropic(model, system, messages, max_tokens):
    """
    Appel spécifique à Anthropic.

    - Le system est passé comme paramètre séparé (pas dans messages).
    - max_tokens est obligatoire chez Anthropic.
    - La réponse contient une liste de blocs ; on prend le premier,
      qui est le bloc de texte.
    - Le SDK fait déjà des retries automatiques sur les erreurs
      temporaires, configurés via max_retries.
    """
    import anthropic
    client = anthropic.Anthropic(max_retries=3, timeout=60.0)
    r = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    return {
        'texte': r.content[0].text,
        'tokens_in': r.usage.input_tokens,
        'tokens_out': r.usage.output_tokens,
        'stop': r.stop_reason,
    }


def _appel_openai(model, system, messages, max_tokens, temperature):
    """
    Appel spécifique à OpenAI.

    - Le system est passé comme message avec role='system', en tête
      de la liste des messages.
    - max_completion_tokens remplace l'ancien max_tokens.
    - La réponse est dans choices[0].message.content.
    - Les compteurs sont dans usage.prompt_tokens et completion_tokens.
    """
    from openai import OpenAI
    client = OpenAI(max_retries=3, timeout=60.0)

    # Insertion du system en tête de la liste des messages
    full_messages = [{'role': 'system', 'content': system}] + messages

    r = client.chat.completions.create(
        model=model,
        messages=full_messages,
        max_completion_tokens=max_tokens,
        temperature=temperature,
    )
    return {
        'texte': r.choices[0].message.content,
        'tokens_in': r.usage.prompt_tokens,
        'tokens_out': r.usage.completion_tokens,
        'stop': r.choices[0].finish_reason,
    }


def _appel_google(model, system, messages, max_tokens, temperature):
    """
    Appel spécifique à Google Gemini.

    - Google attend une conversation sous forme de liste de contents,
      avec des roles 'user' et 'model'.
    - Le system est passé dans config.system_instruction.
    - La réponse est dans r.text (peut être None si bloquée par sécurité).
    - Les compteurs sont dans usage_metadata.
    """
    from google import genai
    from google.genai import types

    client = genai.Client()

    # Conversion des messages au format Google
    contents = []
    for m in messages:
        role = 'user' if m['role'] == 'user' else 'model'
        contents.append(
            types.Content(role=role, parts=[types.Part(text=m['content'])])
        )

    r = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=max_tokens,
            temperature=temperature,
        ),
    )

    # r.text peut être None si la réponse a été bloquée par sécurité.
    # On protège contre ce cas pour éviter un crash silencieux.
    texte = r.text if r.text is not None else '[REPONSE_VIDE_OU_BLOQUEE]'

    usage = r.usage_metadata
    tokens_in = usage.prompt_token_count if usage else 0
    tokens_out = usage.candidates_token_count if usage else 0

    return {
        'texte': texte,
        'tokens_in': tokens_in,
        'tokens_out': tokens_out,
        'stop': getattr(r.candidates[0], 'finish_reason', 'STOP') if r.candidates else 'STOP',
    }


def appeler(
    messages,
    system='',
    provider=None,
    model=None,
    max_tokens=1000,
    temperature=0.0,
):
    """
    Point d'entrée unique pour les trois fournisseurs.

    Paramètres :
    - messages : liste de dicts {'role': 'user'|'assistant', 'content': str}
    - system : consigne système (chaîne)
    - provider : 'anthropic', 'openai' ou 'google'. Si None, lit DEFAULT_PROVIDER du .env.
    - model : nom du modèle. Si None, lit DEFAULT_MODEL du .env.
    - max_tokens : plafond de sortie
    - temperature : variabilité de la génération

    Renvoie un dictionnaire uniforme avec texte, tokens, durée, stop, coût.
    Journalise chaque appel (succès ou échec) dans appels.jsonl.
    """
    # Lecture des valeurs par défaut depuis .env si non fournies
    provider = provider or os.getenv('DEFAULT_PROVIDER', 'anthropic')
    model = model or os.getenv('DEFAULT_MODEL', 'claude-haiku-5-5')

    debut = time.perf_counter()

    try:
        if provider == 'anthropic':
            res = _appel_anthropic(model, system, messages, max_tokens)
        elif provider == 'openai':
            res = _appel_openai(model, system, messages, max_tokens, temperature)
        elif provider == 'google':
            res = _appel_google(model, system, messages, max_tokens, temperature)
        else:
            raise ValueError(f'Fournisseur inconnu : {provider}')
    except Exception as e:
        # Journalisation de l'échec avant de propager l'exception
        _journaliser({
            'date': datetime.now().isoformat(),
            'provider': provider,
            'model': model,
            'erreur': str(e),
        })
        raise

    # Enrichissement du résultat avec durée, provider, model, coût
    res['duree_s'] = round(time.perf_counter() - debut, 2)
    res['provider'] = provider
    res['model'] = model
    res['cout_usd'] = _cout(provider, model, res['tokens_in'], res['tokens_out'])

    # Journalisation de l'appel réussi
    _journaliser({
        'date': datetime.now().isoformat(),
        'provider': provider,
        'model': model,
        'tokens_in': res['tokens_in'],
        'tokens_out': res['tokens_out'],
        'duree_s': res['duree_s'],
        'stop': res['stop'],
        'cout_usd': res['cout_usd'],
    })

    return res