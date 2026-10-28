# Fabulaxiom

**28 octobre — PR #208 terminale, prochaine candidate S1 lifecycle NON QUALIFIÉE :** source `aef3d137762eeea111e67f57d85acf23307f8a4f`, CI #40675104745 SUCCESS, protected `main=90cb86aa6873135890ea762f95eb9480fd9d917c`, postmain indépendante #40676661192 SUCCESS, 199/7/41/139, #38 6467450836. [Contrat S1 Route A](docs/qualification/M3_2_V7_S1_ROUTE_A_LIFECYCLE_DECISION_20261028.md) : Rust Windows test-only, cycle Absent/CleanlyClosed/CrashUnknown/Active/Foreign, 201/7/41/140 ATTENDUS PAS PASS. `CleanlyClosed` est une hypothèse de fixture, aucune admission runtime/atomicité xOpen/absence writer démontrée. STOP M3.2 IN_PROGRESS_NOT_ACCEPTED, G2B NOT_ACCEPTED, writer NOT_PROVEN, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, #35 OPEN/DRAFT ; aucun S3/S4/IPC/CRUD, migration 007, Hello ou accès opérateur. Re-fetch, CI SHA source, diff/reviews/threads, Protect main, expected_head_sha, postmain, #38 append-only.

**27 octobre — PR #195 TERMINALE ; question Windows Hello cadrée, prochaine preuve FileIdInfo NON QUALIFIÉE :** [PR #195](https://github.com/LaurentCOLL1/Fabulaxiom/pull/195) MERGED, source `f84f3035170baa4830879796230675ad8b328a2c`, [CI source #40516204731](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40516204731) SUCCESS (**153 Rust, 7 Greenfield, 34 gardes, 126 contrats**), squash protégé `main=1ab320f7834086ac587ce2fdaa8638d7c29d61f5`, [postmain indépendante #40518270685](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40518270685) SUCCESS et [issue #38 terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6444458042). Le handle natif SQLite est vérifié **APRÈS `xOpen`**, sans garantie de refus préalable ou d'atomicité. **Nouvelle candidate [FileId 128 bits Win32 + frontière d'authentification Windows Hello](docs/qualification/M3_2_WIN32_FILEID_128_AND_WINDOWS_HELLO_BOUNDARY_20261027.md)**, fixture test-only `GetFileInformationByHandleEx(FileIdInfo)` et étude documentaire sans implémentation Hello, compte, PIN ni changement d'authentification : **154 Rust / 7 Greenfield / 35 gardes / 127 contrats ATTENDUS, pas qualifiés**. Une identification future pourrait protéger l'UI ou demander consentement humain, **mais ne prouve jamais identité SQLite pré-`xOpen`, absence d'autre writer, G2B ou G3**. Aucune SQLite v6/v7 ni backup/ACL/sidecar/journal/marqueur Windows opérateur, migration 007, Tauri CRUD/UX v7 ou IPC writer touché ; profil unique `com.fabulaxiom.greenfield.v1`. PR #35 OPEN/DRAFT ; M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Toute PR : deux prompts, handoffs MD/JSON, roadmap/continuité, issue #38 append-only ; CI SHA exact, diff/reviews/threads, `Protect main` actif, squash `expected_head_sha`, postmain indépendante.

**27 octobre — PR #194 TERMINALE ; prochain témoin VFS Windows STRICTEMENT TEST-ONLY ET NON QUALIFIÉ :** [PR #194](https://github.com/LaurentCOLL1/Fabulaxiom/pull/194) MERGED, source `de54c003421d09309f5bff8a31d110fb24d93678`, [CI exacte #40507105063](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40507105063) SUCCESS (**151 Rust, 7 Greenfield, 32 gardes, 125 contrats**), squash protégé `main=567638515444d621749507f9700a3e2a69c52c6b`, [CI postmain indépendante #40508416842](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40508416842) SUCCESS, [issue #38 terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6442750005). Les deux échecs Windows antérieurs #40499869627 / #40501278786 (**150/151 Rust**) réfutent l'immuabilité implicite du nom d'un répertoire feuille vide malgré un handle sans DELETE. **Nouvelle candidate [identité du handle NATIF SQLite Windows après `xOpen`](docs/qualification/M3_2_GREENFIELD_V7_SQLITE_WIN32_NATIVE_HANDLE_POSTOPEN_20261027.md)**, avec un positif sous claim et un contre-exemple de substitution du nom après le précheck ; **153 Rust, 34 gardes, 126 contrats attendus — AUCUN PASS nouveau anticipé**. Le contrôle est **APRÈS** ouverture, donc aucun handoff atomique, aucune défense contre course hostile ni ouverture Tauri v7/CRUD/UX acquise. Profil unique `com.fabulaxiom.greenfield.v1` conservé ; aucun Windows opérateur, SQLite/backup/sidecars actifs, ACL, journaux, marqueur, migration 007 ou IPC writer touché. #35 OPEN/DRAFT, M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. CI au SHA nouveau, diff/reviews/threads, `Protect main`, squash `expected_head_sha`, postmain indépendante et issue #38 append-only obligatoires.

