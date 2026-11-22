# M32-007 / M32-050 — deux modules Rust historiques absents de la PR #35 (22/11/2026)

**Portée : source-only, aucune exécution des modules anciens.** GitHub historique PR #35 DRAFT HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5`, base de contrôle `e9b40532b3f2f902ac259ba1cf9a97bee715ab35` (#413 MERGED). Les audits complets de 84 chemins trouvent 68 absents (dont exactement deux modules Rust) ; 11 divergents et cinq identiques. PR #215 DRAFT a encore quatre REVIEW_NON_ACCEPTED. Les deux modules absents sont **NOT_PORTED** et aucune décision de portage n'est autorisée par cette comparaison.

## Module historique 1 — BLOCK_RUNTIME_IPC

`src-tauri/src/m32_isolated_preflight.rs` comporte un `#[tauri::command]` : `m32_isolated_preflight_status` renvoie des métadonnées et utilise l'identifiant `com.fabulaxiom.m32gate` et un mot d'accord. Ce code n'est ni présent ni enregistré sur la branche main moderne. Même metadata-only, son enregistrement IPC serait un changement d'autorité et exige une revue et une autorisation distinctes. **BLOCK_RUNTIME_IPC, NOT_PORTED**. La revue ne vaut pas accord opérateur.

## Module historique 2 — REVIEW_CI_ONLY

`src-tauri/src/m32_sqlite_concurrency_tests.rs` contient trois tests de SQLite à deux connexions avec fichier scratch fraîchement créé via `OpenOptions::create_new`, choix explicite WAL, transactions et suppression en sortie de scratch DB, `-wal`, `-shm` et `-journal`. Ils ne ciblent aucune base opérateur mais ne représentent pas un contrôle sur main/WAL/SHM vivants ni une garantie ABA. Ces tests ne sont pas intégrés au `src-tauri/src/lib.rs` moderne, donc **REVIEW_CI_ONLY, NOT_PORTED** :

1. `two_connections_hide_uncommitted_chain_and_serialize_writers` — lecture non validée et writers en concurrence
2. `rollback_of_withdrawal_and_replacement_is_atomic_across_connections` — annulation et retrait/remplacement entre connexions
3. `two_connection_readonly_and_cycle_guards_reject_cross_handle_bypass` — refus en lecture seule, cycles et validations croisées

Les onze noms d'API Rust cités dans le module historique sont encore déclarés dans le fichier actuel `src-tauri/src/m32_manual_chronology.rs` : `create_anchor`, `create_precedence`, `decide_precedence`, `restate_revoked_precedence`, `revoke_restatement`, `succeed_withdrawn_restatement`, `revoke_successor`, `list_active_precedence_graph`, `append_chain_correction`, `revoke_chain_correction`, `create_calendar`. Leur présence textuelle **ne démontre ni équivalence de comportement ni sécurité SQLite réelle**. Dans `src-tauri/src/lib.rs`, `m32_manual_chronology` demeure `#[cfg(test)]`.

## Contrôle de non-régression

`tools/test_m32_legacy_pr_reconciliation.py` ajoute les tests source-only #22/#23/#24 : vérifie les trois anciens cas et onze symboles textuels ; refuse les anciennes inscriptions de modules ou commande IPC ; refuse la promotion de `#[cfg(test)]`, la disparition d'API, une déclaration d'admission dans ce rapport et une clôture prématurée M32-007. Ces tests ne téléchargent ni n'exécutent du vieux code et ne créent aucun SQLite. Statut des trois cas et de leur sémantique : **NON QUALIFIÉ avant CI sur HEAD exact**.

**Décision partielle :** aucune fusion/cherry-pick de l'ancienne PR, aucun ajout IPC, aucune exécution de SQLite réel ou récupération WAL/SHM. L'évaluation de réimplémentations sûres en tests jetables demeure distincte et requiert des preuves spécifiques. **M32-007 [ ] et M32-050 [ ] OPEN_NOT_ACCEPTED**, tout comme M3.2 **IN_PROGRESS_NOT_ACCEPTED**, PRODUCT_FIRST_PARALLEL_SAFETY.

Gates : Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5, D3b-5 STOP ; main/WAL/SHM, live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED. STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
