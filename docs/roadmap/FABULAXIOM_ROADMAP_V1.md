# Fabulaxiom — V1 Roadmap

> **25 octobre 2026 — PR #170 MERGED, source/postmain SUCCESS indépendantes.** Source `458f58ad6960b72b81fbfbe588f90168e36c3975`, [CI #40155313316](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40155313316) ; squash `main=93eba0ae4801e5a0a73121fef305dc9212e52761`, [postmain #40156277835](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40156277835), chacune SUCCESS (80 Windows, 104 contrats, 96 Vitest fictifs, Chromium 82/82 chaque mode, 132 Rust), `Protect main` actif. Issue #38 [checkpoint terminal](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6392779819).
>
> **G2-B0 déclaré exécuté par l'opérateur après consentement exact :** quatre noms `.sqlite3` en production M1.5, un en isolé M2.5, `OBSERVED_PARTIAL_ONLY` sans STOP déclaré ; aucune preuve de non-écriture ou d'identité historique ([observation](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6393215331)). Consentement B0 consommé.
>
> **G2-B1 nouveau candidat** : [contrôle d'un marqueur M1.5 de petite taille](../qualification/M3_2_G2B1_ACTIVATION_SELECTOR_REVIEW_20261025.md) : nouvelle lecture du contenu du marqueur choisi, jusqu'à 256 octets, pour comparer son nom cible aux 4 fichiers recensés, sans ouvrir SQLite ni publier de chemin/nom. **`PREPARED_NOT_EXECUTED`** ; CI source-only AST et 10 refus inventés attendus mais non prouvés à ce checkpoint ; nouveau périmètre et consentement exact distinct obligatoires. Aucun G2B PASS par ce candidat.
>
> **STOP inchangés :** `G2B=NOT_ACCEPTED`, `WRITER=NOT_PROVEN`, source `PARTIAL_LOCAL_IDENTITY_ONLY`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, #35 OPEN/DRAFT ; M3.1 v7 et autres rôles `NOT_ASSESSED`. Aucune opération opérateur Windows effectuée par cette PR, aucun original SQLite, sidecar, ACL, backup, marqueur, migration 007 ou IPC writer touché par CI.


> **25 octobre 2026 — PR #169 MERGED, source et postmain SUCCESS indépendamment.** Source `67e2b400510fe4bade797a9fd73997f892ded1ad`, [CI #40127450956](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40127450956) `completed/SUCCESS`, fusion protégée `main=4ea2c5f9ad380863c5634dae65faac9831b1cec3`, [postmain #40128407418](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40128407418) `completed/SUCCESS` au SHA exact ; job Windows **79 étapes toutes réussies**. [Issue #38 : observation terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6392307076). La proposition exacte [G2-B0](../qualification/M3_2_G2B0_METADATA_ONLY_OPERATOR_REVIEW_20261024.md) demeure **PREPARED_NOT_EXECUTED** et exige un consentement local nouveau, ciblé, distinct.
>
> **Tranche candidate source-only, non encore qualifiée :** `tools/m32_g2b0_ast_static_review.ps1` et une étape du runner GitHub Windows **parsant seulement** le bloc G2-B0 via `Parser.ParseInput`, contrôlant la forme des commandes/méthodes, refusant 10 altérations fictives en mémoire, sans jamais exécuter le bloc opérateur. Contrat de continuité #104 ; objectifs non prouvés **80 étapes Windows**, **104 contrats**, 96 Vitest fictifs, Chromium 82/82 normal + 82/82 CSP strict, 132 Rust. Le garde AST ne certifie ni l'OS, ni la non-écriture, ni l'absence de race/file ID ou d'écrivain ; même un succès CI ne vaut pas autorisation G2. Nouveau HEAD source, CI terminale au SHA exact, diff/reviews/threads, `Protect main`, fusion protégée avec `expected_head_sha`, puis postmain indépendante.
>
> **STOP inchangés :** G2-A `PASS_METADATA_ONLY_OWNER_REPORTED` (consentement épuisé) ; G2-B `NOT_ACCEPTED`, origine `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2-C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Deux racines connues seulement ; M3.1 v7 et autres rôles `NOT_ASSESSED`. Aucun Windows opérateur, SQLite originale v6/v7, backup, ACL, journal, marqueur, migration 007 ou IPC writer touché. Les anciennes CI sont uniquement historiques.


> **Checkpoint 24 octobre 2026 :** PR #168 MERGED à `main=a03cc5dad68aaf4cb78c39520de130960dc565f8`, CI source #40117705107 et postmain #40122346098 SUCCESS séparément, 79 Windows/102 contrats. Suivant : [bloc G2-B0 proposé pour revue et approbation opérateur spécifique](../qualification/M3_2_G2B0_METADATA_ONLY_OPERATOR_REVIEW_20261024.md), non exécuté, ne couvrant que deux dossiers de métadonnées ; aucun G2B complet, G3 ni témoin historique. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`.

> **Checkpoint terminal 24 octobre 2026 :** PR #167 MERGED, `main=533bdb27480a2b6dbed630b148501eeaf3c34b1e`, CI source #40115530223 + postmain #40116658246 SUCCESS indépendamment (79 Windows, 101 contrats). En lecture de la seule copie privée M2.5 désérialisée en RAM : `integrity_check=ok`, FK zéro, migrations 1..6 et effectifs structuraux historiques compatibles ; **aucune attestation d'identité originale ni writer prouvé**. Nouveau [cadrage G2 SOLO](../qualification/M3_2_G2_RECOVERED_COPIES_SOLO_APPROVAL_SCOPE_20261024.md) uniquement documentaire non exécutable. G2B NOT_ACCEPTED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED.

> **Checkpoint 24 octobre 2026 :** PR #166 MERGED à `main=c1fee9638c343c51e2e0bdab6ac8fccf2340104b`, CI source #40107790950 et postmain #40108674282 SUCCESS indépendamment, 79 étapes Windows, 100 contrats. Six copies privées retrouvées représentent les cinq rôles historiques et un second manifeste M2.4 : intégrité de copies corroborée partiellement, **aucune attestation indépendante nouvelle**, M3.2 toujours NON ACCEPTÉE, G2B NOT_ACCEPTED et G3 STOP_UNAVAILABLE. Compte rendu GitHub expurgé : [rapprochement des pièces retrouvées](../qualification/M3_2_RECOVERED_COPIES_RECONCILIATION_20261024.md). La voie prospective nécessite une autorisation distincte ; pas de modification SQLite/ACL/bases Windows.

> **Checkpoint ultérieur 24 octobre 2026 :** PR #165 MERGED, `main=e1faacc909d4c8a693e2552e64dda57b6927473f`, CI source #40105412509 + postmain #40106296690 SUCCESS indépendamment ; 79 étapes, 99 contrats, 96 Vitest fictifs, 82/82 Chromium par mode, 132 Rust. Candidate suivante : refuser doublons de notices externes **fictives**, sans attester un des cinq rôles historiques. **M3.2 IN_PROGRESS_NOT_ACCEPTED ; G2B NOT_ACCEPTED ; G3 STOP_UNAVAILABLE.** Checkpoints #164 et antérieurs ci-dessous conservés.

> **Checkpoint ultérieur 24 octobre 2026 :** PR #164 MERGED, `main=ac7c61f779c0981d418d8b5b7bb1d4a8a725cdbe`, CI source #40101820083 et postmain #40103615181 SUCCESS au SHA exact. Nouvelle candidate : classement fictif de recevabilité des cinq preuves historiques manquantes, **aucune attestation réelle ni levée de G2B/G3**, M3.2 toujours NON ACCEPTÉE. Les checkpoints #163 ci-dessous restent historiques.

> **Mise à jour vérifiée :** PR #163 fusionnée, `main=7e4295160b927416d21e69e64f01fd6247d09e92` ; CI source #40094464488 et postmain #40095354727 SUCCESS indépendamment. Risque GLib Linux identifié, non corrigé ; M3.2 NON ACCEPTÉE, G2B–G6 inchangés. Le checkpoint #162 suivant est historique.

> **État revérifié le 24 octobre 2026 (source GitHub seulement, PR #162 terminale) :** voir [le tableau de suivi actuel](ROADMAP_STATUS_CURRENT.md). M0, M1 et M2 sont terminés et normalisés ; M3.1 a été implémentée (PR #33) et normalisée (PR #34) ; **M3.2 est en cours mais NON ACCEPTÉE**, avec PR #35 en brouillon et barrières G2-B–G6 fermées. M3.3–M3.6, M4–M9 et ComfyUI ne sont pas autorisés. Les commentaires ci-dessous « planning PR #31 merged; normalization pending » sont des **checkpoints historiques**, pas le statut actuel. La production conserve SQLite v6 sans migration 007 implicite.

The V1 is the complete first product target. It is intentionally larger than the first technical milestone.

## M0 — Environment and architecture qualification

**Status: COMPLETE + MERGED + NORMALIZED**

Deliverables completed:

- verified Windows development toolchain;
- verified Ollama endpoint and Vulkan compute backend;
- accepted Tauri 2 + React/TypeScript + Rust architecture;
- runnable desktop application;
- React → Tauri → Rust bridge;
- loopback-only read-only Ollama status integration;
- frontend and Rust tests;
- committed dependency locks;
- deterministic Windows CI.

## M1 — Persistence and project foundation

**Status: COMPLETE + MERGED + NORMALIZED**

Detailed plan:
`docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md`

Subdivision status:

- M1.1 — SQLite foundation and migration runner: **COMPLETE + MERGED + NORMALIZED**
- M1.2 — Project hierarchy schema: **COMPLETE + MERGED + NORMALIZED**
- M1.3 — No-AI CRUD service: **COMPLETE + MERGED + NORMALIZED**
- M1.4 — Text revisions and provenance foundation: **COMPLETE + MERGED + NORMALIZED**
- M1.5 — Backup and restore baseline: **COMPLETE + MERGED + NORMALIZED**

M1 deliverables overall:

- SQLite schema and migrations;
- Universe → optional Series → Novel → Chapter → Scene hierarchy;
- stable IDs;
- no-AI hierarchy CRUD;
- text version history;
- transactions and integrity checks;
- backup/restore baseline.

## M2 — Narrative entities and canonical facts

**Status: COMPLETE + MERGED + NORMALIZED.** All M2.1–M2.5 are normalized after protected PR #30 merge `f13b4f8c249866ff60a19d7895b6cfaede56398a`, exact-head Windows CI #38041908126 SUCCESS. V1 remains incomplete; M3 implementation not authorized.

Accepted detailed roadmap: `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md`.

M2.1 delivered SQLite v4 and Universe-scoped entity/alias registry. M2.2 implementation PR #23 merged at `ad7211fa2f292b8bd9812e299dbb6be96214eb89` after real Windows qualification on `b54fffd8e1f0224372e3b99cee07cb6df3203973` (13/13 interactive, 21/21 frontend and 51/51 Rust PASS, Ollama stopped, restored-active SQLite/backup/revisions preserved) and evidence-head CI `37864503602` on `a96870f823f24cb8962c9b0f43336ccb883ad5c3` (terminal success). See `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md`.

**M2.3 — Fact registry and exact revision provenance: COMPLETE + MERGED + NORMALIZED** after separate post-merge normalization acceptance.

PR #25 implemented SQLite v5 STRICT narrative fact/source registry and Rust/Tauri manual create/read/list with exact immutable revision citation spans, same-Universe validation, explicit sourced/unsourced facts and atomic rollback. Qualified code `4d3b4b6015d477c3a6a5c3750d9743174e9c44a7` (21/21 React, 61/61 Rust, 8/8 Windows operator GUI checks, controlled v4→v5 and fully preserved v4 baseline/backup); exact-evidence CI `37961014980` passed on `b015f7df80f38d75375a0e2615fd62d4c40ee1b8`. Implementation merged at `e6e80c26316f11054348a18a235fd08c600e136e`. Evidence: `docs/qualification/M2_3_IMPLEMENTATION_GATE.md`.

**M2.4 — Canon status and human review service: COMPLETE + MERGED + NORMALIZED** after separate M2.4 normalization acceptance.

PR #27 added SQLite v6 STRICT append-only review events and manual Rust/Tauri review/history/status APIs with `draft` default and seven distinct status values. Explicit `APPROVE_CANON`/`REVOKE_CANON` confirmation required. Windows-qualified code `aad56bd59fdb87be5ac1eda99b1969452bf61a26`: 21/21 frontend, 71/71 Rust, 8/8 existing GUI checks, 8/8 isolated review-service Rust tests, v5→v6 controlled migration with exact data/backup preservation. Evidence-HEAD CI `37989040863` succeeded on `b53405779b04c16525ba48a266bd096096af7020`, protected implementation merge `3a069572d00e1680c42b0f13b800e28687c5f0eb`. The reviewer label is not authenticated. Neither a dedicated React review interface nor its E2E IPC acceptance is delivered. Evidence: `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`.

**M2.5 — Usable sourced-facts and human review UI:** implementation PR #29 merged at `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1` from evidence SHA `6f55fc3fc7eab6f2288a54619c0bef70e521f47e` after exact-head CI #38040227617 (32/32 frontend, 72/72 Rust, all 13 Windows steps). Real Windows isolated UI acceptance and independent SQLite v6 verification PASS: 3 facts / 2 exact historical UTF-8 sources / 11 immutable review events, 8/8 hierarchy, 8/8 corrected synchronization, 9/9 facts, 10/10 human review. Source authority is now **COMPLETE + MERGED + NORMALIZED** after protected PR #30 merge `f13b4f8c249866ff60a19d7895b6cfaede56398a` and its own exact-head CI #38041908126 SUCCESS. No M3, AI extraction or ComfyUI implementation is authorized by this milestone closure.

Deliverables:

- characters, places, organizations, objects, events and world rules;
- aliases and renames;
- provenance down to source passage/version;
- status model: canon/draft/suggestion/variant/unknown/ambiguous/contradictory;
- fact validity periods;
- human validation workflow.

## M3 — Time, knowledge and relationships

**PLANNING PR #31 MERGED; NORMALIZATION PENDING.** Planning source `5127ced6c5e175b0919c736c658036382794487e` merged into `main=68db746754e01b441870e0653f17f10ebfc7be2f` after exact-head CI run `38050865413` (`completed/success`, one Windows job, 13/13 steps). The detailed plan is `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`. Once a separate normalization PR passes its own exact-head CI, merges under `expected_head_sha` and new `main` is re-fetched, **M3.1 only** becomes authorized for implementation through a separate bounded PR. M3.2–M3.6, production SQLite v7 migration without preflight, M4+, and ComfyUI remain unauthorized.

Deliverables:

- chronology distinct from narration order and reader reveal order;
- exact, approximate and relative dates;
- asymmetric evolving relationships;
- character knowledge/beliefs;
- narrator knowledge and reader-spoiler state;
- possessions, locations, injuries and life-state changes.

## M4 — Retrieval and narrative memory

Deliverables:

- SQLite FTS5 search;
- hierarchical summaries;
- rebuildable embeddings/indexes;
- local semantic retrieval;
- question-answering over the universe with cited sources;
- targeted context builder.

## M5 — Ollama integration

Deliverables:

- configurable model roles for writing, planning, extraction, summaries and consistency;
- model metadata inspection;
- streaming output;
- cancellation;
- task queue;
- strict JSON validation and bounded retries;
- context/memory budgeting;
- graceful Ollama failure handling.

## M6 — Consistency engine

Deliverables:

- deterministic contradiction rules;
- AI-assisted analysis where useful;
- separation of proven contradictions, suspicions and insufficient information;
- source-linked alerts;
- severity and proposed fixes;
- no automatic manuscript correction.

## M7 — Assisted writing

Deliverables:

- free editing without AI;
- scene goals and planning;
- continuation proposals;
- rewrite selection;
- style variants;
- dialogue assistance;
- targeted retrieval of relevant facts;
- post-generation consistency checks;
- extraction of proposed new facts followed by user validation.

## M8 — Advanced V1 narrative management

Deliverables:

- relationship map at a chosen time;
- shared multi-novel timeline;
- plot-thread tracking;
- clue/mystery/promise/reveal tracking;
- isolated “what if” branches;
- retcon impact analysis;
- spoiler management;
- dashboards for contradictions and pending validations.

## Extension proposée — Atelier de références visuelles et ComfyUI local

**PROPOSAL ONLY — NOT AUTHORIZED FOR IMPLEMENTATION**

See `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md` and issue #19.

The user requests images of narrative characters, scenes, events and situations as optional inspiration and visual evaluation aids. Potential phases: local image import/gallery and associations after narrative identity foundation; then an opt-in ComfyUI local connector and variation/consistency workflows. The exact milestone and subdivision authorization must be accepted through a separate roadmap governance PR. This proposal does not change M2.1's schema-only boundaries or authorize any ComfyUI code.

## M9 — Import, export, resilience and distribution

Deliverables:

- assisted import of existing text;
- Markdown export;
- DOCX export;
- EPUB export;
- documented full-universe export/reimport;
- local visual references;
- automatic/exportable backups;
- tested restore;
- Windows packaging and installer;
- release qualification.
