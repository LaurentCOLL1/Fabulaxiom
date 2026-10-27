# M3.2 — Windows Hello Desktop HWND : audit d'autorisation backend (source/fixtures seulement)

**27 octobre 2026 — CANDIDAT NON QUALIFIÉ avant CI au SHA propre.** Base GitHub re-fetch : `main=34b4174dd79d7c133b3700d72a705236f7623640` après [PR #198](https://github.com/LaurentCOLL1/Fabulaxiom/pull/198), source `9b4b4049c461986c8427620f649a4e2113078800`, [CI #40569850503](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40569850503) SUCCESS, [postmain #40571697037](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40571697037) SUCCESS indépendante, [issue #38 terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6452075388). Ces succès portent sur **165 Rust / 7 Greenfield / 36 gardes / 129 contrats** à leurs SHA, et non sur le candidat ci-dessous. `Protect main` actif et strict, PR #35 toujours OPEN/DRAFT.

## Fait API vérifié : WinRT UWP ≠ interop Desktop HWND

- L'API bureau `IUserConsentVerifierInterop::RequestVerificationForWindowAsync(HWND, HSTRING, REFIID, void**)` prend la fenêtre de l'application active et renvoie une opération asynchrone `UserConsentVerificationResult` ; la documentation Win32 Microsoft indique **Windows build 22000 minimum**. Le support de `UserConsentVerifier`/`RequestVerificationAsync` dès Windows 10 concerne l'API **UWP** et ne qualifie pas par transitivité l'appel desktop. **Windows 10 et tout build inférieur à 22000 doivent être refusés** tant qu'une autre voie n'est pas documentée, spécifiée et acceptée séparément.
- `CheckAvailabilityAsync()` peut retourner `Available`, `DeviceNotPresent`, `NotConfiguredForUser`, `DisabledByPolicy` ou `DeviceBusy`. Le résultat de vérification n'est positif que pour `Verified` ; `DeviceNotPresent`, `NotConfiguredForUser`, `DisabledByPolicy`, `DeviceBusy`, `RetriesExhausted`, `Canceled`, HRESULT, échec asynchrone ou résultat inconnu sont négatifs. Même `Available` ne prouve ni succès futur ni prise en charge de l'interop HWND.
- Le résultat est un **consentement local ponctuel du compte Windows actuel**, pas une signature de décision, pas une nouvelle identité Fabulaxiom, pas une preuve d'absence de writer SQLite ni de protection des octets du fichier. Fabulaxiom ne demande jamais PIN, mot de passe Windows ou biométrie dans son UI.

Sources primaires : [Microsoft méthode Win32/versions minimales](https://learn.microsoft.com/en-us/windows/win32/api/userconsentverifierinterop/nf-userconsentverifierinterop-iuserconsentverifierinterop-requestverificationforwindowasync), [interop pour application Desktop](https://learn.microsoft.com/en-us/windows/apps/develop/ui/display-ui-objects), [classe UserConsentVerifier, UWP vs Desktop](https://learn.microsoft.com/en-us/uwp/api/windows.security.credentials.ui.userconsentverifier), [availability](https://learn.microsoft.com/en-us/uwp/api/windows.security.credentials.ui.userconsentverifieravailability), [résultats](https://learn.microsoft.com/en-us/uwp/api/windows.security.credentials.ui.userconsentverificationresult).

## Frontière source actuelle et refus de raccourcis

| Élément dans `main` | Observation source | Conséquence |
|---|---|---|
| `src-tauri/src/m32_sensitive_action_consent_tests.rs` | Onze tests `#[cfg(test)]` d'intention exacte et ticket consommable ; `TrustedOsOutcome::Verified` **injecté par fixture** | Pas d'OS Hello, pas de jeton IPC utilisable en production |
| `src-tauri/src/lib.rs` — application normale | `invoke_handler` contient des commandes réelles M2 et `database_status` | Une future preuve Hello ne sécurise **pas rétroactivement** ces commandes ; aucun branchement Hello sur elles dans ce candidat |
| `database_status` et `database::open_database` | L'ouverture normale appelle `run_migrations` | Non admissible pour une preuve G3 non migrante ni pour l'ouvreur v7 encore interdit |
| Build `m31-isolated-preview` | Commande de statut lecture seule distincte | Ne pas convertir en writer ni en UI Hello implicite |
| Build `m32-synthetic-preview` | Pas de `invoke_handler` | Conserver ce laboratoire sans accès aux SQLite opérateur |

**Contrat futur à concevoir avant toute activation (non implémenté) :** l'intention exacte naît et reste côté backend de confiance ; le gate indépendant est vérifié avant demande et juste avant action ; le backend relève lui-même un HWND valide lui appartenant (identité de processus, fenêtre active, durée de vie) et la compatibilité Windows ; il interroge la disponibilité puis lance l'interop desktop depuis le contexte adapté, contrôle HRESULT et résultat asynchrone ; il invalide tout jeton dès refus, changement d'intention, changement de fenêtre, expiration, annulation ou course. La vérification Hello reste distincte de la preuve d'identité SQLite **avant `xOpen`**, de l'absence de writer et de l'autorisation de la mutation. Aucun booléen `verified` provenant de React/IPC ne peut activer une commande sensible. Les détails de threading, propriétaire `HWND` et possibilité de réutilisation d'un handle exigent une revue native réelle et des contre-tests Windows ultérieurs ; les prédicats simulés ci-dessous ne les attestent pas.

## Nouvelle tranche test-only exacte

- `src-tauri/src/m32_desktop_hello_boundary_tests.rs`, importée uniquement par `#[cfg(test)]` dans `lib.rs`, utilise **des entiers inventés** pour build, fenêtre, propriétaire et processus ; aucun HWND réel, WinRT, COM, entrée utilisateur, IPC, SQLite, sidecar ou chemin Windows n'est ouvert.
- Six tests Rust nouveaux : Windows 10/moins de 22000 refusé sans fallback UWP ; seuil 22000 seulement *candidat d'appel* ; gate préalable ; fenêtre absente/étrangère/inactive ; cinq indisponibilités ; instantané/autorisation changé après demande. Même l'issue `Ok` finale ne prouve que des valeurs fictives.
- Contrat Python de continuité : aucun symbole `#[tauri::command]`, `RequestVerificationForWindowAsync(` effectif, `Connection::open`, `unsafe` ou appel de Windows natif dans le module test-only ; assertions sur la qualification, les six tests, l'invariant de profil, les STOP et deux prompts.
- **Objectifs seulement** avant toute CI fraîche : **171 Rust**, 7 Greenfield, 36 gardes d'inventaire SQLite, **130 contrats**. Aucun PASS anticipé ni mesure d'OS propriétaire déduite.

## Décisions et critères avant étape native distincte

1. Décider explicitement du support Windows 10/Windows 11 de Fabulaxiom. Avec cette API documentée, Windows 10 = refus de confirmation sensible, **sans mot de passe de repli**. Une autre implémentation exige une revue de compatibilité séparée.
2. Approuver **séparément** une conception concrète d'interface Rust/WinRT HWND (dépendances, threading/dispatcher, propriétaire de fenêtre, codes de sortie, interruption, validation de processus, intégrité du jeton backend), sur un nouveau SHA et CI Windows ; la fixture n'est pas cette approbation.
3. Qualifier ensuite les chemins de refus via banc Windows jetable réellement natif avant toute demande à l'opérateur. Une vraie cérémonie Windows/Hello sur le poste propriétaire impose la présentation du code exact, des interactions et des effets, et un consentement neuf explicite.
4. Avant tout CRUD/UX v7 réel sur **le même profil** `com.fabulaxiom.greenfield.v1`, prouver séparément la non-substitution et l'atomicité **pré-`xOpen`**, la chaîne de répertoires/ACL/reparse, la gestion des sidecars et l'unicité de writer. Windows Hello ne déverrouille aucun de ces gates.

**STOP inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, #35 OPEN/DRAFT. Aucun Windows Hello natif, PIN, compte/mot de passe d'application, nouveau profil, SQLite v6/v7 ou backup opérateur, ACL, WAL/SHM/journal/marqueur, migration 007, writer IPC, M3.3 ni release.

**Gouvernance :** SHA final de PR + `Windows frontend and Rust checks` strict completed/SUCCESS, diff, reviews, threads, ruleset `Protect main`, squash `expected_head_sha`, postmain `push` indépendante, issue #38 append-only. Ces étapes ne sont **pas réalisées pour cette candidate** tant que la CI n'est pas re-fetch et terminée.
