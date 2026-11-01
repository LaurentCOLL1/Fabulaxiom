# M3.2 P3c — relation avant/après explicite avec prévisualisation et refus de cycle

**1er novembre 2026 — CANDIDAT NON QUALIFIÉ**. Parent #262 P3b fusionnée sous Protect main : \`main=26f189218b82c3ae0567ada9c8ee998f31e8b287\`, CI source Windows #41355180008 completed/SUCCESS **302 Rust/7 Greenfield/68 SQLite inventaire/183 continuité, Chromium 85/85**, postmain indépendante #41356340682 à qualifier séparément.

## Fonctionnalité produit visible seulement dans le laboratoire fictif

Étendre **sans créer de second écran** \`src/M32P3FictionalCommandWorkshop.tsx\` : formulaire distinct pour choisir deux ancres actives du même Univers, saisir une justification humaine, prévisualiser la relation et son verdict avant validation. Le réducteur \`applyP3FictionalCommand\` existant exécute la commande typée \`create_precedence\` uniquement sur validation explicite ; les liens non choisis restent indéterminés. Contrôle préliminaire par \`previewFictionalPrecedence\` (déjà existant), témoin de cycle visible, refus auto/self/duplicates/historic/external ID, bouton désactivé si verdict invalide ou justification absente. Historique d'audit et command counter déjà existants conservés. La réinitialisation efface aussi la proposition P3c. Aucun vrai IPC Tauri, aucun nouvel accès au Rust, aucune sauvegarde, aucun accès aux données opérateur.

Quatre tests Vitest \`src/m32P3cPrecedencePreview.test.tsx\` : rendu accessible, lien explicite, cycle/témoin et immutabilité en cas de refus, autres Univers/ancres inconnues. Trois interactions Playwright ajoutées à \`tools/m32_browser_interaction.cjs\` : 86 relation C→D, 87 cycle C→A avec témoin/submit disabled et compteur inchangé, 88 nouveau scénario Univers K→L sans fuite. Les marqueurs historiques Chromium 85/85 restent conservés comme historique et **88/88** deviennent attendus. Aucun fichier source additionnel dans le manifeste navigateur exact 17 blobs ; seuls fichier UI déjà allowlisté, tests TS, driver de test, documents, roadmaps et handoff changent.

## Qualification

Avant CI **302 Rust / 7 Greenfield / 68 SQLite inventaire / 184 continuité ATTENDUS NON QUALIFIÉS**, Chromium **88/88 ATTENDUS NON QUALIFIÉS** dans les deux modes, **4 Vitest nouveaux**. Vérifier HEAD CI Windows, logs, diff/reviews/threads, Protect main ACTIVE strict bypass=[], squash expected_head_sha puis postmain indépendante. Aucun changement au runtime \`src/App.tsx\`, writer \`m32_v7_writer_service.rs\`, Cargo.lock, migration runtime 007 ou profil Greenfield opérateur.

Conserver \`PRODUCT_FIRST_PARALLEL_SAFETY\`, progression produit et R4–R9 sécurité **en parallèle** ; avertir le propriétaire AVANT toute modification de stratégie. Risque Linux GLIB 0.18.5 / GHSA-wrw7-89jp-8q8g **OPEN_NOT_REMEDIATED** issue #160 ; aucune suppression/dismiss ou faux correctif. Issues #38/#160 append-only.

**STOP** M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucune SQLite opérateur, \`M:\\Fabulaxiom\`, profil \`%LOCALAPPDATA%\\com.fabulaxiom.greenfield.v1\`, migration 007 réelle, IPC writer, Windows Hello, sauvegardes/journaux, marqueur ou recovery.
