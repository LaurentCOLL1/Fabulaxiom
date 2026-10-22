# Fabulaxiom M3.2 — Reprise opérationnelle courte

**22 octobre 2026 — PR #134 fusionnée sous Protect main :** source `f0db9b28d0e8492f3bc64c952b722873ae61311e`, [CI source #39837909918](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39837909918) terminale SUCCESS (75 étapes Windows, 69 contrats continuité, 132 Rust, 53/53 Chromium normal et CSP). Fusion `main=a1185b8345999f10814fd54dab96890f70236a5c`, [CI post-main #39839580270](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39839580270) terminale SUCCESS au SHA exact (75 étapes). PR #133 post-main [#39837202639](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39837202639) SUCCESS confirmé **ultérieurement** ; conserver son instantané daté `IN_PROGRESS_AT_CHECKPOINT` séparé de cette observation terminale.

**Décision G2-B → G3 source-only :** [M3_2_G2B_G3_EVIDENCE_DECISION_AFTER_FILEID.md](../qualification/M3_2_G2B_G3_EVIDENCE_DECISION_AFTER_FILEID.md) évalue la sauvegarde SQLite transactionnelle via une connexion propriétaire déjà ouverte et authentifiée, et la copie froide uniquement après preuve indépendante de quiescence et état WAL/journaux. Aucune de ces voies n'est démontrée sur les originaux ; ne jamais ouvrir une nouvelle connexion vers les originaux pour « essayer ». Les 4 contrôles G2B anonymisés sont seulement déclarés par l'opérateur, non attestés indépendamment.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B global `NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 DRAFT. Aucune original SQLite v6/v7, backup, ACL, sidecar, marker, commande Windows opérateur, migration 007, writer IPC, M3.3, ComfyUI, release. Paralléliser uniquement lectures indépendantes ; sérialiser écritures et fusions.


**22 octobre 2026 — PR #133 protégée MERGED :** source corrigée `d2bf3134054c4f1a05432c51055134fec7b4a0b2`, [CI Windows source #39835840939](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39835840939) terminale SUCCESS (8 contre-exemples Win32 fictifs, 68 contrats handoff, 132 Rust, Chromium 53/53 normal et CSP). Premier essai [#39835364262](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39835364262) FAILURE conservé : handle `FILE_READ_ATTRIBUTES / FILE_SHARE_READ` n'interdit pas le nouveau `GENERIC_WRITE` sur fichier fictif ; assertion négative corrigée. Fusion `main=604817c8457aaf7136f587aaaff28ff862e2702a`, [CI post-main #39837202639](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39837202639) `IN_PROGRESS_AT_CHECKPOINT` lors de cette normalisation ; re-fetch terminal indépendant requis, sans modifier rétroactivement cet instantané.

**G2B local — preuves opérateur limitées :** quatre sorties anonymisées fournies par le propriétaire (discovery, marqueur M1.5, métadonnées NTFS, FileIdInfo). Les résultats sont des observations non attestées indépendamment, sans version SQL ni démonstration de quiescence. Les tests CI sont uniquement sur octets fictifs temporaires non-SQLite ; ils montrent qu'un FileId stable ne prouve PAS l'absence d'écrivain. Les chemins, identifiants et contenus privés n'ont pas été publiés.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B global `NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2C et G2B–G6 `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 DRAFT ; pas de SQLite protégée v6/v7, sauvegardes, ACL, sidecars, marqueurs, commandes Windows opérateur, migration 007, writer IPC, M3.3, ComfyUI ou release. Paralléliser lectures indépendantes ; sérialiser écritures et fusions.


**Résultat contradictoire réel de CI fictive PR #133 :** [CI #39835364262](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39835364262) a échoué sur la **supposition** que `FILE_READ_ATTRIBUTES / FILE_SHARE_READ` bloquait un nouveau `GENERIC_WRITE`. L'ouverture concurrente a au contraire **réussi** sur le fichier temporaire Windows. Le test 08 est corrigé pour affirmer le comportement réellement observé (sans rendre possible l'accès aux originaux). La CI précédente est invalidée, nouvelle qualification au SHA corrigé obligatoire ; writer réel `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`.


**22 octobre 2026 — G2B_WIN32_FILEID owner-reported observations, strict partial scope:** [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6347844772) recorded four sanitised local G2-B checks: one restored candidate + activation marker, matching marker target, no observed SQLite sidecar, fixed NTFS stable sampled metadata, FileIdInfo stable across two `FILE_READ_ATTRIBUTES / FILE_SHARE_READ|WRITE|DELETE` openings on three files with ancestor handles. **Owner reported, NOT independent; schemas NOT SQL verified; writer absence NOT_PROVEN, G2B globally NOT_ACCEPTED, G2C NOT_AUTHORIZED, real G3 STOP_UNAVAILABLE.** No private paths/IDs/hashes published.

**New source-only Windows CI candidate:** [M3.2 G2-B fictional FileId/writer counterexample](../qualification/M3_2_G2B_WIN32_FILEID_WRITER_COUNTEREXAMPLE.md) exercises 8 tests (4 plain refusal checks + 4 ephemeral non-SQLite Win32 scratch fixtures on GitHub Actions only). Demonstrates a retained, locally stable FileId can coexist with a new writer and changed bytes when the metadata handle uses `SHARE_ALL`. Fresh exact-HEAD CI REQUIRED; do not borrow prior CI. This experiment is not an operator tool and never sees a protected database.

**Protected PR #132 now MERGED:** source `0ccc9af60075e90942d6e0bd7e2f92694bbe4876`, source [CI #39776896152](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39776896152) SUCCESS (74 Windows, 66 handoff, 132 Rust, Chromium 53/53 twice); `main=202152a3e502b08e6b7b77344769b6b0a1ea76bf`, post-main [CI #39778720560](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39778720560) SUCCESS at exact SHA. Historical PR #131 post-main `IN_PROGRESS_AT_CHECKPOINT` preserved independently from its later verified SUCCESS (run #39776433056).

**STOP ABSOLU :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence writer `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 DRAFT ; pas de SQLite v6/v7 originale, sidecar, ACL, backup, activation marker, commandes Windows opérateur, migration 007, IPC writer, M3.3, ComfyUI, release. Les lectures indépendantes peuvent être parallélisées, écriture/fusion séquentielles.


**22 octobre 2026 — PR #131 fusionnée sous Protect main :** source exacte `6b1973e077e90885d326cb5acbb2358368523bd2`, [CI #39770785693](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39770785693) terminale SUCCESS (74 étapes Windows, 132 Rust, 65 contrats de continuité, 53/53 Chromium normal et strict CSP). Premier échec [#39770570255](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39770570255) corrigé à la source sans altérer les preuves historiques. Fusion protégée `main=37d8aa100e9d6fe61bbe6650f554a147661e703e`; [CI post-main #39776433056](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39776433056) `IN_PROGRESS_AT_CHECKPOINT` lors de cette rédaction, résultat terminal à contrôler ultérieurement indépendamment. L'ascendance des corrections n'est affichée que sur le navigateur fictif, hors `App.tsx` et sans ordre chronologique global inféré.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence d'écrivain réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucun Windows opérateur, SQLite v6/v7 originale, sauvegarde, ACL/sidecar/marqueur, migration 007, writer IPC, M3.3, ComfyUI ni release. Travaux indépendants en parallèle ; mutations Git et fusions séquentielles.


**22 octobre 2026 — PR #130 fusionnée sous Protect main :** HEAD source `f980e8e294f537f6b588ded56f6f79cc772558d6`, [CI PR #39764830760](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39764830760) terminale SUCCESS (74 étapes Windows, 132 Rust, 63 handoff, Chromium 53/53 normal et CSP). Fusion protégée `main=8f330a4feff30092847e5bf180160efed174ebdd`, [CI post-main #39769613787](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39769613787) **IN_PROGRESS_AT_CHECKPOINT lors de la rédaction** ; re-fetch terminal indépendant requis. Aucun code runtime ajouté par cette fusion.

**Tranche suivante candidate, strictement fictive :** rendre lisible le prédécesseur explicite de chaque correction dans `M32FictionalCorrectionHistory`, en conservant l'ancienne assertion `avant/après`, les tests Vitest (8) et Chromium (53 par mode) existants renforcés. **Nouvelle CI au SHA exact obligatoire ; pas encore qualifiée.** Aucune inférence d'ordre global ; jamais dans `App.tsx`, sans SQLite, IPC, stockage, réseau ou écriture.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucune intervention Windows opérateur, original SQLite v6/v7, sauvegarde, ACL/sidecar/marker, migration 007, IPC writer, M3.3, ComfyUI ou release. Lectures et tests indépendants parallélisables ; commits/fusions séquentiels.


**22 octobre 2026 — PR #129 fusionnée sous Protect main :** source `f19d59d2ddf20e502d621555b204935b93ad566f`, [CI source #39756548081](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39756548081) `completed/SUCCESS` (74 étapes Windows). Fusion protégée `main=8f4b84bdccf19842aa98b35defe8e84a02e769db` ; [CI post-main #39758153975](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39758153975) `completed/SUCCESS` (74 étapes Windows) au SHA exact. Cette normalisation documentaire de PR #128 ne constitue ni une preuve opérateur ni une autorisation runtime. Les instantanés historiques `IN_PROGRESS_AT_CHECKPOINT` des PR #127/#128 restent intacts ; leurs observations terminales sont distinctes.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucun Windows opérateur, original SQLite v6/v7 ou backup, ACL/sidecar/marker, migration 007, IPC writer, M3.3, ComfyUI ni release. Paralléliser lectures indépendantes ; sérialiser écritures/fusions.


**22 octobre 2026 — PR #128 fusionnée sous Protect main :** HEAD source `ab5d7ed9cc0d9aafe4803d2b5b40d7b9bd23cabd`, [CI #39751125802](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39751125802) terminale SUCCESS (74 Windows, 132 Rust, 61 contrats, Chromium 53/53 normal et strict CSP). Fusion protégée `main=593b39e531e2a93e2f334220f37f6d8ed9bf9c93`; CI post-main [#39755042137](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39755042137) **IN_PROGRESS_AT_CHECKPOINT au checkpoint**, re-fetch terminal requis. PR #127 source-only React historique fictif reste hors `App.tsx`, sans IPC ni SQLite réelle ; la normalisation historique de PR #126 conserve son statut daté et immuable.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence d'écrivain réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 DRAFT. Aucune intervention Windows, SQLite originale v6/v7, sauvegardes, ACL/sidecars/marker, migration 007, writer IPC, M3.3, ComfyUI ni release. Garder les tâches indépendantes en parallèle et sérialiser commits/fusions.


