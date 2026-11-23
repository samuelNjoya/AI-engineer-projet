"""
Lance un prompt versionné sur ses cas de test.

Usage :
    python run_tests.py <nom_prompt> <version>

Exemple :
    python run_tests.py classification_email v2

Le prompt doit être dans prompts/<nom_prompt>/<version>.txt
Les cas doivent être dans prompts/<nom_prompt>/cas.jsonl
Le résultat est écrit dans results/<nom_prompt>_<version>_<date>.csv

Ce script gère les erreurs de quota et les coupures réseau :
si un appel échoue, il attend puis réessaie (max 3 fois).
Si les 3 essais échouent, il note l'erreur dans le CSV et passe au cas suivant.
"""

import csv
import json
import sys
import time
from datetime import date
from pathlib import Path

from appel import appeler

# Nombre maximum de tentatives par cas en cas d'erreur
MAX_RETRIES = 3

# Délai d'attente entre deux tentatives, en secondes.
# Google recommande souvent 30 à 40 secondes quand on atteint le quota.
DELAI_RETRY = 30


def charger_prompt(nom, version):
    """
    Charge le contenu du prompt versionné depuis le disque.

    Construit le chemin prompts/<nom>/<version>.txt, vérifie qu'il existe,
    et renvoie son contenu sous forme de chaîne.

    Lève FileNotFoundError si le fichier n'existe pas, ce qui permet
    d'arrêter le script immédiatement avec un message clair.
    """
    chemin = Path('prompts', nom, f'{version}.txt')
    if not chemin.exists():
        raise FileNotFoundError(f'Prompt introuvable : {chemin}')
    return chemin.read_text(encoding='utf-8')


def charger_cas(nom):
    """
    Charge la liste des cas de test depuis prompts/<nom>/cas.jsonl.

    Le fichier est au format JSON Lines : une ligne = un objet JSON.
    On ignore les lignes vides (utiles pour aérer le fichier).

    Renvoie une liste de dictionnaires, chacun contenant au moins
    la clé 'texte' avec le contenu à traiter.
    """
    chemin = Path('prompts', nom, 'cas.jsonl')
    if not chemin.exists():
        raise FileNotFoundError(f'Cas introuvables : {chemin}')

    cas = []
    with open(chemin, encoding='utf-8') as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne:  # on saute les lignes vides
                cas.append(json.loads(ligne))
    return cas


def extraire_system_et_user(prompt_complet, texte_cas):
    """
    Sépare le system prompt du message utilisateur.

    Un fichier prompt peut contenir deux sections, délimitées par :
        ===SYSTEM===
        (le system prompt)
        ===USER===
        (le message utilisateur, avec éventuellement {texte})

    Si ces marqueurs sont présents, on sépare les deux.
    Sinon, tout le prompt devient le message utilisateur,
    et le system est vide.

    Ensuite, on remplace {texte} par le contenu du cas.
    """
    if '===SYSTEM===' in prompt_complet and '===USER===' in prompt_complet:
        parts = prompt_complet.split('===USER===', 1)
        system = parts[0].replace('===SYSTEM===', '').strip()
        user = parts[1].strip()
    else:
        system = ''
        user = prompt_complet
    return system, user.replace('{texte}', texte_cas)


def appeler_avec_retry(messages, system, max_tokens, temperature):
    """
    Appelle l'API avec une boucle de retry.

    Essaie jusqu'à MAX_RETRIES fois. Entre chaque essai, attend DELAI_RETRY
    secondes. Si tous les essais échouent, renvoie un dictionnaire d'erreur
    au lieu de lever une exception, pour que le script puisse continuer
    sur les cas suivants.

    Renvoie toujours un dictionnaire avec les clés :
    texte, tokens_in, tokens_out, stop, duree_s, cout_usd.
    En cas d'échec total, texte contient le message d'erreur,
    et tous les compteurs sont à 0.
    """
    derniere_erreur = None
    for tentative in range(MAX_RETRIES):
        try:
            return appeler(
                messages=messages,
                system=system,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except Exception as e:
            derniere_erreur = e
            if tentative < MAX_RETRIES - 1:
                print(f'  Erreur ({type(e).__name__}), '
                      f'attente {DELAI_RETRY}s avant retry...')
                time.sleep(DELAI_RETRY)
            else:
                print(f'  Echec apres {MAX_RETRIES} tentatives : {e}')

    # Tous les essais ont échoué : on renvoie un résultat d'erreur
    return {
        'texte': f'ERREUR: {derniere_erreur}',
        'tokens_in': 0,
        'tokens_out': 0,
        'stop': 'error',
        'duree_s': 0,
        'cout_usd': 0,
    }


def lancer(nom, version):
    """
    Fonction principale : lance le prompt sur tous les cas et écrit le CSV.

    Étapes :
    1. Charge le prompt et les cas.
    2. Crée le dossier results/ s'il n'existe pas.
    3. Ouvre un fichier CSV avec l'en-tête.
    4. Pour chaque cas, appelle l'API (avec retry), écrit une ligne.
    5. Affiche les totaux à la fin.

    Le nom du CSV inclut la date du jour, pour ne pas écraser les
    exécutions précédentes.
    """
    prompt = charger_prompt(nom, version)
    cas = charger_cas(nom)

    dossier_sortie = Path('results')
    dossier_sortie.mkdir(exist_ok=True)
    chemin_sortie = dossier_sortie / f'{nom}_{version}_{date.today()}.csv'

    total_in = 0
    total_out = 0
    total_cout = 0.0

    with open(chemin_sortie, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['cas', 'sortie', 'tokens_in', 'tokens_out', 'stop',
                    'duree_s', 'cout_usd', 'ok'])

        for i, c in enumerate(cas):
            # Pause entre deux cas, pour respecter le quota (RPM)
            if i > 0:
                time.sleep(15)

            system, user = extraire_system_et_user(prompt, c['texte'])
            messages = [{'role': 'user', 'content': user}]

            res = appeler_avec_retry(
                messages=messages,
                system=system,
                max_tokens=1000,
                temperature=0.0,
            )

            total_in += res['tokens_in']
            total_out += res['tokens_out']
            total_cout += res['cout_usd']

            w.writerow([
                i,
                res['texte'],
                res['tokens_in'],
                res['tokens_out'],
                res['stop'],
                res['duree_s'],
                f"{res['cout_usd']:.6f}",
                '',  # colonne 'ok' à remplir à la main
            ])
            print(f'Cas {i+1}/{len(cas)} : {res["tokens_out"]} tokens sortie, '
                  f'{res["duree_s"]}s, stop={res["stop"]}')

    print()
    print(f'Resultats ecrits dans {chemin_sortie}')
    print(f'Total : {total_in} tokens in, {total_out} tokens out, '
          f'{total_cout:.4f} USD')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage : python run_tests.py <nom_prompt> <version>')
        sys.exit(1)
    lancer(sys.argv[1], sys.argv[2])