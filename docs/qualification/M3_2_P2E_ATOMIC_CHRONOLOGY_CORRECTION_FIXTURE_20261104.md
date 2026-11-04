# État du 4 novembre 2026 — P2e SOURCE QUALIFIÉE ET FUSIONNÉE ; POSTMAIN EN ATTENTE

La description de candidature ci-dessous est un instantané historique et ne doit pas servir d'état de gate actuel. **PR #281 FUSIONNÉE sous Protect main ACTIVE strict bypass=[]** : HEAD source `4035537d8278b4a72b948cb4d9e3fe61e051efa1`, CI Windows source #41907264072 completed/SUCCESS au SHA exact, job #126845156051 : **311 Rust, 7 Greenfield, 68 inventaire, 183 continuité, six Vitest, Chromium 85/85 normal et CSP stricte, 19 blobs fictifs**, avec les trois nouveaux tests P2e réussis. Reviews=[] threads=[] ; squash protégé via `expected_head_sha` : nouveau **`main=e58b03c024c644a4eab9bbc40f3f3533ec0caab3`**. CI postmain indépendante **#41921522033 IN_PROGRESS/NOT QUALIFIED à ce checkpoint** ; la qualification de cette CI ne peut être déduite de la source.

Seule l'atomicité des **deux écritures sur connexion SQLite v7 RAM fictive préouverte** est démontrée. Ce succès ne prouve pas la garde atomique des handles natifs SQLite main/WAL/SHM, ni writer adversarial, ni autorisation des données opérateur. P2e conserve historique et SQL v7 brut, aucun runtime 007, Tauri IPC ni writer actif.

`PRODUCT_FIRST_PARALLEL_SAFETY` inchangée. **STOP** M3.2 IN_PROGRESS_NOT_ACCEPTED ; P4 réel/writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; glib Linux GTK3 0.18.5 #160 OPEN_NOT_REMEDIATED. Fixtures CI ≠ admission réelle.

---

## Checkpoint actualisé — #280 fusionnée, P2e rebasée, CI au nouveau SHA requise

#280 a été fusionnée sur `main=3f41b4312395db1d34817a2293f5c79a4b41d0be` sous Protect main strict bypass=[] après succès source #41904254955 (308 Rust/7 Greenfield/68 inventaire/183 continuité/6 Vitest/Chromium 85/85 normal+CSP/19 blobs fictifs). Sa postmain indépendante #41906430494 était encore EN COURS à ce checkpoint. P2e ne peut pas utiliser #41905562089 sur son ancien SHA comme preuve de la nouvelle tête : nouveau commit rebasé et CI Windows exacte requis. Trois tests P2e supplémentaires = 311 Rust attendus, NON QUALIFIÉS. P2e reste une fixture v7 RAM `#[cfg(test)]` et non un writer de production. Toutes les interdictions M3.2 de ce document restent actives.

---

# M3.2 — P2e atomic authored chronology correction (CANDIDAT NON QUALIFIÉ)

**2026-11-04 — test-only, fixture v7 RAM préouverte, dépendante de #280 documentaire.** Parent #279 P2d fusionné sous Protect main au `main=a561d2113092731be9e2f4714a1bbc23853cacba`, source CI exacte #41896850232 SUCCESS (308 Rust / 7 Greenfield / 68 inventory / 183 continuity / 6 Vitest / Chromium 85/85 normal+CSP / 19 fictional Git blobs). La CI postmain #41903211870 et celle de #280 doivent être **terminalement vérifiées avant toute fusion de P2e** ; ne pas réutiliser leur état en cours comme preuve.

## Problème produit et tranche bornée

P2c permet de révoquer une assertion d'ordre temporel ; P2d permet sa reformulation par une nouvelle relation active, mais ces deux commandes distinctes créent un état intermédiaire « relation révoquée sans correction » lors de la rédaction. P2e ajoute un **geste auteur unique et atomique** pour le scénario restreint du stage 4, sans toucher aux archives.

Dans `src-tauri/src/m32_p2_fixture_chronology_service.rs` (`#[cfg(test)]` seulement), `correct_precedence_atomically` vérifie l'overlay stage 4 présent, refuse les couches de correction ultérieures non modélisées, démarre `TransactionBehavior::Immediate`, insère la décision append-only `revoke` de la relation antérieure puis la nouvelle `world_time_precedence_restatements` et ne `commit` que si **les deux** passent les gardes SQLite déjà existantes. Le moindre échec déclenche le rollback complet, préservant l'assertion originale comme toujours active. On conserve raisons explicites et références à la révision historique, sans comparaison calendriers ni ordre total inféré.

Dans `src-tauri/src/m32_p2b_fixture_chronology_actor.rs` (`#[cfg(test)]`), une commande typée `CorrectPrecedence` et une réponse `ActorError::Domain` reprennent la file synchrone bornée et le worker propriétaire unique de P2b : pas de transaction distribuée, pas de nouvel opener ou IPC.

**Trois nouveaux tests Rust candidats** :
1. En RAM jetable, une correction atomique de A→B en B→A conserve l'original historique, écrit exactement une décision et une reformulation, et préserve la provenance `r2` avec `r3` comme tête narrative.
2. Un cycle inverse incohérent avec une troisième relation, un autre Univers ou une révision absente fait échouer la commande et laisse **zéro décision et zéro reformulation** (atomicité du rollback), avec `PRAGMA integrity_check=ok`.
3. L'acteur mono-propriétaire livre une seule commande atomique ; refus cyclique puis réussite, isolation d'univers, consultation d'historique, arrêt du worker et refus des clients après fermeture.

**Attendu, pas acquis avant CI** : 311 tests Rust (308 + 3), 7 Greenfield, 68 inventaire SQLite, 183 continuité, six Vitest, Chromium 85/85 en modes normal et CSP stricte, 19 blobs Git fictifs. Tous les tests doivent tourner dans la CI Windows au SHA de la nouvelle PR. Une CI héritée de #279 ou #280 ne peut pas remplacer la qualification.

## Interdictions et limites

Aucune modification à `src-tauri/sql/m3_1_world_time_v7_candidate.sql` ni à la migration runtime 007 ; aucun changement de l'ancienne contrainte UNIQUE ni du trigger v7, aucun accès à `App.tsx`, Tauri IPC, service réel d'écriture, profil Greenfield existant, données opérateur v6/v7, sauvegardes, journaux, Windows Hello natif, marqueur ou recovery. P2e ne prend pas en charge les successeurs, les révocations de reformulations ou les couches chronologiques futures. Pas d'authentification de handles natifs main/WAL/SHM ni d'exclusion d'écrivains adversariaux : preuves R4–R9 toujours absentes.

Stratégie **PRODUCT_FIRST_PARALLEL_SAFETY** inchangée : prévenir avant tout changement. **M3.2 IN_PROGRESS_NOT_ACCEPTED**, real P4/writer/R1–R9 **NOT_PROVEN**, G2B **NOT_ACCEPTED**, G2C **NOT_AUTHORIZED**, G3 **STOP_UNAVAILABLE**, historique **PENDING_EXTERNAL_ATTESTATION(21/3/2)**, prospective **NOT_STARTED**, D3b-4/5 STOP. Alerte glib 0.18.5 Linux GTK3 issue #160 **OPEN_NOT_REMEDIATED**.

Gates : re-fetch `main`, PR, reviews/threads, exact-head CI Windows, Protect main ACTIVE strict bypass=[], squash `expected_head_sha`, CI postmain indépendante et #38 append-only. **Fixture CI ≠ admission réelle**. Si une condition échoue, laisser la PR en DRAFT et conserver tous les STOP.
