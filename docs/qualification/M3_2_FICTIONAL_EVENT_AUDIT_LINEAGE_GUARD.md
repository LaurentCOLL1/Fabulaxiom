# M3.2 — refus d'historiques d'événements fictifs incohérents

**23 octobre 2026 — strictement source-only, navigateur fictif / objets TypeScript en mémoire.**

## Lacune couverte

L'ancien validateur `inspectFictionalEventNotebook` vérifiait les listes `events` et `audit` séparément. Un appelant pouvait fournir un carnet fictif dont une version d'événement n'avait pas d'entrée d'audit correspondante, ou dont l'action/numéro d'audit ne correspondait pas à la version. La validation ne devait pas présenter ces journaux comme « sûrs ».

La nouvelle qualification impose :
- **Une opération auditée pour chaque version** : cardinalité égale et alignement exact, dans l'ordre d'ajout, de `event_id` et `version` ;
- **Action attendue** : version 1 = `created` ; version supérieure = `amended` ou `withdrawn` selon la dernière pierre tombale ;
- **Identifiants fictifs monotones** : premières créations `<univers>-event-0001`, `...0002` etc., puis `nextId = créations + 1` ; aucun réemploi silencieux ni trou ;
- **Explication non vide et bornée** et refus des versions étrangères, orphelines, sautées ou contradictoires.

Les tests Vitest ajoutés simulent volontairement des carnets falsifiés (audits retirés, dupliqués, échangés, événements réordonnés, identifiants et compteur fabriqués). Un carnet multi-événements avec correction et retrait reste accepté. Aucun appel réseau, disque ou SQLite.

## Frontière de preuve

L'alignement structurel entre des entrées d'audit **n'atteste pas** qu'un acteur ne peut pas modifier simultanément un texte historique et son audit : ce n'est **ni** une signature, ni une attestation indépendante, ni une preuve d'immuabilité physique. Les données de démonstration sont fabriquées ; le V6 actif, V7 isolé, backup, marqueur, sidecars et writer IPC ne sont pas accessibles depuis ce code. L'application Windows et la migration 007 restent hors périmètre.

Le checkpoint GitHub préalable est PR #147 source `472c13344c2d6fe7c75c1812acf05f3236799e65` CI #39979848160 SUCCESS, fusion `main=7e67c5daf98821700f176965dadd52bafd0064fa`, postmain #39981173101 SUCCESS (76 Windows, 82 handoff, 62/62 Chromium par mode, 132 Rust). Cette nouvelle PR n'est pas qualifiée tant que sa propre CI au SHA exact n'est pas terminalement réussie, logs/reviews/threads/ruleset contrôlés et fusion `expected_head_sha` effectuée.

**Gates réels préservés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, provenance `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT.
