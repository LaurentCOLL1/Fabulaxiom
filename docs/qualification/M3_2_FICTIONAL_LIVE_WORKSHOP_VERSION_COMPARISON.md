# M3.2 — Comparaison en direct des versions inventées dans l'atelier manuel

**Candidate source-only du 24 octobre 2026. Aucune exécution sur le Windows de l'opérateur.**

## Justification et périmètre

La PR #156 a qualifié un comparateur interactif à trois menus dans un laboratoire Chromium, mais sur un carnet inventé préconstruit distinct. Cette tranche place le composant existant `M32FictionalEventVersionPairLab` dans le **même** `M32FictionalEventManualWorkshop` (lui-même exclusivement monté dans `m32BrowserLab.tsx`). Il lit la valeur `book` de l'atelier React et suit donc toutes les transitions inventées en RAM : créer, corriger avec une nouvelle version, ajouter une nouvelle correction, retirer sans effacer l'historique.

Par défaut, le composant de comparaison **n'est pas monté** : un bouton natif `aria-expanded=false`, hors formulaire, ouvre et referme explicitement le comparateur. Aucune donnée de l'application réelle n'y transite et aucun nouveau menu n'est monté dans `App.tsx`. Une paire sélectionnée reste une comparaison explicitement choisie, pas un ordre chronologique déduit. Un changement d'Univers remonte un atelier vierge et réinitialise toutes les sélections ; les retraits conservent leur version historique. React échappe les faux scripts.

## Qualification attendue

- 3 nouveaux cas Vitest #88–90 : état initial sans comparaison, historique conservé malgré retrait, refus d'origine SQL usurpée.
- 6 nouveaux cas Chromium #71–76 dans **chacun** des deux modes normal et CSP strict : ouverture contrôlée, création/correction/comparaison, troisième correction vivante, retrait sans invention de contenu, changement d'Univers sans fuite et inertie de contenu de type script.
- Contrat handoff #92 : preuves terminales de PR #156, scope fermé, pas de montage App.tsx ni API persistante, documents et STOP inchangés.
- **Seuils prévisionnels, non observés :** 92 contrats, 90 tests événementiels, 76 interactions Chromium par mode, 132 Rust sans régression. Nouvelle CI au SHA exact de la nouvelle PR obligatoire.

## Référence historique revalidée

[PR #156](https://github.com/LaurentCOLL1/Fabulaxiom/pull/156) source `cb65a8c902146a7252e3682cf1f5f08f54e7f190`, [CI source #40059088846](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40059088846) **SUCCESS** ; fusion protégée `main=4de256f4666500e4fc9a9482e52c8116869a35ca`, [CI postmain #40059860336](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40059860336) **SUCCESS** indépendante. Chacune : 76 étapes Windows, 91 contrats, 87 tests fictifs, 70/70 Chromium dans les deux modes, 132 Rust sans échec. Les deux CI initiales en échec avant corrections demeurent des observations historiques.

## Barrières inchangées

M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; identité `PARTIAL_LOCAL_IDENTITY_ONLY` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Aucune SQLite originale v6/v7, backup, ACL, journaux/sidecars, marqueur M1.5, migration 007, IPC writer, M3.3, ComfyUI, release, Windows opérateur.

Le contrôle de fusion exige un nouveau SHA, les tests source-only terminalement vérifiés, le diff et reviews/threads, le ruleset `Protect main`, `expected_head_sha`, puis une CI postmain distincte. Consigner le résultat dans issue #38 sans réécrire les checkpoints anciens.
