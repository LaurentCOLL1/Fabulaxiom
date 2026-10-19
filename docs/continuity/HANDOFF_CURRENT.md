# Fabulaxiom M3.2 — Reprise opérationnelle courte

**Checkpoint documentaire revérifié le 19 octobre 2026 depuis GitHub, instantané non exécutable ; nouveau re-fetch requis avant toute écriture ou fusion ultérieure.**

## Vérification de reprise du 19 octobre 2026

Lecture GitHub (sans exécution sur le PC opérateur) : `main`, PR #86/#87/#35, issues #36/#38, runs/actions et ruleset #24895490 `Protect main` revérifiés. Ruleset actif, check `Windows frontend and Rust checks` de l'app 15368 exigé, branche `main` sous PR, interdiction de suppression et de non-fast-forward, `bypass_actors=[]`. La lecture REST historique de protection de branche renvoie 403 pour cette intégration ; cela **n'annule pas** le ruleset lu directement. Pas de nouveau résultat G2-A local : `REVISED_NOT_ASSESSED`. Le candidat exact reste dans `docs/qualification/M3_2_G2A_EXACT_BLOCK_REVIEW.md` et requiert revue et consentement explicite neuf avant collage/exécution. Les métadonnées de processus ne prouvent jamais l'absence d'un écrivain SQLite. Cette mise à jour documentaire n'ouvre aucun gate.

## Dernier état effectivement vérifié

- Dépôt : https://github.com/LaurentCOLL1/Fabulaxiom
- `main` observé : `0aa0dc6b097a386e8a192717b7115a41019bbd88` (merge [PR #87](https://github.com/LaurentCOLL1/Fabulaxiom/pull/87), après PR #86).
- PR #86 : correction du filtre G2-A `SearchHost.exe` / `msedgewebview2.exe` **fusionnée** ; CI Windows PR #39241294071 terminale SUCCESS et CI `main` #39242342744 SUCCESS.
- PR #87 : continuité versionnée et garde-fou de fraîcheur **fusionnés** ; CI Windows PR #39271702661 au HEAD `287c178063a4d2719742bac96d3bc57a8fa515bc` SUCCESS (62 étapes, contrôle same-PR PASS) ; CI `main` #39273165266 au SHA ci-dessus SUCCESS (62 étapes dont contrôle PR-only SKIPPED, attendu).
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
