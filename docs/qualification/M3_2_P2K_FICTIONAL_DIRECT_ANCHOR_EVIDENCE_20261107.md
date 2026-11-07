# M3.2 P2k — Preuves directes par ancre touchée (fiction uniquement)

7 novembre 2026 — CANDIDAT NON QUALIFIÉ. Parent main protégé `dde0e2a8b9a90eb741afcec5e8ba2f36c6de4e44` (PR #302), postmain indépendant Windows #42354002526 À QUALIFIER.

## Objectif
Après l'atelier P2j qui liste les ancres directement touchées par une correction fictive, P2k présente, pour une ancre explicitement sélectionnée, **uniquement** les assertions de précédence retirées et ajoutées qui mentionnent cette ancre. La sélection n'est acceptée que si l'ancre figure parmi les ancres touchées P2j. Les relations inchangées sont exclues. Le tri des assertions repose sur leur valeur complète (ID, extrémités, origine), non sur une date ou une priorité narrative.

La projection pure `previewP2kFictionalAnchorEvidence` hérite de toutes les validations P2i/P2j : monde fictif unique, provenance `fictional_browser_memory_only`, refus du writer et G3 réels, DAG sans cycle, pas de self-link ni d'assertion dupliquée. Un ID d'assertion réutilisé avec des extrémités différentes est considéré comme retrait + ajout, jamais comme stabilité de l'ordre. Les valeurs sont échappées par React JSX ; l'erreur produit un refus visible sans exposer les identifiants.

Deux nouveaux modules indépendants `src/M32P2kFictionalAnchorEvidence.tsx` et `src/m32P2kFictionalAnchorEvidence.test.tsx`, **sept nouveaux tests Vitest** (380 attendus, PAS PASS avant CI): directe retirée/ajoutée + immutabilité, ancre inchangée refusée, ID réutilisé, tri complet et absence de transitivité, provenance/writer/univers forgés, cycles/self/dupliqués, accessibilité/échappement/XSS/refus sans fuite.

## Périmètre et STOP
Aucun import depuis `App.tsx` ; aucun appel réseau, Tauri IPC, SQL, Rust, Ollama, disque, sauvegarde, journal ou donnée opérateur. Produit fictif browser RAM seulement, PAS un produit P4 réel et aucune commande réelle. PRODUCT_FIRST_PARALLEL_SAFETY inchangée (prévenir avant changement). M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % estimés 40–50 %), writer/R1–R9 NOT_PROVEN, P4 réel STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; glib issue #160 OPEN_NOT_REMEDIATED. Ni bases opérateur v6/v7 ni profil Greenfield existant, backups/journaux, IPC writer, migration 007, native Hello, marqueur ou recovery.

## Qualification
Parent #302 postmain indépendant terminal/SUCCESS au SHA exact avant fusion ; Windows CI source au HEAD final terminal/SUCCESS attendus 326 Rust, 7 Greenfield, 69 inventaire SQLite, 183 continuité, 380 Vitest, Chromium 85/85 normal+CSP et 19 blobs fictifs. Diff/reviews/threads, Protect main ACTIVE strict bypass=[], squash gardé expected_head_sha, nouvelle CI postmain et issue #38 append-only. CI fixtures != admission réelle.
