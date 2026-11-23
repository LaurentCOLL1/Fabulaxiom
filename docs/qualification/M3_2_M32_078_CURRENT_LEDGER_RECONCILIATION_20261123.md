# M32-078 — réconciliation du registre courant et de l'instantané du 22 novembre

**23/11/2026 SOURCE_ONLY_CANDIDATE_UNQUALIFIED ; HISTORICAL_REPORT_SNAPSHOT_NOT_CURRENT ; NO_AUTO_ACCEPTANCE ; NO_RUNTIME_ADMISSION ; OPEN_NOT_ACCEPTED.**

Le compte rendu historique `docs/qualification/M3_2_M32_078_ACCEPTED_PROOF_GAPS_20261122.md` annonçait **12 CLOSED_SCOPED / 92 OPEN_NOT_ACCEPTED** au 22 novembre. Son JSON associé, la matrice des exigences et la checklist concordent désormais sur **104 exigences : 13 CLOSED_SCOPED / 91 OPEN_NOT_ACCEPTED**, soit **12/92 → 13/91**. L'ancien texte est conservé comme photographie datée et porte un addendum explicite.

| Gates des 91 preuves manquantes | Nombre |
| --- | ---: |
| RUNTIME_NOT_ADMITTED | 42 |
| REQUIRES_INDEPENDENT_R1_G2_PROOFS | 39 |
| SCOPED_EVIDENCE_REQUIRED | 10 |
| **Total ouvert** | **91** |

La clôture documentaire limitée **M32-003 [x]** explique notamment la variation. Aucune ouverture n'a été admise : les 91 lignes du registre restent alignées par ID, track, gate, verification_target et next_proof sur la matrice actuelle ; `accepted_evidence=NONE_ACCEPTED`, `accepted_workflow_head_sha=null`, `accepted_workflow_run_id=null`, `accepted_job_id=null`, `accepted_operator_runtime=false`. Les tests et CI synthétiques ne peuvent remplir ces champs automatiquement.

Parent protégé `main=c79494cbe5a7b7adaa3b39be9cfd3997b3f6126b` après #422 MERGED, CI source #45203664419 completed/SUCCESS au HEAD exact `6c8e567f1a6fc2e81a0de8de54315b82cda30f0c`, postmain indépendante #45211260869 événement push sur parent exact **PENDING_UNQUALIFIED** à la préparation ; journal #38 #7106434972. Ce rapport est un rapprochement documentaire, **pas** une admission de preuve d'exécution.

**M32-078 [ ] reste ouverte**, comme M32-007/050/071/075/081/092/093 ; checklist 104 = 13/91 ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif) ; PRODUCT_FIRST_PARALLEL_SAFETY ; PR #35/#215 DRAFT NON_ADMITTED.

**STOP Writer/R1–R9 NOT_PROVEN**, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED, R2 STOP/R3 partiel/D3c conception/D3b-4/5 et D3b-5 STOP, main/WAL/SHM live SQLite WAL-index et ABA NOT_PROVEN, glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.

Trois contrôles Python source-only distinguent anciens et nouveaux comptes, interdisent la fausse acceptation et la clôture artificielle. Nouvelle CI Windows HEAD exacte requise.
