## Qualification source et fusion protégée P3i — 8 novembre 2026

#321 **FUSIONNÉE** par squash sous Protect main. Parent #320 postmain Windows #42479695823 SUCCESS SHA exact. Source final `d9e5f817e0b1a855483ff8eaf6ed7e013589db35`, Windows #42489171134 **terminal SUCCESS exact SHA** : **332 Rust, 7 Greenfield, 69 inventaire SQLite, 183 continuité, 412 Vitest, 88/88 Chromium normal + 88/88 CSP stricte, 25 blobs Git fictifs exacts**. Source initiale `9510ddd93c6d9df1f17749d0601b67896a51ce83` Windows #42488950858 FAIL sécurisé (marqueur historique `R3` absent dans prompt court), corrigé sans désactiver ni affaiblir le test. Diff 18 chemins, reviews=[] threads=[], Protect main ACTIVE strict bypass=[], squash gardé `expected_head_sha`. Nouveau `main=34695c2d4aa8df46225212d4214b3169da508586`, postmain indépendant #42492553799 **EN COURS / À QUALIFIER** au checkpoint, #38 append-only #6723062267.

« CANDIDAT NON QUALIFIÉ » ci-dessous est une trace **historique pré-CI**, pas le statut actuel de la source fusionnée. P3i n'effectue que des comparaisons littérales de fiches **déclarées fictives** ; les différences sont des invitations à la revue humaine, sans assertion de canon autoritaire, d'identité SQL opérateur ou d'admission du writer. PRODUCT_FIRST_PARALLEL_SAFETY inchangée, prévenir AVANT réorientation ; tous les STOP de M3.2 et l'alerte glib #160 persistent.

---

# M3.2 P3i — revue fictive de cohérence des fiches entre deux romans

8 novembre 2026 — **CANDIDAT NON QUALIFIÉ**. Parent protégé `main=343aadc9800bd6fcaf6ab7250c01d2b6a39e602f` (#320), postmain Windows #42479695823 **SUCCESS exact SHA**. PRODUCT_FIRST_PARALLEL_SAFETY maintenue (prévenir AVANT toute réorientation).

## Valeur produit

La revue P3f existante montre les deux romans et leurs révisions historiques fictives, mais ne permettait pas de rapprocher les faits de personnages déclarés dans deux textes. P3i introduit dans ce **même** laboratoire navigateur isolé des assertions littérales inventées de fiches (entité + propriété + valeur) attachées à la révision historique déclarée de chaque roman. Seules les clés explicites identiques dans les **deux romans** sont comparées ; les valeurs différentes deviennent des **écarts à examiner**, les valeurs identiques des **accords déclarés**. Aucune date, vérité, version autoritaire, chronologie totale ni résolution n'est inférée. Une absence de fiches est affichée comme « cohérence non évaluée », jamais comme preuve de cohérence.

## Sécurité / tests

- `src/M32P3fTwoNovelFictionalReview.tsx` : type `P3iFictionalCanonClaim`, validation fermée univers/roman/scène/révision historique, duplications d'identifiants ou de faits, valeur malformée et limite de 64 assertions ; comparaison à lecture seule avec rendu JSX échappé. Rejette avant l'affichage des sources historiques si une fiche est invalide.
- `src/m32BrowserLab.tsx` : **quatre** faits strictement inventés pour un messager dans deux romans fictifs (un écart, un accord), exclusivement dans le scénario du premier monde.
- `src/m32P3fTwoNovelFictionalReview.test.tsx` : quatre Vitest (09–12), refus des provenances étrangères et HEAD courante, dupliqués et chaînes hostile, absence de fuite dans l'écran refusé. Les anciens tests de navigateur Chromium 88/88 normal+CSP doivent rester inchangés, car aucun nouveau script/IPC n'est ajouté.

**ATTENDUS, NON PASS avant CI finale** : 332 Rust, 7 Greenfield, 69 inventaire, 183 continuité, 412 Vitest, Chromium 88/88 normal+CSP et 25 blobs Git fictifs exacts (liste inchangée, les deux fichiers UI sont déjà autorisés). Aucun App.tsx, base opérateur, IPC, dépendance, workflow, ouverture SQLite ou composant de production.

## STOP

M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45% estimation), writer/R1–R9 `NOT_PROVEN`, P4 réel STOP, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, custody atomique main/WAL/SHM et ABA invisible `NOT_PROVEN`. Alerte glib #160 `OPEN_NOT_REMEDIATED`. Ne pas toucher aux bases opérateur v6/v7, profil Greenfield existant, sauvegardes/journaux, IPC writer, runtime 007, Windows Hello natif, marqueur/recovery. CI fixtures ≠ admission réelle.

Pour fusion : source Windows HEAD exact + postmain parent SUCCESS, diff/reviews/threads, Protect main ACTIVE strict bypass=[], squash `expected_head_sha`, postmain indépendant, issue #38 append-only.
