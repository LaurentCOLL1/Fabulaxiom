# M3.2 — État d'autorité consolidé au 19 octobre 2026

**Snapshot documentaire et contrôle source-only, pas une autorisation d'exécution.** La référence structurée est [M3_2_GATE_SNAPSHOT.json](M3_2_GATE_SNAPSHOT.json), validée par `tools/test_m32_gate_snapshot.py`. Le SHA et la CI ci-dessous sont datés : **re-fetch GitHub obligatoire** avant toute nouvelle PR/fusion ou procédure Windows. Une CI ultérieure ne prouve pas à elle seule l'authenticité des fichiers de l'opérateur.

## Dernier état confirmé

- `main=f9e6b18236fd70674849f6e956c7cff410dcef2c`, PR #82 [fusionnée](https://github.com/LaurentCOLL1/Fabulaxiom/pull/82), CI [#39202144936](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39202144936) terminale 58/58 au HEAD `07ce685d4d418f443b63b6946fe2582455811b9f`.
- CI : tests des manifestes Core **réellement générés dans le runner**, résolution native et refus pour la fenêtre fictive ; Chromium 29/29 ×2, frontend 129, Rust général 100. Ce sont des preuves compile-only et synthétiques, **pas** un test de permissions WebView2 effectives ou une qualification des données opérateur.
- `M32_SECURITY_PREFLIGHT_STOP` maintenu ; `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`.
- PR #35 **OPEN/DRAFT**, issues #36/#38 **OPEN**, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G2 à G6 réels `NOT_AUTHORIZED`.

## Cinq rôles historiques toujours distincts

| Rôle | Preuve actuellement connue | Ce qui manque |
| --- | --- | --- |
| `production/pre_m24_early_manifest` | `OBSERVED_SHA256_ONLY` | Témoin antérieur authentifié du manifest et de son empreinte |
| `acl/original_acls` | `OBSERVED_SHA256_ONLY` | Preuve tierce antérieure des ACL et de leur rôle |
| `acl/pre_repair_json` | `OBSERVED_SHA256_ONLY` | Ancrage contemporain du JSON pré-réparation |
| `production/activation_marker` | `UNANCHORED_OBSERVED` | Octets historiques et chaîne de conservation |
| `m25/isolated_v6` | `UNANCHORED_OBSERVED` | Témoin historique propre à la copie isolée v6 |

Les 21 autres rôles ont un ancrage déjà recensé. **Trois rôles seulement observés ne deviennent pas trois attestations indépendantes.** Les deux rôles non ancrés ne sont pas réparés par les empreintes d'autres sauvegardes. Se reporter à l'[issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36).

## Décision prospective de l'opérateur unique

La politique `SOLO_OPERATOR_COMPENSATING_CONTROLS` est adoptée **au niveau documentaire seulement** : elle permet de préparer une nouvelle baseline future, mais ne répare pas les cinq preuves historiques et ne constitue pas une revue humaine indépendante. La baseline prospective est `NOT_STARTED`.

**Le chemin autorisé maintenant est la préparation documentaire et les essais sur fixtures fictives.** Les gates G2 (observation Windows), G3 (capture), G4 (contrôles et restauration sur copies), G5 (acceptation personnelle du risque) et G6 (premier usage applicatif isolé) ont chacun besoin de preuves et d'autorisations spécifiques supplémentaires. Le [runbook](../qualification/M3_2_PROSPECTIVE_BASELINE_WINDOWS_RUNBOOK_DRAFT.md) reste **NON EXÉCUTABLE**. L'absence de provenance authentique, d'un propriétaire SQLite non migrant ou d'un protocole cold-source approuvé maintient G3 réel STOP.

**Interdit dans cette tranche :** lancer Tauri/WebView2 chez l'opérateur ; ouvrir/modifier les SQLite active v6 ou isolée v7, sidecars, ACL, backups, manifests, activation marker ou sept worktrees ; migration 007, IPC writer, fusion #35, M3.3 ou release. Ne jamais publier d'informations privées dans GitHub.

Le contrôle JSON CI refuse toute promotion de ces statuts. Il ne récupère pas à lui seul les vérifications GitHub en direct et n'autorise aucune étape Windows.
