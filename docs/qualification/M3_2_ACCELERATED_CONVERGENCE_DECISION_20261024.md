# M3.2 — Décision de convergence accélérée (24 octobre 2026)

**AUCUNE AUTORISATION de nouvelle source opérateur, d'accès aux SQLite originales ou de changement de critères d'acceptation.** Document de planification et de séparation des tâches source-only.

## Réalité vérifiée

PR #157 source `956154c4be0645536d356a48c6d75d0bf92bdc37`, CI #40061031363 `completed/SUCCESS`; squash protégé `main=645b50f438d12165d0eae46f1c3d586f07819480`; CI postmain #40061815168 `completed/SUCCESS`, indépendante. Chacune : 76 étapes Windows, 92 contrats, 90 Vitest de carnet inventé, Chromium 76/76 normal et CSP strict, 132 Rust PASS. Ces validations portent uniquement sur code et fixtures ; **M3.2 demeure IN_PROGRESS_NOT_ACCEPTED**.

## Chemin critique — aucun faux raccourci

Issue #36 maintient historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, cinq rôles non prouvés :

| Rôle exact | Constat historique | Étape nécessaire |
|---|---|---|
| `production/pre_m24_early_manifest` | `OBSERVED_SHA256` seulement | Preuve indépendante antérieure du manifeste et de son digest |
| `acl/original_acls` | `OBSERVED_SHA256` seulement | Preuve indépendante des ACL archivées, contenu/digest et rôle |
| `acl/pre_repair_json` | `OBSERVED_SHA256` seulement | Ancrage indépendant du JSON de réparation et de son rôle |
| `production/activation_marker` | `UNANCHORED_OBSERVED` | Authentification historique des octets du marqueur, pas seulement du nom |
| `m25/isolated_v6` | `UNANCHORED_OBSERVED` | Lien indépendant entre ce rôle et l'artefact précis |

Deux voies distinctes : **A** retrouver et qualifier des preuves **préexistantes indépendantes** (date, rôle, digest, authenticité, conservation) ; **B** si une preuve reste introuvable, soumettre à l'opérateur une proposition **nouvelle et prospective** de référence de confiance, avec garde et politique de restauration propre, sans jamais prétendre restaurer la confiance historique. La voie B exige autorisation supplémentaire explicite et procédure détaillée avant tout test ou accès machine. L'absence de relecteur indépendant ne permet pas de fabriquer son attestation. Le fait de cocher des cases dans GitHub ne débloque pas G2B.

Issue #38 : prospective `NOT_STARTED`, writer `NOT_PROVEN`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`. Pour tout accès réel : examen d'identité/provenance du source, absence d'écrivain, sidecars/journaux, intégrité du chemin et sauvegardes, décision autorisée ; des fixtures RAM ne satisfont aucun de ces points. PR #35 reste OPEN/DRAFT.

## Nouvelle politique de vitesse (sans affaiblissement)

1. **Une PR cohérente pour 2–3 petits travaux source-only compatibles**, et non une PR par bouton/test. Exemple cette candidate : répétition contrôlée d'une version fictive, plus plan de convergence et qualification contractuelle.
2. Exécuter **en parallèle** uniquement recherche historique publique, développement React/TypeScript isolé, rédaction et tests de contrat lorsque leurs entrées sont indépendantes. Les écritures concurrentes sur une même branche, la revue finale et la fusion restent sérialisées.
3. Préparer le plus possible **avant** la CI : vérification des imports, exigences de tests, marqueurs Chromium, politique des deux prompts, manifest exact-source et interdits. Ne pas réutiliser la CI d'un HEAD antérieur.
4. Conserver une **unique CI complète obligatoire par HEAD final** (Windows, Vitest, Rust, Chromium normal+CSP, règles source) ; toute correction déclenche une nouvelle CI ; préservation de `Protect main`, examen diff/reviews/threads, fusion protégée `expected_head_sha`, CI postmain indépendante.
5. **Ne pas promettre de réduction chiffrée** : le temps gagné dépend du nombre de cycles CI évités. Aucun bypass de contrôle, aucune accélération en mélangeant les données d'opérateur aux fixtures.
6. Stopper l'accumulation de prototypes lorsque l'incrément ne répond pas à une capacité réelle de M3.2. Le déblocage **humain et historique** est désormais sur le chemin critique ; demander la décision séparée A ou B avant d'envisager la production.

## Frontières inviolables

M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; identité `PARTIAL_LOCAL_IDENTITY_ONLY` ; writer `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE`; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 OPEN/DRAFT. Aucune migration 007, original SQLite v6/v7, copie des archives, ACL, WAL/shm/journal, marqueur M1.5, IPC writer, M3.3, ComfyUI ou exécution Windows opérateur.

**AUCUNE AUTORISATION** implicite par ce document. Conserver la chronologie immuable des preuves dans les issues #36 et #38.