**27 octobre — PR #194 OPEN, STOP observé puis nouvelle vérification bornée (NON QUALIFIÉE) :** base `main=8d034d66c3de76735c356c6f79e436c0b9965dec` (#193 MERGED, postmain #40486676658 SUCCESS). [PR #194](https://github.com/LaurentCOLL1/Fabulaxiom/pull/194) : [CI #40498356467](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40498356467) FAILURE `E0658` ; [#40499869627](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40499869627) et [#40501278786](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40501278786) FAILURE (**151 Rust exécutés, 150 PASS / 1 FAIL**) : une feuille de répertoire vide est renommable malgré handle et partage sans DELETE. [STOP issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6441614257). **Révision candidate test-only, pas preuve nouvelle acquise :** [révalidation des FileIndex des handles retenus après substitution contrôlée, refus avant `xOpen`, plus fixture positive indépendante](docs/qualification/M3_2_GREENFIELD_V7_OWNED_FIXTURE_DIRECTORY_CHAIN_20261027.md) ; **151 Rust / 32 gardes / 125 contrats attendus** au prochain SHA. La révalidation ponctuelle n'élimine PAS la course après contrôle, ni les ancêtres du vrai profil ou le lien SQLite VFS. PR #35 OPEN/DRAFT ; M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucune action Windows opérateur, SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer. CI exacte, diff/reviews/threads, `Protect main`, squash `expected_head_sha`, postmain indépendant et issue #38 append-only restent impératifs.

**27 octobre 2026 — PR #193 TERMINALE ; nouvelle candidate chaîne d'identité des répertoires de fixture :** [PR #193](https://github.com/LaurentCOLL1/Fabulaxiom/pull/193) MERGED, source `38540a4602c5c5e4f9d9b3bdb6b8bf155e0ed256`, [CI source #40485043798](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40485043798) SUCCESS (**149 Rust, 7 Greenfield, 30 gardes, 123 contrats**), squash protégé `main=8d034d66c3de76735c356c6f79e436c0b9965dec`, [postmain #40486676658](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40486676658) SUCCESS indépendante, [issue #38 terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6439378032). **Nouvelle candidate NON qualifiée** : [refus lexical d'évasion, identité volume/FileIndex et épinglage sans DELETE des répertoires appartenant aux seules fixtures jetables](docs/qualification/M3_2_GREENFIELD_V7_OWNED_FIXTURE_DIRECTORY_CHAIN_20261027.md) : **151 Rust, 32 gardes, 124 contrats attendus**, pas des PASS anticipés. Les ancêtres au-dessus de la racine CI, ACL, reparse/junctions de profil réel, identité du handle SQLite VFS et preuve contre adversaire restent NON QUALIFIÉS. Pas de véritable ouvreur/CRUD/UX v7 Tauri, migration 007 ni IPC writer ; profil Windows unique `com.fabulaxiom.greenfield.v1` inchangé, aucun fichier opérateur touché. PR #35 OPEN/DRAFT ; M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. À chaque PR : deux prompts, deux handoffs, roadmap/continuité, issue #38 append-only ; CI au SHA exact, diff/reviews/threads, `Protect main`, squash `expected_head_sha` et postmain indépendante.

**27 octobre 2026 — PR #192 TERMINALE et nouvelle tranche de handoff bornée :** [PR #192](https://github.com/LaurentCOLL1/Fabulaxiom/pull/192) MERGED, source exacte `a061311a4d8ca54b213d134c2affa34defa3f023`, [CI #40474849956](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40474849956) SUCCESS (147 Rust, 28 gardes, 122 contrats), squash protégé `main=0584291d6dc3c8d2fc8860c8c5084250f4c43ba4`, [postmain #40476232974](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40476232974) SUCCESS indépendante et [issue #38 terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6437767007). **Nouvelle candidate test-only NON qualifiée :** [handle OS conservé pendant l'ouverture SQLite Windows, parent immédiat tenu sans partage DELETE et contre-exemple de remplacement du parent](docs/qualification/M3_2_GREENFIELD_V7_PINNED_HANDOFF_PARENT_NAMESPACE_20261027.md). Objectifs seulement : **149 Rust, 30 gardes d'inventaire, 123 contrats**. La propriété de tous les ancêtres, les FileId/ACL/junctions et une ouverture réellement non substituable ne sont **PAS prouvés** ; aucune admission Tauri v7/CRUD/UX opérateur, migration 007 ni writer IPC. Profil unique `com.fabulaxiom.greenfield.v1` inchangé ; #35 OPEN/DRAFT. Gates M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. CI nouvelle exacte, revue diff/reviews/threads, `Protect main`, merge `expected_head_sha`, postmain indépendante et issue #38 append-only obligatoires ; aucune action Windows opérateur.

