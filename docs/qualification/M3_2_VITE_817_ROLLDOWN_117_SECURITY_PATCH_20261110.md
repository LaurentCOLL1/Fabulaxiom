# Fabulaxiom M3.2 — Correctif sécurité Vite 8.1.7 / Rolldown 1.1.7 (branche séparée)

**10 novembre 2026 — CANDIDAT, NON QUALIFIÉ jusqu'à CI Windows sur HEAD exact et postmain indépendant.**
Parent protected `main=9036ddc95a2a0e03ed920f76f4d9fd87963d6fb7`, #337 P3p MERGED sous Protect main actif, strict, `bypass_actors=[]` ; CI source #42905042214 completed/SUCCESS HEAD `e25c4620b8bea7fcc5fb03e66abb39aed90add41`, postmain #42907052087 attempt 1 completed/SUCCESS au SHA main exact (job #130147668093 : 88 SUCCESS, 1 PR-only SKIPPED).

## Avis officiel et périmètre

L'avis critique GitHub Vite [GHSA-p4f5-76q4-ffq7](https://github.com/vitejs/vite/security/advisories/GHSA-p4f5-76q4-ffq7), publié le **10/11/2026**, vise `vite >=8.0.0, <=8.1.6` et déclare corrigé `vite 8.1.7` grâce à `rolldown 1.1.7` (code vulnérable embarqué dans Rolldown v8). L'impact annoncé nécessite un **serveur Vite de développement explicitement accessible au réseau** ; ce n'est ni une preuve d'exploitation locale ni une preuve que le build Tauri distribué est affecté. Dans `vite.config.ts`, la configuration par défaut reste `host: host || false` ; `TAURI_DEV_HOST` peut modifier l'exposition. Aucune machine opérateur n'a été interrogée.

Source authentifiée via runner GitHub éphémère : workflow de bootstrap **#42916864109** sur SHA `198b95c6b21a07efa85722252e0c3f86417fe7f5` completed/SUCCESS, `npm install --package-lock-only --ignore-scripts --no-audit --no-fund --save-exact --save-dev vite@8.1.7`, sans scripts et sans contact avec les sources opérateur. Le lockfile a été produit par le résolveur npm (non reconstruit manuellement), inspecté et transféré sur la branche sécurisée. Le workflow **temporaire a été supprimé avant la PR**.

## Diff et dérives de résolveur contrôlées

- `package.json` : `vite 8.1.6 → 8.1.7`, version exacte.
- `package-lock.json` : entrée Vite, contrainte `rolldown ~1.1.7`, Rolldown `1.1.5 → 1.1.7` et **15 modules binaires optionnels** `@rolldown/binding-*` `1.1.5 → 1.1.7`, y compris win32-x64 et win32-arm64. Intégrités `sha512` conservées par npm.
- Deux autres versions transitives réévaluées par **npm lui-même** : `@napi-rs/wasm-runtime 1.2.5 → 1.1.6` (downgrade) et `tslib 2.8.1 → 2.9.1`. **Aucune assertion de neutralité de cette dérive** : vérifier explicitement la suite Windows et, si nécessaire, isoler une résolution moins intrusive ; ne pas modifier les hash/integrity à la main.
- `tools/test_m32_vite_817_security_lock.py` : 10 tests indépendants source-only, dont refus de downgrade, absence ou désalignement binaire Windows, absence d'intégrité, défaut de binding et contrôle du host par défaut.
- `.github/workflows/m0-ci.yml` : 1 étape supplémentaire `unittest` après les autres contrôles Vite ; **aucune suppression** de contrôle existant ni assouplissement Protect main.

## Barrières de qualification et checklist

La CI Windows doit réussir sur le **HEAD exact de la PR**, avec `npm ci`, TypeScript, Vitest, Chromium synthétique, Rust/Tauri et tous les contrôles existants, plus les 10 refus source-only. Reviews/threads, Protect main strict `bypass_actors=[]`, squash gardé par `expected_head_sha`, puis CI postmain indépendante au SHA exact sont impératifs. Vérifier ensuite le statut réel de l'alerte Dependabot ; **ne pas déclarer issue #160 corrigée** sans preuves de toutes ses dépendances, notamment `glib` Linux et éventuellement `launch-editor`. Ce correctif traite seulement une version Vite vulnérable identifiée, pas toutes les six alertes d'origine.

**Checklist maître : 104 obligations, M32-001 et M32-002 closes, 102 ouvertes. AUCUNE case nouvelle clôturée.** `M32-092 [ ]` preuve partielle Vite, `M32-093 [ ]` glib 0.18.5 non corrigée, `M32-094 [ ]` Windows/Linux à qualifier séparément. #35/#215 restent DRAFT. L'issue #38 reste append-only ; #160 OPEN_NOT_REMEDIATED jusqu'à clôture justifiée.

Stratégie `PRODUCT_FIRST_PARALLEL_SAFETY` conservée, avertir AVANT toute réorientation. M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % estimés), writer/R1–R9 `NOT_PROVEN`, P4 réel STOP, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, main/WAL/SHM et ABA invisible `NOT_PROVEN`. STOP v6/v7, Greenfield existant, `M:\\Fabulaxiom`, backups, IPC writer, migration 007, Windows Hello et recovery. CI fictive ≠ admission.
