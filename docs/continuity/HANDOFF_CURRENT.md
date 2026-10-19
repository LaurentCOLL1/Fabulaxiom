# Fabulaxiom M3.2 — Reprise opérationnelle courte

**Checkpoint documentaire mis à jour après observation opérateur du 19 octobre 2026. Re-fetch GitHub avant toute nouvelle écriture, CI ou fusion. Ce texte n'autorise aucune commande locale.**

## Vérification de reprise du 19 octobre 2026

Lecture GitHub (sans exécution sur le PC opérateur) : `main`, PR #86/#87/#35, issues #36/#38, runs/actions et ruleset #24895490 `Protect main` revérifiés. Ruleset actif, check `Windows frontend and Rust checks` de l'app 15368 exigé, branche `main` sous PR, interdiction de suppression et de non-fast-forward, `bypass_actors=[]`. La lecture REST historique de protection de branche renvoie 403 pour cette intégration ; cela **n'annule pas** le ruleset lu directement. Un résultat opérateur nouveau existe : `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: WEBVIEW2_PARENTAGE`, `STOP_REASON: UNEXPECTED_OR_UNSAFE` sur le candidat exact PR #86. Le consentement spécifique à cet unique essai est consommé ; toute autre commande exige une nouvelle revue et un nouvel accord. Le sous-motif précis est inconnu. Les métadonnées de processus ne prouvent jamais l'absence d'un écrivain SQLite. Cette mise à jour documentaire n'ouvre aucun gate.

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

**Résultat opérateur du 19 octobre 2026 après revue du bloc exact et autorisation distincte :** `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: WEBVIEW2_PARENTAGE`, `STOP_REASON: UNEXPECTED_OR_UNSAFE`, `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, `TAURI_RUNTIME: NOT_TESTED`. Ce compte-rendu est fourni par l'opérateur, pas un audit indépendant. L'ancien STOP `PROCESS_NAMES` reste dans l'historique. Le script masque volontairement le motif interne : parent absent, changement d'instantané, chronologie invalide ou échec CIM ne sont pas individuellement prouvés. **Ne pas relancer ce script ni un nouveau diagnostic sans revue et autorisation distinctes.** Aucune commande PowerShell exécutée automatiquement depuis ChatGPT.

**Hypothèse de défaut source identifié sans essai sur Windows :** le bloc PR #86 refuse tout `ProcessId <= 0` pendant la construction de la table complète `Win32_Process`, alors que cette classe peut retourner `System Idle Process` avec `ProcessId=0`. Si cet enregistrement figure dans l'inventaire, `AMBIGUOUS_PROCESS_ID` provoque le STOP avant tout parcours WebView2. Les 14 fixtures antérieures n'incluent aucun PID 0. Ce mécanisme est une **cause possible forte, non confirmée par la sortie opérateur** car le catch masque le sous-motif ; il faut des tests fictifs PID 0 et une future proposition explicite sans réexécution implicite. Références : https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance et https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-process .

## STOP à préserver

- `G2A_REVISED_RUNTIME=STOP_WEBVIEW2_PARENTAGE` (compte-rendu opérateur), `STOP_REASON=UNEXPECTED_OR_UNSAFE` ; cause fine inconnue. Le précédent `STOP_PROCESS_NAMES` reste historique. Aucun PASS.
- `G2-B/G2-C/G2-D/G3/G4/G5/G6=NOT_AUTHORIZED`, `REAL_G3_STOP_UNAVAILABLE`.
- `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`.
- Interdits : originales SQLite (v6 prod/v7 isolée), sidecars, ACL, sauvegardes, marker d'activation, migration 007, IPC writer, fusion PR #35, M3.3, release. Aucun reset Git destructeur ni faux relecteur indépendant.

## Prochaine action concrète

1. Préserver ce nouveau STOP sans arrêter SearchHost/WebView2 ni répéter les observations locales.
2. Étudier sur sources et fixtures fictives une proposition DISTINCTE de diagnostic fail-closed produisant seulement un code de motif non personnel (`PROCESS_SNAPSHOT_CHANGED`, parent manquant, chronologie invalide, échec CIM, etc.), sans commande Windows aujourd'hui. Les métadonnées de parenté ne prouvent jamais l'absence de writer SQLite.
3. Avant tout script différent ou réexécution, afficher code intégral, interactions et effets ; obtenir un nouvel accord explicite. Aucun accès v6/v7, sidecars, G2-B/G2-C/G2-D ni G3–G6.
4. Re-fetch exact main/PR/CI/ruleset, mettre à jour MD+JSON à chaque PR significative ; requalifier CI au nouveau SHA après commit.

Se reporter à [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) pour les invariants détaillés, sans réutiliser les anciennes CI après un nouveau commit.
