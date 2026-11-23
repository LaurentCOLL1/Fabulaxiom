**ADDENDUM CANDIDATURE DE CLÔTURE 23/11/2026 — M32-074 [x] CLOSED_SCOPED UNIQUEMENT SUR LA FRONTIÈRE SOURCE NON MONTÉE, SOUS RÉSERVE DE QUALIFICATION DU NOUVEAU HEAD.** La baseline #424 : CI #45244745620 completed/SUCCESS au HEAD exact 4723f0c5e3ee8c867355f12feaadedb3102a318b, job #137938442997 étape 32 succès, postmain #45262841960 completed/SUCCESS sur SHA main b5f9f28115dd8acc2b933999e973ebbfcf90a6ba. Cette baseline ne contenait PAS les nouveaux tests M32-074 ; elle fixe seulement le code de source inspecté. Les nouveaux tests ajoutés dans #425 doivent obtenir leur propre CI terminale au HEAD exact de clôture avant fusion. **14 CLOSED_SCOPED / 90 OPEN_NOT_ACCEPTED** seulement si celle-ci passe. M32-067/068/071/075/078/088/099 restent [ ] : aucun montage produit, writer, authentification SQLite, scène/fiche M2 ni opération de production. Une future intégration chronologique doit réouvrir cette frontière pour revue, jamais héritage de preuve automatique. Writer/R1–R9 NOT_PROVEN ; G3 STOP_UNAVAILABLE ; PRODUCT_FIRST_PARALLEL_SAFETY ; M3.2 IN_PROGRESS_NOT_ACCEPTED.

# M32-074 — séparation canon M2 et chronologie M3.2 (23/11/2026)

**PREUVE CANDIDATE SOURCE SEULEMENT — M32-074 [ ] OPEN_NOT_ACCEPTED avant CI.**

Source parent protégé `b5f9f28115dd8acc2b933999e973ebbfcf90a6ba`, PR #424 MERGED Windows #45244745620 completed/SUCCESS HEAD `4723f0c5e3ee8c867355f12feaadedb3102a318b`, postmain indépendante #45262841960 encore NON QUALIFIÉE à la préparation.

Le canon M2 appartient à `src/FactWorkspace.tsx` et `src/factDomain.ts` : APPROVE_CANON/REVOKE_CANON exigent la confirmation humaine. `src/main.tsx` et `src/App.tsx` n'importent pas la chronologie de laboratoire ; les composants M32 de production fictive ne doivent importer ni l'UI des faits M2, ni l'autorité Tauri, ni une API d'écriture.

Trois gardes nouveaux intégrés au test de traçabilité exécuté en CI Windows : audit sur tous les modules M32 non-test, vérification de confirmation humaine M2, injections négatives de canon/IPC/réseau. Un quatrième garde laisse M32-074 ouverte avant qualification. Ces gardes ne démontrent ni admission runtime de la future interface intégrée, ni restauration, ni G3, ni writer. Toute intégration ultérieure doit requérir une preuve nouvelle.

**Aucune clôture maintenant : 13 CLOSED_SCOPED / 91 OPEN_NOT_ACCEPTED**, M32-074 [ ], M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %), PRODUCT_FIRST_PARALLEL_SAFETY. PR #35/#215 DRAFT NON_ADMITTED.

STOP Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP/R3 partiel/D3c conception/D3b-4/5 et D3b-5 STOP ; main/WAL/SHM live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
