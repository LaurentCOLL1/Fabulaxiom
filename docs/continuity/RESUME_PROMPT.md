# Prompt minimal de reprise — Fabulaxiom

Reprends le développement de **Fabulaxiom M3.2** et assure le suivi de la [roadmap V1](https://github.com/LaurentCOLL1/Fabulaxiom/tree/main/docs/roadmap) depuis l'état réel du dépôt : https://github.com/LaurentCOLL1/Fabulaxiom

Lis d'abord `docs/continuity/README.md`, `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md` et `HANDOFF_HISTORY.md` dans ce dossier ; consulte ensuite `NEXT.md`, `STATE.md` et les issues/PR pertinentes.

**Re-fetch GitHub** (main, branches, PRs, CI, ruleset) avant toute action. Les checkpoints enregistrés sont datés. Poursuis la prochaine tâche autorisée, avec tests, CI au SHA exact et fusion protégée si ses critères sont atteints.

**État daté du 20 octobre 2026 :** G2-A PID 0 (PR #89) a été exécuté manuellement une seule fois avec mon autorisation explicite. Sortie : `G2A_LOCAL_METADATA: PASS`, `WEBVIEW2_SEARCHHOST_LINEAGE: 6 OBSERVED_METADATA_ONLY`, `WEBVIEW2_OWNERSHIP_AUTHENTICATED: NO`, `PROCESS_WRITER_ABSENCE: NOT_PROVEN`. Ne pas relancer ce bloc : l'accord unique est consommé. Les STOP des PR #85/#86 sont historiques. État courant roadmap : `docs/roadmap/README.md`, `docs/roadmap/ROADMAP_STATUS_CURRENT.md` ; M3.2 non acceptée malgré les fixtures de G2/G3. État courant G2–G6 : `docs/continuity/M3_2_GATE_DECISION_CURRENT.md` (ne remplace pas le snapshot historique du 19 octobre). Analyses source-only : `docs/qualification/M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md` et `docs/qualification/M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md`, ainsi que `docs/qualification/M3_2_WIDE_RUST_SQLITE_SITE_INVENTORY.md` et le prototype RAM inventée `docs/qualification/M3_2_PREOPENED_QUERY_ONLY_RAM_READER_TOY.md` et `docs/qualification/M3_2_SHARED_RAM_EXTERNAL_WRITER_NEGATIVE_PROOF.md` ; aucun audit runtime autorisé. Les autres G2-B/C/D, G3-G6 restent non autorisés. Avant toute autre commande locale, montre-moi le **code exact**, tous les effets/interactions (Entrée/`q`/UAC/disque/réseau), et recueille mon nouvel accord explicite.

**Ne touche jamais** à la production SQLite v6, à la v7 isolée, aux sauvegardes/ACL/markers, ni aux opérations G3–G6, migration 007, IPC writer ou release sans autorisation distincte. Ne réutilise pas de CI d'un ancien HEAD.

**À chaque PR importante, actualise** `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json` et si nécessaire `HANDOFF_HISTORY.md`, `NEXT.md`, `STATE.md`. Lorsque la conversation devient longue, donne-moi seulement un prompt de reprise court pointant vers ces fichiers et l'état actuel.
