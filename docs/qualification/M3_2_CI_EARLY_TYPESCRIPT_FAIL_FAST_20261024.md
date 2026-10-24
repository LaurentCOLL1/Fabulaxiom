# M3.2 — Précontrôle TypeScript anticipé : qualification de la vitesse sans nouveau privilège

**Candidat du 24 octobre 2026, GitHub Actions uniquement.** Pas de commande sur la machine Windows de l'opérateur, pas de SQLite originale, aucun changement des protections de branche.

## Problème observé et réponse

La PR #158 a subi un cycle CI infructueux #40063282786 : les 93 contrats de continuité, les 96 tests événementiels et les 82/82 interactions Chromium dans **chacun des deux modes** avaient réussi, mais l'étape tardive `Frontend production build` a échoué sur trois appels `Array.prototype.at` incompatibles avec la cible TypeScript du dépôt. Ce n'était pas une panne navigateur ni Rust ; le coût des étapes Chromium avait déjà été payé.

Dans `.github/workflows/m0-ci.yml`, ajouter **uniquement** un test précoce `npx tsc --noEmit --pretty false` après `npm ci`, avant les tests et Chromium. `--noEmit` n'écrit pas de fichiers JavaScript. La commande `npm run build` existante doit **rester** en fin de parcours (vérifie aussi Vite), tout comme les contrôles source-only, Vitest, Chromium normal + CSP strict, cargo test/check, audits Tauri et garde des deux prompts.

Ce changement ajoute un seul pas Windows, soit **77 au lieu des 76 historiques**, si la configuration reste inchangée. Il améliore le *délai de détection* de problèmes TypeScript ; ce n'est **pas** une preuve de diminution de la durée d'un run PASS. Un SHA modifié impose sa propre CI complète, puis un contrôle postmain indépendant.

## Traitement séparé du cache Cargo

La même revue a confirmé que `actions/setup-node` utilise déjà `cache: npm`, et que la CI ne configure pas explicitement de cache Cargo. [GitHub — dependency caching](https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching) signale que les caches ne sont pas signés, que des forks peuvent les lire, et qu'un cache contaminé est une entrée non fiable. [GitHub — cache access](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) explicite les restrictions propres aux PR, aux merges, et aux caches de `main`.

**Décision : ne PAS ajouter de cache Cargo à cette PR.** Une étude source-only séparée examinera les effets sur la chaîne de confiance, l'action épinglée par SHA, la portée du cache, les branches autorisées à l'écrire, les tests de corruption, les métriques avant/après, les limites de stockage et le comportement en absence de cache. Aucun risque d'empoisonnement ne peut être écarté par simple hypothèse. Aucun secret ou artefact propriétaire dans un cache.

## Contrat CI de cette tranche

Le contrat handoff #94 garantit : PR #158 fusionnée et ses CI terminales source #40063511352 / postmain #40064299969 distinctes ; précontrôle exactement une fois après `npm ci` et avant Chromium ; construction complète et tous les autres tests préservés ; permissions `contents: read` ; aucun cache nouveau ; deux prompts, deux handoffs et roadmap mis à jour. Aucun changement `Protect main` ou `src-tauri`.

**Gates réelles immuables :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; identité `PARTIAL_LOCAL_IDENTITY_ONLY` ; absence d'écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Aucune base originale v6/v7, backups, ACL, sidecars, marqueur, migration 007, writer IPC, exécution Windows opérateur, M3.3, ComfyUI ou release.

**Préqualifications non anticipées :** 94 contrats, 96 tests événementiels, 82/82 Chromium dans chaque mode, 132 Rust, 77 pas Windows, nouveau SHA et CI terminale ; revue de la totalité du diff, reviews, threads, règles `Protect main`, fusion `expected_head_sha`, vérification postmain.
