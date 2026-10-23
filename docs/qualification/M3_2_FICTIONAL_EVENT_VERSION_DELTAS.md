# M3.2 — Différences de contenu entre versions d'événements inventés

**23 octobre 2026 — candidate source-only strictement fictive, en mémoire RAM, non reliée à l'application Tauri.**

## Problème
Un auteur peut consulter l'historique de corrections, mais il est difficile d'identifier précisément quel champ a été modifié entre deux versions. Éviter de comparer une version à un autre événement lorsque les actions sont intercalées. La création initiale et la pierre tombale d'un retrait ne constituent pas un changement de contenu.

## Solution testable
Dans `auditedFictionalEventHistory`, après validation du carnet fictif complet, regrouper les versions par identifiant explicite et calculer `changed_fields` uniquement par rapport à la version précédente du même événement : `title`, `note`, `anchor_id`, `source_revision_id`. Chaque tableau de modifications est gelé, comme les copies détachées des versions et audits. Pas de reconstruction ni d'authentification des données réelles.

La vue isolée `M32FictionalEventNotebookPreview` affiche « modifications de contenu : titre, note, ancre, révision » selon les champs effectivement différents, ou « aucune » pour une création ou un retrait sans modification. Elle conserve le composant natif `<details><summary>` repliable et l'échappement JSX. Elle ne prétend pas connaître une date ou un ordre dans l'univers.

Huit tests Vitest #50–57 : création sans changement, titre seul, note seule, liaison ancre/révision, retrait sans changement, intercalage entre plusieurs événements, immutabilité du résultat, HTML échappé. Contrat de continuité #87. Aucune édition originale, aucune requête SQL, aucun IPC, aucune production.

## Checkpoint précédent terminal distinct
[PR #151](https://github.com/LaurentCOLL1/Fabulaxiom/pull/151) source finale `ab0ffd3e1c0d08cb57325a2f5ef91c1967616716`, [CI source #40010733862](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40010733862) SUCCESS ; merge `main=2e0b29bfc2d2698a636f4adc41d5b4e5a87c3ece`, [postmain #40012175419](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40012175419) SUCCESS exacte (76 Windows, 86 contrats, 49 événements, Chromium 62/62 deux modes, 132 Rust). Première tentative [#40010433915](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40010433915) FAILURE sur SHA différent, non réutilisée.

## Critères de qualification de la nouvelle PR
87 contrats, 57 tests de carnet, Chromium 62/62 deux modes, Rust sans régression, nouveau SHA avec CI terminale. Refetch `main`, PR, ruleset, CI, revues, threads, diff. Fusion uniquement `expected_head_sha`, puis postmain indépendante dans l'issue #38.

**Gates réels inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, identité source `PARTIAL_LOCAL_IDENTITY_ONLY`, absence d'écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Pas de SQLite v6/v7 réelle, backup, ACL, journaux, marqueur, migration 007, IPC writer, M3.3, ComfyUI, release ni validation opérateur.
