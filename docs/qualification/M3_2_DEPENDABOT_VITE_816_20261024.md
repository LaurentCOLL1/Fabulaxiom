# Fabulaxiom — Traitement contrôlé de cinq alertes Dependabot npm (Vite 8.1.6)

**Candidate du 24 octobre 2026 — PR [#161](https://github.com/LaurentCOLL1/Fabulaxiom/pull/161) ; aucune nouvelle autorité opérateur.**

## Source des alertes

Capture Dependabot fournie par le propriétaire : six alertes ouvertes, dont cinq sont attribuées à `vite` dans `package-lock.json` ; la sixième est `glib` Rust. La baseline exacte `main=3cbe793e4c6d7779802a2cba55640419599df1b3` fixe `vite=8.0.16` (`package.json`, `package-lock.json`), `glib=0.18.5` (`src-tauri/Cargo.lock`). Le manifeste npm ne contient **aucun paquet direct autonome `node_modules/launch-editor`** : les avis `launch-editor` sont aussi déclarés pour la série Vite concernée.

Les cinq avis npm indépendants répertoriés par GitHub, avec leurs fixes officiels :
- [GHSA-587h-7wmj-h5pm](https://github.com/advisories/GHSA-587h-7wmj-h5pm) — High, Windows fs.existsSync / launch-editor.
- [GHSA-r825-w8mm-5pxw](https://github.com/advisories/GHSA-r825-w8mm-5pxw) — Moderate, arguments éditeurs.
- [GHSA-698v-4r3x-3vcv](https://github.com/advisories/GHSA-698v-4r3x-3vcv) — Moderate, échappement du % Windows.
- [GHSA-rq7h-c2jc-7f22](https://github.com/advisories/GHSA-rq7h-c2jc-7f22) — Moderate, contrôle `server.fs.allow` hors Windows.
- [GHSA-9jrq-w75r-8gcw](https://github.com/advisories/GHSA-9jrq-w75r-8gcw) — Low, middleware custom.
Toutes documentent `vite 8.1.6` comme version corrigée dans sa série 8.1.

Sixième alerte [GHSA-wrw7-89jp-8q8g](https://github.com/advisories/GHSA-wrw7-89jp-8q8g) : `glib` `0.18.5`, correctif amont `0.20.0`, mais la résolution dépend de GTK/WebKit/Tauri et ne peut pas être forcée isolément. **Cette PR laisse `Cargo.lock` entièrement intact**. La vulnérabilité Rust demeure ouverte tant qu'une migration compatible validée n'est pas livrée ou qu'une décision motivée n'est pas adoptée.

## Méthode vérifiée de génération du verrou

Le conteneur d'analyse ne peut pas résoudre `registry.npmjs.org`, donc nous n'avons **ni inventé ni édité manuellement** les `integrity` du lock npm. Un commit préliminaire temporaire de la PR #161 a exécuté sur GitHub Actions Windows, avec permissions `contents: read` et scripts npm **désactivés** :

```text
npm install --package-lock-only --save-dev --save-exact vite@8.1.6 --ignore-scripts --no-audit --no-fund
```

Le run [#40071348881](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40071348881) s'est arrêté intentionnellement après émission du verrou exact depuis npm. Son FAILURE est **prévu, historique et non qualifiant**. Le verrou récupéré contient `vite=8.1.6` et un champ d'intégrité `sha512-` validé, les mêmes versions `vitest=5.0.3` et `@vitejs/plugin-react=6.0.2`, et la résolution npm a actualisé 22 entrées du graphe, notamment rolldown. Son écriture GitHub doit être atomique avec `package.json`, la suppression du générateur temporaire et les documents de continuité. L'ancien workflow doit être rétabli **octet pour octet**, sans génération de lock ni permission supplémentaire dans le futur `main`.

## Contrats obligatoires avant fusion

- `package.json`, root `package-lock.json` et `node_modules/vite` déclarent tous exactement `8.1.6`, `integrity sha512-`, pas de version `launch-editor` directe créée.
- `npm ci` est obligatoire (reproduit le verrou signé par le registre), `tsc --noEmit` avant Chromium, `npm run build` final, tests Vitest, code/provenance, Chromium normal + CSP strict, Rust, Tauri et toutes les règles de protection.
- `src-tauri/Cargo.lock`, `src/App.tsx`, `src-tauri`, les SQLite v6/v7 de l'opérateur, backups/ACL, migration 007 et writer IPC sont inchangés.
- Contrat handoff #95 et mise à jour des deux prompts, deux handoffs, historique et roadmap.
- Après changement des versions exactes, **nouvelle CI terminale au HEAD final** avant fusion. `Protect main`, diff complet, reviews et threads vérifiés, fusion `expected_head_sha`, puis CI postmain indépendante. Ne jamais réutiliser le run volontairement rouge.
- Le nombre réel d'alertes Dependabot doit être revérifié par le propriétaire après ingestion du nouveau `main` : le connecteur ne peut pas lire les alertes privées. **Ne pas annoncer '5 CLOSED' avant observation dans GitHub**. Garder l'[issue #160](https://github.com/LaurentCOLL1/Fabulaxiom/issues/160) ouverte pour `glib`.

## États M3.2

M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; identité `PARTIAL_LOCAL_IDENTITY_ONLY` ; writer `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Aucune promotion implicite de gate ou intervention sur le Windows de l'opérateur.
