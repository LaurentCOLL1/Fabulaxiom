# P3aa — qualification de la CI indépendante post-fusion (#361)

**Date : 14 novembre 2026.** Périmètre : laboratoire fictif React non monté, aucune admission M3.2.

## Source et fusion protégée

- Parent `main=811e743040ce2e3681d4b384e18eafdc6afae9bb` ; postmain parent #43580142753 `completed/SUCCESS` au SHA exact.
- PR #361 HEAD `61e392e78499d55e5be489c5a99881387b12b050`; [CI source #43580781801](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43580781801) `completed/SUCCESS` au HEAD exact. Job « Windows frontend and Rust checks » : 93/93 étapes SUCCESS ; 37 fichiers / 485 tests Vitest PASS, 12 cas P3aa déclarés dans `src/m32ExplorerRevisionSourceFilter.test.tsx`.
- Protect main ACTIVE, strict=true, bypass_actors=[] ; reviews=[] et threads=[] ; squash avec `expected_head_sha=61e392e78499d55e5be489c5a99881387b12b050` ; `main=fc50e9d570609c84876d19173915c19ef87d35f4`.
- [CI postmain indépendante #43589717137](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43589717137) `completed/SUCCESS` au même SHA exact ; 92 étapes SUCCESS, une étape destinée aux seules PR SKIPPED.
- Journal de gouvernance [issue #38, entrée append-only](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6876536092) créé au moment de la fusion avant constat du PASS postmain. Ce rapport qualifie désormais ce résultat sans réécrire les événements passés.

## Matrice de preuves partielles

| Tâche | Élément contrôlé | Limite non couverte | Décision |
| --- | --- | --- | --- |
| M32-071 | Filtre exact `source_revision_id` sur les ancres affichées en laboratoire | Navigation et inspection de sources historiques réelles | OUVERTE |
| M32-075 | HTML hostile échappé, état sélection séparé du filtrage fictif | Accessibilité réelle et fonctionnement hors ligne de l'application | OUVERTE |
| M32-078 | Tests fictifs + source Windows 93/93 et postmain SHA exact | Traçabilité complète de chaque exigence de production et preuves R1–R9 | OUVERTE |
| M32-081 | Vue historique `revoked`/`superseded`, sélection explicite préservée | Correction/révocation persistante prouvée et historique authentifié | OUVERTE |
| M32-082 | Ordre Unicode scalaire et refus d'un Universe étranger dans la fixture | Isolation réelle de données entre Universe, IDs et stockage Windows | OUVERTE |

Ces tests ne créent aucune jointure authentifiée entre ID de révision fictif et roman ou scène. Aucun test M32-071/075/078/081/082 n'est réputé complet par ces seules preuves.

## Gate inchangée

**M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %).** Checklist **8/104 closes, 96 ouvertes**. PRODUCT_FIRST_PARALLEL_SAFETY maintenue. R1–R9 et writer NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE. Aucune opération sur v6/v7 original, M:\Fabulaxiom, Greenfield, backups, IPC writer, migrations 007, Hello ou recovery. main/WAL/SHM, WAL-index vivant, ABA NOT_PROVEN ; glib #160 OPEN. Continuer sur preuves fictives et sécurité source-only, sans promouvoir à l'acceptation runtime.
