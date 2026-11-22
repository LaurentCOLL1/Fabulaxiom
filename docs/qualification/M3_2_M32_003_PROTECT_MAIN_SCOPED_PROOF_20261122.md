# M32-003 — preuve de protocole Protect main, portée documentaire (22/11/2026)

## Critère et limite de clôture

Exigence : **« Revoir le diff, les reviews, threads et le ruleset Protect main pour chaque future PR »**. La qualification proposée porte **uniquement sur la mise en place et l'exécution documentée de ce protocole**, jamais sur les PR futures non encore créées. Pour chaque nouvelle PR, le contrôle complet demeure **OBLIGATOIRE** avant tout squash. Un contrôle d'une PR passée ne vaut ni approbation automatique ni dispens(e) de revue pour la suivante.

## Contrôles réels examinés, non inférés

| Périmètre | Observation vérifiée |
| --- | --- |
| PR #415, HEAD attendu | `f452c3f37f760f8c35a7be7370d95a12c7d9bd52`, base protégée `856ccba4af54d7c517f98db9471e8e2c5ce84cae` |
| #415 diff | 12 fichiers, inventaire 20 outils/20 tests Python PR35, handoff/roadmap et tests source-only ; aucune modification runtime, `main` non modifié directement |
| #415 reviews/threads/comments | trois listes vérifiées, **0 review, 0 thread, 0 commentaire**, donc 0 conversation en attente au moment de la décision |
| #415 CI de source | run **#45006510217** event `pull_request` completed/SUCCESS au HEAD exact ; job Windows **#137159200585**, étape **28** « M3.2 living handoff source-only contract checks » completed/SUCCESS, 93 étapes au total ; un succès d'étape ne démontre pas chaque assertion indépendante |
| Protect main | ruleset **#24895490** `active` ; `bypass_actors=[]` ; `strict_required_status_checks_policy=true` ; contrôle requis « Windows frontend and Rust checks » ; PR obligatoire, squash guarded `expected_head_sha` |
| #415 fusion | READY après revue ; `squash` guardé `expected_head_sha=f452c3f37f760f8c35a7be7370d95a12c7d9bd52` ; nouveau `main=7bc17f9cb2c9b8d17d7b0cf53f8446e9f6bdf7fb`, pas de bypass |
| Parent postmain | #414 `#45006027231` completed/SUCCESS sur `856ccba4af54d7c517f98db9471e8e2c5ce84cae` avant la fusion #415 |
| Nouveau postmain indépendant | #45029746719 event `push` sur `7bc17f9cb2c9b8d17d7b0cf53f8446e9f6bdf7fb`, **IN_PROGRESS_UNQUALIFIED** au moment du dossier ; ne pas annoncer PASS sans terminal SUCCESS |
| Journal | issue #38 commentaire **#7080128468** append-only consignant le merge #415 et la CI non qualifiée |

## Décision proposée sous contrôle CI

**M32-003 [x] CLOSED_SCOPED — procédure de qualification des PR démontrée**, sous réserve d'une CI Windows SUCCESS sur le HEAD exact de cette PR de normalisation et d'un postmain indépendant. Les traces précédentes étayent le protocole ; elles ne créent aucune autorité opérateur et ne qualifient aucun writer. La case cochée est documentaire/protocolaire et **n'autorise aucune dérogation future** aux contrôles. À tout manquement futur, arrêter la fusion et rouvrir le dossier de qualification.

La preuve `CHECKLIST_SCOPED SHA=f452c3f37f760f8c35a7be7370d95a12c7d9bd52 RUN=#45006510217` identifie explicitement un workflow **source** déjà terminé et qualifié, pas une CI future. Le job 137159200585, étape 28, est un repère de CI, **pas** une attestation de recette Windows opérateur ni d'un test individuel. Le nouveau SHA de cette PR est à qualifier séparément. M32-007/050/078/101/102/103 restent OPEN_NOT_ACCEPTED.

## Contrôle récurrent indispensable pour chaque PR future

Pour chaque PR : relire le diff exact et les fichiers sensibles, les reviews, threads et commentaires non résolus ; revérifier HEAD/base et `mergeable`, ruleset #24895490 en enforcement active bypass=[], job Windows requis strict et SUCCESS au **nouveau HEAD exact**, postmain parent exact ; passer DRAFT à READY, guarded squash avec `expected_head_sha`, nouveau `main`, puis run indépendant `push` terminé sur ce SHA et entrée append-only #38. **Si un état est PENDING ou FAIL : STOP**, aucune fusion. En cas de modification du ruleset, de nouveau bypass ou de contrôle manquant : réévaluation et non-admission.

Gate global **M3.2 IN_PROGRESS_NOT_ACCEPTED**, PRODUCT_FIRST_PARALLEL_SAFETY. STOP Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5, D3b-5 STOP ; main/WAL/SHM, live SQLite WAL-index/ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
