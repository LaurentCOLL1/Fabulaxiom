# P3ap — changement de cible, source proposée remise à zéro (17 novembre 2026)

## Produit
Lors d'une correction d'ancre fictive, le choix d'une autre ancre réinitialise explicitement la scène/révision proposée, le drapeau de détachement et la prévisualisation avant/après. Sans cette règle, la sélection immuable d'une source du précédent dossier pouvait être reportée implicitement dans le suivant. Les ancrages historiques restent intacts. Le message explicatif est visible dans le laboratoire React inventé.

## Preuves candidates
Vitest #33 : message d'explication sans prétendue sauvegarde. Chromium #103 : ancre D avec scène s1/révision `invented-rev-B`, première revue, bascule vers C (correction bloquée par relations actives), confirmation que la scène/révision et la prévisualisation antérieures sont effacées, retour vers D et nouvelle revue sans cette provenance. Attendu Chromium 103/103, CSP strict et tests antérieurs conservés ; **CANDIDAT NON QUALIFIÉ jusqu'à CI Windows propre sur HEAD exact**.

## Autorité
Parent `main=ff5ce8859706536928dea32f2f10eec7ab38c2b1`, PR #383 P3ao MERGED avec CI source Windows #44016538312 completed/SUCCESS HEAD exact `e715e008dc42df7eab11df8c431967f1a8bba7f4`, postmain indépendante #44124691663 PENDING_UNQUALIFIED au checkpoint. Protect main ACTIVE strict bypass=[] et aucun succès hérité du HEAD source. Checklist 104 = 9 closes/95 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif), PRODUCT_FIRST_PARALLEL_SAFETY. Writer/R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, PENDING_EXTERNAL_ATTESTATION(21/3/2), main/WAL/SHM/live WAL-index/ABA NOT_PROVEN, glib #160 OPEN_NOT_REMEDIATED. Aucun IPC writer, SQLite d'origine, migration, v6/v7, sauvegarde, Hello ou recovery. DRAFT/STOP MERGE jusqu'au parent postmain SUCCESS HEAD exact, CI P3ap propre, diff/reviews/threads, Protect main strict, guarded squash expected_head_sha, postmain indépendante, #38 append-only.
