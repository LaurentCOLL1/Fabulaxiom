# Fabulaxiom M3.2 — Reprise opérationnelle courte

**Checkpoint documentaire au 19 octobre 2026, à revérifier sur GitHub avant toute action.**

## Dernier état effectivement vérifié

- Dépôt : https://github.com/LaurentCOLL1/Fabulaxiom
- `main` observé : `6d9650ee09d6f8a695a9b71a9ef1e1118f7229c9` (merge [PR #86](https://github.com/LaurentCOLL1/Fabulaxiom/pull/86)).
- PR #86 : correction du filtre G2-A `SearchHost.exe` / `msedgewebview2.exe` **déjà fusionnée** ; CI Windows PR #39241294071 terminale SUCCESS, contrôle obligatoire réussi. La CI `main` après fusion a également réussi (#39242342744).
- PR #35 : **OPEN / DRAFT**. Issues [#36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) et [#38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38) : **OPEN**. Ruleset Protect main #24895490 actif, sans bypass (au checkpoint).
- Application : Windows, React + Tauri v2 + Rust + SQLite. Production SQLite v6 protégée, v7 isolée ; **aucune ouverture/migration des fichiers opérateur**. Pas de migration 007.
- Historique de provenance : `PENDING_EXTERNAL_ATTESTATION(21/3/2)` (21 ancrés, 3 empreintes observées seulement, 2 non ancrés). Politique compensatoire opérateur unique documentaire, baseline prospective `NOT_STARTED`.

## Incident G2-A et correctif

Le bloc G2-A de PR #85 a été exécuté manuellement après autorisation et a retourné **`G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: PROCESS_NAMES`**. Une capture de Process Explorer montrait six processus WebView2 sous `SearchHost.exe`, compatible avec la recherche Windows. **Ce n'est pas une preuve d'absence de processus écrivain SQLite**.

La PR #86 a préparé [le nouveau bloc exact](../qualification/M3_2_G2A_EXACT_BLOCK_REVIEW.md) **en Markdown uniquement**, qui examine `Win32_Process` (PID, PID parent, date de création, nom), compare les inventaires et refuse parent absent, cycle, chronologie incohérente, Fabulaxiom/Ollama actif ou WebView2 d'origine incertaine. Une parenté SearchHost cohérente peut être observée sans stopper les processus. La vérification PowerShell AST en CI est **syntaxique uniquement**, et les parentés sont testées sur fixtures fictives.

**L'accord donné oralement par l'opérateur pour poursuivre G2-A ne démontre pas la relecture des octets de la version modifiée #86.** Ne pas l'exécuter sur Windows avant de montrer le nouveau bloc exact, d'expliquer l'usage de WMI/CIM et d'obtenir son approbation explicite sur cette version. Aucune commande PowerShell n'est exécutée automatiquement depuis ChatGPT.

## STOP à préserver

- `G2A_REVISED_RUNTIME=NOT_ASSESSED` ; le STOP précédent est conservé jusqu'à un nouveau résultat opérateur.
- `G2-B/G2-C/G2-D/G3/G4/G5/G6=NOT_AUTHORIZED`, `REAL_G3_STOP_UNAVAILABLE`.
- `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`.
- Interdits : originales SQLite (v6 prod/v7 isolée), sidecars, ACL, sauvegardes, marker d'activation, migration 007, IPC writer, fusion PR #35, M3.3, release. Aucun reset Git destructeur ni faux relecteur indépendant.

## Prochaine action concrète

1. Re-fetch **live** `main`, PR/heads, CI et ruleset GitHub, puis lire les fichiers de ce dossier.
2. Montrer la version **exacte** du bloc G2-A corrigé (PR #86) et ses interactions éventuelles (touche Entrée, aucun `q`, pas d'UAC, pas d'arrêt ; lecture WMI/CIM) pour revue.
3. Obtenir un accord distinct sur ses octets et limiter toute exécution à G2-A ; demander seulement la sortie `PASS/STOP` non personnelle.
4. Après chaque changement significatif/PR : mettre à jour **HANDOFF_CURRENT.md + HANDOFF_CURRENT.json**, puis éventuellement `HANDOFF_HISTORY.md`, `STATE.md` et `NEXT.md` avant CI et fusion.

Se reporter à [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) pour les invariants détaillés, sans réutiliser les anciennes CI après un nouveau commit.
