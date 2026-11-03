**3 novembre — ADDENDUM TERMINAL PR #265** : source HEAD `75790e9922b416ba4ae2ad22bf33c55ee787b293` CI #41508917914 SUCCESS ; squash Protect main strict bypass=[] `main=d85ef94e4242e578b2f5d756f5cef6842e2ca378` ; postmain #41510862693 completed/SUCCESS 302/7/68/183, 85/85 Chromium normal + CSP stricte ; reviews=[] threads=[]. Le statut candidat ci-dessous est un état historique avant fusion ; writer/G3 STOP inchangés.

# M3.2 — P3d : révocation explicite et correction avec historique sur atelier fictif

**2 novembre 2026 — CANDIDAT NON QUALIFIÉ.** Parent PR #264 P3c fusionnée sous Protect main active strict bypass=[] : `main=2ff56d7bbee531990da5644f857517e88e924959`. Windows CI source #41363608420 et postmain #41364545825 completed/SUCCESS sur leurs SHA exacts (302 Rust, 7 Greenfield, 68 inventaire, 183 continuité, Chromium 85/85 normal et CSP stricte).

## Livrable isolé P3d

- `src/m32P3FictionalCommandContract.ts` : deux commandes fictives typées supplémentaires, `revoke_precedence` et `supersede_anchor`. Elles réutilisent les fonctions existantes de `m32FictionalManualChronology.ts` sans écrire un nouveau moteur, ni changer les commandes P3a/P3c. Le réducteur conserve l'immuabilité de l'état en cas de refus, le compteur d'actions, l'audit et la provenance d'une révision historique exacte.
- `src/M32P3FictionalCommandWorkshop.tsx` : formulaire de révocation d'une relation **actuellement en vigueur**, justification humaine obligatoire ; puis formulaire de correction d'une ancre courante. La prévisualisation `previewFictionalCorrection` refuse la correction tant qu'une relation active la concerne ; la révocation doit donc être explicitement demandée et motivée. Correction par nouvelle ancre, ancien état `superseded` conservé, source historique préservée si aucune nouvelle source saisie. Calendrier, précision et date sont des champs de fiction. Vues du temps du monde, ordre de narration et révélation restent séparées et la révélation reste `not_authored`.
- `src/m32P3dReversibleChronology.test.tsx` : 6 Vitest nouveaux. Vérifient la présence de formulaires distincts et des refus, la révocation sans destruction, l'obligation de motif, les mauvaises références et Univers, l'impossibilité de corriger un ancêtre lié sans révocation préalable, la conservation de la révision `fiction-r2`, l'audit, la non-mutation sur refus et le refus d'une deuxième révocation/correction.
- Préserver les **11 tests P3a**, les **3 tests P3c** et les **4 tests P3b** dans leurs modules historiques. Ne pas augmenter fictivement les comptes Rust/continuité. Aucun changement `App.tsx`, de Rust/Tauri, de `Cargo.lock`/`package-lock.json`, migrations, capabilities, sécurité opérateur, ouverture SQLite ou IPC writer.

## Qualification à acquérir

CI Windows exact SHA : 302 Rust, 7 Greenfield, 68 inventaire, 183 continuité attendus inchangés ; +6 Vitest, Chromium 85/85 normal et CSP stricte. Auditer diff, reviews, threads et strict Protect main bypass=[] ; uniquement sur SUCCESS au SHA exact : squash avec `expected_head_sha`, puis postmain indépendante SUCCESS. Un scénario navigateur fictif réussi **ne prouve pas** le writer ou l'admission G3.

**Stratégie : `PRODUCT_FIRST_PARALLEL_SAFETY` ACTIVE, réversible.** La sécurité R4 main/WAL/SHM, régions SHM >0, custody atomique et R5–R9 continue séparément. Prévenir l'utilisateur AVANT changement de stratégie. glib 0.18.5 Linux GTK3 / GHSA-wrw7-89jp-8q8g (Dependabot #1, issue #160) `OPEN_NOT_REMEDIATED`; ne pas masquer ni simuler de mise à jour compatible.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; writer/R1–R9 `NOT_PROVEN` ; G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucun SQLite v6/v7 opérateur, profil `%LOCALAPPDATA%\\com.fabulaxiom.greenfield.v1`, backups/journaux, migration 007 runtime, IPC writer, Hello natif, marqueur ou recovery. Issues #38/#160 append-only.
