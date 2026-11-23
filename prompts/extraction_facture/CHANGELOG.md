# CHANGELOG — extraction_facture

## v1 — 2026-10-22
- Version initiale. Consigne simple, pas de règles, pas de format précis.
- Problème connu : sorties variables, parfois avec préambule, parfois en texte libre, montants en chaînes, dates en formats variés.

## v2 — 2026-10-22
- Ajout de règles précises : source unique, null pour absent, format des montants, format des dates, format de la devise.
- Ajout du format JSON exact avec les clés attendues.
- Amélioration attendue : structure plus stable, formats normalisés, moins d'inventions sur les champs absents.

## v3 — 2026-10-22
- Ajout d'un exemple complet avec entrée et sortie attendue.
- Ajout d'une consigne finale stricte : "sans texte avant ou après".
- Amélioration attendue : élimination du préambule, le modèle imite l'exemple, meilleur taux de JSON valide.