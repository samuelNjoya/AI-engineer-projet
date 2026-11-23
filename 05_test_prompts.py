
from pathlib import Path

def charger_prompt(nom, version):
    chemin = (
        Path(__file__).resolve().parent
        / "prompts"
        / nom
        / f"{version}.txt"
    )
    return chemin.read_text(encoding="utf-8")


# Exemple de facture fictive.
texte_facture = """
FACTURE N° FAC-2026-0042
Fournisseur : Boutique du Centre
Date : 20/10/2026
Montant HT : 105 000 FCFA
TVA : 20 000 FCFA
Montant TTC : 125 000 FCFA
"""

# Charger le prompt depuis le fichier v2.txt.
prompt = charger_prompt("extraction_facture", "v2")

# Insérer le texte de la facture dans le prompt.
prompt = prompt.replace("{texte}", texte_facture)

# Afficher le prompt final.
print("===== PROMPT FINAL =====")
print(prompt)

print("\n===== FIN DU TEST =====")



    