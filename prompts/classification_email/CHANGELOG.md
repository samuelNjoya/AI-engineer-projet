# CHANGELOG — classification_email

## v1 — 2026-10-22
- Version initiale.
- System minimal, consigne simple.
- Sortie attendue : un mot de catégorie.
- Problème connu : le modèle produit parfois une phrase au lieu d'un mot, ou choisit une catégorie au hasard sur les cas ambigus.

## v2 — 2026-10-22
- Ajout de définitions précises pour chaque catégorie.
- Ajout de règles : priorité en cas d'ambiguïté, format de sortie strict.
- Amélioration attendue : meilleure précision sur les cas ambigus, sortie plus propre.

## v3 — 2026-10-22
- Ajout de 5 exemples few-shot, un par catégorie, dont un cas limite (email court et neutre classé "autre").
- Amélioration attendue : le modèle imite le format des exemples, meilleure couverture des cas limites.
- À mesurer : comparer v2 et v3 sur les 10 cas, regarder surtout les cas ambigus.