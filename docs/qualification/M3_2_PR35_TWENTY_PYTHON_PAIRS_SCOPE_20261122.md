# PR #35 — inventaire des 20 couples Python historiques absents (22/11/2026)

**Portée : inventaire nominal et dépendances exemplaires, pas de portage.** PR #35 DRAFT HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5`, parent protected main `856ccba4af54d7c517f98db9471e8e2c5ce84cae` après #414 MERGED. L'audit d'arbre daté `M3_2_PR35_84_PATH_TREE_AUDIT_20261121.md` recense 84 chemins : 5 identiques, 11 divergents, 68 absents. Parmi les 68, **20 outils Python et leurs 20 tests historiques** sont exactement appariés par nom, sans fichier supplémentaire ni doublon. Les 26 documents absents et 2 modules Rust font l'objet de traitements séparés. **NO_SEMANTIC_EQUIVALENCE** : présence/absence de noms et appariement ne valent aucune équivalence comportementale.

## Inventaire des 20 paires (40 fichiers)

| Script historique absent | Test historique absent | Statut |
| --- | --- | --- |
| `tools/m3_2_chronology_batch_coherence_reference.py` | `tools/test_m3_2_chronology_batch_coherence_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_comparison_batch_reference.py` | `tools/test_m3_2_chronology_comparison_batch_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_comparison_reference.py` | `tools/test_m3_2_chronology_comparison_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_navigation_reference.py` | `tools/test_m3_2_chronology_navigation_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_pagination_reference.py` | `tools/test_m3_2_chronology_pagination_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_presentation_reference.py` | `tools/test_m3_2_chronology_presentation_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_projection_reference.py` | `tools/test_m3_2_chronology_projection_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_readonly_handoff_reference.py` | `tools/test_m3_2_chronology_readonly_handoff_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_selection_review_reference.py` | `tools/test_m3_2_chronology_selection_review_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_witness_consultation_reference.py` | `tools/test_m3_2_chronology_witness_consultation_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_witness_presentation_reference.py` | `tools/test_m3_2_chronology_witness_presentation_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_chronology_witness_reference.py` | `tools/test_m3_2_chronology_witness_reference.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_direct_custody_readonly.py` | `tools/test_m3_2_direct_custody_readonly.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_independent_authority_gate.py` | `tools/test_m3_2_independent_authority_gate.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_isolated_v7_physical_readonly.py` | `tools/test_m3_2_isolated_v7_physical_readonly.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_m31_semantic_readonly.py` | `tools/test_m3_2_m31_semantic_readonly.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_multiroot_readonly.py` | `tools/test_m3_2_multiroot_readonly.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_operator_readonly_gate.py` | `tools/test_m3_2_operator_readonly_gate.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_provenance_triage.py` | `tools/test_m3_2_provenance_triage.py` | NOT_PORTED_SOURCE_ONLY |
| `tools/m3_2_supersession_reference.py` | `tools/test_m3_2_supersession_reference.py` | NOT_PORTED_SOURCE_ONLY |

## Sémantique examinée, sans portage

L'ancien outil Stage 21 `m3_2_chronology_projection_reference.py` expose `inspect_anchor`, `universe_view`, `lineage` et `relative_world_order` sur un `SyntheticSnapshot` issu de `m3_2_supersession_reference.py`. Il refuse l'ordre fictif inféré depuis les dates et les connexions entre Universes ; rien ne prouve une correspondance intégrale à l'atelier React actuel non monté.

L'outil Stage 23 `m3_2_chronology_pagination_reference.py` dépend des anciens modules `projection_reference`, `presentation_reference` et `supersession_reference`. Son curseur versionné utilise un fingerprint de snapshot (pas un MAC ni une autorité), une taille maximale 64 et une borne de 4096 octets. Il **diffère** de la simple pagination actuelle des identifiants 5/10/20 ; ne pas copier son curseur ni considérer ce comportement comme couvert par P3bi. Les 18 autres paires sont inventoriées **uniquement par nom**, sans comparaison détaillée de source. Les champs de revue futurs pourront déterminer quels témoins synthétiques valent une réimplémentation ciblée.

## Gardes et décision

Les tests source-only #25/#26/#27 dans `tools/test_m32_legacy_pr_reconciliation.py` vérifient la partition stricte 20 outils /20 tests /68 absents, appariement exact, interdiction de fausse équivalence ou admission et conservation des cases checklist ouvertes. Ils ne chargent ni n'exécutent les modules historiques, ni SQLite, ni IPC, ni commandes opérateur. **NON QUALIFIÉ avant CI Windows HEAD exact**.

**M32-007 [ ] / M32-050 [ ] OPEN_NOT_ACCEPTED**, **NO_RUNTIME_ADMISSION**. Les PR #35/#215 restent DRAFT NON ADMISES. Aucune migration, production, backup, ouverture de base ni lancement d'un ancien script. M3.2 IN_PROGRESS_NOT_ACCEPTED ; PRODUCT_FIRST_PARALLEL_SAFETY.

STOP Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5, D3b-5 STOP ; main/WAL/SHM live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED. STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
