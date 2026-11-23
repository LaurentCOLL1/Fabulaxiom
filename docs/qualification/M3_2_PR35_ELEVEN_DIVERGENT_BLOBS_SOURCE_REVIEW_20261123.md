# PR #35 — 11 chemins divergents, comparaison des blobs Git en lecture seule (23/11/2026)

**SOURCE_ONLY_CANDIDATE_UNQUALIFIED ; NO_RUNTIME_ADMISSION ; NO_SEMANTIC_EQUIVALENCE ; NO_AUTO_PORT ; OPEN_NOT_ACCEPTED.** PR historiques #35 et #215 DRAFT NON_ADMITTED. Historique PR35 HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5`. Instantané `main=2116f8a7b1725f9fad552be4ffb7795f8a9552eb` après #420 fusionnée, sans présumer de réussite de sa CI postmain indépendante. Les SHA de la colonne `main` sont un **instantané daté de provenance textuelle** et ne doivent pas être traités comme des gages de provenance SQLite réelle ou d'admission à des opérations.

Les 11 divergences ont été inspectées exclusivement par contenu GitHub. La classification **4 BUILD_SECURITY + 3 CONTINUITY + 3 ISOLATED_PRODUCT + 1 SQL_FIXTURE** est un triage de portée ; **11/11 REVIEW_CURRENT_DIFF_NO_OVERRIDE** signifie **zéro restauration de l'ancienne version**.

| Chemin existant sur les deux branches | SHA Git blob PR35 historique | SHA blob de `main` au parent exact | Classe | Décision de revue |
| --- | --- | --- | --- | --- |
| `.github/workflows/m0-ci.yml` | `e12bf78e22ba6eb71ed7678a0ddf4ad54fa35e27` | `c35a8f076b2770e676f63da48e9a93b6cc495b81` | BUILD_SECURITY | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `README.md` | `e0191b8f01d84fc97db40f1d5eb5031f0364d06d` | `9e3408aeb459170a006a60e94721fabcb1595f3b` | CONTINUITY | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `docs/continuity/NEXT.md` | `b24b245b02c423f26f1a2315de0a6110a724eca0` | `6aa0cf07e526aef18977a0d5c42546eaf17f6e80` | CONTINUITY | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `docs/continuity/STATE.md` | `0d05054b5bb5d7e7bbcffab846d09285f3272067` | `635f6c15eee06e7502a71a37cd80e35c135592e6` | CONTINUITY | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/Cargo.toml` | `9c0c286062dbf3c881b7d76d1a1ea45d85385766` | `50a36053f4772bd11769d2cd13a5b8b633038a78` | BUILD_SECURITY | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/build.rs` | `32adde45c871d1c31639d1debc0fe779c0c69881` | `d860e1e6a7cac333c3cc0bc9cb67faf286b07d69` | BUILD_SECURITY | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/sql/m3_2_chronology_decisions_candidate.sql` | `fbd2a6244e6356a68e4fa707a7395fcbafe0449e` | `786dc766769467ab6bf3243971855da31ff0dfbd` | SQL_FIXTURE | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/src/lib.rs` | `22cd1cdcbc5ecd9ae08bfa5e926ea56834c6a343` | `25796459e334f040f7e8ec8e677636f37f6dc947` | BUILD_SECURITY | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src-tauri/src/m32_manual_chronology.rs` | `f75e4bc7787b60ac345cbe137355f4888243829c` | `c5542fed19b338752563f144a9484a34f9f79688` | ISOLATED_PRODUCT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src/M32ChronologyPreview.tsx` | `d7b6e5972a4730f487d346ae4e8116a9f7d84bca` | `f57a48f26b4460d9f0aefec23b1880e722a3d860` | ISOLATED_PRODUCT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |
| `src/m32ChronologyPreview.test.tsx` | `bdc8e0b5ec3d22a784a864e81c82895915d2bc08` | `c6aa039d3e8ad0db556dc1a7f53417d82f4c3193` | ISOLATED_PRODUCT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |

## Comparaisons de portée, sans équivalence prétendue

- **Build/security (4)** : l'ancien workflow (147 lignes) et le workflow courant (441 lignes) ne sont pas substituables. Le feature historique `m32-isolated-preflight` et son ancien allowlist à la compilation dans `build.rs` sont distincts des features actuels (`m32-synthetic-preview`, contrôles de gates et services test-only). Ne pas copier l'ancien build/IPC, ni altérer les permissions Tauri, ni réactiver le writer.
- **Continuité (3)** : `README.md`, `STATE.md` et `NEXT.md` ont évolué depuis #35. Leur ancienne version ne peut remplacer les autorités vivantes, la checklist ou les derniers checkpoints. Aucune preuve historique authentique n'est produite par ces textes.
- **Produit isolé (3)** : service Rust de chronologie toujours test-only (1279 lignes historiques contre 1305 au parent), aperçu React non monté (208 contre 307 lignes), tests TS historiques (92 contre 287 lignes). Les ajouts récents changent le périmètre ; la parité fonctionnelle et les assertions de tests anciens ne sont **pas démontrées**.
- **SQL fixture (1)** : le fichier courant précise les fixtures jetables en mémoire ou fichiers neufs possédés par le runner (123 lignes anciennes contre 124 au parent). Cet ajout de commentaire ne prouve pas seul l'identité de toutes les constructions SQL, ne transforme pas le script en migration et n'autorise jamais l'accès à SQLite opérateur.

**11/11 SOURCE_SCOPED_NOT_ADMITTED ; 0/11 PORTED ; 0/11 ADMITTED.** 5 chemins historiquement identiques à l'ancien audit restent hors de ce lot. Les 26 documents et 20 paires Python absents sont décrits séparément ; deux Rust absents et les quatre chemins REVIEW de #215 restent non admis. Les comparaisons approfondies comportementales ou tests de parité devront être de nouvelles preuves ciblées, non de simples comparaisons SHA.

**M32-007 [ ] / M32-050 [ ] / M32-078 [ ]**, 13 CLOSED_SCOPED / 91 OPEN_NOT_ACCEPTED (104), M3.2 IN_PROGRESS_NOT_ACCEPTED (~45% indicatif). **R1–R9 NOT_PROVEN** ; STOP Writer, P4, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED, R2 STOP/R3 partiel/D3c conception/D3b-4/5 STOP, main/WAL/SHM live SQLite WAL-index et ABA NOT_PROVEN, glib #160 OPEN_NOT_REMEDIATED, v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.

Trois gardes purement source #37–39 vérifient l'inventaire, les SHA d'origine, les catégories, le refus de falsification et la non-clôture des gates. Aucune exécution d'ancien module, Tauri, migration, commande ou base opérateur ; tests candidats non qualifiés avant CI Windows HEAD exacte.
