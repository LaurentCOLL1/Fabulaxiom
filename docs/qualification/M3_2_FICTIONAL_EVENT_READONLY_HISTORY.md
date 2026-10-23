# M3.2 — Historique de versions d'événements en lecture seule (univers inventés)

**23 octobre 2026 — candidate source-only en mémoire fictive ; non montée dans l'application Windows.**

## Objectif
Une création, une correction ou un retrait manuel fictifs doivent rester consultables dans l'ordre **explicite de leurs versions**. Ne jamais déduire l'ordre temporel dans le monde du récit, ni effacer les motifs humains d'une correction. L'inspecteur expose l'audit apparié à chaque version ; le rendu `<details>` est replié par défaut et conserve les entrées retirées, tout en laissant inchangée la liste des seuls événements courants.

## Périmètre
- `auditedFictionalEventHistory(book, eventId)` inspecte d'abord toute la structure fictive, refuse un ID inconnu/étranger/non-chaîne, puis retourne **des copies détachées et gelées** de chaque version et de son entrée d'audit (pas de pointeur partagé vers les enregistrements du carnet).
- `M32FictionalEventNotebookPreview` affiche une section d'historique `aria-label`, les justifications, notes, ancres explicitement liées et IDs de révision source, avec échappement HTML React. Les événements retirés restent consultables. Aucun lecteur, calendrier ou temps de monde n'est inféré.
- Tests Vitest #42–49 : séquences créer/corriger/retirer, événements intercalés, refus IDs absents/étrangers/non typés, veto sur audit falsifié, immutabilité des copies affichées, rendu HTML sécurisé et maintien de l'absence de sauvegarde.
- **Aucune connexion à `App.tsx`, aucun appel Tauri IPC, SQLite, disque ou réseau, aucun changement de migration ou d'autorisations.** Le module reste sur les fixtures inventées du laboratoire source CI. `Object.freeze` n'authentifie pas les données historiques originales.

## Checkpoint GitHub antérieur terminal, vérifié indépendamment
[PR #150](https://github.com/LaurentCOLL1/Fabulaxiom/pull/150) source `b39506bce112b828477d9c4b1d1f14076dc3fb38` qualifiée par [CI #40006337923](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40006337923) terminal SUCCESS ; fusion protégée `main=20658fdc87fd8deca712611f74f4e9cdf1389807`, [CI postmain #40007837202](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40007837202) terminal SUCCESS. 76 étapes Windows, 85 contrats, 41 tests du carnet, 62/62 Chromium normal et CSP strict chacun, 132 tests Rust principaux. Les deux CI sont distinctes et vérifiées par SHA.

## Qualification exigée de cette candidate
86 contrats handoff, 49 tests d'événements, Chromium isolé 62/62 dans chacun des deux modes, Rust sans régression ; aucune CI antérieure réutilisable. Re-fetch du SHA GitHub, diff/reviews/threads, ruleset Protect main, fusion protégée avec `expected_head_sha`, puis CI postmain indépendante et issue #38 actualisée.

**STOP réel inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B `NOT_ACCEPTED`; identité `PARTIAL_LOCAL_IDENTITY_ONLY`; absence d'écrivain `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; G3 réel `STOP_UNAVAILABLE`; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 OPEN/DRAFT. Ne toucher ni bases SQLite originales v6/v7 ni backups, ACL, sidecars, marqueurs, migration 007, IPC writer, M3.3, ComfyUI, release ou PC opérateur.
