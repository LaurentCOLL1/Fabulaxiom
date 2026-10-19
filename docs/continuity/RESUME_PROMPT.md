# Prompt minimal de reprise — Fabulaxiom

Reprends le développement de **Fabulaxiom M3.2** depuis l'état réel du dépôt : https://github.com/LaurentCOLL1/Fabulaxiom

Lis d'abord `docs/continuity/README.md`, `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md` et `HANDOFF_HISTORY.md` dans ce dossier ; consulte ensuite `NEXT.md`, `STATE.md` et les issues/PR pertinentes.

**Re-fetch GitHub** (main, branches, PRs, CI, ruleset) avant toute action. Les checkpoints enregistrés sont datés. Poursuis la prochaine tâche autorisée, avec tests, CI au SHA exact et fusion protégée si ses critères sont atteints.

Le bloc G2-A corrigé après le STOP WebView2/SearchHost (PR #86) n'a pas encore été exécuté sur mon PC. J'ai exprimé mon accord pour poursuivre l'observation G2-A, mais montre le **code exact de la version corrigée**, ses effets et interactions, et obtiens mon accord explicite sur cette version avant exécution. Préviens-moi avant une touche `q`, un UAC, toute ouverture interactive ou action sur disque.

**Ne touche jamais** à la production SQLite v6, à la v7 isolée, aux sauvegardes/ACL/markers, ni aux opérations G3–G6, migration 007, IPC writer ou release sans autorisation distincte. Ne réutilise pas de CI d'un ancien HEAD.

**À chaque PR importante, actualise** `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json` et si nécessaire `HANDOFF_HISTORY.md`, `NEXT.md`, `STATE.md`. Lorsque la conversation devient longue, donne-moi seulement un prompt de reprise court pointant vers ces fichiers et l'état actuel.
