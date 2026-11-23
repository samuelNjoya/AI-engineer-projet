# Parcours IA de 10 mois (v3.1) : projets réels pour devenir AI Engineer

Avec 20 à 25 h par semaine sur 10 mois (43 semaines), tu disposes d'environ **860 à 1 075 h**. Chaque phase doit produire quelque chose d'utile pour de vraies personnes, avec un résultat mesurable, et pas seulement un exercice de cours.

## Règle des projets

Chaque projet doit cocher trois cases : **un vrai utilisateur** (toi, ton employeur, une association, un petit commerce), **un chiffre de réussite** (taux de bonnes réponses, temps gagné, coût par document) et **un livrable public** (dépôt, démo, README).

## Fil rouge : un assistant d'automatisation documentaire pour organisations

Il traite les documents réels d'une organisation (factures, contrats, emails, scans, enregistrements audio), répond aux questions à partir d'eux et déclenche des actions. Tu choisis dès la semaine 1 **l'organisation réelle** qui servira de premier utilisateur. C'est ce qui rend le projet crédible en entretien.

## Calendrier

| Phase | Sem. | Thème | Terminé quand… |
| --- | --- | --- | --- |
| 1 | 1-4 | Fondations LLM, API, prompt engineering | extraction fiable sur 50 vrais documents + bibliothèque de prompts versionnés |
| 2 | 5-6 | Évaluation et observabilité LLM | scores automatiques en CI + traces |
| 3 | 7-13 | RAG, bases vectorielles, ingénierie du contexte | démo publique + 5 utilisateurs réels |
| 4 | 14-17 | Fullstack IA | SaaS minimal multi-organisation |
| — | 18 | Semaine tampon |  |
| 5 | 19-25 | Agents, MCP, LangGraph, garde-fous | agent en usage réel, validation humaine, attaques bloquées mesurées |
| 6 | 26-28 | Multimodal | scans et audio traités de bout en bout |
| 7 | 29-34 | ML et Deep Learning | comparaison chiffrée fine-tuning vs API |
| — | 35 | Semaine tampon |  |
| 8 | 36-41 | Production, sécurité, conformité, coûts | déployé, audité, coût réduit et mesuré |
| 9 | 42-43 | Finalisation et entretiens | portfolio complet, entretiens en cours |

**Les candidatures commencent à la semaine 14**, avec le RAG public comme premier argument, et s'intensifient à partir de la semaine 33.

## Phase 1 : Fondations et prompt engineering (semaines 1-4)

- *Semaine 1, prompt engineering* : bibliothèque de prompts versionnés pour ton fil rouge (consignes, exemples, formats de sortie), chacun avec son score sur un petit jeu de test.
- *Fil rouge v0 (semaines 2-4)* : extraction de factures, CV ou emails en JSON validé (FastAPI + Pydantic).
- *Mini-projet 1* : trier et classer tes propres emails et documents avec un script.
- *Mini-projet 2* : benchmark de 3 modèles sur 50 vrais documents, avec rapport de coût et de qualité.
- Dès maintenant : travaille avec un outil de développement assisté par IA (Claude Code ou Cursor) et note ce qu'il fait bien ou mal.

## Phase 2 : Évaluation (semaines 5-6)

- *Fil rouge* : jeu de référence de 50 documents annotés à la main, tests automatiques (promptfoo ou équivalent) exécutés en CI, traçage des appels (Langfuse).
- *Mini-projet* : tableau de bord coût/qualité par modèle et par prompt.

## Phase 3 : RAG, bases vectorielles et contexte (semaines 7-13)

