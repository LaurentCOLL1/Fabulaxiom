# PR #215 — 4 chemins REVIEW comparés sur les tests nommés (21/11/2026)

État de référence : [#215](https://github.com/LaurentCOLL1/Fabulaxiom/pull/215) DRAFT HEAD `8203b7323877edc87ffabaad1694c52d2523023d` ; protected main=`8ad583528179061c473359b3a62713afc38c4cbe` après #405. Inventaire Git du contenu uniquement, **pas de preuve de comportement équivalent ni de runtime**.

| Chemin REVIEW #215 | Cas/nom anciens | Cas/nom sur main | Noms anciens absents | Disposition |
| --- | ---: | ---: | ---: | --- |
| `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs` | 26 | 34 | 0 | REVIEW_CFG_TEST_ONLY |
| `tools/m32_rust_sqlite_open_inventory.py` | source, 0 test | source, 0 test | n/a | REVIEW_READONLY_INVENTORY |
| `tools/test_m32_handoff_contract.py` | 152 | 183 | 7 | REVIEW_HANDOFF_GUARDS |
| `tools/test_m32_rust_sqlite_open_inventory.py` | 41 | 69 | 0 | REVIEW_INVENTORY_TESTS |

Analyse strictement sur les définitions `def test_*`, `fn m32_*` et `def guard_*` : 26/26 fonctions Rust nommées anciennes existent sur main et huit fonctions supplémentaires ; 41/41 tests d'inventaire Python anciens existent sur main. Dans le contrat handoff, 145 noms anciens sur 152 sont encore présents ; **les 7 absents** sont `test_146_production_writer_custody_design_has_no_runtime_admission`, `test_147_owner_p1_trusted_sid_ollama_context_no_runtime_promotion`, `test_148_p1_single_owner_session_proof_plan_is_documentary_only`, `test_149_p1_d2_windows_disposable_integrated_session_is_not_runtime`, `test_150_p1_d3_design_separates_volatile_mutex_wal_shm_crash_from_runtime`, `test_151_d3a_windows_disposable_delegated_wal_shm_close_is_not_runtime`, `test_152_d3b_windows_disposable_crash_requires_stop_before_sqlite_reopen`. **Noms disparus ≠ garanties perdues** : tests courants #146–#152 ont été remplacés/renumérotés ; revue des assertions et témoins réels requise.

Aucune copie de l'ancienne branche ; les quatre chemins demeurent **REVIEW**, aucun des tests nommés n'autorise D3b-4/5, R3/R4 ou recovery. Prochaines preuves : comparer assertions des 7 tests de handoff et source de l'outil d'inventaire, puis contrôler CI Windows des témoins jetables et éviter toute dégradation des garde-fous modernes. PR #35 68 absents sans décision d'admission ; M32-007 [ ] et M32-050 [ ] OPEN_NOT_ACCEPTED, 104=12/92.

M3.2 IN_PROGRESS_NOT_ACCEPTED, PRODUCT_FIRST_PARALLEL_SAFETY. STOP Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5, D3b-5 STOP ; main/WAL/SHM, live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
