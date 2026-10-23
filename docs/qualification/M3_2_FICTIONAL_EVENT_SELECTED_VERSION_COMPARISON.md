# M3.2 — Comparaison explicite de versions sélectionnées d'un événement fictif

**23 octobre 2026 — candidature autonome de laboratoire fictif, mémoire uniquement.**

## Raison d'être

Les PR #151–153 permettent de consulter l'historique et les écarts entre versions *consécutives*. Pour un auteur, il est utile de comparer une version ancienne avec une version plus récente en ignorant les corrections intermédiaires. Il s'agit d'une comparaison de **contenu narratif inventé**, nullement d'un ordre temporel du monde fictif.

## Contrat strict

La fonction pure `compareFictionalEventVersions(book,eventId,fromVersion,toVersion)` examine d'abord les invariants de tout le carnet fictif, puis un historique **du seul eventId**. Elle exige des entiers sûrs et `fromVersion < toVersion`, refuse les versions absentes, ID étranger, valeurs non typées. Les écarts `field_differences` sont dérivés exclusivement des valeurs exactes `title`, `note`, `anchor_id` et `source_revision_id` des deux versions sélectionnées. Une correction intermédiaire ensuite annulée ne produit donc aucun écart cumulatif. La réponse, la liste et les paires sont gelées, détachées de l'état source. L'état final `withdrawn` reste visible sans inventer de changement de contenu.

La vue `M32FictionalEventNotebookPreview`, **non montée par App.tsx**, présente automatiquement une comparaison du premier au dernier état dans des éléments `<details>/<summary>` repliables et échappés par React. Le choix arbitraire des versions est possible **via la fonction pure**, pas encore via un sélecteur interactif dans la vue ; ne pas prétendre le contraire.

Neuf tests Vitest #66–74 couvrent le cumul, l'annulation de corrections, le retrait, la version égale/inversée/non entière/non sûre, les versions absentes, les IDs étrangers, les événements intercalés, les données gelées, et l'échappement HTML. Contrat de continuité #89. Aucun stockage, SQL, IPC, réseau, changement de migration, identité Tauri ou exécution Windows opérateur.

## Checkpoint indépendant PR #153

[PR #153](https://github.com/LaurentCOLL1/Fabulaxiom/pull/153) HEAD `a211822c0618e68090633f874cde6b2c216204a8`, [source CI #40020544737](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40020544737) terminale SUCCESS ; fusion protégée `main=c581ceb5056cb8e0d61646c02d3af722afb47a3e`, [postmain #40021898423](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40021898423) SUCCESS au SHA de fusion exact. 76 étapes Windows, 88 contrats, 65 tests du carnet, Chromium 62/62 dans chaque mode, 132 Rust. Confirmation terminale dans issue #38, conservant la précédente observation `IN_PROGRESS_AT_CHECKPOINT` comme fait historique.

## Critères de fusion de la nouvelle PR

Nouvelle CI sur HEAD final : **89 contrats**, **74 tests fictifs**, Chromium 62/62 dans les deux modes, Rust sans régression et garde des deux prompts PASS. Re-fetch `main`, PR, ruleset et check-run exact, diff, reviews/threads ; fusion `expected_head_sha` seulement sous protections conformes. Puis CI postmain indépendante et commentaires successifs en issue #38.

**Barrières réelles absolues :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, source `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Bases SQLite originales v6/v7, backups, ACL, journaux, activation, migration 007, IPC writer, M3.3, ComfyUI, release, opérateur Windows interdits sans autorisation distincte.
