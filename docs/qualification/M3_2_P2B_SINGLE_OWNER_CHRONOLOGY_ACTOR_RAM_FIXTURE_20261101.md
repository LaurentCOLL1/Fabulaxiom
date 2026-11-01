# M3.2 P2b — acteur Rust de chronologie sur fixture v7 RAM

**1er novembre 2026 — CANDIDAT NON QUALIFIÉ avant CI Windows HEAD exact.** Parent protégé : PR #259 P2a fusionnée, main \`8ecf0a9174d00d2f3581e635526ad3941e52117e\`, CI source #41342616672 SUCCESS 297/7/68/180 ; CI postmain #41343742102 completed/SUCCESS indépendante au SHA exact (297/7/68/180). Stratégie propriétaire \`PRODUCT_FIRST_PARALLEL_SAFETY\` maintenue.

## Livrable produit

\`src-tauri/src/m32_p2b_fixture_chronology_actor.rs\` est **compilé seulement sous #[cfg(test)]** dans \`lib.rs\`. Le module s'inspire du modèle *single owner* déjà préparé dans \`m32_v7_writer_service.rs\`, sans en modifier \`PreparedV7Writer\`, ses règles de v6, son admission scellée ou son runtime. Il reçoit exactement une connexion SQLite v7 fictive déjà ouverte et exclusivement détenue par le test, valide le contrat P2a avant de la déplacer dans un worker Rust. Aucun appel d'ouverture SQLite, migration production, accès au profil, Tauri State/IPC, URL, cloud, modèle ou écriture opérateur.

Les types \`AnchorInput\`/\`RelationInput\` possèdent leurs valeurs et sont transportés sur une file MPSC bornée de capacité 8 vers un thread unique. Les commandes typed incluent calendrier, création d'ancre avec relation atomique optionnelle, précédent humain explicite et snapshot par Univers. Le résultat est synchrone pour l'appelant, sans faux succès ; les erreurs SQLite/contrat remontent. \`shutdown\` et \`Drop\` ferment le worker et invalident les clients clonés. Le service P2a conserve les transactions \`IMMEDIATE\`, rollback et séparation des Univers.

**Quatre tests Rust RAM inventée, aucune nouvelle ouverture SQLite** : deux clients concurrents → une connexion/ordre de traitement sans ordre temporel global induit ; rollback de l'ancre si relation invalide et cycle refusé ; refus v6/\`query_only\` ; \`shutdown\`/\`Drop\` déconnectent les clients. Les 297 tests Rust P2a restent en référence et P1 conserve seul le témoin de persistance fichier v7 NEW_ONLY.

## Ce qui n'est pas prouvé

Ne prouve NI l'admission d'une source réelle, NI l'identité atomique main/-wal/-shm, NI l'absence d'autres writers, NI l'interface opérateur. Ne raccorde PAS l'acteur au véritable \`PreparedV7Writer\` ni ne crée de jeton d'admission. P3 doit fournir une UI React fictive isolée avec un contrat de commande et une bannière de non-persistance, sans \`App.tsx\` ni IPC writer de production. R4–R9 se poursuivent en parallèle ; alerter l'utilisateur avant toute modification de stratégie.

## Qualification / sécurité

**301 Rust / 7 Greenfield / 68 inventaire SQLite / 181 continuité ATTENDUS NON ACQUIS** avant CI. Contrôler CI source exacte, revue diff/threads, ruleset \`Protect main\` strict bypass=[], squash \`expected_head_sha\`, CI post-fusion indépendante et suivi #38/#160 append-only. GLIB 0.18.5 (Linux GTK3, Dependabot #1) \`OPEN_NOT_REMEDIATED\`, aucune correction simulée ni dismissal.

**STOP inchangés :** M3.2 IN_PROGRESS_NOT_ACCEPTED, writer/R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucune base opérateur v6/v7, profil Greenfield existant, journaux, backups, migration 007 runtime, Windows Hello natif, marqueur/recovery, nouveau profil ni ouverture de chemins sous M:\Fabulaxiom.