**22 octobre 2026 — PR #127 MERGED sous Protect main :** source `d71288e5f7a046c6e90131118de5cecd8a6ee5cb`, CI [#39749304955](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39749304955) terminale SUCCESS (74 étapes Windows, 132 Rust, 60 contrats, 53/53 Chromium normal et CSP, 11 Git blobs fictifs). Fusion protégée `main=dd578161f1c84554c03434d0f1066f65d6e53dc6`, CI post-main [#39750459759](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39750459759) **IN_PROGRESS_AT_CHECKPOINT au checkpoint**, re-fetch terminal requis. Le panneau React d'historique de corrections n'est monté que dans le laboratoire navigateur fictif et n'autorise aucune saisie produit ou IPC.

**STOP maintenu :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. PR #35 historique OPEN/DRAFT. Aucune commande Windows opérateur, SQLite originale v6/v7 ou backup, ACL/sidecars/marker, migration 007, writer IPC, M3.3, ComfyUI ni release. Règle permanente : paralléliser uniquement les tâches indépendantes et sérialiser écritures/merges.


**22 octobre 2026 — PR #126 MERGED :** source `0a5f972472eec1e53cd2621ca1fb3d6955e5f18f`, CI source [#39727486056](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39727486056) **SUCCESS** terminale (74 étapes, 132 tests Rust, 58 handoff, 50/50 Chromium normal et strict CSP). Fusion protégée `main=7c4ff2f84bb67b51c8ca01eef0f9ca78a1bfe8d9`; CI post-main [#39748359823](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39748359823) **IN_PROGRESS_AT_CHECKPOINT au checkpoint**, re-fetch terminal obligatoire. Nouvelle tranche React fictive candidate séparée : consultation de la filiation explicite des corrections avec 8 Vitest et 53 scénarios Chromium par mode, **non qualifiée** ; uniquement laboratoire navigateur en mémoire, hors `App.tsx`, sans Tauri, SQLite ni réseau.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 historique OPEN/DRAFT. Aucun Windows opérateur, base originale v6/v7, sauvegarde/sidecars/ACL/marker, migration 007, writer IPC, M3.3, ComfyUI ni release. Lectures indépendantes parallélisées, writes et merges sérialisés.


**22 octobre 2026 — PR #125 MERGED sous Protect main :** HEAD source `8ce7bb3ae2295662dfba8f4b5961f9394f1e771f`, CI [#39723734278](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39723734278) terminale **SUCCESS**, 74 étapes Windows, 132 Rust, 57 contrats de continuité, Chromium 50/50 normal et 50/50 CSP. Fusion protégée `main=4b14afbc7fe8de607429e795b656179724d7ee7f` avec `expected_head_sha` ; [CI post-main #39726331901](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39726331901) **SUCCESS terminale au SHA exact** (re-fetch terminal obligatoire). L'historique PR #124 est immuable et qualifié seulement en fixtures Rust / SQLite RAM.

**STOP unchanged :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucun opérateur Windows, aucune SQLite originale v6/v7 ou backup, ACL, journal/sidecar, activation marker, migration 007, writer IPC, M3.3, ComfyUI ni release. La règle permanente de parallélisation des travaux indépendants et sérialisation des mutations est maintenue.


**22 octobre 2026 — PR #124 MERGED sous Protect main :** source `1fdbe18b163dc8caa48bfde439a36b93b81c848a`, [CI #39721484412](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39721484412) terminale **SUCCESS** (74 étapes, 132 Rust, 56 contrats, Chromium 50/50 normal et 50/50 CSP). Fusion protégée `main=db09722076561d35dcc0fe3495e21cf0d0ceef9f`. [CI post-main #39723495236](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39723495236) **IN_PROGRESS_AT_CHECKPOINT au checkpoint**, résultat terminal à re-fetch. Septième tranche Rust historique : chaînes de corrections explicites append-only, SQL candidat et quatre tests adversariaux, seulement module `#[cfg(test)]`, SQLite fictive `Connection::open_in_memory()`. Aucun IPC, migration 007 ni écriture réelle.

**STOP maintenu :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence de writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 historique OPEN/DRAFT. Aucune commande Windows opérateur, SQLite originale v6/v7, sauvegardes/ACL/sidecars/marqueurs, migration 007, writer IPC, M3.3, ComfyUI ou release. Travaux indépendants parallélisables, mais commits concurrents et fusions sérialisés.


**22 octobre 2026 — PR #123 protégée MERGED :** source `f72f1dd51d50661af7dfab39f4059e7a25940472`, [CI #39719646691 tentative 2](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39719646691) terminale **SUCCESS** (74 étapes, 128 Rust, 54 contrats, Chromium 50/50 normal et CSP). Ancien essai Chromium WebSocket échoué conservé. Fusion `main=a3c4112b335bba69e3d5d4fa4673ae05f1a57241` ; [CI push #39720904972](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39720904972) **IN_PROGRESS_AT_CHECKPOINT au checkpoint**, re-fetch terminal indispensable.

**Nouvelle tranche source-only séparée candidate :** chaînes de correction explicitement révoquées, à partir du SQL historique `m3_2_recursive_chain_candidate.sql` et des fonctions `append_chain_correction`, `revoke_chain_correction`, `list_chain_history`. Quatre tests adversariaux Rust ajoutés. Module `#[cfg(test)]` uniquement, `Connection::open_in_memory()`, aucune migration 007 de production, aucun writer IPC. Cette tranche nécessite sa nouvelle CI au HEAD exact, elle ne fait pas accepter M3.2.

**STOP strict :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; absence de vrai writer `NOT_PROVEN` ; G2B–G6 `NOT_AUTHORIZED` ; vrai G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Aucune commande Windows opérateur, SQLite v6/v7 originale, backups, ACL/sidecars/marker, migration 007, Tauri writer, M3.3, ComfyUI ni release. Travaux indépendants en parallèle, intégrations et décisions de sécurité en série.


**22 octobre 2026 — PR #122 MERGED sous Protect main :** HEAD exact source `1ade25c7b8c500d712c452a08d90ed26a1ffbe89`, [CI #39717330885](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39717330885) **SUCCESS terminale**, 74 étapes Windows, 128 Rust, 53 contrôles de continuité. Fusion protégée `main=52b06099ba0cff0da15fa697b0e2043afc883a00`, CI post-main [#39718851557](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39718851557) **SUCCESS terminale au SHA exact**, à re-fetch au SHA exact. Sixième tranche: révocation immuable du seul successeur (SQL candidat, `revoke_successor`, `list_successor_history`), uniquement Rust `#[cfg(test)]` et SQLite fictive RAM, historique préservé. Aucune correction récursive.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence de writer SQLite réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. PR #35 OPEN/DRAFT ; aucune commande Windows opérateur, original SQLite v6/v7, backups/ACL/sidecars/marker, migration 007, writer IPC, M3.3, ComfyUI ni release. La règle permanente de parallélisation des lectures/analyses et sérialisation des écritures/fusions demeure.

**Prochain travail source-only possible :** après cette normalisation et CI HEAD exact, analyser et éventuellement développer **séparément** la correction récursive à partir de la PR #35 historique (`m3_2_recursive_chain_candidate.sql`) sur une nouvelle branche avec SQLite uniquement en RAM et tests adversariaux ; jamais de promotion des gates réels.


**22 octobre 2026 — PR #121 MERGED sous Protect main :** HEAD source `6a1a22dedaa4e3d2c302a56959083017578dc7da`, CI PR [#39713440057](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39713440057) **SUCCESS terminale** (74 étapes Windows, 125 tests Rust). Fusion protégée `main=08caad24e20eae484e94fd084edb487b5c370bd5`; CI post-fusion [#39716352685](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39716352685) **SUCCESS au SHA exact**.

**Tranche suivante candidate, non qualifiée :** sixième importation Rust limitée à une révocation terminale immuable d'un successeur fictif : `m3_2_successor_revocations_candidate.sql`, `revoke_successor`, `list_successor_history`, 3 nouveaux tests adversariaux. Module `#[cfg(test)]` et SQLite exclusivement `Connection::open_in_memory()`. Ne pas confondre cette tranche avec les chaînes récursives de PR #35 ; aucune migration de production ou commande Tauri.

**STOP non levé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; absence d'écrivain SQLite réel `NOT_PROVEN` ; G2B–G6 `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED`. Pas de commande Windows sans approbation distincte, aucune SQLite réelle v6/v7, sauvegarde, ACL, sidecar, marqueur, migration 007, writer IPC, M3.3, ComfyUI ou release. Travailler en parallèle uniquement sur les sources et analyses indépendantes ; intégrations et fusions séquentielles avec re-fetch/CI au HEAD exact.


**22 octobre 2026 — PR #120 fusionnée :** source HEAD `f7ef3ceeaee40bb90e1cb9fe180121f11867fc28`, [CI PR #39685054113](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39685054113) **SUCCESS terminale** (74 étapes Windows), fusion protégée `main=01766707a347a269b283c2aa7ea02f44979759e9`, [CI post-fusion #39686405108](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39686405108) **SUCCESS terminale au SHA exact**. Le cinquième module Rust de chronologie reste strictement `#[cfg(test)]`, utilise SQLite RAM et démontre un **successeur humain unique** après retrait d'une reformulation, avec graphe actif en ordre partiel. Aucun code de production/IPC n'est activé.

