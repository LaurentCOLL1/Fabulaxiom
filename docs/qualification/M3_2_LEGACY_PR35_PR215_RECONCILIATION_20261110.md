# M3.2 — Réconciliation source-only des PR historiques #35 et #215

**10 novembre 2026, lecture GitHub publique, sans opération locale.** Parent protégé `main=7ffd1fb7ae2091dcba05a7c29860b0e11961a093` (#333), CI postmain indépendante [#42757811330](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/42757811330) SUCCESS au SHA exact. Ruleset Protect main ACTIVE, checks strict, bypass=[]. Ces résultats ne donnent aucune admission writer, ni autorisation Windows opérateur.

## Comparaison exhaustive des 107 chemins de diff

| PR | HEAD historique | Chemins | SHA blob identiques à main | Même chemin, octets différents | Chemins absents de main | Situation |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| [#35](https://github.com/LaurentCOLL1/Fabulaxiom/pull/35) | `41ce7b915e76d22785d53d7fffe288d113dd0bf5` | 84 | **5** | **11** | **68** | OPEN/DRAFT ; pas de merge ou rebase direct |
| [#215](https://github.com/LaurentCOLL1/Fabulaxiom/pull/215) | `8203b7323877edc87ffabaad1694c52d2523023d` | 23 | **6** | **17** | **0** | OPEN/DRAFT au checkpoint ; témoin D3b déjà conservé dans main |

Méthode : les chemins du diff de chaque PR sont comparés aux arbres Git des HEAD exacts et de `main`, via les SHA blobs. **Identique** = mêmes octets pour ce chemin ; **différent** = même nom mais octets différents (pas nécessairement conflit sémantique) ; **absent** = chemin non présent (pas nécessairement fonctionnalité perdue, un portage peut avoir été renommé). Une comparaison de chemins **n'est pas un test d'exécution** ; aucune ancienne CI n'est transposée sur main.

## PR #215 — D3b présente, refus de recovery toujours actif

Le module Rust `mod d3b_p1_disposable_crash_refusal` dans `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs` a été comparé textuellement sur les deux HEAD : **10 097 caractères identiques** entre #215 et main, quatre tests préservés :
- `m32_d3b_child_fixture_terminate_before_sqlite_close`
- `m32_d3b_committed_wal_abandoned_mutex_refuses_unattested_reopen`
- `m32_d3b_pending_wal_vanished_mutex_still_refuses_unattested_reopen`
- `m32_d3b_busy_close_does_not_attest_restart_even_after_final_close`

`src-tauri/src/lib.rs` conserve `#[cfg(all(test, windows))]` devant ce module. Les **six dossiers** de qualification D2/D3/D3a/D3b/P1 de #215 ont les SHA blobs identiques à main. Les 17 autres fichiers ont évolué depuis 28/10 : ne **jamais restaurer** leurs anciennes versions de continuité/test en fusionnant #215. D3b ne prouve ni recovery, ni garde atomique main/WAL/SHM, ni writer production. **Clôture ultérieure de #215 en tant que superseded possible uniquement avec justification et journal #38**, sans merge de son contenu ancien.

## PR #35 — décision de portage réellement ouverte

Le service `src-tauri/src/m32_manual_chronology.rs` est déjà sur main avec des fonctions supplémentaires et `#[cfg(test)]` dans `src-tauri/src/lib.rs` : pas d'IPC writer. Les cinq SQL candidats identiques sont listés plus bas ; `m3_2_chronology_decisions_candidate.sql` diffère. Les **68 chemins absents** comprennent des études, références Python/test-only, `m32_isolated_preflight.rs` et `m32_sqlite_concurrency_tests.rs` anciens. Les absences de chemins ne prouvent ni manque fonctionnel ni absence de garde ; **triage unitaire obligatoire**, à commencer par les quatre temporalités, 2 Universes, 2 Romans, conflits, supersession et sources historiques exactes. Un ancien IPC préflight même « metadata only » n'est **pas autorisé** à être réintroduit sans nouvelle revue.

Décision : conserver #35 OPEN/DRAFT ; construire une branche neuve pour chaque **portage ciblé** nécessaire, sans modifier sa branche historique ni les fichiers opérateur. Référence : `M3_2_PR35_SAFE_RECONCILIATION_PLAN.md`.

## Checklist et frontières

**M32-007 [ ] reste OUVERTE. AUCUNE case nouvelle clôturée** : les 107 noms sont inventoriés mais les 68 chemins absents de #35 n'ont pas tous une décision de portage/abandon fondée sur leurs comportements. M32-011/012, 016–020, 025–027, 050 et la décision de writer/R1–R9 restent ouvertes. Ce rapport documente une preuve **partielle**, pas l'acceptation d'une étape réelle.

**PRODUCT_FIRST_PARALLEL_SAFETY** inchangée : informer AVANT tout changement. M3.2 **IN_PROGRESS_NOT_ACCEPTED** (~45 % estimés) ; writer/R1–R9 **NOT_PROVEN**, P4 réel STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 **STOP_UNAVAILABLE** ; main/WAL/SHM atomique et ABA invisible NOT PROVEN ; historique **PENDING_EXTERNAL_ATTESTATION(21/3/2)** ; prospective NOT_STARTED ; glib issue #160 **OPEN_NOT_REMEDIATED**. STOP originaux v6/v7, profil Greenfield existant, backups/journaux, IPC writer, migration 007, Hello natif ou recovery. CI fictive ≠ admission.

## Inventaire de chaque chemin (aucun caché)

### pr35 : identical (5)

- `src-tauri/sql/m3_2_active_precedence_candidate.sql`
- `src-tauri/sql/m3_2_recursive_chain_candidate.sql`
- `src-tauri/sql/m3_2_restatement_revocations_candidate.sql`
- `src-tauri/sql/m3_2_restatement_successors_candidate.sql`
- `src-tauri/sql/m3_2_successor_revocations_candidate.sql`

### pr35 : different (11)

- `.github/workflows/m0-ci.yml`
- `README.md`
- `docs/continuity/NEXT.md`
- `docs/continuity/STATE.md`
- `src-tauri/Cargo.toml`
- `src-tauri/build.rs`
- `src-tauri/sql/m3_2_chronology_decisions_candidate.sql`
- `src-tauri/src/lib.rs`
- `src-tauri/src/m32_manual_chronology.rs`
- `src/M32ChronologyPreview.tsx`
- `src/m32ChronologyPreview.test.tsx`

### pr35 : absent (68)

- `docs/qualification/M3_2_ACTIVATION_MARKER_INVENTORY.md`
- `docs/qualification/M3_2_APPEND_ONLY_SUPERSESSION_DESIGN.md`
- `docs/qualification/M3_2_DIRECT_READONLY_CUSTODY.md`
- `docs/qualification/M3_2_EXTERNAL_ATTESTATION_RESOLUTION_MATRIX.md`
- `docs/qualification/M3_2_INDEPENDENT_AUTHORITY_GATE.md`
- `docs/qualification/M3_2_ISOLATED_IPC_PREFLIGHT.md`
- `docs/qualification/M3_2_ISOLATED_V7_PHYSICAL_READONLY.md`
- `docs/qualification/M3_2_M31_SEMANTIC_HARDENING.md`
- `docs/qualification/M3_2_M31_SEMANTIC_READONLY_GATE.md`
- `docs/qualification/M3_2_MANUAL_CHRONOLOGY_STAGE1.md`
- `docs/qualification/M3_2_MANUAL_CHRONOLOGY_UX_CONTRACT.md`
- `docs/qualification/M3_2_MULTIROOT_READONLY_GATE.md`
- `docs/qualification/M3_2_POST_RESTART_GATE.md`
- `docs/qualification/M3_2_PROVENANCE_CLAIM_TRIAGE.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_BATCH_COHERENCE.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_COMPARISON.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_COMPARISON_BATCH.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_NAVIGATION.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_PAGINATION.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_PRESENTATION.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_PROJECTION.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_SELECTION_REVIEW.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS_CONSULTATION.md`
- `docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS_PRESENTATION.md`
- `docs/qualification/M3_2_READONLY_HANDOFF_REFERENCE.md`
- `src-tauri/src/m32_isolated_preflight.rs`
- `src-tauri/src/m32_sqlite_concurrency_tests.rs`
- `tools/m3_2_chronology_batch_coherence_reference.py`
- `tools/m3_2_chronology_comparison_batch_reference.py`
- `tools/m3_2_chronology_comparison_reference.py`
- `tools/m3_2_chronology_navigation_reference.py`
- `tools/m3_2_chronology_pagination_reference.py`
- `tools/m3_2_chronology_presentation_reference.py`
- `tools/m3_2_chronology_projection_reference.py`
- `tools/m3_2_chronology_readonly_handoff_reference.py`
- `tools/m3_2_chronology_selection_review_reference.py`
- `tools/m3_2_chronology_witness_consultation_reference.py`
- `tools/m3_2_chronology_witness_presentation_reference.py`
- `tools/m3_2_chronology_witness_reference.py`
- `tools/m3_2_direct_custody_readonly.py`
- `tools/m3_2_independent_authority_gate.py`
- `tools/m3_2_isolated_v7_physical_readonly.py`
- `tools/m3_2_m31_semantic_readonly.py`
- `tools/m3_2_multiroot_readonly.py`
- `tools/m3_2_operator_readonly_gate.py`
- `tools/m3_2_provenance_triage.py`
- `tools/m3_2_supersession_reference.py`
- `tools/test_m3_2_chronology_batch_coherence_reference.py`
- `tools/test_m3_2_chronology_comparison_batch_reference.py`
- `tools/test_m3_2_chronology_comparison_reference.py`
- `tools/test_m3_2_chronology_navigation_reference.py`
- `tools/test_m3_2_chronology_pagination_reference.py`
- `tools/test_m3_2_chronology_presentation_reference.py`
- `tools/test_m3_2_chronology_projection_reference.py`
- `tools/test_m3_2_chronology_readonly_handoff_reference.py`
- `tools/test_m3_2_chronology_selection_review_reference.py`
- `tools/test_m3_2_chronology_witness_consultation_reference.py`
- `tools/test_m3_2_chronology_witness_presentation_reference.py`
- `tools/test_m3_2_chronology_witness_reference.py`
- `tools/test_m3_2_direct_custody_readonly.py`
- `tools/test_m3_2_independent_authority_gate.py`
- `tools/test_m3_2_isolated_v7_physical_readonly.py`
- `tools/test_m3_2_m31_semantic_readonly.py`
- `tools/test_m3_2_multiroot_readonly.py`
- `tools/test_m3_2_operator_readonly_gate.py`
- `tools/test_m3_2_provenance_triage.py`
- `tools/test_m3_2_supersession_reference.py`

### pr215 : identical (6)

- `docs/qualification/M3_2_V7_P1_D2_DISPOSABLE_SESSION_VFS_WAL_SHM_EXPERIMENT_20261028.md`
- `docs/qualification/M3_2_V7_P1_D3A_WAL_SHM_HANDLE_CUSTODY_DISPOSABLE_WINDOWS_FIXTURE_20261028.md`
- `docs/qualification/M3_2_V7_P1_D3B_DISPOSABLE_WINDOWS_CRASH_RESTART_REFUSAL_FIXTURE_20261028.md`
- `docs/qualification/M3_2_V7_P1_D3_WAL_SHM_LIFECYCLE_CRASH_RESTART_DESIGN_20261028.md`
- `docs/qualification/M3_2_V7_P1_SINGLE_OWNER_SESSION_PROOF_PLAN_20261028.md`
- `docs/qualification/M3_2_V7_PRODUCTION_WRITER_CUSTODY_DESIGN_STUDY_20261028.md`

### pr215 : different (17)

- `README.md`
- `docs/continuity/HANDOFF_CURRENT.json`
- `docs/continuity/HANDOFF_CURRENT.md`
- `docs/continuity/HANDOFF_HISTORY.md`
- `docs/continuity/HANDOFF_PROTOCOL.md`
- `docs/continuity/M3_2_GATE_DECISION_CURRENT.md`
- `docs/continuity/NEXT.md`
- `docs/continuity/README.md`
- `docs/continuity/RESUME_PROMPT.md`
- `docs/continuity/RESUME_PROMPT_SHORT.md`
- `docs/continuity/STATE.md`
- `docs/roadmap/FABULAXIOM_ROADMAP_V1.md`
- `docs/roadmap/ROADMAP_STATUS_CURRENT.md`
- `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs`
- `tools/m32_rust_sqlite_open_inventory.py`
- `tools/test_m32_handoff_contract.py`
- `tools/test_m32_rust_sqlite_open_inventory.py`

### pr215 : absent (0)

Aucun.


*Chaque ligne est un chemin du diff historique au SHA indiqué, pas une preuve d'admission.*