- *Fil rouge v1* : questions-réponses sur les documents de ton organisation réelle, avec sources citées et score de fidélité.
- *Mini-projet 1* : assistant sur la documentation Laravel et tes propres notes techniques (tu l'utiliseras vraiment).
- *Mini-projet 2* : RAG de questions bibliques avec citation des versets, pour SmartFaith.
- *Mini-projet 3, bases vectorielles* : comparer pgvector et une base dédiée (par exemple Qdrant) sur tes vrais documents : vitesse, qualité, coût, complexité.
- *Mini-projet 4, ingénierie du contexte* : choisir quoi mettre dans le contexte, résumer et compacter l'historique, gérer mémoire court et long terme, ordre des informations et budget de tokens. Fais tenir un long dossier de documents dans ton assistant et mesure la qualité des réponses selon la stratégie de contexte.
- *Jalon semaine 13* : déploiement public, démo vidéo, README, retours écrits de 5 utilisateurs. Commence à rédiger en anglais.

## Phase 4 : Fullstack IA (semaines 14-17)

- *Fil rouge v2* : transformation en SaaS minimal : espaces par organisation, authentification, import de fichiers asynchrone (files d'attente Laravel + Redis), réponses en streaming, quotas.
- *Mini-projet* : intégration propre entre ton application Laravel et le service Python, avec tests d'intégration.

## Phase 5 : Agents, MCP, LangGraph et garde-fous (semaines 19-25)

- *Fil rouge v3* : agent qui lit les emails entrants, extrait les données, crée les enregistrements dans l'application et **demande une validation humaine** avant les actions sensibles. Construis-le d'abord sans framework, puis réécris-le en graphe **LangGraph** (états, reprise après erreur, point de validation humaine).
- *Garde-fous* : validation des entrées et des sorties, masquage des données personnelles, liste des actions autorisées, limites par outil. Teste-les avec des cas hostiles et mesure le taux d'attaques bloquées.
- *Mini-projet 1* : serveur MCP qui expose une de tes applications Laravel.
- *Mini-projet 2* : système chercheur + rédacteur qui prépare tes publications sur les prompts IA, avec relecture de ta part.
- *Mini-projet 3* : agent de veille technologique quotidien, avec mémoire long terme simple.

## Phase 6 : Multimodal (semaines 26-28)

- *Fil rouge v4* : factures papier scannées (OCR + vision), transcription et résumé de réunions (Whisper).
- *Mini-projet* : transcription d'un audio long avec résumé structuré et chapitres, applicable à l'audio de SmartFaith.

## Phase 7 : ML et Deep Learning (semaines 29-34)

- *Fil rouge v5* : classifieur de catégories de documents ou de dépenses entraîné sur les données réelles de l'organisation.
- *Mini-projet* : fine-tuning LoRA d'un petit modèle sur la tâche d'extraction, comparé à l'API sur ton jeu de référence (qualité, coût, vitesse). Si le petit modèle suffit, tu l'intègres, sinon tu documentes pourquoi.
- C'est ici que MLflow et DVC deviennent utiles.

## Phase 8 : Production, sécurité, conformité, coûts (semaines 36-41)

- *Fil rouge v6* : Docker, CI/CD, déploiement cloud, supervision (latence, coûts, qualité).
- *Audit* : 20 attaques d'injection de prompt contre ta propre application, correctifs et rapport (OWASP LLM Top 10).
- *Conformité* : note RGPD/AI Act sur les données réellement traitées.
- *Optimisation* : cache de prompts, API batch, routage entre petits et grands modèles, avec coût **avant/après** chiffré.
- *Mini-projet* : comparaison d'un modèle local (Ollama) face à une API.

## Phase 9 : Finalisation et entretiens (semaines 42-43)

- README et démo en anglais, schéma d'architecture, ADR, un article technique publié, une contribution à un projet open source.
- 4 simulations d'entretien de conception de système LLM chronométrées, 2 sessions de questions de code, préparation comportementale.

## Note : 9,5/10

Le plan est cohérent (un fil rouge unique), équilibré (fullstack et IA), couvrant les 12 compétences d'un AI Engineer (prompts, RAG, bases vectorielles, outils, MCP, LangGraph, contexte, évaluations, garde-fous, observabilité), avec des tampons et des critères de fin par phase. Il ne peut pas atteindre 10 sur le papier : sa valeur dépendra de l'existence de **vrais utilisateurs** et de ta régularité.

|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
