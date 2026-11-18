# P3au — Reconciliation ciblée du témoin historique PR #35 : inversion A/B après révocation (18 novembre 2026)

## Analyse de couverture
Ancienne PR #35 (DRAFT, HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5`), `src-tauri/src/m32_manual_chronology.rs`, test `reversed_edge_after_revocation_is_current_without_erasing_history`. Le service actuel possède des tests de révocation/restatement, mais pas le témoin positif équivalent **A avant B retiré → B avant A restaté** avec rejet du chemin d'insertion historique, projection courante inversée, invariants de non-mutation, isolation de l'autre Universe et version 6 dans la même preuve.

## Portage minimal
Un seul test Rust `p3au_explicit_reverse_restatement_keeps_legacy_history_in_ram`, ajouté à l'implémentation actuelle **déjà `#[cfg(test)]`**. Aucune fonction de production ajoutée, aucune table changée, aucun cherry-pick/fusion des 84 fichiers de #35. Fixture `:memory:` construite dans le test, v7 candidate en RAM et schéma officiel v6 inchangé. Le témoin refuse UPDATE/DELETE, réécriture secondaire et insertion legacy après retrait ; la relation originelle reste consultable, seul l'edge nouveau explicitement justifié figure au graphe actif. Le second Universe reste isolé.

## Preuves et décisions
Protected parent `main=e98673bdc1731f834e419128841270648890c235` après #388 MERGED (CI source #44239075023 SUCCESS au HEAD exact `9c10c10e077dfc17f1f41d65ea634f627e4d1645`, postmain indépendante #44287862525 completed/SUCCESS au SHA exact parent) ; Protect main ACTIVE, strict, bypass=[]. Ce nouveau test est **CANDIDAT, NON QUALIFIÉ** jusqu'à sa propre CI Windows source exacte. Périmètre M32-007/M32-050/M32-081 **PARTIEL [ ]**, jamais clos par un témoin RAM. #35 et #215 restent OPEN/DRAFT ; arbre #35=5 identiques/11 divergents/68 absents ; #215=6 identiques/17 divergents. Prochaine étape : CI exacte, review diff/threads, guarded squash expected_head_sha, postmain indépendante, #38 append-only. Checklist 104=9 closes/95 ouvertes, gate IN_PROGRESS_NOT_ACCEPTED (~45% indicatif).

## STOP inchangés
PRODUCT_FIRST_PARALLEL_SAFETY ; writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5 et D3b-5 STOP ; main/WAL/SHM, live WAL-index, ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
