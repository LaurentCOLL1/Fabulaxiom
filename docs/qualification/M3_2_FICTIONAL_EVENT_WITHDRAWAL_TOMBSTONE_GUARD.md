# M3.2 — retrait fictif : pierre tombale sans réécriture silencieuse

**23 octobre 2026 — proposition source-only, objets de démonstration inventés en RAM.**

## Défaut démontré

Après le contrôle structurel de PR #148, un historique artificiellement fourni pouvait encore présenter un événement avec `version=1` déjà `withdrawn` et un audit `created`, ou modifier le titre, la note ou les références historiques lors de l'ajout d'une pierre tombale. Ces formes ne sont pas produites par les opérations humaines `create/amend/withdraw` du carnet fictif.

Le validateur refuse désormais tout retrait sans version antérieure ainsi que tout retrait dont `title`, `note`, `anchor_id` ou `source_revision_id` diffère de la version directement précédente. Cinq nouveaux tests Vitest #28–32 injectent des structures falsifiées (retrait initial, remplacement du titre, de la note et des références ancre/révision), puis conservent un scénario positif amendement et retrait. Les événements et audits de l'application Windows réelle ne sont pas consultés.

**Limite importante :** aucune signature, journal append-only protégé ou source externe indépendante. Un adversaire qui réécrit de manière cohérente tout un historique inventé n'est pas détecté. Les contrôles de chronologie fictive ne prouvent jamais l'authenticité des données, la fermeture d'une connexion écrivain SQLite ou l'acceptation de M3.2.

## Checkpoint source antérieur vérifié

PR [#148](https://github.com/LaurentCOLL1/Fabulaxiom/pull/148) source `f4ff680ef82d91e2b10fe7ea9701e90d073453b4`, CI [#39985794291](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39985794291) SUCCESS, fusion protégée `main=4a8d09d99c1b2b2eb716b17acf733981c51ac340`, postmain [#39987313809](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39987313809) SUCCESS au SHA exact. Les deux jobs comprennent 76 étapes Windows, 83 contrats de continuité, 27 tests de carnet d'événements, Chromium 62/62 par mode et 132 Rust principaux.

**Qualification de la présente candidate :** nouvelle CI de PR sur **son SHA exact**, lecture des logs complets, diff, reviews/threads et `Protect main` avant toute éventuelle fusion avec `expected_head_sha`. Ne jamais réutiliser les CI de #148.

**STOP inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, origine `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucun original SQLite v6/v7, sauvegarde, ACL, WAL, marqueur, migration 007, IPC writer, M3.3, ComfyUI, release ni opération sur le Windows opérateur.
