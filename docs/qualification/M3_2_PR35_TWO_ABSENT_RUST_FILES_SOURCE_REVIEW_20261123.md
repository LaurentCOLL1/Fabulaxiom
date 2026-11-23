# PR35 — deux modules Rust historiques absents (23/11/2026)

**SOURCE_ONLY_CANDIDATE_UNQUALIFIED ; NO_AUTO_PORT ; NO_RUNTIME_ADMISSION ; NO_SEMANTIC_EQUIVALENCE ; OPEN_NOT_ACCEPTED.**
Ancienne PR #35 HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5`; parent candidat protégé `main=2116f8a7b1725f9fad552be4ffb7795f8a9552eb` après fusion #420. Inspection de fichiers Git historiques uniquement ; aucune compilation, import, test Rust ancien ou accès aux données utilisateur. **2/2 ABSENT_NOT_ADMITTED ; 0/2 PORTED ; 0/2 ADMITTED**.

| Chemin historique absent de main | SHA blob historique Git | Catégorie | Définitions `#[test]` historiques | Décision |
| --- | --- | --- | --- | --- |
| `src-tauri/src/m32_isolated_preflight.rs` | `49a41a233e342a0ea541f74c4cea7dfedcb887c5` | OLD_METADATA_ONLY_IPC | 3 | HISTORICAL_SOURCE_ONLY |
| `src-tauri/src/m32_sqlite_concurrency_tests.rs` | `a940fb0996ae9361c69768979969f4b29ad7f6aa` | CI_SCRATCH_SQLITE_TESTS | 3 | HISTORICAL_SOURCE_ONLY |

## Contraintes de non-transfert

- `m32_isolated_preflight.rs` correspondait à un ancien feature de préflight DEVELOPMENT-ONLY et une **commande Tauri de métadonnées seulement**. Son propre en-tête nie les écritures/SQLite, mais sa réintroduction comme commande ou capacité IPC n'est pas autorisée. Les trois tests Rust historiques examinent des identifiants, accusés et statuts de refus. **BLOCK_RUNTIME_IPC**, aucune décision opérateur implicite.
- `m32_sqlite_concurrency_tests.rs` décrit trois tests `#[test]` portant sur deux connexions, WAL et rollback d'un **fichier SQLite temporaire créé par le runner**. La suppression par son garde RAII concerne exclusivement les sidecars de cette fixture jetable. **Jamais le `main/-wal/-shm` d'un opérateur**, ni témoin suffisant de SHM live, Win32, ABA, provenance ou writer R1–R9. **BLOCK_OPERATOR_SQLITE**.
- Les services Rust et tests existants dans `main` possèdent des contrats et gates distincts. La présence de fonctions ressemblantes, un ancien succès CI sur la PR #35 ou les 3+3 tests historiques **ne prouve aucune équivalence** ni admission.
- L'inventaire PR #35 compte toujours 84 chemins : 5 identiques, 11 divergents, 68 absents. Les 26 documents et 20 couples Python ont des dossiers source-only séparés ; la PR #215 reste DRAFT avec ses 4 chemins REVIEW_NON_ACCEPTED.

M32-007 [ ] ; M32-050 [ ] ; M32-078 [ ] — **13 CLOSED_SCOPED / 91 OPEN_NOT_ACCEPTED (104)**. M3.2 IN_PROGRESS_NOT_ACCEPTED (~45% indicatif) ; PRODUCT_FIRST_PARALLEL_SAFETY ; PR #35/#215 DRAFT NON_ADMITTED.

**STOP Writer/R1–R9 NOT_PROVEN** ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5 et D3b-5 STOP ; live SQLite WAL-index, main/WAL/SHM, ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.

Trois gardes #40–42 strictement Python source-only contrôlent SHA/absence/restauration interdite, fausse promotion et clôture. **Nouvelle CI Windows HEAD exacte requise** avant intégration documentaire.
