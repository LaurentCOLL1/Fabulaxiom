# Fabulaxiom M3.2 — deux Univers fictifs, deux romans et isolation des chronologies

**23 octobre 2026 — TEST-ONLY et READ-ONLY ; non utilisable avec les bases privées.**

## Traçabilité roadmap

L'acceptation M3.2 de `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md` impose deux Univers, plusieurs Romans, des temps exacts/approximatifs/relatifs/inconnus, des contradictions, cycles, références exactes aux révisions historiques et des validations Windows réelles. Ce travail apporte uniquement une **qualification préalable en mémoire inventée** :

- `src/M32TwoUniverseSafetyPreview.tsx` affiche côte à côte des informations de deux brouillons inventés, sans autoriser une chronologie commune ni écrire dans l'application ;
- `src/m32TwoUniverseIsolation.test.tsx` ajoute 14 scénarios : deux Univers et deux romans par Univers, homonymes sans identité croisée, dates distinctes, refus de sources et révisions étrangères, cycles, supersession, révocation, preuve humaine par révision exacte et impossibilité d'inférer un ordre inter-Univers ;
- `src/App.tsx`, les commandes Tauri, les migrations et les SQLite originales restent **strictement inchangées**.

## Résultats et barrières

Dernier `main` authentifié au début de la tranche : `cf90661173e9e6ed8d29caa181557b04e2d6fb63`, PR #143 fusionnée (source `61ae15427863ccaae7f2cd8a5b8ea6ff04c83f4c`, CI source #39935643729 SUCCESS, CI postmain #39936839961 SUCCESS, vérifications Windows 76 étapes/78 handoff/12 guards/132 Rust/Chromium 53/53 par mode). Les tests de cette nouvelle tranche sont **candidats jusqu'à CI terminale sur leur propre SHA, diff/reviews/threads/ruleset et fusion protégée**. L'ancien main ne vaut pas acceptation Windows de M3.2.

État M3.2 : `IN_PROGRESS_NOT_ACCEPTED`; G2B réel `NOT_ACCEPTED`; source `PARTIAL_LOCAL_IDENTITY_ONLY` ; absence d'écrivain `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; G3 réel `STOP_UNAVAILABLE`; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 `OPEN/DRAFT`. Aucune migration 007, sauvegarde, ACL, marqueur, sidecar, IPC d'écriture, release, M3.3 ou action Windows opérateur autorisée.
