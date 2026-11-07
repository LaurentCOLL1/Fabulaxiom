# M3.2 R4 — WAL preheld sans FILE_SHARE_DELETE : preuve Windows jetable

7 novembre 2026 — **CANDIDAT NON QUALIFIÉ**. Parent protégé `main=1e26526f2f86173b4962b4de7c71d5b504ee9894` (#308). Parent postmain Windows #42394767935 À QUALIFIER.

## Hypothèse limitée
Les HANDLEs R4 existants autorisent le partage DELETE (`share_mode(1|2|4)`) ; une substitution du nom entre FileId128 et le `xOpen` SQLite délégué reste possible. Microsoft documente qu'omettre FILE_SHARE_DELETE empêche une demande d'accès DELETE, dont le renommage a besoin. Aucun changement de VFS de production ici.

Deux tests Windows `#[cfg(all(test,windows))]` dans le VFS NON DÉFAUT déjà isolé : (1) WAL sous nouveau `%TEMP%/Scratch` avec `CREATE_NEW` et `share_mode(1|2)` : renommage refusé tant que le HANDLE est ouvert, identité FileId128 stable, réouverture lecture/écriture possible, renommage permis après fermeture ; (2) essai SQLite réel mais sur même fixture jetable, `locking_mode=NORMAL`, `journal_mode=WAL`, lecture/écriture synthétiques, `xShmMap` exercé, HANDLE WAL délégué observé, renommage refusé pendant le garde. Si SQLite refuse ce mode, la CI doit échouer et le résultat sera documenté **INCOMPATIBLE**, non converti en admission.

Deux tests Rust nouveaux, **328 Rust attendus, PAS PASS avant CI**. Autres attentes : 7 Greenfield/69 inventaire/183 continuité/396 Vitest/Chromium 85/85 normal+CSP/19 blobs Git fictifs. Source Windows final HEAD, diff/reviews/threads, Protect main strict bypass=[], squash `expected_head_sha`, postmain indépendant et #38 append-only obligatoires.

## STOP inchangés
Une propriété de renommage sur **un WAL** n'établit ni custody indivisible main/WAL/SHM, ni confinement des chemins parents ou alias, ni absence d'ABA non observée, ni hostilité même utilisateur, ni crash/recovery. Aucune donnée opérateur v6/v7/profil Greenfield existant, sauvegarde/journal, IPC writer, migration 007 runtime, Windows Hello natif, marqueur/recovery ou P4 réel. Aucun `App.tsx`/Tauri runtime modifié.

PRODUCT_FIRST_PARALLEL_SAFETY inchangée, prévenir avant changement. M3.2 IN_PROGRESS_NOT_ACCEPTED (~45% estimés 40–50%), writer/R1–R9 NOT_PROVEN, P4 réel STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, glib #160 OPEN_NOT_REMEDIATED. CI fixtures ≠ admission réelle.
