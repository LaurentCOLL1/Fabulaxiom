# M3.2 — CRUD manuel d'événements inventés, sans SQLite ni Tauri

**23 octobre 2026 — tranche purement fictive et indépendante du produit.**

La roadmap M3.2 prévoit le CRUD manuel des événements **et** des ancres, des références à des révisions de scènes historiques, un mode hors ligne et des contrôles déterministes. Cette tranche ajoute un carnet d'événements *uniquement en mémoire navigateur* (`m32FictionalEventNotebook.ts`) qui peut créer, corriger et retirer un événement. Chaque correction est **une nouvelle version**, jamais une réécriture de la version antérieure ; chaque retrait crée une pierre tombale et garde l'audit. Les titres homonymes ne sont jamais des clés, les identifiants sont propres à chaque Univers et aucune liaison de révision n'est devinée.

Un aperçu React séparé `M32FictionalEventNotebookPreview.tsx` est **lecture seule**, non monté par `App.tsx`. Les 15 tests inventés `m32FictionalEventNotebook.test.tsx` couvrent création sans date inventée, lien à une révision historique immuable, correction/révocation, entrées étrangères, histoires malformées, titres homonymes et séparation entre Univers.

**Ce qui n'est PAS fait :** pas de véritable CRUD Windows sur la base active v6 ni la copie isolée v7, pas de migration 007, pas d'accès aux données de l'opérateur, pas d'IPC de modification, pas de sauvegarde et pas d'acceptation réelle M3.2. Les événements fictifs ne sont pas un canon narratif durable ; la source M2 n'est jamais écrite.

**Checkpoint GitHub vérifié :** PR #144 source `48b1e873292b4f65de90fbe128f76f0b5759d4db`, CI source #39940937603 SUCCESS ; fusion protégée `main=c969f2c29e168e99e24d675c25a3217e789c9e2d`, CI postmain #39942208143 SUCCESS (76 étapes Windows, 79 handoffs, 14 tests deux Univers, 132 Rust, Chromium 53/53 dans chaque mode). L'ancienne source #144 comporte deux CI échouées sur d'anciens SHA, conservées comme historique. La présente candidate requiert sa **propre CI finale sur le nouveau SHA** avant éventuelle fusion.

**Gates inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; source `PARTIAL_LOCAL_IDENTITY_ONLY` ; absence de writer `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT.
