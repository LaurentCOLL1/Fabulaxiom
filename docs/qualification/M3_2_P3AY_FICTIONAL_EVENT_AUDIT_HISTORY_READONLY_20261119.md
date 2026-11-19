# P3ay — consultation explicite de l'historique d'événements fictifs (19 novembre 2026)

## Besoin produit, périmètre
L'atelier manuel fictif affichait les événements courants et permettait une comparaison de versions, mais ne rendait pas directement lisible l'historique humain complet après retrait d'un événement. P3ay ajoute un sélecteur **explicite, en lecture seule** de tous les IDs d'événements inventés ayant une version 1, y compris lorsque leur dernière version est une pierre tombale `withdrawn`. Avant une sélection, aucune version détaillée n'est affichée.

Après sélection explicite, l'UI restitue **les versions historiques** déjà validées par `auditedFictionalEventHistory`, en conservant les champs exacts du témoin fictif : statut, titre, note, ancre, ID de révision source, action et motif humain fictif, ainsi que les différences de champs avec la version précédente. L'ordre est celui des **versions d'un même événement**, sans inférence d'ordre mondial, de dates, de narration ou de révélation. Le panneau n'ajoute **aucune action de restauration** et ne modifie aucune révision passée. L'échappement React s'applique aux chaînes ressemblant à du HTML.

## Témoins candidats
- Vitest atelier #20 : le sélecteur d'historique s'affiche, mais aucune version n'est révélée avant le choix ; données d'entrée inchangées.
- Vitest atelier #21 : après retrait inventé, l'événement est absent des courants mais reste sélectionnable dans l'historique, sans permission de restauration.
- Chromium fixture-only #110 : créer un événement lié à une révision source explicite, modifier son titre avec motif humain, examiner ses deux versions, puis le retirer ; l'historique conserve trois versions, toutes les sources, le motif de retrait, et zéro bouton d'édition dans le panneau.
- Chromium fixture-only #111 : titre hostile de forme `<script>` affiché en texte inerte ; basculement d'Universe réinitialise le sélecteur et efface les anciennes données.
- **Tous ces témoins sont CANDIDATS NON QUALIFIÉS** jusqu'à CI source Windows terminée au SHA exact de la PR P3ay. Aucun résultat de simulation ne ferme M32-071/075/081.

## Parent et décision
Parent protected `main=38a9dc204f6f1a9d768c6d9e45519b472e420e8c`, PR #392 MERGED par squash protégé. CI source [#44412057826](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/44412057826) completed/SUCCESS au HEAD exact `c8dce8c150b50d528c04a32779a6e8ded1fbe2c4`; CI postmain indépendante [#44416272668](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/44416272668) completed/SUCCESS au SHA exact du parent. Protect main ACTIVE strict bypass=[] ; checklist 104=9 closes/95 ouvertes ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif), PRODUCT_FIRST_PARALLEL_SAFETY ; #35/#215 DRAFT.

**STOP maintenus** : writer/R1–R9 NOT_PROVEN ; P4 réel STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5 et D3b-5 STOP ; main/WAL/SHM, live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED. STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.

Pas de Tauri, IPC, SQLite, écrivain, sauvegarde, migration, fichier ni profil opérateur. Atelier fictif isolé non monté dans App.tsx. Après qualification source sur HEAD exact et relecture diff/reviews/threads/ruleset, guarded squash expected_head_sha, nouvelle postmain indépendante et issue #38 append-only.
