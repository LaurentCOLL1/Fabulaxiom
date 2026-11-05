# M3.2 P2j — Ancres mentionnées par les relations modifiées (atelier de fiction)

Date : 5 novembre 2026. **CANDIDAT / NON QUALIFIÉ** tant que le CI Windows à SHA exact n'a pas été inspecté.

## Objet et contrat

La projection pure \`previewP2jFictionalTouchedAnchors\` complète P2i. Elle n'affiche que les identifiants des ancres directement mentionnées dans les assertions de précédence **retirées** et/ou **ajoutées** après une correction inventée en mémoire. Elle exclut les liens inchangés. Une même ancre peut apparaître dans les deux catégories de changement. Le tri est lexicographique pour l'affichage uniquement : **pas de dates, ordre total, transitivité implicite, narration ou révélation inférés**. Les IDs comparés reprennent les valeurs complètes des liens P2i, et non seulement leurs noms.

La validation et les refus sont hérités de P2i : provenance exclusivement \`fictional_browser_memory_only\`, même univers, flags de production/G3 strictement \`false\`, DAG sans cycle, pas de self-link ni de doublon exact. Erreur : refus visible sans fuite des identifiants. Valeurs fictives affichées sous JSX échappé.

Fichiers : \`src/M32P2jFictionalTouchedAnchors.tsx\` et \`src/m32P2jFictionalTouchedAnchors.test.tsx\`. **Six nouveaux tests Vitest (373 total attendus, NON ACQUIS)** : différence et absence de mutation, inchangés exclus, ID réutilisé, provenance étrangère, cycles et self-links, accessibilité/lecture seule/échappement HTML.

## Frontières préservées

Module non importé par \`App.tsx\`, sans pont Rust, Tauri IPC, réseau, disque, SQLite, Ollama ni écriture. Aucun profil ou fichier opérateur, backup/journal, migration 007, native Hello, marqueur ou recovery. Le produit réel P4 et le writer restent **STOP**. La stratégie \`PRODUCT_FIRST_PARALLEL_SAFETY\` est inchangée, avertir avant tout changement. **M3.2 IN_PROGRESS_NOT_ACCEPTED**, estimation inchangée ~45 % (40–50 %). R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, glib #160 OPEN_NOT_REMEDIATED.

## Qualification demandée

Vérifier le postmain indépendant de la PR #290 et son SHA, le **CI Windows complet au HEAD exact** de P2j, les tests TypeScript/Vitest (373 attendus), Rust 320, Greenfield 7, inventaire 68, continuité 183, Chromium 85/85 normal+CSP, 19 blobs Git fictifs. Auditer diff/reviews/threads et Protect main actif strict bypass=[] ; fusion seulement par PR protégée avec \`expected_head_sha\`, puis **nouveau** CI postmain indépendant et issue #38 append-only. Tests sur fixtures ≠ admission writer réelle.