**27 octobre 2026 — PR #188 TERMINALE ; candidat de refus de provenance dans le MÊME profil :** [PR #188](https://github.com/LaurentCOLL1/Fabulaxiom/pull/188) MERGED, source `9ca23c1b78c5fb2e3f49c2c3728024be374caeba` / [CI #40450684268](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40450684268) SUCCESS, squash protégé `main=e4cd6ba8151f2d6cbab8723d2fb200d3ac3ffebc` / [postmain #40451602743](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40451602743) SUCCESS indépendante ([issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6434133177)). 142 Rust, 6/6 Greenfield, 118 contrats. **Nouvelle candidate source/fixtures seulement :** [refus d'une sauvegarde revendiquant un autre `schema_owner` ou une lignée de migration 006 falsifiée](docs/qualification/M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_SCHEMA_REFUSAL_20261027.md), même lorsque SQLite est structurellement saine ; aucun basculement du marqueur, fichiers SQLite anciens/actifs et sauvegardes préservés. Cibles **143 Rust, 7/7 Greenfield, 9 gardes, 119 contrats** NON qualifiées avant la CI du nouveau SHA. Le profil Windows existant `com.fabulaxiom.greenfield.v1` **reste le même**, aucun second profil ; AUCUNE restauration Windows opérateur ni attestation indépendante. STOP M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. CI exacte, diff/reviews/threads, `Protect main`, fusion `expected_head_sha`, postmain indépendante, issue #38 append-only ; PowerShell toujours `& { ... }`.

**27 octobre 2026 — PR #187 TERMINALE ; candidate de REFUS FK dans le MÊME profil :** [PR #187](https://github.com/LaurentCOLL1/Fabulaxiom/pull/187) MERGED, source `3029bf61d526a243a431bf2c151de0ebeaf50818` / [CI #40444374426](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40444374426) SUCCESS, squash protégé `main=0b0964a723340fd832134691fdd93563c1afe9c0` / [postmain #40445392523](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40445392523) SUCCESS indépendante ([issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6433265532)). 141 Rust, 5/5 Greenfield, 117 contrats. **Nouvelle candidate source/fixtures uniquement :** [sauvegarde SQLite structurellement saine mais clés étrangères incohérentes — restauration refusée](docs/qualification/M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_KEY_RESTORE_REFUSAL_20261027.md) : `integrity_check=ok` ne suffit pas, `foreign_key_check` doit interdire l'activation ; fichiers SQLite ancien/actif, sauvegardes et marqueur conservés. Cibles **142 Rust, 6/6 Greenfield, 8 gardes et 118 contrats**, NON qualifiées avant CI au SHA candidat. Le profil opérateur **`com.fabulaxiom.greenfield.v1` demeure le même**, aucun deuxième profil ; AUCUNE SQLite/backup/activation Windows opérateur utilisée et aucune preuve indépendante. STOP M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. CI exacte, diff/reviews/threads, `Protect main`, fusion `expected_head_sha`, postmain indépendante et issue #38 append-only ; PowerShell toujours `& { ... }`.


Fabulaxiom est une application locale de création et de gestion d'histoires, de romans, de sagas et d'univers fictifs, avec mémoire narrative persistante et intégration Ollama.

## Principes du projet

- fonctionnement local-first, sans abonnement ni API cloud obligatoire ;
- conservation durable et vérifiable des textes et des faits narratifs ;
- séparation entre canon validé, brouillons, suggestions, variantes et informations incertaines ;
- traçabilité des faits jusqu'à leurs sources ;
- validation humaine avant toute promotion d'une suggestion IA vers le canon ;
- détection des incohérences avec distinction entre contradiction démontrée, suspicion et information insuffisante ;
- fonctionnement utile même sans IA ;
- priorité à la fiabilité de la mémoire narrative et à la maîtrise des modifications.

## État actuel

**23 octobre 2026 — PR #137 fusionnée avec protection de `main` :** source corrigée `892a42e9ea0c84ab9af9fb45536d502d99252155`, [CI #39876891920](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39876891920) terminale SUCCESS (75 étapes Windows, 72 contrats handoff, 132 Rust principaux, 53/53 Chromium normal et CSP, contre-exemple owner Rust PASS). Fusion `main=4d5a2bcb68dd439fac1846d354f3f808138457f1`. [CI post-main #39900039763](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39900039763) `IN_PROGRESS_AT_CHECKPOINT` lors de la rédaction : la revérifier ultérieurement sans réécrire cet instantané.