**Aucune promotion des gates :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT non fusionnable, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, attestations historiques `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, baseline prospective `NOT_STARTED`. Aucun accès opérateur Windows, SQLite v6/v7 originale, backup, ACL, WAL/SHM, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release. Parallélisation autorisée pour lectures et travaux indépendants, mais commits sur même branche et merges séquentiels avec CI SHA exact.

**Prochain développement permis en source-only :** étudier une tranche **séparée** de révocation d'un successeur fictif (`m3_2_successor_revocations_candidate.sql`) avec conservation immuable de l'historique et refus des cycles, puis seulement plus tard les chaînes récursives dans un dossier distinct. Chaque incrément exige fixture SQLite RAM, branche propre, tests adversariaux et CI au HEAD exact. Les recherches sur les preuves historiques #36 et la baseline prospective #38 peuvent avancer en parallèle, sans inventer de preuves ni utiliser les fichiers Windows protégés.


**22 octobre 2026 — PR #119 MERGED sous Protect main :** source `0df96696e4abefe692f8a0fdca3ab10e726fa9d3`, CI PR #39661776335 SUCCESS (74 étapes, 121 tests Rust, 48 tests continuité, 21 inventaires SQLite, 50 Chromium par mode). Nouveau `main=61e07deaf10fc393c567e8f1960874b75d81adc4`, CI post-fusion #39684342539 **IN_PROGRESS_AT_CHECKPOINT** ; revérifier le résultat terminal au SHA exact.

**Cinquième tranche test-only candidate :** un successeur humain unique d'une reformulation retirée, `succeed_withdrawn_restatement`, lecture du graphe actif partiel par `list_active_precedence_graph` et SQL candidat `m3_2_restatement_successors_candidate.sql` sur SQLite exclusivement en RAM. Quatre nouveaux tests Rust : retrait obligatoire, unicité, cycles/doublons, ancres retirées et historique immuable. Aucune correction en chaîne, aucune révocation de successeur, aucune inférence de chronologie totale.

**STOP non levé :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 OPEN/DRAFT, écrivain SQLite réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Pas de Windows opérateur, SQLite originale v6/v7, backups, ACL, sidecars, marker, migration 007, writer IPC, M3.3, ComfyUI ou release.


**21/10/2026 — CI #39661237200 première tentative PR #119 : FAIL source-only handoff historique (3 assertions).** Les tests #36/#37/#39 consultaient le champ `main_ci_post_merge` vivant au lieu des snapshots historiques #112/#113/#114 ; correction ciblée vers `x["main_ci"]`, sans modifier les statuts réels, les comptes d'ouvertures SQLite ou les politiques STOP. Aucun test Rust de la nouvelle tranche n'a encore été qualifié sur ce HEAD. Nouvelle CI complète obligatoire.


**21 octobre 2026 — PR #118 MERGED :** source `ff996fc27da6df12697d68a46b8580a3a33e30b3`, CI #39658544037 SUCCESS (74 étapes, 117 Rust, 46 contrats, 21 inventaires SQLite, 50 Chromium par mode), fusion protégée `main=a0942b9566d6de21cf73e55dce47c3797dcb7c81`. CI push #39660168071 **IN_PROGRESS_AT_CHECKPOINT** : ne pas prétendre sa réussite terminale sans re-fetch exact. Nouvelle tranche test-only, uniquement SQLite RAM : révocation immuable de reformulation, historique conservé, 4 tests Rust supplémentaires ; aucune écriture active supplémentaire déduite.

**STOP toujours effectif :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 OPEN/DRAFT, réel writer NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique 21/3/2 PENDING_EXTERNAL_ATTESTATION, prospective NOT_STARTED. Pas de Windows opérateur, original SQLite v6/v7, backup, ACL, journal, marker, migration 007, IPC writer, M3.3 ni release.


**21 octobre 2026 — PR #117 fusionnée et CI post-fusion exacte confirmée :** source `99d78a46e61a0765b6673353900cea55eb039e74`, CI #39653506345 **SUCCESS** (74 étapes, 112 tests Rust, 44 tests de continuité, 21 tests d'inventaire, 50 Chromium par mode). Fusion protégée `main=b76e6c00c579bee36c194872e3679c48fe9788fa` ; CI post-merge #39655214998 **SUCCESS terminale** sur ce SHA. La règle permanente de parallélisation des tâches indépendantes est toujours en vigueur.

**Troisième tranche test-only candidate :** reprise strictement limitée de la reformulation humaine explicite d'une précédence révoquée (`restate_revoked_precedence`) et du SQL candidat `m3_2_active_precedence_candidate.sql` sur SQLite **uniquement en mémoire**. Cinq tests Rust supplémentaires prévus : source révoquée obligatoire, interdiction de cycle, unicité, conservation immuable et blocage d'ancres retirées / insertion brute abusive. Le module reste `#[cfg(test)]`, sans exposition Tauri, migration 007 ni donnée locale opérateur. Révocation des reformulations, successeurs et corrections en chaîne sont hors portée. CI nouvelle au HEAD exact requise.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT/non fusionnable ; absence d'écrivain SQLite réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, provenance `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucune commande Windows opérateur, base v6 active/v7 isolée, sidecars, ACL, sauvegardes, activation marker, IPC writer, M3.3, ComfyUI ou release.


**21 octobre 2026 — PR #116 fusionnée et CI post-fusion vérifiée :** HEAD source `0b2555833c1a2c0152cba2185c8122f3d3ecbbae`, CI PR #39626827246 **SUCCESS** (74 étapes Windows ; 106 Rust dont 6 nouveaux tests RAM, 42 contrats de continuité, 21 inventaires SQLite, 50 Chromium par mode). Fusion protégée `main=388cb745888f9f2d4d0a07fce1ed19fad9b4a548`, CI post-merge #39628479487 **SUCCESS terminale au SHA exact**. PR #35 reste DRAFT/non fusionnable. Règle permanente de parallélisation inchangée.

**Deuxième tranche source-only candidate :** reprise bornée de `decide_anchor`, `decide_precedence`, `supersede_anchor_atomically`, `list_current_anchor_ids`, `list_current_precedence_ids`, `list_anchor_decisions` et de `m3_2_chronology_decisions_candidate.sql` historique. Module Rust `#[cfg(test)]` uniquement, SQL candidat chargé **après v6 et v7 fictifs en mémoire** ; six nouveaux tests Rust prévus pour révocation, conservation de l'historique, rollback transactionnel, Univers distincts, cycles/contraintes. Aucune migration 007, aucun IPC ni base réelle ; CI au HEAD candidat obligatoire. Les restatements et chaînes de corrections restent hors portée.

**STOP maintenu :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; `PROCESS_WRITER_ABSENCE=NOT_PROVEN`; G2-B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, baseline prospective `NOT_STARTED`. Aucune action opérateur Windows, SQLite active v6, isolée v7, sauvegarde, ACL, sidecar, marqueur, migration 007, writer IPC, M3.3, ComfyUI ou release.


**Correction CI du 21/10/2026 :** la CI #39626066048 a refusé une assertion Python dont le saut de ligne entre `#[cfg(test)]` et `mod m32_manual_chronology;` était mal échappé. Deux tests ont été corrigés avec `chr(10)` ; les sources Rust, les compteurs d'ouverture SQLite et les interdictions restent identiques. Nouvelle CI au nouveau HEAD obligatoire.


**21 octobre 2026 — correction de qualification PR #116 :** la première CI #39625498131 a délibérément **échoué** au contrôle d'inventaire textuel des occurrences Rust SQLite après ajout du module `#[cfg(test)]`. Comptage exact observé dans le nouveau fichier : `Connection::open_in_memory` **1**, `run_migrations` **1**, et **0** occurrence pour `Connection::open` disque, ouverture applicative, ATTACH, VACUUM, flags ouverts ou API backup brute. Après revue limitée à ces textes publics, l'inventaire attendu ajoute explicitement `(1,0,1,0,0,0,0)` pour `src-tauri/src/m32_manual_chronology.rs`, conserve toutes les entrées existantes et ajoute trois tests adversariaux (21 au lieu de 18). Toute autre occurrence, y compris dans ce module, reste un **STOP**. Cette qualification ne prouve pas l'absence de writer réel ni la sécurité des fichiers opérateur ; une nouvelle CI complète au nouveau HEAD est obligatoire.


**21 octobre 2026 — PR #115 fusionnée :** HEAD source `3f1c5676f7035398b61bc143a16eae5e115cdfbe`, CI PR #39619267259 **SUCCESS** (74 étapes, 40 tests de continuité, 60 Vitest fictifs, 50 Chromium par mode, 100 tests Rust au commit source). Fusion protégée `main=33846c8c6813acda5eda5089827f81df99175d2c` ; CI post-fusion #39620942276 **SUCCESS terminale au SHA exact**. La règle de parallélisation reste active. La PR #35 demeure OPEN/DRAFT non fusionnable ; le portage décrit ci-dessous est indépendant, strictement test-only, et ne constitue aucune autorisation de fusion de #35.

**Nouvelle tranche candidate source-only :** portage limité des opérations `create_calendar`, `create_anchor`, `create_precedence`, `list_anchors`, `list_precedences` du Rust historique de PR #35 vers un module `#[cfg(test)]` sur `main`, avec six tests utilisant exclusivement des bases SQLite **en mémoire**, les deux Univers fictifs, quatre temporalités, ordre humain explicite, cycles interdits et révisions immuables. **Aucun IPC**, pas d'activation du schéma v7 réel ou de migration 007, aucune ouverture des fichiers opérateur. Une nouvelle CI SHA exact doit encore qualifier cette tranche ; les fonctions de supersession de PR #35 ne sont pas portées dans cette étape.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, réel writer `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, historique 21/3/2 non résolu, baseline prospective `NOT_STARTED`, aucune opération Windows opérateur ni production v6, v7 isolée, backups, ACL, journaux, activation marker, migration 007, writer IPC, M3.3 ou release.


**21 octobre 2026 — PR #114 fusionnée et CI post-fusion vérifiée :** la [PR #114](https://github.com/LaurentCOLL1/Fabulaxiom/pull/114), source `8262659d58045c127fe4ee3ac56e6dd5681a9f5f` et [CI PR #39612803528](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39612803528) **SUCCESS (job Windows 74 étapes)**, a été fusionnée sous protection à `main=ddb23311f40f09c04983b164ccd7afa361698ea8`. La [CI main #39614175650](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39614175650) est **SUCCESS terminale** au SHA de fusion exact. La règle permanente de parallélisation des tâches indépendantes figure dans `HANDOFF_PROTOCOL.md` sur `main`, sans autoriser les opérations Windows privées.

**Décision inchangée :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; PR #35 OPEN/DRAFT, GitHub `mergeable=false` au HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` et prospective `NOT_STARTED` ; absence d'écrivain réel `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`. Aucune migration 007, writer IPC, M3.3, release ni opération sur production v6/isolée v7, sauvegardes, ACL, sidecars, marqueurs ou Windows opérateur.

**Voies parallèles sûres à poursuivre :** A : réconciliation *source-only* de la PR #35, sur branche nouvelle et fixtures inventées ; B : étude documentaire des cinq témoins historiques (issue #36), sans falsifier la provenance ; C : examen du protocole de baseline prospective et du propriétaire SQLite non migrant (issue #38), sans lecture de sources privées. Ces études peuvent avancer en parallèle ; commits concurrents vers la même branche et merges restent séquentiels, avec re-fetch et CI exacte. [Plan borné de réconciliation](../qualification/M3_2_PR35_SAFE_RECONCILIATION_PLAN.md).


