# M3.2 — Atelier manuel d'événements fictifs, sans persistance

**Qualification strictement source-only.** Cette tranche fait évoluer le carnet fictif introduit dans la PR #145 vers une interface React **interactive**, mais volontairement NON montée dans `App.tsx`. L'utilisateur fictif peut saisir un titre, une note, sélectionner expressément une ancre et une révision historique, puis créer, corriger (nouvelle version avec justification) ou retirer (pierre tombale, conservation d'historique) un événement. Les champs et la liste ne vivent que dans `useState` ; aucune API disque, réseau, stockage navigateur, commande Tauri, sauvegarde ou connexion SQLite n'est ajoutée.

Le contrôleur pur `applyFictionalWorkshopAction` délègue uniquement à `createFictionalEvent`, `amendFictionalEvent` et `withdrawFictionalEvent`. Le modèle vérifie explicitement les identifiants et refuse les liaisons historiques devinées ou étrangères à l'Univers. Les 18 tests Vitest inventés vérifient les transactions métier, l'immuabilité, le retrait, les références, la séparation des univers, et le rendu SSR des champs ; ils **ne constituent pas des interactions Chromium réelles de ce composant**, car celui-ci n'est pas monté dans l'application.

**Checkpoint daté :** PR #145 source `8151f1720c0e657fe66a191c21dafc084449486a`, CI #39945373971 SUCCESS, fusion protégée `main=26987ffaf6ec7c1a02bca8c288243a3da2092469`, CI post-main #39946911406 SUCCESS vérifiée séparément (76 étapes Windows, 80 tests de continuité, 15 tests CRUD fictifs, 132 Rust, Chromium 53/53 par mode). CI #39945062578 a échoué sur l'ancien SHA et ne qualifie pas le commit source final.

Cette nouvelle tranche reste **CANDIDATE**, nécessite CI Windows terminale sur son propre SHA, re-fetch Protect main/threads/reviews et fusion `expected_head_sha`. Aucun passage à l'acceptation Windows M3.2.

**Gates :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B global `NOT_ACCEPTED` ; source `PARTIAL_LOCAL_IDENTITY_ONLY` ; absence d'écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; réel G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT.
