# Fabulaxiom — Point d'entrée pour reprendre les discussions ChatGPT

Ce dossier constitue la **mémoire de travail versionnée du projet**. Lire en priorité, dans cet ordre :

1. [HANDOFF_CURRENT.md](HANDOFF_CURRENT.md) : état opérationnel concis, dernier checkpoint vérifié et prochaine action.
2. [HANDOFF_CURRENT.json](HANDOFF_CURRENT.json) : mêmes barrières de sécurité en format vérifiable par CI, sans autorité d'exécution.
3. [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) : règles permanentes de reprise et de mise à jour.
4. [HANDOFF_HISTORY.md](HANDOFF_HISTORY.md) : étapes déjà fusionnées, pour éviter de refaire les mêmes audits.
5. [NEXT.md](NEXT.md), puis [STATE.md](STATE.md) : historique détaillé et plans antérieurs (certains en-têtes anciens ont un statut « en attente » depuis clos).
6. [M3_2_GATE_DECISION_CURRENT.md](M3_2_GATE_DECISION_CURRENT.md) : **état décisionnel courant** séparant G2-A PASS observé et G2-B à G6 non autorisés.
7. [M3_2_GATE_SNAPSHOT.md](M3_2_GATE_SNAPSHOT.md) : photographie **historique du 19 octobre**, pas l'état G2-A actuel.
8. [bloc historique PR #86](../qualification/M3_2_G2A_EXACT_BLOCK_REVIEW.md) : **déjà exécuté sur Windows une fois, résultat STOP_WEBVIEW2_PARENTAGE** ; ne pas relancer.
9. [nouveau candidat G2-A PID 0](../qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md) : **exécuté une seule fois après accord explicite le 20 octobre 2026 : PASS de métadonnées locales seulement** ; toute réexécution nécessite un nouvel accord.

10. [Analyse source-only de l'absence d'écrivain SQLite](../qualification/M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md) : aucun moyen d'accès aux originales et aucun déblocage G2-B/G3.

11. [Audit source-only des points d'entrée SQLite Rust](../qualification/M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md) : six fonctions connues et 18 tests de dérive, G3 réel toujours STOP.

12. [Inventaire élargi des sites SQLite Rust](../qualification/M3_2_WIDE_RUST_SQLITE_SITE_INVENTORY.md) : 25 modules Rust/Tauri, surveillance textuelle et 18 tests de refus, sans inspection des bases.

13. [Prototype Rust de lecteur préouvert en RAM fictive](../qualification/M3_2_PREOPENED_QUERY_ONLY_RAM_READER_TOY.md) : 13 tests Rust sous feature non défaut et cfg(test), G3 réel toujours STOP.

14. [Deux connexions RAM fictives et preuve négative d'absence d'écrivain](../qualification/M3_2_SHARED_RAM_EXTERNAL_WRITER_NEGATIVE_PROOF.md) : 12 tests CI sur SQLite en mémoire, G3 toujours STOP.

Pour une nouvelle conversation, copier seulement le [prompt court](RESUME_PROMPT.md). Le dépôt GitHub réel prévaut sur tout texte ou souvenir du modèle. Les SHA inscrits ici sont des **repères historiques**, jamais la preuve que GitHub n'a pas changé entre-temps.

Les PR qui modifient le code ou les procédures de M3.2 doivent aussi mettre à jour `HANDOFF_CURRENT.md` et `HANDOFF_CURRENT.json` ; un garde-fou CI refusera leur omission. Ce garde-fou ne met pas les fichiers à jour automatiquement : **le développeur doit inscrire une preuve juste, datée et vérifiable**. Seule une fusion réussie les rendra disponibles dans `main`.
