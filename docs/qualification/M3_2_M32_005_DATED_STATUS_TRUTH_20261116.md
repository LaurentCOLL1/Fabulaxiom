# M32-005 — cohérence datée des statuts de preuve (16 novembre 2026)

## État d'origine, contrôle réel externe séparé
Parent protégé `main=3c326c457d7b054c9b9a7e26de86558b6f412ad7` après #375 MERGED ; source Windows [#43772456415](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43772456415) SUCCESS au HEAD exact `10526ef4b2689c549cb901b639e60c084cd45a7e`. Postmain indépendante [#43803577302](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43803577302) **PENDING_UNQUALIFIED** au checkpoint de création ; sa réussite devra être observée à nouveau via GitHub et consignée comme élément distinct. Les champs de preuve ci-dessous ne sont pas une attestation GitHub temps réel.

## Six tests de refus source-only
La suite existante `tools/test_m32_completion_master_checklist.py` reçoit les tests 12–17. Ils recoupent le champ `date=YYYY-MM-DD` du prompt court, le début ISO français `DD/MM/YYYY` des huit documents, le SHA du parent, le run et SHA de la CI source Windows, l'identifiant et statut de postmain, et les comptes 104 / 9 / 95. Tests négatifs : date obsolète, réussite postmain alléguée sans SHA lié, source CI inventée, fausse clôture, statut `ACCEPTED`, admission writer/opérateur. Aucun réseau, stockage opérateur, lancement de l'application, profil Windows ou source SQLite.

## Conditions de qualification
P3ai #374 et cohérence M32-004 #375 ne suffisent pas à fermer M32-005. Exiger source CI Windows terminal SUCCESS au HEAD exact de cette PR, postmain parent #375 terminal SUCCESS exact main, Protect main ACTIVE bypass=[], reviews/threads, protected squash avec `expected_head_sha`, postmain indépendante et journal #38 append-only. **M32-004 et M32-005 restent [ ].** Checklist 9 closes/95 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %). PRODUCT_FIRST_PARALLEL_SAFETY et STOP R1–R9/P4/G2B/G2C/G3, glib #160 OPEN, main/WAL/SHM et ABA NOT_PROVEN, aucun accès bases originales v6/v7, Greenfield, backups, IPC, 007, Hello, recovery.