**Candidat PR #138 — fail-closed des voies d'écriture :** après le contre-exemple PR #137, `tools/m3_2_g3_owner_runtime_contract.py` ajoute l'exigence hypothétique `all_mutation_entrypoints_mediated=False` par défaut, uniquement pour `EXISTING_OWNER_SERVICE`. Trois tests fictifs confirment le STOP même avec mutex/owner déclarés et l'absence d'autorité réelle. Nouvelle note [M3_2_OWNER_ALL_WRITER_CHANNELS_GUARD.md](docs/qualification/M3_2_OWNER_ALL_WRITER_CHANNELS_GUARD.md). CI au commit exact de cette PR requise : les tests ne prouvent pas une exclusion réelle.

**STOP immuable :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B global `NOT_ACCEPTED`; écrivain réel `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; G3 réel `STOP_UNAVAILABLE`; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 OPEN/DRAFT. Aucun SQLite original v6/v7, sauvegarde, marker, ACL, sidecar, migration 007, writer IPC, M3.3, release ni opération Windows opérateur. Maintenir les deux fichiers de handoff, roadmap et prompt dans la même PR ; re-fetch GitHub, vérifier CI exacte, reviews/threads et Protect main avant merge `expected_head_sha`. Les lectures indépendantes peuvent être parallélisées, les écritures et fusions restent séquentielles.

**23 octobre 2026 — PR #136 protégée MERGED :** source `ea94377a80001fbd701ec06c7a84b7cba5b95036`, [CI source #39848398829](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39848398829) SUCCESS (75 étapes Windows, 71 contrats de continuité, 132 Rust, Chromium 53/53 normal et CSP). Fusion `main=d4837f1b292f37ec4b87926bc79a7c1c999d1fbe`, [CI post-main #39849940959](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39849940959) terminale SUCCESS (75 étapes) au SHA exact. Les précédents instantanés datés sont préservés.

**Candidat PR #137 — contre-exemple Rust strictement fictif :** un jeton du propriétaire `OwnerSlot` reste valide après une modification SQL valide mais non médiée sur sa connexion **en RAM inventée** ; un second snapshot transactionnel est cohérent sans que le jeton prouve l'absence d'écrivain. Un test Rust ajouté sous `cfg(test, feature="m32-g3-owned-ram-toy")`, documentation [M3_2_OWNER_UNMEDIATED_WRITE_NEGATIVE_WITNESS.md](docs/qualification/M3_2_OWNER_UNMEDIATED_WRITE_NEGATIVE_WITNESS.md), nouveau contrat #72. **Nouvelle CI propre au HEAD de PR #137 requise**, ne pas inférer une qualification. Aucune ouverture de fichier original, IPC, migration, Tauri normal ou opération Windows opérateur.

**STOP conservé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B global `NOT_ACCEPTED`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, G2B–G6 `NOT_AUTHORIZED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Re-fetch main/PR/workflows/reviews/ruleset avant chaque mutation et fusion ; tâches indépendantes en parallèle, écritures et merges séquentiels ; `expected_head_sha` obligatoire. Mettre à jour ce prompt et les deux handoffs dans chaque PR matérielle.

**22 octobre 2026 — PR #135 fusionnée sous Protect main :** source exacte `acb901bd1844d93ea0562415a7438a4b21e7f4b8`, [CI source #39841578935](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39841578935) terminale SUCCESS : 75 étapes Windows, 70 tests de continuité, 132 Rust, 53/53 Chromium normal et CSP. Fusion protégée `main=b54f4111eed020c80a70f91bd3e15b544f842545`, [CI post-main #39843166291](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39843166291) terminale SUCCESS (75 étapes) au SHA exact. La [décision d'architecture G2B→G3](../qualification/M3_2_G2B_G3_EVIDENCE_DECISION_AFTER_FILEID.md) est documentaire seulement. La PR #35 demeure OPEN/DRAFT.

