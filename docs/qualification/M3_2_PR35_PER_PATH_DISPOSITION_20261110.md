# M3.2 — Disposition unitaire des 84 chemins de l'ancienne PR #35

**10 novembre 2026.** Source historique [PR #35](https://github.com/LaurentCOLL1/Fabulaxiom/pull/35) HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5`, référence de comparaison protected `main=425cb621d20b86f66a24aac1d6c1f63ffe479b0c` (postmain #42847268108, attempt 1, terminal SUCCESS au SHA exact, Windows 88 succès/1 skipped). La PR #334 a fusionné le [rapport SHA-blobs](M3_2_LEGACY_PR35_PR215_RECONCILIATION_20261110.md). **Le présent triage ne change aucune branche historique et ne transforme aucune ancienne preuve en admission.**

## État des décisions — M32-007 reste ouverte

Chaque chemin ci-dessous reçoit une **orientation d'action explicite**, mais « REVIEW » et « HOLD » restent des demandes d'examen, **pas** des dispositions finales de portage/abandon. **AUCUNE case nouvelle clôturée : 104 obligations, M32-001/002 closes, 102 ouvertes, M32-007 [ ] ouverte.** Toute fermeture future exige preuve de comparaison fonctionnelle et décision de portage ciblé ou d'abandon motivé, puis source CI Windows exacte et postmain, issue #38 append-only.

Les **5 chemins identiques** sont conservés sans portage ; les **11 chemins divergents** requièrent revue ciblée, jamais écrasement ; les **68 absents de main** comportent 26 dossiers historiques, 20 scripts Python de référence, leurs 20 tests, et 2 modules Rust. Une absence de chemin ne prouve pas une fonctionnalité absente.

## Prochain lot concret (ordre)

1. **Produit / chronologie fictive** : comparer le service `m32_manual_chronology.rs` et le laboratoire `M32ChronologyPreview.tsx` actuels aux contrats de Stage 20–32 de #35, particulièrement pagination/sélection cohérente, témoins d'ordre, supersession et 2 univers/romans. Porter **un** cas négatif strictement fictif uniquement si non couvert, sur PR neuve + checklist vivante.
2. **Rust CI jetable** : examiner `m32_sqlite_concurrency_tests.rs` contre les protections actuelles ; ne porter que des témoins nouveaux sur fichier jetable. Aucun `SQLite` opérateur, aucun processus Windows utilisateur.
3. **Audits opérateur/G2B–G6** : conserver comme références historiques les vieux scripts et études de custody ; **aucun accès à l'ancien profil, backups, ACL, journaux ou aux cinq attestations manquantes**. Leurs tests ne changent pas `PENDING_EXTERNAL_ATTESTATION(21/3/2)`.
4. **IPC ancien** : ne pas porter `m32_isolated_preflight.rs` (même metadata-only) sans nouveau dossier, revue et autorisation distincte. Conserver `#[cfg(test)]` pour les services Rust de laboratoire.
5. **PR #215** : test-only D3b existe sur main, bloc identique de 10 097 caractères et six dossiers inchangés ; décision de clôture `superseded` possible seulement sur preuve et journal #38, **sans** merger ses 17 anciens fichiers divergents.

## Matrice exhaustive : un statut par chemin de #35

| Chemin exact de #35 | Orientation | Motif, portée et prochaine preuve |
| --- | --- | --- |
| `src-tauri/sql/m3_2_active_precedence_candidate.sql` | `KEEP_IDENTICAL` | SHA blob identique dans main au checkpoint #334 : garder l'existant, ne pas cherry-pick. |
| `src-tauri/sql/m3_2_recursive_chain_candidate.sql` | `KEEP_IDENTICAL` | SHA blob identique dans main au checkpoint #334 : garder l'existant, ne pas cherry-pick. |
| `src-tauri/sql/m3_2_restatement_revocations_candidate.sql` | `KEEP_IDENTICAL` | SHA blob identique dans main au checkpoint #334 : garder l'existant, ne pas cherry-pick. |
| `src-tauri/sql/m3_2_restatement_successors_candidate.sql` | `KEEP_IDENTICAL` | SHA blob identique dans main au checkpoint #334 : garder l'existant, ne pas cherry-pick. |
| `src-tauri/sql/m3_2_successor_revocations_candidate.sql` | `KEEP_IDENTICAL` | SHA blob identique dans main au checkpoint #334 : garder l'existant, ne pas cherry-pick. |
| `.github/workflows/m0-ci.yml` | `REVIEW_DIVERGENCE` | Conserver le workflow strict actuel ; la configuration du brouillon ne porte pas les contrats CI ajoutés depuis. |
| `README.md` | `REVIEW_DIVERGENCE` | Conserver le sommaire courant et les nouveaux gates ; ancienne copie non transposable. |
| `docs/continuity/NEXT.md` | `REVIEW_DIVERGENCE` | Journal courant et étapes depuis #35 : ne pas écraser avec le checkpoint d'octobre. |
| `docs/continuity/STATE.md` | `REVIEW_DIVERGENCE` | L'état courant de protection prime sur le statut ancien de #35. |
| `src-tauri/Cargo.toml` | `REVIEW_DIVERGENCE` | Comparer seulement d'éventuels besoins test-only, sans déplacer les dépendances du Rust actuel. |
| `src-tauri/build.rs` | `REVIEW_DIVERGENCE` | Conserver les contraintes de build actuelles ; ancienne configuration non admise. |
| `src-tauri/sql/m3_2_chronology_decisions_candidate.sql` | `REVIEW_DIVERGENCE` | Les octets diffèrent ; comparer contraintes, supersessions et refus avant toute proposition de migration. |
| `src-tauri/src/lib.rs` | `REVIEW_DIVERGENCE` | Le main courant garde m32_manual_chronology derrière cfg(test) ; aucun IPC préflight à réintroduire. |
| `src-tauri/src/m32_manual_chronology.rs` | `REVIEW_DIVERGENCE` | Le service est déjà porté en test-only et enrichi ; faire une analyse différentielle des fonctions et scénarios, jamais de remplacement. |
| `src/M32ChronologyPreview.tsx` | `REVIEW_DIVERGENCE` | Le parcours fictif courant a évolué ; comparer uniquement comportements non couverts, aucun portage complet. |
| `src/m32ChronologyPreview.test.tsx` | `REVIEW_DIVERGENCE` | Préserver les nouveaux tests ; sélectionner uniquement des cas négatifs non couverts et indépendants. |
| `docs/qualification/M3_2_ACTIVATION_MARKER_INVENTORY.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_APPEND_ONLY_SUPERSESSION_DESIGN.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de rectification append-only sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_DIRECT_READONLY_CUSTODY.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_EXTERNAL_ATTESTATION_RESOLUTION_MATRIX.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_INDEPENDENT_AUTHORITY_GATE.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_ISOLATED_IPC_PREFLIGHT.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement. Ancienne identité préflight non autorisée. |
| `docs/qualification/M3_2_ISOLATED_V7_PHYSICAL_READONLY.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_M31_SEMANTIC_HARDENING.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_M31_SEMANTIC_READONLY_GATE.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_MANUAL_CHRONOLOGY_STAGE1.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de chronologie manuelle sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_MANUAL_CHRONOLOGY_UX_CONTRACT.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de chronologie manuelle sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_MULTIROOT_READONLY_GATE.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_POST_RESTART_GATE.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_PROVENANCE_CLAIM_TRIAGE.md` | `ARCHIVE_OPERATOR_GATE` | Étude d'audit/autorité historique (source PR #35) ; préserver pour #36 et les gates G2B–G6, mais aucun nouveau script sur profil/bases/archives opérateur sans consentement.  |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_BATCH_COHERENCE.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de présentation chronologique sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_COMPARISON.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de présentation chronologique sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_COMPARISON_BATCH.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de présentation chronologique sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_NAVIGATION.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de navigation paginée sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_PAGINATION.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de navigation paginée sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_PRESENTATION.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de présentation chronologique sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_PROJECTION.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de présentation chronologique sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_SELECTION_REVIEW.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de présentation chronologique sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de preuve d'ordre sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS_CONSULTATION.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de preuve d'ordre sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS_PRESENTATION.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de preuve d'ordre sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `docs/qualification/M3_2_READONLY_HANDOFF_REFERENCE.md` | `ARCHIVE_SYNTHETIC_DESIGN` | Contrat/étude historique de présentation chronologique sur données fictives ; confronter aux tests TS/Rust actuels avant portage, ne pas republier l'ancien statut candidat comme vérité actuelle. |
| `src-tauri/src/m32_isolated_preflight.rs` | `BLOCK_RUNTIME_IPC` | Ancien préflight déclarant un IPC metadata-only ; aucun enregistrement IPC, profil ou commande Windows sans gate distinct et accord opérateur. |
| `src-tauri/src/m32_sqlite_concurrency_tests.rs` | `REVIEW_CI_ONLY` | Tests Rust sur SQLite jetable à deux connexions ; envisager seulement les contre-exemples non déjà couverts, derrière cfg(test), sans vraie source opérateur. |
| `tools/m3_2_chronology_batch_coherence_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (comparaison/présentation) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_comparison_batch_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (comparaison/présentation) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_comparison_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (comparaison/présentation) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_navigation_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (navigation/pagination) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_pagination_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (navigation/pagination) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_presentation_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (comparaison/présentation) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_projection_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (comparaison/présentation) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_readonly_handoff_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (comparaison/présentation) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_selection_review_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (comparaison/présentation) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_witness_consultation_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (témoin d'ordre) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_witness_presentation_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (témoin d'ordre) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_chronology_witness_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (témoin d'ordre) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/m3_2_direct_custody_readonly.py` | `HOLD_OPERATOR_TOOL` | Script source-only de custody/lecture physique ou manifeste ; contient des chemins/lectures de fichiers, ne pas restaurer ni exécuter sur opérateur, gate G2B–G6 et autorisation séparée exigés. |
| `tools/m3_2_independent_authority_gate.py` | `HOLD_OPERATOR_TOOL` | Script source-only de custody/lecture physique ou manifeste ; contient des chemins/lectures de fichiers, ne pas restaurer ni exécuter sur opérateur, gate G2B–G6 et autorisation séparée exigés. |
| `tools/m3_2_isolated_v7_physical_readonly.py` | `HOLD_OPERATOR_TOOL` | Script source-only de custody/lecture physique ou manifeste ; contient des chemins/lectures de fichiers, ne pas restaurer ni exécuter sur opérateur, gate G2B–G6 et autorisation séparée exigés. |
| `tools/m3_2_m31_semantic_readonly.py` | `HOLD_OPERATOR_TOOL` | Script source-only de custody/lecture physique ou manifeste ; contient des chemins/lectures de fichiers, ne pas restaurer ni exécuter sur opérateur, gate G2B–G6 et autorisation séparée exigés. |
| `tools/m3_2_multiroot_readonly.py` | `HOLD_OPERATOR_TOOL` | Script source-only de custody/lecture physique ou manifeste ; contient des chemins/lectures de fichiers, ne pas restaurer ni exécuter sur opérateur, gate G2B–G6 et autorisation séparée exigés. |
| `tools/m3_2_operator_readonly_gate.py` | `HOLD_OPERATOR_TOOL` | Script source-only de custody/lecture physique ou manifeste ; contient des chemins/lectures de fichiers, ne pas restaurer ni exécuter sur opérateur, gate G2B–G6 et autorisation séparée exigés. |
| `tools/m3_2_provenance_triage.py` | `REVIEW_CLAIM_TOOL` | Triage des revendications externes comme données non fiables ; peut alimenter #36 sur fixtures JSON, jamais attestations ni récupération d'originaux. |
| `tools/m3_2_supersession_reference.py` | `REVIEW_SYNTHETIC_REFERENCE` | Référence Python uniquement en mémoire (supersession) ; contrôler la couverture existante TS/Rust sans prétendre une équivalence ni introduire IPC/SQL. |
| `tools/test_m3_2_chronology_batch_coherence_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_comparison_batch_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_comparison_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_navigation_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_pagination_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_presentation_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_projection_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_readonly_handoff_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_selection_review_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_witness_consultation_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_witness_presentation_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_chronology_witness_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |
| `tools/test_m3_2_direct_custody_readonly.py` | `HOLD_OPERATOR_TEST` | Ancien test de lecture/audit multi-racines ou autorité externe ; pas de réexécution sur données utilisateur, requalifier seulement fixtures jetables si un trou est démontré. |
| `tools/test_m3_2_independent_authority_gate.py` | `HOLD_OPERATOR_TEST` | Ancien test de lecture/audit multi-racines ou autorité externe ; pas de réexécution sur données utilisateur, requalifier seulement fixtures jetables si un trou est démontré. |
| `tools/test_m3_2_isolated_v7_physical_readonly.py` | `HOLD_OPERATOR_TEST` | Ancien test de lecture/audit multi-racines ou autorité externe ; pas de réexécution sur données utilisateur, requalifier seulement fixtures jetables si un trou est démontré. |
| `tools/test_m3_2_m31_semantic_readonly.py` | `HOLD_OPERATOR_TEST` | Ancien test de lecture/audit multi-racines ou autorité externe ; pas de réexécution sur données utilisateur, requalifier seulement fixtures jetables si un trou est démontré. |
| `tools/test_m3_2_multiroot_readonly.py` | `HOLD_OPERATOR_TEST` | Ancien test de lecture/audit multi-racines ou autorité externe ; pas de réexécution sur données utilisateur, requalifier seulement fixtures jetables si un trou est démontré. |
| `tools/test_m3_2_operator_readonly_gate.py` | `HOLD_OPERATOR_TEST` | Ancien test de lecture/audit multi-racines ou autorité externe ; pas de réexécution sur données utilisateur, requalifier seulement fixtures jetables si un trou est démontré. |
| `tools/test_m3_2_provenance_triage.py` | `REVIEW_CLAIM_TEST` | Tests de formulaires de revendication non attestés : référence pour issue #36, aucun PASS de provenance historique. |
| `tools/test_m3_2_supersession_reference.py` | `REVIEW_SYNTHETIC_TEST` | Tests du prototype Python immuable correspondant : comparer les cas négatifs aux Rust/TS actuels, importer seulement si une lacune est prouvée et isolée. |

## Résultat de revue et non-admission

Répartition par étiquette (nombre de chemins, **pas** étapes validées) :

- `ARCHIVE_OPERATOR_GATE` : **11**
- `ARCHIVE_SYNTHETIC_DESIGN` : **15**
- `BLOCK_RUNTIME_IPC` : **1**
- `HOLD_OPERATOR_TEST` : **6**
- `HOLD_OPERATOR_TOOL` : **6**
- `KEEP_IDENTICAL` : **5**
- `REVIEW_CI_ONLY` : **1**
- `REVIEW_CLAIM_TEST` : **1**
- `REVIEW_CLAIM_TOOL` : **1**
- `REVIEW_DIVERGENCE` : **11**
- `REVIEW_SYNTHETIC_REFERENCE` : **13**
- `REVIEW_SYNTHETIC_TEST` : **13**

Les anciens documents restent disponibles sur la branche #35 pour audit ; **aucune importation massive**, suppression d'historique, modification de test, migration ou lancement Tauri. La stratégie `PRODUCT_FIRST_PARALLEL_SAFETY` reste en place, **prévenir AVANT réorientation**.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % estimés), writer/R1–R9 `NOT_PROVEN`, P4 réel STOP, garde atomique main/WAL/SHM et ABA invisible NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, glib [#160](https://github.com/LaurentCOLL1/Fabulaxiom/issues/160) `OPEN_NOT_REMEDIATED`. STOP v6/v7 opérateur, profil Greenfield existant, sauvegardes, journaux, IPC writer, migration 007, Hello et recovery. **Tests fictifs ≠ admission.**
