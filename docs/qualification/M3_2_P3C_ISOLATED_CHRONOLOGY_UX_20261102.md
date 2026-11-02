**2 novembre 2026 — ADDENDUM TERMINAL PR #264** : source HEAD `cad79d5e479d1d92fcec2abbd4f9e5f6c602c5bb`, CI #41363608420 completed/SUCCESS ; squash sous Protect main strict bypass=[], `main=2ff56d7bbee531990da5644f857517e88e924959` ; CI indépendante postmain #41364545825 completed/SUCCESS, **302/7/68/183 et Chromium 85/85 normal + CSP stricte**. Reviews=[], threads=[], issue #38 commentaire append-only #6565935760. Les annotations « candidat » ci-dessous reflètent uniquement l'état AVANT qualification et restent historiques. Prochaine étape P3d sur fixtures uniquement. M3.2/writer/G3 STOP inchangés.

# M3.2 — P3c atelier React fictif : ergonomie et ordre partiel

**2 novembre 2026 — CANDIDAT NON QUALIFIÉ.** Base vérifiée PR #262 fusionnée : `main=26f189218b82c3ae0567ada9c8ee998f31e8b287`, Windows source CI #41355180008, postmain #41356340682 completed/SUCCESS, 302 Rust / 7 Greenfield / 68 inventaire / 183 continuité. Règle Protect main active stricte, bypass=[].

## Portée du changement

- `src/M32P3FictionalCommandWorkshop.tsx`, **non monté dans App.tsx** : nouveau formulaire distinct « Relier deux dates déjà créées » avec sélection explicite de deux ancres de même Univers et justification humaine. Il utilise la commande existante `create_precedence` et le réducteur TS purement fictif P3a ; pas de création involontaire d'ancre. Les refus (cycle, doublon, identifiants inconnus, motif vide, même ancre) laissent l'ancien état immuable. Le reset remet aussi à zéro les choix du second formulaire.
- Consultation intégrée de la projection `M32ChronologyPreview` existante, avec trois vues **distinctes** : temps du monde (ancres et seuls liens humains déclarés), narration ordonnée uniquement au sein de chaque roman, révélation au lecteur « non renseignée ». Une liste triée par identifiant n'est jamais présentée comme ordre chronologique.
- Trois tests Vitest dans `src/m32P3cFictionalUx.test.tsx`, séparés des 11 tests P3a d'origine : étiquettes et vues séparées, création d'une relation sans nouvelle ancre, refus du cycle/de l'auto-lien/de la raison vide sans mutation. `App.tsx`, Tauri, Rust, schémas, lockfiles, IPC et migrations inchangés.

## Qualification attendue — PAS ACQUISE

Windows source CI à SHA exact : **302 Rust / 7 Greenfield / 68 inventaire / 183 continuité**, frontend Vitest +3 par rapport à P3b et Chromium 85 attendus. Vérifier logs, audit diff, reviews et threads, `Protect main` strict sans bypass, puis seulement si tout est conforme squash avec `expected_head_sha` et postmain CI indépendante. La présence de tests n'est pas une preuve de fonctionnement réel.

**Stratégie active : `PRODUCT_FIRST_PARALLEL_SAFETY`.** P3c n'est pas une connexion Rust/React, un atelier de production, une persistance disque, une démonstration d'IPC, une autorisation du writer ni une admission P4/P5. Les expérimentations R4–R9, SHM regions >0 et custody atomique main/WAL/SHM continuent parallèlement ; prévenir l'utilisateur avant tout changement de stratégie. glib 0.18.5 GTK3 Linux Dependabot #1 OPEN_NOT_REMEDIATED (#160), aucun faux correctif/dismiss.

**STOP inchangés :** M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucune base opérateur, profil Greenfield existant, journaux/sauvegardes, migration 007, writer IPC, Windows Hello natif, marqueur ou recovery. Issues #38/#160 append-only.
