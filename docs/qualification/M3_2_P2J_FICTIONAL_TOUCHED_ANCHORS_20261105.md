**05/11 — #291 P2j FUSIONNÉE / POSTMAIN À QUALIFIER** : source #42097245194 SUCCESS 320 Rust/7 Greenfield/68 inventaire/183 continuité/373 Vitest/Chromium 85/85+CSP/19 blobs, HEAD fa7b10188593c5b16f6534a8aab11be68dcf7b5a. Protect main ACTIVE strict bypass=[], squash expected_head_sha, main=0bb80afa95f4e78b5a16f9d53e6ba17dedf72212 ; parent #290 postmain #42095684848 SUCCESS ; #291 postmain #42107333266 IN_PROGRESS/NON QUALIFIÉ au checkpoint ; issue #38 append-only #6669124828. P2j n'utilise que des assertions fictives en mémoire React : ni App.tsx, ni service/IPC writer, ni données/profil opérateur, 007 runtime, native Hello, sauvegarde/journal, marqueur ou recovery. PRODUCT_FIRST_PARALLEL_SAFETY inchangée, prévenir AVANT changement ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % 40–50 % estimés) ; writer/P4 réel/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; glib #160 OPEN. CI fixtures ≠ admission réelle.

# M3.2 P2j — Ancres mentionnées par les relations modifiées (atelier de fiction)

Date : 5 novembre 2026. **CANDIDAT / NON QUALIFIÉ** tant que le CI Windows à SHA exact n'a pas été inspecté.

## Objet et contrat

La projection pure `previewP2jFictionalTouchedAnchors` complète P2i. Elle n'affiche que les identifiants des ancres directement mentionnées dans les assertions de précédence **retirées** et/ou **ajoutées** après une correction inventée en mémoire. Elle exclut les liens inchangés. Une même ancre peut apparaître dans les deux catégories de changement. Le tri est lexicographique pour l'affichage uniquement : **pas de dates, ordre total, transitivité implicite, narration ou révélation inférés**. Les IDs comparés reprennent les valeurs complètes des liens P2i, et non seulement leurs noms.

La validation et les refus sont hérités de P2i : provenance exclusivement `fictional_browser_memory_only`, même univers, flags de production/G3 strictement `false`, DAG sans cycle, pas de self-link ni de doublon exact. Erreur : refus visible sans fuite des identifiants. Valeurs fictives affichées sous JSX échappé.

Fichiers : `src/M32P2jFictionalTouchedAnchors.tsx` et `src/m32P2jFictionalTouchedAnchors.test.tsx`. **Six nouveaux tests Vitest (373 total attendus, NON ACQUIS)** : différence et absence de mutation, inchangés exclus, ID réutilisé, provenance étrangère, cycles et self-links, accessibilité/lecture seule/échappement HTML.

## Frontières préservées

Module non importé par `App.tsx`, sans pont Rust, Tauri IPC, réseau, disque, SQLite, Ollama ni écriture. Aucun profil ou fichier opérateur, backup/journal, migration 007, native Hello, marqueur ou recovery. Le produit réel P4 et le writer restent **STOP**. La stratégie `PRODUCT_FIRST_PARALLEL_SAFETY` est inchangée, avertir avant tout changement. **M3.2 IN_PROGRESS_NOT_ACCEPTED**, estimation inchangée ~45 % (40–50 %). R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, glib #160 OPEN_NOT_REMEDIATED.

## Qualification demandée

Vérifier le postmain indépendant de la PR #290 et son SHA, le **CI Windows complet au HEAD exact** de P2j, les tests TypeScript/Vitest (373 attendus), Rust 320, Greenfield 7, inventaire 68, continuité 183, Chromium 85/85 normal+CSP, 19 blobs Git fictifs. Auditer diff/reviews/threads et Protect main actif strict bypass=[] ; fusion seulement par PR protégée avec `expected_head_sha`, puis **nouveau** CI postmain indépendant et issue #38 append-only. Tests sur fixtures ≠ admission writer réelle.
