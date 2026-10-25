# M3.2 — Plafond de preuve SOURCE-ONLY G2B → G3 (25 octobre 2026)

**STATUT : CLASSIFICATION DOCUMENTAIRE / SYNTHÈSE SOURCE-ONLY.** Ne constitue ni attestation indépendante, ni G2B accepté, ni G2C/G3 autorisé, ni consigne d'exécution Windows. Le vocabulaire de preuve est volontairement borné aux sources explicitement observées.

## Dernier checkpoint GitHub vivant au moment de cette PR

La [PR #178](https://github.com/LaurentCOLL1/Fabulaxiom/pull/178) a été fusionnée par squash protégé : source exacte `c13a166f07c4850258628db5279594699b5ccfe8`, [CI source #40229362824](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40229362824) `pull_request/completed/SUCCESS` (81/81 Windows) ; `main=dd5e6f17c6a4d71f4ac19ba0da4821a362f2af7d`, [CI postmain indépendante #40230066592](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40230066592) `push/completed/SUCCESS` (80 SUCCESS + 1 SKIPPED attendu, 0 FAILURE). Journaux des deux SHA : **112 contrats**, **96 Vitest fictifs**, **Chromium 82/82** normal et **82/82** stricte, **132 Rust**, `toy_26` PASS sous feature opt-in. [Observation terminale append-only issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6402812191). Ce checkpoint ne qualifie qu'un état source à deux SHA et doit être re-fetch avant tout futur travail.

## Quatre catégories NON substituables

| Catégorie | Matière vérifiable | Plafond de preuve ; interdiction d'inférence |
| --- | --- | --- |
| **Rapports du propriétaire** | G2-A métadonnées `PASS_METADATA_ONLY_OWNER_REPORTED` ; B0 quatre noms de fichiers SQLite en M1.5 et un en M2.5 ; B1 `RESTORED` et exactement un nom sélectionné, `OBSERVED_PARTIAL_ONLY_OWNER_REPORTED`. Les consentements exacts précédents sont consommés. | Ne certifient pas par un tiers l'identité historique de la source, son schéma, le contenu/état journal, ni un écrivain absent entre deux observations. G2B `NOT_ACCEPTED`. |
| **Contrats et CI sur sources/fixtures fictives** | `toy_14` à `toy_26` (SQLite en RAM), contre-exemples FileId/partage Win32 sur fichiers jetables, tests offline refusant des dérives ; source et postmain exact SHA. | Prouvent seulement le résultat des jeux de tests à ces SHA. Une double lecture sale stable, `query_only`, `total_changes`, `data_version`, FileId ou absence de fichiers annexes ne prouvent **ni transaction validée ni quiescence** sur Windows opérateur. |
| **Audit de code/architecture** | [Décision A/B/C post-B1](M3_2_POST_G2B1_CUSTODY_ROUTE_DECISION_20261025.md), [audit de propriétaire Tauri préouvert](M3_2_G3_TAURI_OWNER_INTEGRATION_AUDIT.md), [décision G3 source](M3_2_G3_SOURCE_ACQUISITION_DECISION.md) : pas de propriétaire SQLite réel préouvert et non migrant qualifié ; les entrypoints connus peuvent ouvrir/migrer. | Une preuve de **ce qui manque dans le code** n'est ni un handle opérateur authentifié, ni une preuve de non-écriture ou de capture sans effet de bord. Un opener neuf n'invente pas un propriétaire de confiance. |
| **Attestation externe indépendante** | Dossier historique encore `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, six copies récupérées sans attestation indépendante ; prospective `NOT_STARTED`. | L'attestation **n'existe pas ici**. Ne jamais attribuer ce rôle aux rapports du propriétaire, à la CI, à un agent, à un test fictif ou à une répétition de métadonnées. |

## Routes de custody : décision inchangée

| Route | Condition absente et non déduite de la CI | Verdict réel |
| --- | --- | --- |
| **A** propriétaire SQLite **préexistant**, authentifié, déjà ouvert sans migration et sous médiation complète ; Online Backup vers RAM | Aucune connexion originale de confiance démontrée ; le jouet d'owner ne s'applique qu'à une connexion inventée. | `UNAVAILABLE_NOT_PROVEN` |
| **B** custody à froid, identité et quiescence continues, writers/journaux/ABA/WAL/rollback maîtrisés, capture sans migration | Ni scan B0/B1 ni stable FileId avec `FILE_SHARE_WRITE`, ni double échantillon, ni `data_version` ne garantissent ce continuum. | `NOT_PROVEN` |
| **C** développement de sources **nouvellement inventées** et futures simulations | Ne contient ni v6/v7 protégée, ni identité historique indépendante, ni acceptation M3.2 sur poste réel. | `DEVELOPMENT_ONLY` |

Références primaires limitées aux propriétés techniques : [SQLite `PRAGMA data_version`](https://www.sqlite.org/pragma.html#pragma_data_version) détecte des **commits tiers entre lectures de la même connexion**, pas un écrivain inexistant ; [SQLite shared-cache et `read_uncommitted`](https://www.sqlite.org/sharedcache.html#read_uncommitted_isolation_mode) autorisent des lectures sales dans cette configuration particulière ; [Microsoft `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew) définit `FILE_SHARE_WRITE` comme une permission d'ouvertures d'écriture compatibles ; [SQLite Online Backup](https://www.sqlite.org/backup.html) décrit un mécanisme de copie cohérente **conditionné à une connexion source réelle appropriée**, qui n'est pas fournie par le jouet. Ces documents ne donnent aucune autorisation opérateur.

## Invariant fail-closed pour la reprise suivante

- **Sans attestation indépendante, source/owner réel vérifié et nouvelle autorisation locale exacte, ne pas promouvoir :** G2B `NOT_ACCEPTED`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 `OPEN/DRAFT`.
- **Aucune nouvelle exécution opérateur** : ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer. Le protocole exige une proposition locale et une autorisation distincte pour toute action future, non incluse ici.
- Les rapports B0/B1 restent `OBSERVED_PARTIAL_ONLY_OWNER_REPORTED`, et les consentements utilisés ne sont **pas renouvelés**. M3.1 v7 isolée et autres rôles `NOT_ASSESSED` par ces rapports.
- Cette synthèse n'ajoute aucun test Rust ou procédure ; le **113e contrat offline** vérifie que la classification ci-dessus et le JSON vivant demeurent explicitement non-promus. Aucune ancienne CI ne vaut pour le futur HEAD ; PR source et postmain doivent chacun être conclus sur leur propre SHA.

**Conclusion : NO_ELIGIBLE_REAL_G3_STRATEGY_STOP**, source-only. Cette formulation ne vaut pas nouvelle gate ni attestation externe.
