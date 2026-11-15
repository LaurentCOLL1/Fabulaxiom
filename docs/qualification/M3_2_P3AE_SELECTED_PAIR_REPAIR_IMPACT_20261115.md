# P3ae — impact avant/après d'une correction de précédence fictive, paire choisie (15/11/2026)

## Parent et stratégie

Parent `main=85c246ce723ca9866935e1226d8e6fb0c0bd9a59`, PR #367 P3ad MERGED par squash `expected_head_sha=c697cc0191987f30d5fb83249ddd50434b791147`, source Windows CI #43668424751 completed/SUCCESS au HEAD exact (93 étapes). Postmain indépendante #43695902106 **PENDING_UNQUALIFIED** à la préparation de cette PR ; condition impérative avant sa fusion. Ruleset `Protect main` strict ACTIVE `bypass=[]`.

## Changement produit

Extension du laboratoire non monté de la PR #367 : lors de la prévisualisation d'un lot de corrections/révocations fictives, l'auteur peut choisir **exactement deux ancres courantes** pour confronter la relation établie et les témoins humains avant/après ce lot. Le contrôle est facultatif et n'infère aucune information depuis l'ordre des romans, les dates, une temporalité globale ou la révélation au lecteur.

- Revalidation globale du lot de corrections par la même fonction pure que la PR #367 avant comparaison.
- Comparaison sur snapshots de la même origine `fictional_browser_memory_only` ; `compareM32WorldOrder` donne les témoins actifs minimaux, ou `incomparable` sans chaîne justificative.
- Signale séparément `relation_changed` et `witness_changed`. Une relation `before` peut demeurer `before` alors que sa justification est différente après correction.
- Les deux sélecteurs sont explicites et optionnels ; un seul sélectionné refuse la prévisualisation, pas de succès partiel. Changer la sélection invalide le dernier résultat.
- Le rendu affiche les chaînes avant/après, jamais un faux succès de sauvegarde.
- Aucun `App.tsx`, Tauri IPC, SQLite, filesystem, réseau, profil opérateur ni changement de lockfile.

## Preuves candidates

`src/m32FictionalRepairPairImpact.test.tsx` : **14 cas Vitest synthétiques** (révocation cassant A→C, paire non affectée, nouveau chemin par remplacement, témoin changé avec relation identique, ordre inverse, identifiants étrangers/historiques, Unicode malformé, cycle global sur paire non concernée, immutabilité, provenance non opérateur, non-inférence narration/révélation, identité égale, UI sans faux succès, échappement HTML). Source CI au HEAD exact et postmain à qualifier ; résultats non acceptés avant qualification.

Contribution partielle uniquement à M32-072/073/078/080/081/083, toutes [ ] ; aucune promotion à une recette métier réelle, R1–R9 ou à la clôture M3.2.

## Limitations et refus

Il s'agit d'une comparaison de **la paire explicitement sélectionnée** ; aucune assertion sur l'absence d'autres effets dans le graphe, le cycle d'une base réelle, les bases historiques v6/v7, une transaction SQL, main/WAL/SHM ou ABA. R4 M32-017/019/020 NON PROUVÉ ; P4/G2B/G2C/G3 STOP, writer/R1–R9 NOT_PROVEN. `glib #160` OPEN_NOT_REMEDIATED ; M32-092/093 OPEN. Aucune modification d'origines, `M:\Fabulaxiom`, Greenfield, backups, IPC writer, migration 007, Hello, recovery.

**Checklist 104 = 9 clôtures ciblées / 95 ouvertes**, `M3.2 IN_PROGRESS_NOT_ACCEPTED (~45%)` ; `PRODUCT_FIRST_PARALLEL_SAFETY` inchangée. DRAFT jusqu'à Windows CI exacte, reviews/threads, Protect main strict, postmain parent indépendante, guarded squash expected_head_sha, nouvelle postmain et #38 append-only.