**Checkpoint GitHub confirmé le 21 octobre 2026 :** PR [#113](https://github.com/LaurentCOLL1/Fabulaxiom/pull/113) **MERGED** sous Protect main, HEAD source `6fd369de970e6e35d42c2162f197eb57009a1d42`, [CI exacte #39605681206](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39605681206) **SUCCESS** (74 étapes Windows, 60 Vitest atelier fictif, 50 Chromium par mode), `main=e74f1001c01eff1f37c8b35d97d4ef34f6fbccb3` et [CI post-fusion #39607280677](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39607280677) **SUCCESS terminale au SHA exact**. PR #35 reste OPEN/DRAFT, GitHub `mergeable=false` ; source réelle G2B–G6 non autorisée, absence d'écrivain SQLite réel `NOT_PROVEN`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`. Aucun geste opérateur local réalisé.

**Règle permanente de parallélisation :** dès que des tâches sont indépendantes, privilégier leur exécution simultanée (re-fetch/lecture GitHub, analyses de roadmap, recherches de preuves, tests sur fixtures isolées), avec périmètres et branches séparés. Sérialiser toute modification d'un même fichier/ref Git, les fusions, la qualification d'une CI par SHA exact et les décisions de sécurité. Aucun parallélisme ne permet de contourner un gate, un STOP ou une autorisation Windows. Voir [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md).


**21 octobre 2026 — résultat terminal post-fusion PR #112 :** la CI push [#39597532619](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39597532619) a terminé **SUCCESS** sur `main=3c489aa727129e4b090e2e80a49a93fb3fa95877`, SHA exact du merge #112. Les mentions plus anciennes « en cours au checkpoint » sont des photographies historiques, et ne décrivent pas l'état terminal. Cette mise à jour de la PR #113 impose une CI nouvelle sur son nouveau HEAD. M3.2 reste IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT, writer réel NOT_PROVEN, G2B–G6 STOP, aucun essai Windows opérateur ni SQLite protégée.


**21 octobre 2026 — PR #112 fusionnée avec CI source exacte :** [PR #112](https://github.com/LaurentCOLL1/Fabulaxiom/pull/112) MERGED sous Protect main au SHA `3c489aa727129e4b090e2e80a49a93fb3fa95877` ; HEAD source `56c5d4d55a616469cda36c5fef7f63369a08bdb2`, [CI #39596187154](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39596187154) terminale **SUCCESS** au HEAD exact (74 étapes Windows, 60 Vitest d'atelier fictif, 50 Chromium par mode normal et CSP stricte). [CI push `main` #39597532619](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39597532619) **EN COURS AU CHECKPOINT** au SHA de fusion ; revérification terminale requise. Cette fonctionnalité fictive relie deux révisions immuables explicitement choisies à une chaîne de précédences humaines actives sans faire dépendre le temps du monde de l'ordre narratif.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT, G2-A metadata-only (accord ponctuel consommé), écrivain SQLite réel `NOT_PROVEN`, G2-B à G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`. Aucun Windows opérateur, base réelle v6/v7, sauvegarde, ACL, WAL/SHM, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release.


**Candidat de preuves du monde par révisions exactes — 21/10/2026 :** le laboratoire fictif permet de sélectionner deux scènes et leurs révisions immuables pour lire une chaîne de précédences **humaines actives** entre leurs ancres, lorsque chacune possède exactement une ancre courante. Dates, ordre narratif entre romans et révélations ne sont pas déduits. Historique/révisions étrangères/ambiguïté : refus ou indétermination. 60 Vitest et 50 Chromium par mode **à qualifier sur une nouvelle CI**. Aucune intégration `App.tsx`/Tauri/SQLite.

**STOP :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT, G2-A accord consommé, écrivain réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE. Aucun Windows opérateur, original SQLite v6/v7, sauvegarde/ACL/journal, migration 007, IPC writer, M3.3 ou release.


**Vérification terminale post-fusion #110 (21 octobre 2026) :** [CI `main` #39591429432](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39591429432) **SUCCESS terminale** sur le SHA exact `2bf4b6a62ca22a21e1e7d34f5ead4e86dafe450b` ; PR #110 MERGED. Les anciennes mentions « en cours » documentent uniquement un instantané antérieur. Cette normalisation dans la PR #111 nécessite sa **propre CI fraîche au HEAD modifié** ; les deux CI de #110 ne sont pas transférables. **M3.2 toujours IN_PROGRESS_NOT_ACCEPTED**, PR #35 DRAFT ; G2-A métadonnées avec accord consommé, absence d'écrivain réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE ; aucune commande Windows opérateur, originale SQLite, migration 007, IPC writer, M3.3 ni release.


## 21 octobre 2026 — PR #110 fusionnée : effet hypothétique de révocation (atelier fictif)

**Checkpoint GitHub confirmé le 21 octobre 2026 :** PR [#110](https://github.com/LaurentCOLL1/Fabulaxiom/pull/110) **MERGED** sous Protect main sur `main=2bf4b6a62ca22a21e1e7d34f5ead4e86dafe450b` ; source `f69e36a24aedda15222bb3a4e3a198ba57d0174a`, CI PR [#39577527093](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39577527093) **SUCCESS terminale sur ce HEAD** (74 étapes Windows, 55 Vitest d'atelier fictif et 48 Chromium par mode normal / précompilé strict CSP). CI push [#39591429432](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39591429432) **EN COURS AU CHECKPOINT** sur le SHA du merge : re-fetch terminal obligatoire. Les anciennes mentions « candidat » sont historiques ; aucune CI d'ancien SHA transférable.

Le laboratoire en mémoire inventée affiche avant toute révocation si une autre chaîne humaine active conserve une preuve d'ordre. L'aperçu ne modifie aucun lien ; l'action réelle reste un choix humain séparé. La fonctionnalité **n'est pas intégrée au produit Windows** et ne constitue pas l'acceptation M3.2.

**Sécurité inchangée :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT ; G2-A PASS sur métadonnées seulement (accord unique consommé), absence d'écrivain SQLite réel `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`. Aucune commande Windows opérateur, aucun original v6/v7, sauvegarde, WAL/SHM, ACL, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release.

---


## 21 octobre 2026 — candidat M3.2 : conséquence d'une révocation humaine (fiction uniquement)

**CANDIDAT — CI du nouveau SHA encore requise.** L'atelier manuel fictif permet de choisir une relation `avant/après` existante et de **prévisualiser sans modification** si sa révocation supprimerait toute preuve d'ordre entre ses deux ancres, ou si une autre chaîne de précédences **humaines actives** subsisterait. Témoins affichés par identifiants exacts. La suppression effective reste un clic humain distinct. Pas de date inventée, ordre total, changement de roman, révélation au lecteur ou propagation de canon.

Cibles de qualification : **55 tests Vitest de l'atelier**, **48 scénarios Chromium dans chacun des modes standard et précompilé strict CSP**, CI à HEAD exact. Ce nouveau candidat ne peut pas réutiliser les tests verts de #108/#109. Exclusivement navigateur avec données inventées, pas de Tauri/App.tsx/SQLite opérateur.

**Gates STOP :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 OPEN/DRAFT, G2-A metadata-only ponctuel consommé, écrivain réel NOT_PROVEN, G2-B à G6 NOT_AUTHORIZED, vrai G3 STOP_UNAVAILABLE, M3.3/release non autorisées, aucune originale v6/v7, sauvegarde, ACL, journaux, migration 007 ou IPC writer.

---


## 21 octobre 2026 — CI post-fusion #108 maintenant terminale

GitHub re-vérifié : `main=ba4b8a599910cef6d1c76fa1e4fb561a0b45e631`, PR #108 MERGED. CI PR #39572172593 **SUCCESS** au source head `fd62c1afd4ad6eff9a6f9d2f18679ef0704f59c1` (51 Vitest atelier fictif, 46 Chromium par mode, 74 étapes Windows). CI [post-fusion #39573518324](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39573518324) **SUCCESS terminale** sur le SHA du merge. Les passages « en cours au checkpoint » restent historiques. Aucun de ces résultats n'est transférable à une nouvelle PR.

**M3.2 IN_PROGRESS_NOT_ACCEPTED**, PR #35 OPEN/DRAFT, G2A metadata-only ponctuel consommé, `PROCESS_WRITER_ABSENCE=NOT_PROVEN`, G2B–G6 NOT_AUTHORIZED, vrai G3 STOP. Aucune originale SQLite v6/v7, sauvegarde, ACL, WAL/SHM, marqueurs, migration 007, IPC writer, M3.3, ComfyUI, release ni commande Windows opérateur.

---


## 21 octobre 2026 — PR #108 fusionnée : sélections historiques explicites

Source GitHub vérifiée : PR [#108](https://github.com/LaurentCOLL1/Fabulaxiom/pull/108) MERGED sous Protect main au `main=ba4b8a599910cef6d1c76fa1e4fb561a0b45e631`. HEAD de PR `fd62c1afd4ad6eff9a6f9d2f18679ef0704f59c1`, CI PR [#39572172593](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39572172593) terminale SUCCESS : 74 étapes Windows, 51 tests Vitest de l'atelier et 46/46 Chromium dans chacun des deux modes. CI push main [#39573518324](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39573518324) **EN COURS au présent checkpoint**, ne pas convertir en succès sans re-fetch.

L'atelier navigateur **exclusivement fictif** indique quand une ancre choisie pour consulter une preuve est devenue historique après correction, conserve son ancienne identité en option désactivée, supprime la comparaison courante jusqu'à nouvelle sélection et réinitialise les choix entre Univers fictifs. Les anciens paragraphes « candidat » sont des instantanés historiques conservés. **M3.2 IN_PROGRESS_NOT_ACCEPTED**, PR #35 OPEN/DRAFT ; aucune preuve Windows opérateur ou intégration SQLite réelle.

**STOP inchangé :** G2-A metadata-only PASS avec accord ponctuel consommé, absence d'écrivain réel NOT_PROVEN, G2-B/C/D et G3–G6 NOT_AUTHORIZED, réel G3 STOP_UNAVAILABLE ; M3.3, migration 007, IPC writer, original v6/v7, sauvegardes, journaux, ACL, marqueurs, ComfyUI, release et commandes Windows opérateur non autorisés.

---


## 21 octobre 2026 — historique du candidat PR #108, désormais fusionné

Candidat **NON QUALIFIÉ** exclusivement dans l'atelier navigateur inventé : si une ancre choisie pour consulter une preuve temporelle est explicitement remplacée, l'ancien identifiant reste visible comme **historique, désactivé** dans le sélecteur, avec une explication. Aucune preuve d'ordre courant ne s'affiche pour une référence historique. Un nouvel identifiant courant peut être choisi ; le changement d'Univers fictif repart sans sélection étrangère.

Objectif d'acceptation au SHA **neuf** : trois Vitest additionnels (**51 atelier**) et deux scénarios Chromium (**46 par mode**). Ne pas recycler la CI des PR #106 ou #107. Pas de calendrier inféré, de révélation lecteur, de Tauri, d'App.tsx ou de persistance SQLite. **M3.2 IN_PROGRESS_NOT_ACCEPTED**, PR #35 DRAFT, G2-A metadata-only consommé, absence writer réel NOT_PROVEN ; G2B–G6 NOT_AUTHORIZED et G3 réel STOP_UNAVAILABLE. Aucun accès aux bases, sauvegardes, ACL, journaux, migration 007, IPC writer ou Windows opérateur.

---


## 21 octobre 2026 — qualification post-fusion #106 devenue terminale

GitHub revérifié : PR #106 MERGED sur `main=fbfc785afa6e5bdf92c337004d1bd2f925c4957a`. La CI PR #39566947725 a terminé **SUCCESS** au source head `4abcc5217be07cb65d089e55fa042ff757b9043e` (48 Vitest / 44 Chromium par mode). La CI push main [#39567933461](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39567933461) a maintenant terminé **SUCCESS**, sur le SHA exact du merge. Toutes les mentions plus anciennes « en cours au checkpoint » restent des instantanés historiques. Ce nouveau correctif documentaire nécessite **sa propre CI au nouveau HEAD**, jamais réutilisée.

**M3.2 IN_PROGRESS_NOT_ACCEPTED** ; PR #35 OPEN/DRAFT ; G2A metadata-only (accord consommé), écrivain SQLite réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE. Aucune originale v6/v7, WAL/SHM, sauvegarde, ACL, marqueur, migration007, IPC writer, M3.3, release ni exécution Windows opérateur.

---


## 21 octobre 2026 — PR #106 fusionnée : preuves humaines fictives

**Re-fetch GitHub (instantané daté) :** [PR #106](https://github.com/LaurentCOLL1/Fabulaxiom/pull/106) MERGED sous « Protect main » au `main=fbfc785afa6e5bdf92c337004d1bd2f925c4957a`. HEAD source `4abcc5217be07cb65d089e55fa042ff757b9043e`, CI PR [#39566947725](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39566947725) SUCCESS terminale (74 étapes Windows, 48 tests Vitest atelier et 44/44 scénarios Chromium dans deux modes). CI post-merge main [#39567933461](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39567933461) **EN COURS AU CHECKPOINT**, résultat à vérifier avant de le déclarer terminal. Les anciennes CI ne sont pas transférables.

**Produit :** `M32WorldOrderComparison` déjà existant rendu consultable dans l'atelier fictif de chronologie, avec deux ancres, témoins de précédence et motifs humains, exclusion des liens révoqués et actualisation après révocation humaine explicite. Aucun nouvel algorithme de graphe, aucune preuve de temps déduite de la narration, aucune révélation lecteur, aucune connexion App.tsx/Tauri/SQLite ou données opérateur. **M3.2 reste IN_PROGRESS_NOT_ACCEPTED**, PR #35 OPEN/DRAFT.

**STOP :** G2-A metadata-only PASS, accord ponctuel consommé, écrivain réel NOT_PROVEN, G2B/C/D à G6 NOT_AUTHORIZED, REAL_G3 STOP_UNAVAILABLE. Aucune originale v6/v7, sauvegarde, ACL, journaux, marqueur, migration 007, writer IPC, M3.3, ComfyUI, release ou commande Windows opérateur. Prochaine étape : confirmer CI post-main exacte ; développement ultérieur uniquement sur fixtures.

---


## 21 octobre 2026 — historique du candidat PR #106 (depuis fusionné)

**CANDIDAT, PAS ENCORE QUALIFIÉ :** dans le seul atelier navigateur `M32ManualChronologyLab`, choisir deux ancres imaginaires actives pour afficher la relation temporelle existante et les identifiants/motifs des liens humains qui la justifient. Réutiliser `M32WorldOrderComparison` au lieu de recopier son moteur. Les liens révoqués, les ancres historiques et les scènes du manuscrit ne prouvent aucune relation actuelle. Vérifier l'actualisation après révocation manuelle. **Cible : 48 tests Vitest de l'atelier (+6), 44 scénarios Chromium par mode (+3)** ; nouvelle CI au SHA exact obligatoire.

**STOP inchangé :** G2-A metadata-only avec accord consommé ; writer absence NOT_PROVEN, G2B–G6 NOT_AUTHORIZED ; M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT, vrai G3 STOP_UNAVAILABLE, M3.3 non autorisée. Aucun original SQLite v6/v7, WAL/SHM/journal, ACL, sauvegarde, migration 007, IPC writer, App.tsx ou commande opérateur Windows. Les résultats CI de #104 et #105 ne couvrent pas ce nouvel incrément.

---


## 21 octobre 2026 — vérification terminale CI après PR #104

GitHub vérifié : `main=997b60901e1f18a426eae3efa34ddb29c07b5721`, PR [#104](https://github.com/LaurentCOLL1/Fabulaxiom/pull/104) fusionnée ; CI PR [#39553745685](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39553745685) **SUCCESS** (42 Vitest fictifs, 41 Chromium dans chacun des deux modes), CI push `main` [#39554622761](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39554622761) **SUCCESS terminale** au SHA exact. Les passages « CI en cours » plus bas sont des instantanés historiques.

**STOP inchangé :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT ; G2-A PASS_METADATA_ONLY_OWNER_REPORTED (accord unique consommé), PROCESS_WRITER_ABSENCE NOT_PROVEN, G2-B/C/D et G3–G6 NOT_AUTHORIZED. Aucun accès original SQLite v6/v7, WAL/SHM, backups, ACL, migration 007, writer IPC, M3.3 ni release. Prochaine UX source-only : traçabilité des précédences humaines fictives, jamais inférées de l'ordre narratif.

---


## 21 octobre 2026 — PR #104 fusionnée : comparaison des trois ordres fictifs

**Autorité publique datée, pas autorisation opérateur :** PR [#104](https://github.com/LaurentCOLL1/Fabulaxiom/pull/104) MERGED au `main=997b60901e1f18a426eae3efa34ddb29c07b5721` après CI PR [#39553745685](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39553745685) terminale SUCCESS (**74 étapes Windows**, **42 tests Vitest atelier**, **41/41 Chromium** en modes normal et précompilé). HEAD exact de source `b320b711763659d9a3af670b685254eeb8b815e9`. CI push post-merge [#39554622761](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39554622761) **EN COURS au checkpoint : ne pas la déclarer SUCCESS sans preuve terminale**. CI d'ancien HEAD non transférable.

**Fonction produit strictement fictive :** choix de deux scènes inventées ; ordre de narration comparable uniquement *dans un roman* ; ordre inter-romans et temps du monde indéterminés, révélation au lecteur non renseignée. Lecture seule, aucun lien inventé ni mutation du canon, pas de Tauri, SQLite ou Windows opérateur. Les en-têtes antérieurs marqués « candidat » sont des preuves datées désormais closes par #104 ; ne pas recommencer leur travail. **M3.2 IN_PROGRESS_NOT_ACCEPTED**, PR #35 OPEN/DRAFT.

**Sécurité inchangée :** G2-A PASS_METADATA_ONLY_OWNER_REPORTED (accord ponctuel consommé), PROCESS_WRITER_ABSENCE NOT_PROVEN ; G2-B/C/D–G6 NOT_AUTHORIZED, réel G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucune originale SQLite v6/v7, WAL/SHM/journal, backup, ACL, marqueur, migration 007, writer IPC, M3.3, ComfyUI ni release. Toute nouvelle commande Windows demanderait script intégral/effets/interactions et autorisation explicite.

**Prochaine action prudente :** vérifier le terminal de la CI push #39554622761 et normaliser le statut documentaire sans promouvoir M3.2. Poursuivre l'UX sur fixtures inventées uniquement jusqu'à autorisation nouvelle pour la vraie destination.

---

## 21 octobre 2026 — historique du candidat PR #104 (depuis fusionné)

Candidat de **laboratoire navigateur uniquement** : sélectionner deux scènes inventées et afficher séparément l'ordre de narration **dans un même roman**, l'indétermination **entre romans distincts**, et les états **chronologie du monde indéterminée** / **révélation non renseignée**. Aucun lien automatique entre position de manuscrit, ancre temporelle et connaissance du lecteur. Vérifications de scènes absentes/étrangères et d'une même scène, sans modification de l'historique.

**Objectif de CI fraîche, pas résultat constaté :** 6 tests unitaires supplémentaires (**42 atelier**) et 3 scénarios Chromium (**41** par mode). Le précédent PR #102 (36/38) reste une preuve historique fusionnée, pas une CI transférable au candidat. Aucune fonction Tauri, SQLite original, IPC writer, donnée privée, App.tsx, commande Windows ou réseau externe.

**Gates fermés :** M3.2 IN_PROGRESS_NOT_ACCEPTED ; PR #35 DRAFT ; G2A PASS_METADATA_ONLY_OWNER_REPORTED (accord consommé), absence d'écrivain réel NOT_PROVEN, G2-B/C/D et G3–G6 NOT_AUTHORIZED, REAL_G3 STOP_UNAVAILABLE, M3.3 et release interdits.

---


## 21 octobre 2026 — PR #102 fusionnée et CI post-fusion vérifiée

**Checkpoint public daté (non exécutable) :** [PR #102](https://github.com/LaurentCOLL1/Fabulaxiom/pull/102) MERGED sous « Protect main », HEAD source `07baf294286d427185c0817310d82418eb8c3fd2`, CI PR [#39543328344](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39543328344) terminale SUCCESS (**74 étapes Windows** ; **36 tests unitaires de l'atelier / 38 scénarios Chromium**, en modes standard et précompilé). Merge `main=1f0a8cd9a369106202b57102aa28915de65b7472` et [CI push #39544279201](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39544279201) **SUCCESS terminale** sur ce SHA. Les anciens passages « candidat / CI à qualifier » demeurent des preuves datées, pas des tâches à rejouer.

**Fonctionnalité fusionnée :** deuxième roman, scène et révision immuable du même Univers **strictement inventé** ; liste des révisions filtrée par identifiant exact de scène, sans déduire l'ordre du monde ni l'ordre de révélation des positions dans les manuscrits. Laboratoire navigateur seulement, sans accès SQLite réel, App.tsx, Tauri IPC ou exécution Windows opérateur. **M3.2 reste IN_PROGRESS_NOT_ACCEPTED**, PR #35 OPEN/DRAFT.

**Limites de gouvernance inchangées :** G2-A PASS_METADATA_ONLY_OWNER_REPORTED (accord unique consommé) ; PROCESS_WRITER_ABSENCE=NOT_PROVEN ; G2-B/C/D et G3–G6 NOT_AUTHORIZED ; REAL_G3=STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucune ouverture/mutation des originales v6/v7, journaux, sauvegardes, ACL, marqueur, migration 007, writer IPC, M3.3, ComfyUI ou release. Toute commande Windows demanderait script intégral, effets et autorisation distincte.

**Prochaine tranche admissible :** améliorer la lecture humaine des **trois ordres sans les confondre** sur fixtures uniquement ; CI neuve au prochain SHA, sans réutiliser celles de #102.

---

## 21 octobre 2026 — historique candidat PR #102 (depuis fusionnée)

Tranche **NON ENCORE QUALIFIÉE** : enrichir `m32BrowserLab.tsx` avec un deuxième roman imaginaire, une scène et une révision immuable propres au même Univers fictif. L'atelier filtre les révisions par identifiant exact de scène (jamais par titre) et rappelle que l'ordre de narration de deux romans ne définit ni chronologie du monde ni révélation au lecteur. Cible : **36 tests Vitest atelier / 38 scénarios Chromium** ; nouvelle CI au HEAD exact obligatoire, non interchangeable avec la CI PR #100 (32/36).

Aucune donnée opérateur, accès disque SQLite, Tauri IPC, réseau externe, migration 007, writer ou commande Windows. G2-A PASS_METADATA_ONLY_OWNER_REPORTED (accord consommé), écrivain SQLite absent NON PROUVÉ, G2B–G6 NOT_AUTHORIZED, réel G3 STOP ; M3.2 toujours IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT, M3.3 STOP.

---


## 21 octobre 2026 — statut vérifié après fusion de PR #100

**GitHub (checkpoint daté, sans autorisation opérateur) :** [PR #100](https://github.com/LaurentCOLL1/Fabulaxiom/pull/100) MERGED, `main=bf59b28b437470a4759a5971968e8f00f9fa895c`, head PR `95e2e0385979e2b226aa1d6289e12250c6e6e19d`. CI PR [#39533766395](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39533766395) SUCCESS terminale au head exact ; CI push main [#39534698504](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39534698504) SUCCESS terminale au merge exact. Ces CI ne valent pas pour de nouveaux commits.

**Produit :** prévisualisation d'un chemin qui créerait un cycle, relations actives bloquant une correction, révocation humaine explicite avant supersession ; atelier exclusivement fictif (32 Vitest, 36 Chromium) et non persistant. M3.1 COMPLETE/MERGED/NORMALIZED ; **M3.2 IN_PROGRESS_NOT_ACCEPTED**, PR #35 OPEN/DRAFT. Ne pas refaire la PR #100. Prochain incrément autorisé sur fixtures uniquement : distinction entre ordre du monde, ordre de narration et ordre de révélation.

**Gates :** G2-A PASS_METADATA_ONLY_OWNER_REPORTED, autorisation unique consommée ; PROCESS_WRITER_ABSENCE NOT_PROVEN ; G2-B/C/D et G3–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucune opération Windows autorisée, ni accès aux originales v6/v7, journaux, sauvegardes, ACL, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release. Avant toute commande locale : texte intégral, effets, interactions et nouvel accord explicite.

---


**Checkpoint du 21 octobre 2026 après PR #99. Instantané documentaire : re-fetch GitHub obligatoire. Aucune autorisation Windows, SQLite ou G2-B/G3 créée.**

## 2026-10-21 — historique candidat PR #100 depuis fusionnée

- Re-fetch GitHub : PR #99 fusionnée à `main=205a328150c90bf1fb4f52abd7fb8c04f3959468`, CI de PR #39480662913 SUCCESS **74/74** au HEAD `37a98b2d70126fdffa6ba06ce599aaa42f88ca7a`, CI push main #39482419125 **SUCCESS terminale**. Ces badges restent rattachés à ces SHA.
- [Aperçu de conflits du laboratoire fictif](../qualification/M3_2_FICTIONAL_CONFLICT_WITNESS_AND_CORRECTION_PREFLIGHT.md) : un graphe actif avant/après affiche le chemin `B → ... → A` qui rendrait cyclique l'ajout `A avant B`, avec les identifiants de relations humaines existantes. Correction d'ancre : les relations encore actives et la révision historique sont visibles ; **révocation humaine explicite** exigée avant remplacement append-only. Pas d'ordre total ou date inventée.
- Dix tests Vitest supplémentaires (**32 en tout**) et deux tests Chromium (**36 en tout**) à qualifier sur le **nouveau SHA** ; les contrôles de provenance Git exact-source existants restent inchangés, aucun nouveau fichier dans l'allowlist.
- **M3.2 IN_PROGRESS_NOT_ACCEPTED**, PR #35 DRAFT, pas de CRUD persistant ni GUI de production. G2A PASS métadonnées uniquement (accord consommé), writer `NOT_PROVEN`, G2B/C/D–G6 `NOT_AUTHORIZED`, réel G3 STOP ; historique 21/3/2 non attesté, prospective NOT_STARTED. Aucun PC Windows, base v6/v7, journaux, sauvegarde, ACL, marqueur, migration007, IPC writer ou release touché.

## 2026-10-20 — scènes et révisions historiques exactes (laboratoire fictif, candidat)

- PR #98 fusionnée sur `main=7477001cd0ebc69d4701f21eddbda898f94c79c5` sous ruleset Protect main, CI PR [#39447951647](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39447951647) **SUCCESS 74/74** au HEAD `783e9e10f225f877a3222a089008a394e596fcc8`; CI push main #39449601527 SUCCESS terminal.
- [Nouvelle tranche fictive](../qualification/M3_2_FICTIONAL_SCENE_REVISION_EXACT_BINDING.md) : sélection manuelle **scène fictive + identifiant exact de révision immuable**, même ancienne, sans lecture `head` ni contenu. Rejet d'une révision hors scène/roman/Univers, dupliquée ou inconnue ; préservation de la référence précédente lors de la supersession ; aucune persistance.
- 9 nouveaux cas Vitest (22 au total pour l'atelier) et 2 cas Chromium (34 au total) **à qualifier dans une nouvelle CI au HEAD exact**. Deux allowlists restent limitées aux 9 sources historiques fictives ; pas de nouvelle dépendance, pas d'IPC.
- M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 DRAFT. G2-A `PASS_METADATA_ONLY_OWNER_REPORTED`, absence writer `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique 21/3/2 et prospective NOT_STARTED. V6/v7, sidecars, ACL, backups, marqueurs, migration 007, writer IPC, M3.3, release protégés.

## 2026-10-20 — incrément produit M3.2 : édition de chronologie en navigateur fictif (candidat)

- Après [PR #97](https://github.com/LaurentCOLL1/Fabulaxiom/pull/97) fusionnée sur `main=a839953f73f17379aa7c5ccde69d807b5b99a2f6`, CI PR #39426793283 SUCCESS (74 étapes) au HEAD `00defd8fb25891f4cffb7f2acdd7871ef005cccc`; CI push main #39428345389 terminale SUCCESS. La roadmap V1 est désormais assortie d'une matrice de suivi et de neuf tests.
- Nouveau [laboratoire manuel fictif](../qualification/M3_2_SYNTHETIC_MANUAL_CHRONOLOGY_LAB.md) en candidat : formulaire de création des quatre dates, ajout de relation `avant/après` avec veto de cycle, révocation explicite, remplacement append-only préservant les sources anciennes et journal dans l'état mémoire. `src/m32BrowserLab.tsx` seul expose l'atelier ; **pas** `App.tsx` ni Tauri production, aucune DB, fichier, IPC ou donnée opérateur.
- 13 nouveaux tests Vitest de contrat fonctionnel et refus, **plus 3 scénarios Chromium réels (32 au total)** sur manifest Git exact limité aux deux nouveaux modules fictifs, à faire qualifier par la **nouvelle CI au SHA final** avant toute fusion. Les contrôles d'historique M2, identité, chronologie monde/narration/révélation restent inconditionnels ; le caractère synthétique ne constitue PAS le CRUD réellement accepté.
- M3.2 **IN_PROGRESS_NOT_ACCEPTED** ; PR #35 toujours DRAFT, UI native Windows et preuve de préservation réelles absentes. G2A PASS metadata-only déjà autorisé/consommé ; absence écrivain `NOT_PROVEN`, G2B/C/D et G3–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique 21/3/2 non attesté, prospective NOT_STARTED. Protection v6/v7, WAL, sidecars, ACL, sauvegardes, marqueur, migration 007, writer IPC, M3.3 et release inchangée.

## 2026-10-20 — audit intégral des cinq roadmaps V1, M3.2 encore non livrée

- Re-fetch `main=e35b7c92441c517d4f0fcacb829711c4d1e9da97`, PR #96 fusionnée sous ruleset, CI PR #39414915855 au HEAD `5ac35ff196b27ca85b79f73296c33082044c0d98` SUCCESS (73/73) ; CI push main #39416303498 terminale SUCCESS (72 étapes), sans effet sur les gates.
- Audit des **cinq** fichiers de `docs/roadmap/`, avec [index de suivi](../roadmap/README.md) et [matrice actuelle](../roadmap/ROADMAP_STATUS_CURRENT.md). M0–M2 `COMPLETE + MERGED + NORMALIZED` ; M3.1 aussi (PR #33 implémentation, PR #34 normalisation) ; M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 DRAFT. M3.3–M3.6, M4–M9 non autorisés ; ComfyUI proposition issue #19 OPEN.
- **Écart produit** : les tests de sécurité G2/G3 et fixtures permettent de préparer M3.2, mais **ne remplissent pas** son CRUD manuel chronologique, l'UX acceptée et l'audit Windows de données. Les plans historiques « M3 planning pending » / « M3 unauthorized » sont explicitement datés, non une règle courante.
- Ajout de 9 tests **source-only** `tools/test_m32_roadmap_traceability.py` en CI : présence des cinq plans, états acceptés, livrables restant, interdictions et ComfyUI. La roadmap **n'accorde jamais** une autorisation locale.
- G2-A `PASS_METADATA_ONLY_OWNER_REPORTED` (consentement consommé), writer réel `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique 21/3/2, prospective NOT_STARTED. Aucune action PC/SQLite v6/v7, backup, ACL, sidecar, marker, migration 007, writer IPC, PR #35 merge, M3.3, release.

## 2026-10-20 — autre écrivain SQLite malgré query_only : contre-exemples sur RAM fictive

- PR #95 fusionnée sur `main=a8578b8e128af2264e85a7341a96e13d0e086b23`, HEAD qualifié `29bae8aee7e6985e20bfd1ebda34f7a5b2c8732d`, CI PR #39406700987 SUCCESS (72/72) et CI push main #39407869929 SUCCESS recontrôlée. Les 13 tests Rust précédents sont donc intégrés, mais leur effet reste exclusivement local à une connexion fictive.
- Nouvelle [preuve négative en RAM partagée](../qualification/M3_2_SHARED_RAM_EXTERNAL_WRITER_NEGATIVE_PROOF.md) : deux connexions SQLite Python distinctes, URI figée `mode=memory&cache=shared` validée par chemin principal vide, sans aucun fichier opérateur. Douze tests source-only montrent qu'une deuxième connexion peut écrire malgré le `query_only=ON` de la première et que `total_changes` du lecteur ne change pas.
- `PRAGMA data_version` peut signaler une modification externe passée, mais ne prouve pas une quiescence continue ni une identité de propriétaire. Le test n'est pas un mécanisme à déployer : shared-cache uniquement pour l'expérience fictive.
- **Décision inchangée** : G2-A `PASS_METADATA_ONLY_OWNER_REPORTED`, absence de writer réel `NOT_PROVEN`, G2-B/C/D/G3/G4/G5/G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE` ; historique 21/3/2 et prospective NOT_STARTED ; consentement G2-A consommé. Aucune commande Windows, ni original v6/v7, sidecars, backups, ACL, marqueur, migration 007, IPC writer, PR #35 ou release.

## 2026-10-20 — lecture préouverte query-only en RAM fictive, Rust TEST-ONLY

- Re-fetch GitHub : PR #94 fusionnée sur `main=632e6d6d985affa6989bb220ddec99911e6ba1e6` après CI [#39394068343](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39394068343) SUCCESS au HEAD `74395428c185198632cc2cd2c19eec4b7132e4ad` (71 étapes). La CI post-merge de main doit être revérifiée avant de déclarer un succès terminal ; cette qualification ne déverrouille aucun gate.
- Nouveau [prototype Rust fictif](../qualification/M3_2_PREOPENED_QUERY_ONLY_RAM_READER_TOY.md) : seule une connexion `&Connection` déjà ouverte sur une base RAM **inventée** est empruntée ; la fixture seule fait `Connection::open_in_memory`, puis PRAGMA `query_only=ON`. 13 tests négatifs vérifient lecture sans migration, refus des écritures, schémas ATTACH supplémentaires et dérives de la même connexion. Feature non défaut + `cfg(test)` ; aucune API de production/Tauri/IPC.
- La surveillance source-only élargie reconnaît maintenant 26 fichiers Rust, dont 21 comportent des marqueurs SQLite. Son test des comptes textuels est ajusté pour la nouvelle fixture, sans reconnaître de droit de lecture sur les originaux.
- **Limits** : query_only et total_changes ne concernent que cette connexion ; aucun écrivain externe Windows authentifié ou exclu. G2-A reste `PASS_METADATA_ONLY_OWNER_REPORTED` (consentement consommé), writer SQLite absent `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, `REAL_G3=STOP_UNAVAILABLE`, historique 21/3/2, prospective NOT_STARTED. Ne rien exécuter localement, ne pas ouvrir v6/v7, sidecars, backups, ACL, marqueurs, migration 007, writer IPC ou PR #35.

## 2026-10-20 — inventaire élargi de tous les modules Rust Tauri (source-only)

- Re-fetch GitHub : PR #93 fusionnée sur `main=15c91039243206dc61190fec5668f32a87f3faf0`, CI PR [#39391766661](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39391766661) SUCCESS au HEAD `dcad1a905d8f21cf0a18a03e2cfc2c95050cf100` (70 étapes). CI push main #39393215542 EN COURS au checkpoint.
- Nouvel [inventaire textuel complet des sites SQLite Rust](../qualification/M3_2_WIDE_RUST_SQLITE_SITE_INVENTORY.md) : 25 fichiers `.rs` du dépôt, 20 contenant les motifs retenus ; garde-fou CI + 18 tests sur modifications fictives. La seule présence de nouveaux noms/calls force réévaluation des empreintes textuelles, sans lire un seul fichier SQLite privé.
- Limite : le scanner ne comprend pas les macros/alias Rust ni les appels dynamiques ; plusieurs substitutions compensatoires peuvent préserver les compteurs. C'est un **tripwire de maintenance**, jamais une preuve de sécurité runtime ni une autorisation de G2B-G6.
- G2-A `PASS_METADATA_ONLY_OWNER_REPORTED` (accord unique consommé) ; `PROCESS_WRITER_ABSENCE=NOT_PROVEN`, owner non migrant non attesté, G3 `STOP_UNAVAILABLE`, provenance historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucune commande sur Windows ou accès aux originales v6/v7/journaux/backups/ACL/markers, migration 007, writer IPC, PR #35, M3.3/release.

## 2026-10-20 — décision courante des gates distincte de l'historique

- Main `8e358d61b7f5438b893a416aa8f82d884569c5da` après fusion protégée de [PR #92](https://github.com/LaurentCOLL1/Fabulaxiom/pull/92), HEAD `cb5e1eaeaaf64bd684be6a80c9cc3b85fc56492b`, CI [#39388988034](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39388988034) SUCCESS (70 étapes). La CI push `main` #39391283127 était EN COURS au checkpoint et ne constitue pas un PASS terminal.
- [Table de décision G2–G6 actuelle](M3_2_GATE_DECISION_CURRENT.md) : **G2-A PASS exclusivement de métadonnées** (déclaration opérateur), G2-B/C/D NON AUTORISÉS ; G3 réel STOP, G4-G6 NON AUTORISÉS. Writer SQLite absent : `NOT_PROVEN` ; aucun owner non migrant attesté, aucune source froide quiescente qualifiée.
- [Snapshot précédent](M3_2_GATE_SNAPSHOT.md) explicitement historique au 19 octobre : ne pas confondre son `G2: NOT_AUTHORIZED` de l'époque avec le résultat G2-A du 20. Le nouveau document **ne remplace ni les preuves historiques ni le runbook de capture**.
- Consentement unique au bloc G2-A consommé ; nouveau script Windows soumis à revue intégrale et approbation spécifique distincte AVANT exécution. Pas de bases v6/v7, sidecars, ACL, backups, marqueurs, migration 007, IPC writer, PR #35, M3.3 ou release.

## 2026-10-20 — garde-fou textuel des points d'entrée SQLite (source-only)

- PR #91 fusionnée sur main=fb4625450439ecf236cc9065f434eda002f71533 après CI #39376628743 SUCCESS au HEAD 94c9886e4e362867cab86c39efc5b13125a94dac (69 étapes Windows). G2-A PASS métadonnées UNIQUEMENT, absence d'écrivain SQLite NOT_PROVEN, G3 réel STOP.
- [Audit source-only des points d'entrée Rust](../qualification/M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md) : open_database peut créer le dossier et ouvrir avec READ_WRITE|CREATE puis migrer ; database_status et create_backup appellent cette fonction ; backup réserve un nouveau fichier puis ferme son handle avant VACUUM INTO ; une lecture READ_ONLY n'atteste pas la non-modification de sidecars WAL.
- Nouveau garde-fou examine seulement trois fichiers Rust publics ; ses 18 tests sur modifications fictives exigent une nouvelle revue en cas de dérive, même si le changement serait une amélioration. **Ce n'est pas une preuve exhaustive de sécurité Rust**, ni une procédure opérateur.
- Interdictions inchangées : G2B/G2C/G2D/G3/G4/G5/G6, originaux v6/v7, sidecars/ACL/backups/markers, migration 007, writer IPC, PR #35, M3.3/release. Aucune commande locale autorisée sans procédure entière et nouvel accord explicite.

## 2026-10-20 — écart de preuve SQLite writer après G2-A PASS (source-only)

- Re-fetch `main=45ce1511aa616fce9664dfc08cea39f290d2273d` après fusion protégée [PR #90](https://github.com/LaurentCOLL1/Fabulaxiom/pull/90), PR head `9c53d06c94cfbae62215c2407e4e146e7a344773`, CI PR #39342493152 SUCCESS (68 étapes Windows). Aucun nouveau résultat opérateur après G2-A PASS_METADATA_ONLY.
- Nouvelle [matrice source-only d'absence d'écrivain SQLite](../qualification/M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md) : noms de processus absents, hashes, sidecars, noms de fichiers, verrous ponctuels ou fixtures `already-open` ne prouvent pas la quiescence du writer réel. Aucune ouverture de fichier/handle SQLite local.
- Audit public ciblé : `database::open_database` peut créer le parent et exécuter `run_migrations`, `lib.rs::database_status` l'utilise, `backup::create_backup` l'utilise puis `VACUUM INTO`. Ces chemins **ne sont pas des commandes G3 autorisées** pour les originaux protégés.
- Deux stratégies futures théoriques restent indisponibles sur originaux réels : propriétaire déjà ouvert non migrant et vérifiable, ou protocole cold-source avec origine/ancêtres authentifiés, quiescence continue et journaux résolus. Tests de refus sur fixtures fictives (aucune vraie connexion).
- **STOP invariant :** `G2A_LOCAL_METADATA=PASS_METADATA_ONLY` ; `PROCESS_WRITER_ABSENCE=NOT_PROVEN` ; `REAL_G3=STOP_UNAVAILABLE` ; `G2B/C/D/G3/G4/G5/G6=NOT_AUTHORIZED`. Pas de manipulation des DB prod v6/v7, sidecars, ACL, sauvegardes, marqueurs, migration 007, IPC writer ou release. Une nouvelle opération Windows demande code exact, effets et autorisation propre.

## 2026-10-20 01:31:24 +02:00 — G2-A PID 0 : PASS de métadonnées (déclaration opérateur)
  
- Le propriétaire a examiné le bloc exact PR #89 et donné un **nouvel accord explicite limité à une exécution**. Sortie communiquée : `G2A_LOCAL_METADATA: PASS`, `TOKEN_INTEGRITY: MEDIUM`, `FABULAXIOM_OLLAMA_PROCESS: NONE_MATCHED`, `WEBVIEW2_SEARCHHOST_LINEAGE: 6 OBSERVED_METADATA_ONLY`, `WEBVIEW2_OWNERSHIP_AUTHENTICATED: NO`, `PROCESS_WRITER_ABSENCE: NOT_PROVEN`, `PUBLIC_GITHUB_CHECK: NOT_ASSESSED_BY_THIS_BLOCK`, `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, `TAURI_RUNTIME: NOT_TESTED`. PowerShell 5.1.26100.9587 ; fuseau Romance Standard Time. Preuve déclarative de l'opérateur, non attestée indépendamment.
- **Le PASS porte exclusivement sur l'observation locale G2-A.** Le contrôle n'authentifie pas SearchHost et ne démontre pas l'absence d'écrivain SQLite ; la cause détaillée de l'ancien STOP PR #86 reste **inconnue**, même si le nouveau script corrige son rejet théorique du PID 0.
- Une seule exécution de ce nouveau texte a été approuvée et effectuée. **Consentement consommé** : ni deuxième exécution, ni G2-B/C/D, ni G3/G4/G5/G6 sans approbation distincte du propriétaire.
- GitHub `main=f14e5991d34350682647ef6f0bd67b1d2055f41a`, [PR #89](https://github.com/LaurentCOLL1/Fabulaxiom/pull/89) fusionnée ; CI push main #39341197526 recontrôlée SUCCESS et CI PR #90 #39341376262 était SUCCESS à son **ancien** HEAD avant cette modification. Toute CI de PR #90 au HEAD nouveau doit être entièrement requalifiée.
- Production SQLite v6 et v7 isolée, sidecars, sauvegardes, ACL, marqueur, migration 007, writer IPC, PR #35, M3.3 et release restent interdits. Provenance historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, issues #36/#38 OPEN.

## 20 octobre 2026 — checkpoint AVANT l'exécution locale G2-A (historique)

- `main=f14e5991d34350682647ef6f0bd67b1d2055f41a` (fusion [PR #89](https://github.com/LaurentCOLL1/Fabulaxiom/pull/89)), CI `pull_request` [#39339365546](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39339365546) terminale SUCCESS sur le HEAD `e188a98090112551b6a35dd78e8327914c0e9965` ; **68 étapes Windows SUCCESS**, dont 22 fixtures fictives, 11 tests source-only et parser AST PowerShell sans exécution. CI `push main` #39341197526 EN COURS au checkpoint, non qualifiée PASS.
- Le nouveau [bloc PID 0 exact](../qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md) est intégré en Markdown, **jamais exécuté sur Windows et NON AUTORISÉ pour l'opérateur**. Le bloc PR #86 reste distinct, intact, et son unique essai autorisé a déjà retourné `STOP_WEBVIEW2_PARENTAGE`.
- Les causes exactes de ce STOP restent inconnues. Correction PID 0 = hypothèse de défaut de source, **pas confirmation runtime**. Tous les G2-B à G6, bases privées v6/v7, sauvegardes, ACL, markers, sidecars, migration 007, IPC writer, PR #35, M3.3 et release restent bloqués.
- Prochaine frontière : présenter au propriétaire le **code intégral du nouveau bloc** avec effets (PowerShell, CIM/WMI, Entrée, pas de q/UAC prévu, journaux OS possibles) et solliciter son accord explicite distinct. Aucun `Continue` n'autorise à lui seul l'exécution.

## Reprise au 20 octobre 2026 — bloc candidat PID 0 SOURCE-ONLY

- Après re-fetch GitHub : PR #88 fusionnée sur `main=6d9d9ff52459873347180f509717180ccccd0d5f` ; CI PR #88 [#39303355912](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39303355912) terminale SUCCESS au HEAD exact `0b7c55f30f0a7967270e9a58be7beae25087fec5` ; CI push `main` #39338867733 initialement EN COURS, ne pas la présenter comme PASS.
- Une branche technique DISTINCTE propose [un nouveau bloc exact](../qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md), **non exécuté et non autorisé**. La version PR #86 réellement exécutée et son blob `ebeb8800f9f8e8cd9918579fca7e32c9e5231622` demeurent inchangés.
- Diff intentionnel : un seul PID 0 admis seulement s'il est nommé exactement `System Idle Process`, non ajouté aux ancêtres. Deux PID 0, nom atypique, PID négatif, PID parent zéro WebView2 et tous les veto antérieurs continuent STOP. Tests adversariaux sur fixtures, garde de diff exact et analyse PowerShell AST **sans exécuter**.
- La cause réelle du STOP `WEBVIEW2_PARENTAGE` n'est **pas identifiée** ; le PID 0 est une hypothèse techniquement plausible, pas une preuve sur le PC. Ancienne autorisation entièrement consommée. Aucune nouvelle commande Windows, SQLite, ACL, backup, marqueur ou Tauri.
- G2-B/G2-C/G2-D/G3/G4/G5/G6, migration 007, IPC writer, PR #35, M3.3 et release restent `NOT_AUTHORIZED`.

## Vérification de reprise du 19 octobre 2026

Lecture GitHub (sans exécution sur le PC opérateur) : `main`, PR #86/#87/#35, issues #36/#38, runs/actions et ruleset #24895490 `Protect main` revérifiés. Ruleset actif, check `Windows frontend and Rust checks` de l'app 15368 exigé, branche `main` sous PR, interdiction de suppression et de non-fast-forward, `bypass_actors=[]`. La lecture REST historique de protection de branche renvoie 403 pour cette intégration ; cela **n'annule pas** le ruleset lu directement. Un résultat opérateur nouveau existe : `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: WEBVIEW2_PARENTAGE`, `STOP_REASON: UNEXPECTED_OR_UNSAFE` sur le candidat exact PR #86. Le consentement spécifique à cet unique essai est consommé ; toute autre commande exige une nouvelle revue et un nouvel accord. Le sous-motif précis est inconnu. Les métadonnées de processus ne prouvent jamais l'absence d'un écrivain SQLite. Cette mise à jour documentaire n'ouvre aucun gate.

## Dernier état effectivement vérifié

- Dépôt : https://github.com/LaurentCOLL1/Fabulaxiom
- `main` observé : `f14e5991d34350682647ef6f0bd67b1d2055f41a` (merge [PR #89](https://github.com/LaurentCOLL1/Fabulaxiom/pull/89), après PR #88/#87/#86).
- PR #86 : correction du filtre G2-A `SearchHost.exe` / `msedgewebview2.exe` **fusionnée** ; CI Windows PR #39241294071 terminale SUCCESS et CI `main` #39242342744 SUCCESS.
- PR #87 : continuité versionnée et garde-fou de fraîcheur **fusionnés** ; CI Windows PR #39271702661 au HEAD `287c178063a4d2719742bac96d3bc57a8fa515bc` SUCCESS (62 étapes, contrôle same-PR PASS) ; CI `main` #39273165266 au SHA ci-dessus SUCCESS (62 étapes dont contrôle PR-only SKIPPED, attendu).
- PR #35 : **OPEN / DRAFT**. Issues [#36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) et [#38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38) : **OPEN**. Ruleset Protect main #24895490 actif, sans bypass (au checkpoint).
- Application : Windows, React + Tauri v2 + Rust + SQLite. Production SQLite v6 protégée, v7 isolée ; **aucune ouverture/migration des fichiers opérateur**. Pas de migration 007.
- Historique de provenance : `PENDING_EXTERNAL_ATTESTATION(21/3/2)` (21 ancrés, 3 empreintes observées seulement, 2 non ancrés). Politique compensatoire opérateur unique documentaire, baseline prospective `NOT_STARTED`.

## Incident G2-A et correctif

Le bloc G2-A de PR #85 a été exécuté manuellement après autorisation et a retourné **`G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: PROCESS_NAMES`**. Une capture de Process Explorer montrait six processus WebView2 sous `SearchHost.exe`, compatible avec la recherche Windows. **Ce n'est pas une preuve d'absence de processus écrivain SQLite**.

La PR #86 a préparé [le nouveau bloc exact](../qualification/M3_2_G2A_EXACT_BLOCK_REVIEW.md) **en Markdown uniquement**, qui examine `Win32_Process` (PID, PID parent, date de création, nom), compare les inventaires et refuse parent absent, cycle, chronologie incohérente, Fabulaxiom/Ollama actif ou WebView2 d'origine incertaine. Une parenté SearchHost cohérente peut être observée sans stopper les processus. La vérification PowerShell AST en CI est **syntaxique uniquement**, et les parentés sont testées sur fixtures fictives.

**Résultat opérateur du 19 octobre 2026 après revue du bloc exact et autorisation distincte :** `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: WEBVIEW2_PARENTAGE`, `STOP_REASON: UNEXPECTED_OR_UNSAFE`, `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, `TAURI_RUNTIME: NOT_TESTED`. Ce compte-rendu est fourni par l'opérateur, pas un audit indépendant. L'ancien STOP `PROCESS_NAMES` reste dans l'historique. Le script masque volontairement le motif interne : parent absent, changement d'instantané, chronologie invalide ou échec CIM ne sont pas individuellement prouvés. **Ne pas relancer ce script ni un nouveau diagnostic sans revue et autorisation distinctes.** Aucune commande PowerShell exécutée automatiquement depuis ChatGPT.

**Hypothèse de défaut source identifié sans essai sur Windows :** le bloc PR #86 refuse tout `ProcessId <= 0` pendant la construction de la table complète `Win32_Process`, alors que cette classe peut retourner `System Idle Process` avec `ProcessId=0`. Si cet enregistrement figure dans l'inventaire, `AMBIGUOUS_PROCESS_ID` provoque le STOP avant tout parcours WebView2. Les 14 fixtures antérieures n'incluent aucun PID 0. Ce mécanisme est une **cause possible forte, non confirmée par la sortie opérateur** car le catch masque le sous-motif ; il faut des tests fictifs PID 0 et une future proposition explicite sans réexécution implicite. Références : https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance et https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-process .

## STOP historique PR #86 et interdictions toujours applicables

- `G2A_REVISED_RUNTIME=STOP_WEBVIEW2_PARENTAGE` (compte-rendu opérateur), `STOP_REASON=UNEXPECTED_OR_UNSAFE` ; cause fine inconnue. Le précédent `STOP_PROCESS_NAMES` reste historique. Aucun PASS de ce bloc historique PR #86 (le nouveau bloc PR #89 a ensuite produit un PASS de métadonnées).
- `G2-B/G2-C/G2-D/G3/G4/G5/G6=NOT_AUTHORIZED`, `REAL_G3_STOP_UNAVAILABLE`.
- `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`.
- Interdits : originales SQLite (v6 prod/v7 isolée), sidecars, ACL, sauvegardes, marker d'activation, migration 007, IPC writer, fusion PR #35, M3.3, release. Aucun reset Git destructeur ni faux relecteur indépendant.

## Prochaine action concrète

**Priorité actuelle au 20 octobre après le PASS local :** conserver le PASS limité aux métadonnées, requalifier la CI au nouveau HEAD documentaire, poursuivre seulement l'analyse source-only de l'absence d'écrivain SQLite NON PROUVÉE ; toute autre commande Windows nécessite un accord explicite neuf. Les étapes précédentes ci-dessous sont historiques.


1. Préserver ce nouveau STOP sans arrêter SearchHost/WebView2 ni répéter les observations locales.
2. Étudier sur sources et fixtures fictives une proposition DISTINCTE de diagnostic fail-closed produisant seulement un code de motif non personnel (`PROCESS_SNAPSHOT_CHANGED`, parent manquant, chronologie invalide, échec CIM, etc.), sans commande Windows aujourd'hui. Les métadonnées de parenté ne prouvent jamais l'absence de writer SQLite.
3. Avant tout script différent ou réexécution, afficher code intégral, interactions et effets ; obtenir un nouvel accord explicite. Aucun accès v6/v7, sidecars, G2-B/G2-C/G2-D ni G3–G6.
4. Re-fetch exact main/PR/CI/ruleset, mettre à jour MD+JSON à chaque PR significative ; requalifier CI au nouveau SHA après commit.

Se reporter à [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) pour les invariants détaillés, sans réutiliser les anciennes CI après un nouveau commit.

**Revalidation terminale indépendante — 22 octobre 2026 :** [CI push main #39755042137](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39755042137) est maintenant `completed/SUCCESS` (74/74 étapes Windows) sur le SHA exact `593b39e531e2a93e2f334220f37f6d8ed9bf9c93`. Le snapshot historique de PR #128 `IN_PROGRESS_AT_CHECKPOINT` reste **inchangé** ; l'observation ultérieure est ajoutée séparément dans `HANDOFF_CURRENT.json`, sans promotion de M3.2 ou des gates réels.
