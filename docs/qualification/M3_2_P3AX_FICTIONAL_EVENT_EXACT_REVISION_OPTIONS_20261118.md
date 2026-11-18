# P3ax — choix de révision lié à l'ancre active (18 novembre 2026)

## Écart de parcours et correction

Dans l'atelier fictif `M32FictionalEventManualWorkshop.tsx`, le sélecteur affichait toutes les révisions de l'Universe, même quand une seule pouvait correspondre à l'ancre actuellement choisie. Le domaine `checkInput` refusait déjà les associations incohérentes. Ce cycle affine **seulement le formulaire** : sélection d'une ancre active puis propositions limitées à sa révision source exacte et au même Universe, autres sources absentes, sélecteur désactivé si aucune révision associée. Il n'y a **aucune préselection** : le choix humain de la source reste explicite. Changer d'ancre continue d'effacer une révision auparavant sélectionnée.

## Témoins candidats, sans admission

- Vitest #19 (atelier manuel) : pour un catalogue comprenant deux révisions inventées mais une seule attachée à l'ancre A, seules les options exactes sont exposées. Ancre B, absence de choix et identifiant manquant n'offrent aucune révision. Aucune mutation.
- Chromium #109 `109-fictional-event-revisions-match-explicit-active-anchor` : au départ aucune révision disponible ; sélection A n'expose que `invented-rev-A` sans la choisir ; soumission sans révision est refusée ; sélection A→B→A efface la révision ancienne ; un nouveau choix explicite permet une création uniquement RAM, sans sauvegarde.
- Les tests sont **CANDIDATS NON QUALIFIÉS** jusqu'à CI Windows source HEAD exact P3ax, puis comparaison diff/reviews/threads, squash protégé attendu `expected_head_sha` et nouvelle postmain indépendante.

## Parent et STOP

Parent protected `main=0667f38e1bc2b1a55d1890c5da5a9ed535fb9e5d`, PR #391 MERGED par squash, Windows CI source #44388441801 completed/SUCCESS au HEAD `1e6cc412e9c7db757cc65b17e13c9d6943a11d73`, postmain indépendante #44394799523 completed/SUCCESS sur SHA exact parent ; Protect main ACTIVE strict bypass=[]. Checklist 104=9 closes/95 ouvertes ; M32-070/071/075 [ ] PARTIELS ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif), PRODUCT_FIRST_PARALLEL_SAFETY.

Atelier fictif non monté dans App.tsx : aucune lecture d'une base réelle, aucun IPC, Tauri, writer, migration, disque, fichier opérateur, ni permission G3. STOP Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5, D3b-5 STOP ; main/WAL/SHM, live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