**Reprise suivante :** [PR #136](https://github.com/LaurentCOLL1/Fabulaxiom/pull/136) candidate documentaire de normalisation #135 et actualisation du prompt ; **qualification CI au NOUVEAU HEAD requise** avant toute fusion. Re-fetch GitHub (`main`, PR, HEAD, workflows, revues, commentaires, ruleset) avant chaque mutation. Les vérifications indépendantes peuvent se faire en parallèle ; commits et fusions doivent rester séquentiels. Les checkpoints historiques conservent leurs états originaux, toute observation terminale ultérieure est distincte.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2-B global `NOT_ACCEPTED`, absence écrivain réel `NOT_PROVEN`, G2-C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, G2B–G6 `NOT_AUTHORIZED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucun original SQLite v6/v7, backup, ACL, sidecar, marqueur M1.5, migration 007, IPC writer, M3.3, ComfyUI, release ou commande Windows opérateur sans autorisation spécifique distincte. Les essais fictifs ne prouvent pas l'identité ni la quiescence réelles.

**22 octobre 2026 — PR #134 fusionnée sous Protect main :** source `f0db9b28d0e8492f3bc64c952b722873ae61311e`, [CI source #39837909918](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39837909918) terminale SUCCESS (75 étapes Windows, 69 contrats continuité, 132 Rust, 53/53 Chromium normal et CSP). Fusion `main=a1185b8345999f10814fd54dab96890f70236a5c`, [CI post-main #39839580270](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39839580270) terminale SUCCESS au SHA exact (75 étapes). PR #133 post-main [#39837202639](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39837202639) SUCCESS confirmé **ultérieurement** ; conserver son instantané daté `IN_PROGRESS_AT_CHECKPOINT` séparé de cette observation terminale.

**Décision G2-B → G3 source-only :** [M3_2_G2B_G3_EVIDENCE_DECISION_AFTER_FILEID.md](../qualification/M3_2_G2B_G3_EVIDENCE_DECISION_AFTER_FILEID.md) évalue la sauvegarde SQLite transactionnelle via une connexion propriétaire déjà ouverte et authentifiée, et la copie froide uniquement après preuve indépendante de quiescence et état WAL/journaux. Aucune de ces voies n'est démontrée sur les originaux ; ne jamais ouvrir une nouvelle connexion vers les originaux pour « essayer ». Les 4 contrôles G2B anonymisés sont seulement déclarés par l'opérateur, non attestés indépendamment.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B global `NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 DRAFT. Aucune original SQLite v6/v7, backup, ACL, sidecar, marker, commande Windows opérateur, migration 007, writer IPC, M3.3, ComfyUI, release. Paralléliser uniquement lectures indépendantes ; sérialiser écritures et fusions.

**22 octobre 2026 — PR #133 protégée MERGED :** source corrigée `d2bf3134054c4f1a05432c51055134fec7b4a0b2`, [CI Windows source #39835840939](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39835840939) terminale SUCCESS (8 contre-exemples Win32 fictifs, 68 contrats handoff, 132 Rust, Chromium 53/53 normal et CSP). Premier essai [#39835364262](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39835364262) FAILURE conservé : handle `FILE_READ_ATTRIBUTES / FILE_SHARE_READ` n'interdit pas le nouveau `GENERIC_WRITE` sur fichier fictif ; assertion négative corrigée. Fusion `main=604817c8457aaf7136f587aaaff28ff862e2702a`, [CI post-main #39837202639](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39837202639) `IN_PROGRESS_AT_CHECKPOINT` lors de cette normalisation ; re-fetch terminal indépendant requis, sans modifier rétroactivement cet instantané.

**G2B local — preuves opérateur limitées :** quatre sorties anonymisées fournies par le propriétaire (discovery, marqueur M1.5, métadonnées NTFS, FileIdInfo). Les résultats sont des observations non attestées indépendamment, sans version SQL ni démonstration de quiescence. Les tests CI sont uniquement sur octets fictifs temporaires non-SQLite ; ils montrent qu'un FileId stable ne prouve PAS l'absence d'écrivain. Les chemins, identifiants et contenus privés n'ont pas été publiés.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B global `NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2C et G2B–G6 `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 DRAFT ; pas de SQLite protégée v6/v7, sauvegardes, ACL, sidecars, marqueurs, commandes Windows opérateur, migration 007, writer IPC, M3.3, ComfyUI ou release. Paralléliser lectures indépendantes ; sérialiser écritures et fusions.

**22 octobre 2026 — G2B_WIN32_FILEID owner-reported observations, strict partial scope:** [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6347844772) recorded four sanitised local G2-B checks: one restored candidate + activation marker, matching marker target, no observed SQLite sidecar, fixed NTFS stable sampled metadata, FileIdInfo stable across two `FILE_READ_ATTRIBUTES / FILE_SHARE_READ|WRITE|DELETE` openings on three files with ancestor handles. **Owner reported, NOT independent; schemas NOT SQL verified; writer absence NOT_PROVEN, G2B globally NOT_ACCEPTED, G2C NOT_AUTHORIZED, real G3 STOP_UNAVAILABLE.** No private paths/IDs/hashes published.

**New source-only Windows CI candidate:** [M3.2 G2-B fictional FileId/writer counterexample](../qualification/M3_2_G2B_WIN32_FILEID_WRITER_COUNTEREXAMPLE.md) exercises 8 tests (4 plain refusal checks + 4 ephemeral non-SQLite Win32 scratch fixtures on GitHub Actions only). Demonstrates a retained, locally stable FileId can coexist with a new writer and changed bytes when the metadata handle uses `SHARE_ALL`. Fresh exact-HEAD CI REQUIRED; do not borrow prior CI. This experiment is not an operator tool and never sees a protected database.

**Protected PR #132 now MERGED:** source `0ccc9af60075e90942d6e0bd7e2f92694bbe4876`, source [CI #39776896152](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39776896152) SUCCESS (74 Windows, 66 handoff, 132 Rust, Chromium 53/53 twice); `main=202152a3e502b08e6b7b77344769b6b0a1ea76bf`, post-main [CI #39778720560](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39778720560) SUCCESS at exact SHA. Historical PR #131 post-main `IN_PROGRESS_AT_CHECKPOINT` preserved independently from its later verified SUCCESS (run #39776433056).

**STOP ABSOLU :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence writer `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 DRAFT ; pas de SQLite v6/v7 originale, sidecar, ACL, backup, activation marker, commandes Windows opérateur, migration 007, IPC writer, M3.3, ComfyUI, release. Les lectures indépendantes peuvent être parallélisées, écriture/fusion séquentielles.

**22 octobre 2026 — PR #131 fusionnée :** [CI source #39770785693](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39770785693) SUCCESS sur `6b1973e077e90885d326cb5acbb2358368523bd2` ; fusion protégée `main=37d8aa100e9d6fe61bbe6650f554a147661e703e` ; [CI post-main #39776433056](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39776433056) `IN_PROGRESS_AT_CHECKPOINT`. L'affichage du prédécesseur reste dans le laboratoire fictif, hors application réelle. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, écrivain réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE` ; aucune opération sur les bases protégées ni Windows opérateur.

**22 octobre 2026 — PR #130 protégée MERGED :** source `f980e8e294f537f6b588ded56f6f79cc772558d6` ; [CI #39764830760](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39764830760) terminale SUCCESS (74 étapes Windows, 132 Rust, 63 contrats, 53/53 Chromium normal et CSP) ; fusion `main=8f330a4feff30092847e5bf180160efed174ebdd`. [CI post-main #39769613787](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39769613787) `IN_PROGRESS_AT_CHECKPOINT` ici : préserver cet instantané, vérifier le résultat terminal séparément.

**Candidat suivant — source-only :** dans le navigateur fictif, afficher explicitement la correction précédente et son ancienne relation humaine `avant/après`, sans inférer de nouvelle chronologie. Tests existants renforcés ; qualification neuve obligatoire avant fusion. `App.tsx` et le runtime restent inchangés.

**STOP strict :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, attestations `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucun Windows opérateur, SQLite originale v6/v7, backups, sidecars, ACL, marqueur, migration 007, writer IPC, M3.3, ComfyUI, release. Parallélisation seulement indépendante ; commits/merges séquentiels.

**22 octobre 2026 — PR #129 :** normalisation documentaire fusionnée (`main=8f4b84bdccf19842aa98b35defe8e84a02e769db`) ; [CI PR #39756548081](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39756548081) et [CI post-main #39758153975](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39758153975) terminales SUCCESS au SHA exact. M3.2 demeure `IN_PROGRESS_NOT_ACCEPTED` : pas d'écrivain réel prouvé, G2B–G6 non autorisés, aucune action sur bases SQLite protégées ou Windows opérateur. Travaux de laboratoire fictifs uniquement.

**M0 — Environment and architecture qualification : COMPLETE + MERGED + NORMALIZED**

Architecture retenue :

- Tauri 2 ;
- React + TypeScript ;
- cœur applicatif Rust/Tauri ;
- SQLite pour la persistance structurée (FTS5 est planifié pour M4) ;
- intégration Ollama locale directe sur la boucle locale ;
- aucun runtime Python/FastAPI obligatoire pour M0/M1.

**M1 — Persistence and project foundation : COMPLETE + MERGED + NORMALIZED**

M1.1 — SQLite foundation and migration runner est **COMPLETE + MERGED + NORMALIZED**.

M1.2 — Project hierarchy schema est **COMPLETE + MERGED + NORMALIZED**.

M1.3 — No-AI CRUD service est **COMPLETE + MERGED + NORMALIZED**.

M1.4 — Text revisions and provenance foundation est **COMPLETE + MERGED + NORMALIZED**.

M1.5 — Backup and restore baseline est **COMPLETE + MERGED + NORMALIZED**.

Le socle persistant comprend désormais :

- SQLite embarqué via rusqlite ;
- migrations transactionnelles versionnées ;
- clés étrangères activées et vérifiées par connexion ;
- schéma v2 Universe → Series optionnelle → Novel → Chapter → Scene ;
- IDs stables et immuables ;
- ordre déterministe des éléments frères ;
- contraintes d'intégrité inter-univers ;
- services Rust CRUD avec erreurs déterministes et transactions explicites ;
- commandes Tauri minces ;
- écrans/formulaires React utilisables pour toute la hiérarchie ;
- CRUD opérationnel avec Ollama arrêté ;
- révisions de texte de scène immuables, historique append-only et provenance par parent ;
- pointeur de révision courante et restauration non destructive ;
- migration SQLite v3 qualifiée sur Windows ;
- sauvegardes SQLite vérifiées avec noms non écrasants ;
- restauration vers une nouvelle base indépendante, avec activation contrôlée sans écraser la précédente ;
- conservation de l'historique de révisions et des sauvegardes antérieures ;
- qualification Windows et CI déterministe.

## M2 — Entités narratives et faits canoniques

**M2.1 à M2.5 : COMPLETE + MERGED + NORMALIZED.** PR #30 de normalisation fusionnée à `f13b4f8c249866ff60a19d7895b6cfaede56398a` après CI exacte #38041908126. Les fonctionnalités M2 décrites ci-dessous sont livrées ; cela ne signifie pas que la V1 est terminée.

M2.1 — Entity registry schema and migration est **COMPLETE + MERGED + NORMALIZED**.

SQLite v4 ajoute un registre d'entités narratives lié à chaque univers et une table d'alias. Les six types pris en charge au niveau schéma sont : personnages, lieux, organisations, objets, événements et règles du monde. Le schéma préserve les identifiants et les contraintes d'intégrité.

La migration réelle v3 → v4 a été qualifiée sur Windows avec une sauvegarde vérifiée de la base restaurée réellement active. Le contrôle a confirmé la conservation des données M1, notamment des trois révisions textuelles et du pointeur courant. Les sauvegardes opérateur préexistantes sont conservées.

**M2.2 — No-AI entity and alias CRUD : COMPLETE + MERGED + NORMALIZED** après fusion de la PR de normalisation dédiée.

La PR #23 d'implémentation a été fusionnée à `ad7211fa2f292b8bd9812e299dbb6be96214eb89` après les qualifications Windows (13/13 tests interactifs, 21/21 frontend, 51/51 Rust, base SQLite active et historique vérifiés). Les formulaires React et services Rust/Tauri permettent de créer, consulter, renommer et supprimer des entités narratives ainsi que leurs alias, avec identifiants immuables, rejet des doublons d'alias par entité et garde de suppression des entités liées, même avec Ollama arrêté.

**M2.3 — Registre des faits et provenance exacte : COMPLETE + MERGED + NORMALIZED** après fusion de la PR de normalisation dédiée.

La PR #25 est fusionnée à `e6e80c26316f11054348a18a235fd08c600e136e`. SQLite **v5** ajoute les tables STRICT `narrative_facts` et `fact_sources`. Les services **Rust/Tauri** permettent de créer et consulter manuellement des faits sourcés ou non sourcés, avec identifiants durables, citations rattachées aux révisions immuables des scènes, bornes d'octets UTF-8 et contrôles d'univers/transaction. Les opérations restent locales et ne requièrent pas Ollama.

La migration réelle v4 → v5 a été qualifiée sur Windows après une sauvegarde cohérente vérifiée. **8/8 contrôles d'interface**, **21/21 tests React** et **61/61 tests Rust** PASS ; les neuf entités, huit alias, trois révisions et leur pointeur courant ont été conservés. Voir `docs/qualification/M2_3_IMPLEMENTATION_GATE.md`.

**M2.4 — Statuts canoniques et service de revue humaine : COMPLETE + MERGED + NORMALIZED** après fusion de la PR de normalisation dédiée.

Implémentation PR #27 fusionnée à `3a069572d00e1680c42b0f13b800e28687c5f0eb`. SQLite **v6** ajoute `fact_review_events`, un journal de décisions de revue `STRICT` dont les événements ne peuvent pas être modifiés ou supprimés par les commandes normales. Les fonctions Rust/Tauri permettent de consulter les statuts et l'historique, de demander une transition déterministe et d'approuver ou révoquer explicitement le canon. Sept statuts : `draft`, `suggestion`, `canon`, `variant`, `unknown`, `ambiguous`, `contradictory`.

Qualification : **21/21 tests frontend**, **71/71 Rust**, **8/8 contrôles existants de l'interface Windows**, **8/8 tests Rust de revue isolée**, migration réelle v5→v6 et conservation vérifiée de toutes les données historiques, sauvegardes et pointeurs. Voir `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`.

**À distinguer :** le nom du relecteur est déclaré, non authentifié. Le service ne constitue pas un écran React de gestion de faits : aucun test d'interaction E2E de revue via la fenêtre Tauri n'est revendiqué. Ollama est facultatif et aucune promotion au canon n'est automatique.

**M2.5 — Interface de faits sourcés et revue humaine : COMPLETE + MERGED + NORMALIZED.** PR #29 fusionnée à `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1` après la CI exacte #38040227617 (32/32 frontend, 72/72 Rust) et la qualification Windows isolée sans Ollama. L'écran React permet de saisir des faits sourcés ou non sourcés, citer la révision de scène historique exacte, consulter les sept statuts, l'historique de revue et confirmer explicitement l'approbation/révocation canonique. Tests Windows : 8/8 hiérarchie, 8/8 synchronisation, 9/9 faits, 10/10 revue ; audit indépendant SQLite v6 : 3 faits, 2 sources et 11 événements immuables dans une base isolée. La base réelle et les sauvegardes sont restées intactes. Voir `docs/qualification/M2_5_SOURCED_FACTS_REVIEW_UI.md`.

Une proposition distincte d'atelier visuel local ComfyUI pour les personnages, scènes et événements figure dans `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md`. Elle est **documentée mais non autorisée à l'implémentation**.

## Utilisations actuellement disponibles

- **Organiser un univers narratif** : créer une hiérarchie Univers → Série facultative → Roman → Chapitre → Scène ; modifier les noms et l'ordre dans les limites des garde-fous.
- **Rédiger et retrouver l'historique d'une scène** : sauvegarder de nouvelles révisions, consulter leur historique et changer la révision courante sans écraser les versions antérieures.
- **Gérer les personnages et éléments de l'univers** : ajouter des personnages, lieux, organisations, objets, événements et règles du monde, avec identifiants stables même en cas de noms identiques.
- **Gérer les alias** : créer plusieurs alias par entité, les renommer ou les supprimer ; les doublons sur une même entité sont refusés.
- **Protéger le projet** : créer des sauvegardes applicatives SQLite et restaurer une sauvegarde dans une nouvelle base sans écraser l'ancienne ; un marqueur sélectionne la base active.
- **Travailler hors IA** : les opérations précédentes restent disponibles sans Ollama ; le diagnostic Ollama est indépendant.

- **Saisir des faits depuis l'interface graphique (M2.5)** : ajouter un attribut/une valeur à une entité, facultativement préciser une validité temporelle fictive, distinguer les faits sans source et les faits avec citation vérifiable.
- **Choisir un passage exact de scène** : sélectionner une ancienne révision immuable, capturer une citation en octets UTF-8 même avec accents/émojis, puis retrouver cette révision indépendamment du texte courant.
- **Gouverner le canon manuellement** : distinguer brouillon, suggestion, canon, variante, inconnu, ambigu et contradictoire ; consulter l'historique non effaçable des revues ; approuver ou révoquer explicitement avec justification et confirmation.
- **Actualiser les modules** : les nouveaux univers et entités, ainsi que les révisions de scènes, deviennent disponibles dans l'espace des faits sans forcer la fermeture ou le rechargement complet.
- **Utiliser l'application sans Ollama** : les fonctions manuelles M2 ne requièrent ni modèle actif ni service distant. L'identité du réviseur est une étiquette déclarée, pas une authentification.

**Non encore livrés :** la chronologie et les connaissances des personnages (M3), les recherches FTS5/sémantiques (M4), la génération/extraction IA (M5), le moteur automatique de cohérence (M6) et l'atelier d'images ComfyUI. Ce dernier reste une proposition distincte (issue #19), même si ComfyUI fonctionne déjà localement.

## Prochaine étape : normalisation M3 puis M3.1 uniquement

La planification M3 a été fusionnée par la PR #31 à `68db746754e01b441870e0653f17f10ebfc7be2f`, après sa CI exacte #38050865413 (13/13 étapes Windows). Elle organise six phases distinctes : temps fictif et schéma, chronologie manuelle, relations historiques directionnelles, croyances/connaissances, révélations narrateur/lecteur et états narratifs évolutifs. Voir `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`.

**Aucune fonctionnalité M3 n'est encore livrée.** Après la qualification et la fusion d'une normalisation documentaire indépendante, **seule M3.1** peut être développée dans une nouvelle PR. Toute migration SQLite v6→v7 sur la machine de production exige une sauvegarde cohérente préalable et une qualification Windows distincte. M3.2–M3.6, M4+ et ComfyUI ne sont pas autorisés par cette planification. L'atelier visuel ComfyUI reste une proposition future (issue #19).

## Documentation d'autorité

- `docs/continuity/STATE.md` — état courant du projet ;
- `docs/continuity/NEXT.md` — prochaine étape autorisée ;
- `docs/roadmap/FABULAXIOM_ROADMAP_V1.md` — feuille de route V1 ;
- `docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md` — plan détaillé M1 ;
- `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md` — plan détaillé M2 ;
- `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md` — plan gouverné M3, sans implémentation ;
- `docs/qualification/M3_PLANNING_POST_MERGE_NORMALIZATION.md` — qualification documentaire indépendante de la planification M3 ;
- `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md` — preuves de qualification M2.2 ;
- `docs/qualification/M2_3_IMPLEMENTATION_GATE.md` — qualification M2.3, sauvegarde v4 et migration Windows v5 ;
- `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md` — qualification M2.4, sauvegarde v5 et migration Windows v6 ;
- `docs/qualification/M2_5_SOURCED_FACTS_REVIEW_UI.md` — qualification Windows M2.5, provenance et revue humaine ;
- `docs/qualification/M2_5_POST_MERGE_NORMALIZATION.md` — preuves et frontière de normalisation M2.5 ;
- `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md` — proposition visuelle non implémentée ;
- `docs/architecture/ARCHITECTURE_DECISIONS.md` — décisions d'architecture ;
- `docs/PRODUCT_SCOPE_V1.md` — périmètre fonctionnel V1.

## Développement

Chaque jalon doit produire un résultat utilisable, documenté, testé et reproductible avant le suivant.
