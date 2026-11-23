
import tiktoken

enc = tiktoken.get_encoding("o200k_base")

textes = [
    "Hello world",
    "Bonjour le monde",
    "Python est un langage de programmation.",
    "Facture numero 2024-0042, montant TTC : 1 250,00 euros",
]

for texte in textes:
    tokens = enc.encode(texte)
    print(len(texte), "caracteres vers", len(tokens), "tokens")


