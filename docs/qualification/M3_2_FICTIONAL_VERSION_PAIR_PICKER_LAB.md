# M3.2 — Sélecteur interactif de deux versions fictives (laboratoire isolé)

**Candidate du 24 octobre 2026 — source-only et RAM inventée. Aucune utilisation de l'application Windows réelle.**

## Périmètre

Après la PR #155, la prévisualisation accepte une prop `selection` validée, mais n'a pas de menu interactif. Cette tranche crée `M32FictionalEventVersionPairLab.tsx`, **monté exclusivement** dans la page Chromium de laboratoire `m32BrowserLab.tsx`, jamais dans `App.tsx`. Trois `select` natifs et étiquetés permettent de choisir une identité stable d'événement, puis deux versions strictement croissantes appartenant au même événement et au même Univers inventé. Changer l'événement ou la version de départ efface la sélection obsolète. Les événements retirés restent consultables ; aucun changement de contenu fictif n'est attribué à la seule pierre tombale.

La fixture est construite exclusivement en RAM inventée : deux événements, deux corrections explicites, une justification, un retrait. Une étiquette `<script>` factice demeure inerte grâce à l'échappement React. Aucune API de stockage, fetch réseau, SQL, IPC, calendrier calculé, ordre mondial, provenance privée, migration, écriture opérateur ni date inférée.

## Qualifications à obtenir avant fusion

Quatre nouveaux tests Vitest #84–87 : état vierge, retrait historique conservé, refus d'origine SQLite forgée, échappement HTML. Huit nouveaux cas Chromium #63–70, réellement exécutés dans **chacun** des modes normal et CSP strict, avec staging exact des Git objects sur checkout Windows jetable. Contrat de continuité #91 : PR #155 et deux CI prouvés séparément, code hors `App.tsx`, manifest allowlist, absence d'API persistante et mise à jour des deux prompts, deux handoffs et roadmap.

**Seuils attendus, non anticipés :** 91/91 contrats, 87 tests événementiels, 70/70 Chromium par mode, 132 tests Rust sans régression. Nouvelle CI sur le SHA final de cette PR et preuve source exacte **obligatoires**.

## Preuve historique de départ

[PR #155](https://github.com/LaurentCOLL1/Fabulaxiom/pull/155) HEAD `45b5febd3dbd594e28eab51bea62806ff3e43017` ; [CI source #40029859356](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40029859356) completed/SUCCESS ; fusion protégée `ccf5ba31b35c57b5ea572109e64015fdc1ca35cd` ; [CI postmain #40030841723](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40030841723) completed/SUCCESS. Chacune : 76 étapes Windows, 90 contrats, 83 tests fictifs, Chromium 62/62 deux modes, 132 Rust.

**STOP réel :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Bases v6/v7, sauvegardes, ACL, sidecars, marqueur, migration 007, writer IPC, M3.3, ComfyUI et release interdits.

**Gate GitHub :** re-fetch HEAD/source CI, changed files, reviews, threads, Protect main et expected_head_sha avant toute fusion. L'issue #38 recevra une observation séparée sans réécrire les checkpoints antérieurs.
