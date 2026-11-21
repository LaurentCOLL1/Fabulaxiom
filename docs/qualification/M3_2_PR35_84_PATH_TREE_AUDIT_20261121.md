# PR #35 — audit SHA des 84 chemins (21/11/2026)

Arbres Git non tronqués : #35 HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5` / protected main `f1d3d0539c437f1111a300c8a955798d7c8e529c`. #35 et #215 DRAFT, aucune fusion. **84 chemins : 5 IDENTICAL / 11 DIVERGENT / 68 ABSENT**. Sur 68 absents : 26 DOC, 20 PY_TOOL, 20 PY_TEST, 2 RUST_SQL. Une différence SHA ≠ conflit fonctionnel ; un chemin absent ≠ défaut actuel.

**M32-007 [ ] et M32-050 [ ] OPEN_NOT_ACCEPTED.** KEEP_IDENTICAL_NO_REPLAY = ne pas recopier ; REVIEW_CURRENT_DIFF_NO_OVERRIDE = ne pas écraser main ; REVIEW_ABSENT_NO_AUTO_PORT = évaluer utilité/dépendances avant un éventuel portage ciblé. Ces valeurs ne sont que des orientations de triage, pas des décisions finales d'admission/rejet. Quatre chemins REVIEW de #215 restent séparés.

