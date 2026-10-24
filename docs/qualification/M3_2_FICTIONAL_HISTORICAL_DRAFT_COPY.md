# M3.2 — Reprise contrôlée d'une version historique fictive (qualification source-only)

**Candidate groupée du 24 octobre 2026 — jamais montée dans l'application Windows, sans aucune source opérateur.**

## Tranche A — comportement du carnet

`prepareFictionalEventHistoricalDraft(book,eventId,version)` retourne **seulement** les quatre champs éditables d'une version historique antérieure d'un événement fictif encore actif. Entrées strictement contrôlées : origine `fictional_browser_memory_only`, Univers exact, ID existant et actif, version entière sûre, strictement inférieure à la version courante, statut `superseded`. Refus si l'événement est retiré (aucune résurrection implicite), étranger, ou version absente. Retour détaché et gelé (`Object.freeze`) ; carnet et audit inchangés.

Dans le seul `M32FictionalEventManualWorkshop`, le rédacteur choisit une **version précédente** puis clique sur « Préparer la correction depuis cette version ». Cette opération **préremplit le formulaire seulement** ; la justification est effacée et doit être ressaisie. Le clic explicite sur « Enregistrer une nouvelle version » utilise ensuite le chemin actuel `amendFictionalEvent` qui ajoute une nouvelle version avec audit ; aucune modification du passé. Changer d'événement/Univers efface la sélection historique. Textes de forme script sont échappés par React.

6 nouveaux Vitest #91–96 ; 6 nouveaux tests d'interactions Chromium #77–82 **dans chacun** des modes normal/CSP strict. Source exacte déjà allowlistée : aucun changement au stage Git 15 blobs.

## Tranche B — accélération gouvernée

[Décision de convergence](M3_2_ACCELERATED_CONVERGENCE_DECISION_20261024.md) : regrouper les développements fictifs compatibles + leurs qualifications indépendantes dans une PR cohérente, paralléliser uniquement investigations source/docs/tests indépendants, et éviter de relancer 76 étapes Windows pour chaque micro-changement. Aucune altération de `Protect main`, de l'exact-SHA final, des revues/threads ou de la qualification post-main. Prioriser la résolution réelle des cinq preuves historiques ou une décision **séparée** de nouvelle référence prospective. Les travaux de laboratoire supplémentaires ne prouvent pas ces prérequis.

## États et conditions

Checkpoint précédent [PR #157](https://github.com/LaurentCOLL1/Fabulaxiom/pull/157) source `956154c4be0645536d356a48c6d75d0bf92bdc37`, [CI source #40061031363](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40061031363) **SUCCESS** ; fusion `645b50f438d12165d0eae46f1c3d586f07819480` ; [CI postmain #40061815168](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40061815168) **SUCCESS** séparément vérifiée. 76 étapes Windows, 92 contrats, 90 tests événementiels fictifs, Chromium 76/76 deux modes, Rust 132 PASS.

**Seuils prospectifs, NON encore prouvés pour ce nouveau HEAD :** 93 contrats, 96 Vitest événementiels, Chromium 82/82 par mode normal et CSP strict, 132 Rust sans régression. Nouveau run exact final HEAD, inspection complète, diff/reviews/threads, `Protect main`, fusion `expected_head_sha`, postmain indépendante, commentaires issue #38.

**STOP réel inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Bases v6/v7, backups, ACL, journaux, marqueur, migration 007, IPC writer, M3.3, ComfyUI, release, Windows opérateur interdits.
