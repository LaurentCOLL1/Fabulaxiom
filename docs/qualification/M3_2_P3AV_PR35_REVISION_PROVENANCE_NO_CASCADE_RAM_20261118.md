# P3av — Réconciliation ciblée de deux témoins Rust historiques #35 (18 novembre 2026)

## Provenance et justification
La PR historique [#35](https://github.com/LaurentCOLL1/Fabulaxiom/pull/35), HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5`, portait des scénarios `correction_revision_must_belong_to_original_universe` et `precedence_decisions_preserve_retracted_edges_without_cascade`. Le service actuel avait des tests proches mais n'unifiait pas ces deux propriétés, pour une origine historique de même Universe et pour deux liens actifs indépendants. Aucun cherry-pick ni merge de #35 : seuls deux nouveaux témoins dans les tests Rust actuels.

## Deux tests candidats sous `#[cfg(test)]`
1. `p3av_foreign_revision_cannot_authorize_local_anchor_or_edge_revocation` : deux Universes et deux révisions de scène fictives ; refus sans effet d'une provenance étrangère pour la révocation d'ancre et de précédence ; acceptation uniquement de la révision locale, ancienne relation maintenue dans l'historique.
2. `p3av_revoking_one_edge_never_cascades_to_independent_human_relation` : relations A→B et B→C ; seule A→B est révoquée, B→C reste active et intacte ; refuser double retrait, retrait inter-Universe, DELETE des tables immuables et insertion legacy B→A ; schéma runtime v6 inchangé.

Ces deux tests utilisent **exclusivement SQLite `:memory:` et des noms fictifs**. Le code hors module de tests reste identique. Ceci **n'est pas** la preuve de persistance ni l'admission du writer réel. Ne jamais assimiler à un test main/WAL/SHM ou à une récupération.

## Contrôles avant fusion
Parent protected `main=7e29f3900187ad58d2a129308a962a2a46742f17` après #389 MERGED ; source Windows CI #44335035324 completed/SUCCESS HEAD exact `c4591d51f4b8a5fbd3a01be2962f8d9abace99db` (333 Rust, Chromium 107/107, CSP 98/98) ; postmain indépendante #44338089528 **completed/SUCCESS au SHA exact du parent** ; Protect main ACTIVE strict bypass=[]. CI source P3av propre, diff/reviews/threads, guarded squash `expected_head_sha`, postmain indépendante et issue #38 append-only restent obligatoires. Anciennes #35 et #215 OPEN/DRAFT : M32-007/M32-050/M32-081 non clôturés. Checklist 104=9 closes/95 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif), PRODUCT_FIRST_PARALLEL_SAFETY.

## Interdictions
Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5 et D3b-5 STOP ; main/WAL/SHM, live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