| Chemin PR35 | Blob #35 | Blob main | État | Orientation |
| --- | --- | --- | --- | --- |
| `.github/workflows/m0-ci.yml` | `e12bf78e22ba6eb71ed7678a0ddf4ad54fa35e27` | `c35a8f076b2770e676f63da48e9a93b6cc495b81` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `README.md` | `e0191b8f01d84fc97db40f1d5eb5031f0364d06d` | `9e3408aeb459170a006a60e94721fabcb1595f3b` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `docs/continuity/NEXT.md` | `b24b245b02c423f26f1a2315de0a6110a724eca0` | `a8852e941a3e59f752e6ded6ebb274db33b7e1c6` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `docs/continuity/STATE.md` | `0d05054b5bb5d7e7bbcffab846d09285f3272067` | `8d594323b4feb88ccf50c9ea18cf7127694f299e` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `docs/qualification/M3_2_ACTIVATION_MARKER_INVENTORY.md` | `b5529fc9bdcec01478600e699ef0b547e7f8d560` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_APPEND_ONLY_SUPERSESSION_DESIGN.md` | `28a93cb252bdef2b8aba68d3ec369dceccdd83b2` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_DIRECT_READONLY_CUSTODY.md` | `a82b76e5e55c57d3462ebfc081c0ece786a94b79` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_EXTERNAL_ATTESTATION_RESOLUTION_MATRIX.md` | `673fd153df11b479f7bb4893fc8b54c7826f1464` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_INDEPENDENT_AUTHORITY_GATE.md` | `0d5793f2250a2a9b8f2e23ed3c6a50b15177c99c` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_ISOLATED_IPC_PREFLIGHT.md` | `2b2bd2bbc9f20687f7a0a65242f4cdec1aff2457` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_ISOLATED_V7_PHYSICAL_READONLY.md` | `1211d66dd69e2d1bb703c434434e50d02703dbe5` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_M31_SEMANTIC_HARDENING.md` | `31f01f45dcdfe4dc72c90ee36ea854dbe2c96f4c` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_M31_SEMANTIC_READONLY_GATE.md` | `ee96c6a4abb91985aaa7069747ea1a7fc7e4d240` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_MANUAL_CHRONOLOGY_STAGE1.md` | `2d35b688093bfd75032dfae7082a3ea353857d7f` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_MANUAL_CHRONOLOGY_UX_CONTRACT.md` | `7372b2c332821faab238dfc4ed113aff963feece` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_MULTIROOT_READONLY_GATE.md` | `a1a515312d40f415ca014888246d820c6ec40aa5` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_POST_RESTART_GATE.md` | `0be718bc9e004daf0abba6e6591cc65e958d00c4` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_PROVENANCE_CLAIM_TRIAGE.md` | `9380c98f9bbbd2147e1db0c2fbe9d6c72c425337` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_BATCH_COHERENCE.md` | `4238b941a6157a924082813d0c2549aee1bd8b36` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_COMPARISON.md` | `619cc24ea5ad6f899745b30524b9996242faa6cd` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_COMPARISON_BATCH.md` | `9eb25d602bc9751bfd57a090a638aaffb4f2f367` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_NAVIGATION.md` | `02115fe271c6849cdffa60dd8db039927a10e62b` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_PAGINATION.md` | `9786816bb428abfc703b939f8c2b33bdbc7266f2` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_PRESENTATION.md` | `809e1772e4b212565f11af1ecec7d9bfdb989cac` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_PROJECTION.md` | `0650d66851135030a961e506eb1c8cc9c5ebb737` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_SELECTION_REVIEW.md` | `fe8849a7a4a30d6718d69294f1f34b167db422d8` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS.md` | `62740aed0cc1d959cd1a3abc0ef111f827c3f95e` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS_CONSULTATION.md` | `6ad6585df74e64f59077a8941ad74eb266d7266a` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS_PRESENTATION.md` | `d92c6d9f03b92a77613023bed8ff58c2296ecfa1` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `docs/qualification/M3_2_READONLY_HANDOFF_REFERENCE.md` | `a0215b0a5b47fabe3d1b7f2871b71f3a4fb02b7c` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `src-tauri/Cargo.toml` | `9c0c286062dbf3c881b7d76d1a1ea45d85385766` | `50a36053f4772bd11769d2cd13a5b8b633038a78` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/build.rs` | `32adde45c871d1c31639d1debc0fe779c0c69881` | `d860e1e6a7cac333c3cc0bc9cb67faf286b07d69` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/sql/m3_2_active_precedence_candidate.sql` | `4cec6e522c93f1be2605d1fc4040e58f58a29c9b` | `4cec6e522c93f1be2605d1fc4040e58f58a29c9b` | IDENTICAL | KEEP_IDENTICAL_NO_REPLAY |
| `src-tauri/sql/m3_2_chronology_decisions_candidate.sql` | `fbd2a6244e6356a68e4fa707a7395fcbafe0449e` | `786dc766769467ab6bf3243971855da31ff0dfbd` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/sql/m3_2_recursive_chain_candidate.sql` | `eeb1319c0e07c6c95e8e6fa628cbd10549b1393c` | `eeb1319c0e07c6c95e8e6fa628cbd10549b1393c` | IDENTICAL | KEEP_IDENTICAL_NO_REPLAY |
| `src-tauri/sql/m3_2_restatement_revocations_candidate.sql` | `846d3b7c88b9022327b347df035a2a307209ad87` | `846d3b7c88b9022327b347df035a2a307209ad87` | IDENTICAL | KEEP_IDENTICAL_NO_REPLAY |
| `src-tauri/sql/m3_2_restatement_successors_candidate.sql` | `efa953964633312dd5d3a3ef2b9c271dde3a600c` | `efa953964633312dd5d3a3ef2b9c271dde3a600c` | IDENTICAL | KEEP_IDENTICAL_NO_REPLAY |
| `src-tauri/sql/m3_2_successor_revocations_candidate.sql` | `ad0d31c13ee38850eb022e85efa8549c86c11f12` | `ad0d31c13ee38850eb022e85efa8549c86c11f12` | IDENTICAL | KEEP_IDENTICAL_NO_REPLAY |
| `src-tauri/src/lib.rs` | `22cd1cdcbc5ecd9ae08bfa5e926ea56834c6a343` | `25796459e334f040f7e8ec8e677636f37f6dc947` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/src/m32_isolated_preflight.rs` | `49a41a233e342a0ea541f74c4cea7dfedcb887c5` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `src-tauri/src/m32_manual_chronology.rs` | `f75e4bc7787b60ac345cbe137355f4888243829c` | `c5542fed19b338752563f144a9484a34f9f79688` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/src/m32_sqlite_concurrency_tests.rs` | `a940fb0996ae9361c69768979969f4b29ad7f6aa` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `src/M32ChronologyPreview.tsx` | `d7b6e5972a4730f487d346ae4e8116a9f7d84bca` | `f57a48f26b4460d9f0aefec23b1880e722a3d860` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src/m32ChronologyPreview.test.tsx` | `bdc8e0b5ec3d22a784a864e81c82895915d2bc08` | `c6aa039d3e8ad0db556dc1a7f53417d82f4c3193` | DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `tools/m3_2_chronology_batch_coherence_reference.py` | `092906f5d7c1f71303f3eff0659eebaa42926c9f` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_comparison_batch_reference.py` | `fabc802887e5f7960c0fac255021050d87e03339` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_comparison_reference.py` | `9f6dfd8d09cb4829b6b2ee168f0a1043212d1885` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_navigation_reference.py` | `5826f9c79532e11520e139637859b1d778f92e7f` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_pagination_reference.py` | `f3f1da59524ea863044b87346f6fde87ce4a5597` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_presentation_reference.py` | `811f29ba968a401fbafa3dbf423ddee0527c505b` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_projection_reference.py` | `b4fbf91d787e7083672d5c068b5f02bc16eacf91` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_readonly_handoff_reference.py` | `0f3607ad9e74dd1934e0e0ab21a39dd25e9587f2` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_selection_review_reference.py` | `a6985f28f1f91cd4afc415469ef59c11f867c5c4` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_witness_consultation_reference.py` | `93969516981211ffd3723daaa222121c55cf9773` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_witness_presentation_reference.py` | `c346fbf923ca4e6bf87d188c846b167ea4c479af` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_chronology_witness_reference.py` | `8dfdf8b706593c84be5b151b61080ae44c3dd007` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_direct_custody_readonly.py` | `b50f86359708e0ccc37679d77a50c79192d58de8` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_independent_authority_gate.py` | `baafb72e571de8dc85986749a7c9755ef7f5ca44` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_isolated_v7_physical_readonly.py` | `2a6bb6f67eb7e2c97483b25d2e27f5e3dbe37acd` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_m31_semantic_readonly.py` | `82044b24c8f70fd9c5f414c53cd20039e98ae682` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_multiroot_readonly.py` | `171fdd7c067f217c2985d510908326507a187d6b` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_operator_readonly_gate.py` | `6a2281e9b12e2a83f282e1bfd936eb3314ef6108` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_provenance_triage.py` | `0f40cc90905b2e22dcde364b3896a86dc7b62200` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/m3_2_supersession_reference.py` | `77ff7cf61e8fe6df581cab3ba83b21cd4e0c5c3a` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_batch_coherence_reference.py` | `cfea445305060c139f62248f8b01cb812a169296` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_comparison_batch_reference.py` | `f9696030d20321d9dc9789a1fb12ce5cca3b39c3` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_comparison_reference.py` | `6488ec2fdec95566358e48d0c6ef1ddbb5d7fad7` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_navigation_reference.py` | `91fabd546a22fb8f98481f7f0b8cba85600a1490` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_pagination_reference.py` | `77793b6f55fcc4b2a9696424c3d9c44bf50a5833` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_presentation_reference.py` | `44f30a03c4fe751513394e1a5f1ab0a1646590cc` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_projection_reference.py` | `9f5d7917ac30d7f11d142fe1db72bae0ae971ab7` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_readonly_handoff_reference.py` | `131887a4552551eda574f55ad64538026478abe0` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_selection_review_reference.py` | `86dac0ab3aa3ae3fe524c2d77a406fd1852d2160` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_witness_consultation_reference.py` | `9b4c19e7c3a62d6f56566655ac489af26e31cc4e` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_witness_presentation_reference.py` | `a7b64a754ee42b74c4e8bb0d65e83cb929cd0d8c` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_chronology_witness_reference.py` | `11e93ed4e45f5da5f488bb01b21e8eb6e05b49f0` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_direct_custody_readonly.py` | `fd98291dd4590d9c446415bcc0c1d177dd2bafa8` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_independent_authority_gate.py` | `d03b32d9e6d18be114fd7096392c6e73f0301088` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_isolated_v7_physical_readonly.py` | `0b1cd5393ff6943126b4ee8e0fb4bc655ef4fec5` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_m31_semantic_readonly.py` | `d1831b3c2b3b3f09f0f87cd99608fc18123464a4` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_multiroot_readonly.py` | `87d1fe01a8f193a2efddc82f53a1e2d230b4b1ef` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_operator_readonly_gate.py` | `ca7ada469eec00f07d984be8aefc4f881661c0c7` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_provenance_triage.py` | `6703160f7ca532f6c9c8f99ece2a84e5b01187da` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |
| `tools/test_m3_2_supersession_reference.py` | `cc91ab96c0928974a4f01230a4365dde9e88862b` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |

## Travaux restants

Étudier indépendamment les 40 Python absents (témoins jetables uniquement), les 2 Rust/SQL absents et 11 divergents (cfg(test), workflow, lib.rs, recouvrements) sans admission writer ; conserver les 26 docs comme références historiques sans rétablir une autorité ancienne. Finir les quatre revues PR215. Aucun cherry-pick/merge en bloc.

M3.2 IN_PROGRESS_NOT_ACCEPTED, PRODUCT_FIRST_PARALLEL_SAFETY. STOP Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5, D3b-5 STOP ; main/WAL/SHM, live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED. STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
