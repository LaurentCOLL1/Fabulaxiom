# M3.2 — Prévisualisation fictive contrôlée d'une paire de versions

**23 octobre 2026 — laboratoire source-only, RAM inventée, aucun runtime réel.**

## Motivation
La PR #154 a ajouté une fonction de comparaison explicite de deux versions d'un même événement fictif, mais la prévisualisation isolée n'affichait que le bilan de la première à la dernière version. Cette tranche permet à un **appelant de laboratoire** de passer `selection={event_id,from_version,to_version}` comme prop du composant `M32FictionalEventNotebookPreview`. Ce n'est pas encore un menu que l'utilisateur de l'application Windows peut actionner, et le composant n'est pas monté dans `App.tsx`.

Sans sélection, la vue existante reste identique. Avec une sélection explicite, une région `aria-label="Comparaison fictive demandée explicitement"` affiche les valeurs avant/après exactes de ces deux versions inventées, ou « aucun écart », tout en gardant le détail historique et le bilan cumulatif actuel. Les références supprimées restent `(non lié)`, les champs vides restent `(vide)` et React échappe les chaînes au rendu.

Un objet `selection` null, un tableau, une version absente, égale, inversée ou fractionnaire, ou un ID issu d'un autre univers sont **refusés**. Le validateur de carnet contrôle l'historique complet avant toute comparaison. Aucune date, provenance authentifiée ou chronologie mondiale n'est déduite ; aucune modification des événements n'est autorisée.

Neuf tests Vitest #75–83 : absence de sélection, milieu→fin, événements intercalés, versions inversées/non entières, versions absentes, univers étranger, forme de sélection mal définie, injection HTML et retrait sans différence de contenu. Contrat Python #90. Aucun SQL, IPC, réseau, disque, migration ni appareil Windows opérateur.

## Preuve de départ PR #154
[PR #154](https://github.com/LaurentCOLL1/Fabulaxiom/pull/154) source `5d91e198e455c33a2782804310377f19ec746bee`, [CI #40025773741](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40025773741) terminale SUCCESS ; fusion protégée `main=391cc3972c87b7f3ae0fda033b55971f268d7fbe`, [postmain #40027154468](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40027154468) terminale SUCCESS. Chacune : 76 étapes Windows, 89 contrats, 74 tests du carnet fictif, 62/62 Chromium par mode, 132 Rust.

## Gates de la nouvelle PR
Exiger au HEAD final **90 contrats**, **83 tests fictifs**, Chromium 62/62 dans chaque mode, Rust sans régression et garde des deux prompts PASS. Re-fetch GitHub, diff, reviews/threads, ruleset Protect main et status check exact issu du bon GitHub App ; fusion seulement `expected_head_sha` puis postmain indépendante. Reporter en issue #38 sans réécrire les observations historiques.

**STOP réel :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, identité source `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucune SQLite originale v6/v7, sauvegarde, ACL, WAL/sidecars, marqueur d'activation, migration 007, IPC writer, M3.3, ComfyUI, release ou machine opérateur.
