# M3.2 — matrice vivante exigences → tests → preuves (104 obligations)

**11 novembre 2026 — CANDIDAT source-only / NON QUALIFIÉ.** Référence protected `main=b2b032c0010a9d879103718cfa0786a827c5ac56`, PR #343 [fusionnée](https://github.com/LaurentCOLL1/Fabulaxiom/pull/343) avec CI source #43101935892 attempt 1 completed/SUCCESS exact HEAD ; CI postmain indépendante #43103763204 **À QUALIFIER**. La matrice recopie les cases de la checklist canonique **104 = 7 closes/97 ouvertes** au SHA de base ; toute modification de la checklist devra synchroniser cette matrice dans la même PR.

**Sémantique :** `CLOSED_GITHUB` n'atteste que la tâche GitHub nommée ; `CLOSED_DOCUMENTARY` uniquement la documentation/contrat explicite, jamais l'admission d'un runtime ; `OPEN_PARTIAL_ONLY` indique une piste de test ou un rapport mais **pas** la preuve d'acceptation ; `OPEN_UNPROVEN` signifie qu'aucune preuve complète n'a été produite. `NO_TARGETED_TEST` et `NO_ACCEPTANCE_PROOF` sont des manques déclarés, pas des validations cachées. Les chemins cités existent dans le dépôt mais ne prouvent pas à eux seuls le contrat intégral.

**Portée:** inventaire source-only lisible et vérifiable des 104 obligations ; **M32-078 reste [ ]** tant que la qualification de la matrice elle-même et sa décision de clôture ne sont pas complètes. Cette matrice n'autorise pas writer/R1–R9, P4 réel, G2B–G6, migration 007, Windows Hello natif ni données opérateur. `PRODUCT_FIRST_PARALLEL_SAFETY` inchangée, M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45% estimés), historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, main/WAL/SHM/WAL-index live/ABA NOT_PROVEN, glib #160 OPEN.

| Obligation | Case | Critère | Test ou piste source-only | Preuve ciblée | Portée actuelle |
| --- | :---: | --- | --- | --- | --- |
| M32-001 | x | Qualifier la CI postmain indépendante de la fusion #330 au SHA bef699511ff18e987a4858c797fde7aa88dfc59b | `tools/test_m32_completion_master_checklist.py` | `CHECKLIST_CLOSURE_001` | CLOSED_GITHUB |
| M32-002 | x | Réconcilier la PR produit #331 P3n après la fusion #330 | `tools/test_m32_handoff_contract.py` | `CHECKLIST_CLOSURE_002` | CLOSED_GITHUB |
| M32-003 |   | Revoir le diff, les reviews, threads et le ruleset Protect main pour chaque future PR | `tools/test_m32_handoff_contract.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-004 |   | Éviter que les prompts de reprise et l'historique de handoff divergent | `tools/test_m32_resume_pr_diff_policy.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-005 |   | Écrire le statut vrai à la date de chaque checkpoint | `tools/test_m32_handoff_contract.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-006 |   | Conserver issue #38 comme journal append-only des décisions et refus | `tools/test_m32_handoff_contract.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-007 |   | Concilier les deux anciennes PR #35 et #215 avant toute décision sur leur devenir | `tools/test_m32_legacy_pr_reconciliation.py` | `docs/qualification/M3_2_LEGACY_PR35_PR215_RECONCILIATION_20261110.md` | OPEN_PARTIAL_ONLY |
| M32-008 |   | Faire autoriser séparément toute opération Windows sur machine opérateur | `tools/test_m32_g2a_consent_contract.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-009 |   | R1 — fixer le profil/identité/autorité du propriétaire unique | `tools/test_m32_greenfield_profile_contract.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-010 |   | R1 — tester refus de propriétaire/profil/ACL étranger | `tools/test_m32_g2a_exact_block_source.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-011 |   | R2 — protéger l'arborescence ancêtre jusqu'au fichier ouvert | `tools/test_m32_rust_sqlite_open_inventory.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-012 |   | R2 — rejeter substitutions du nom et ABA sur les ancêtres | `tools/test_m32_g2b_fileid_writer_counterexample.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-013 |   | R3 — vérifier l'objet SQLite main effectivement délégué | `tools/test_m32_rust_sqlite_open_inventory.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-014 |   | R3 — qualifier verrous Win32 natifs SHARED/RESERVED/PENDING/EXCLUSIVE | `tools/test_m32_shared_ram_other_writer_counterexample.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-015 |   | R3 — qualifier fermeture et erreurs de callbacks | `tools/test_m32_rust_sqlite_open_inventory.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-016 |   | R4 — identifier et gérer journal, -wal et -shm comme objets distincts | `tools/test_m32_rust_sqlite_open_inventory.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-017 |   | R4 — couvrir toutes les primitives SQLite SHM en mode WAL NORMAL | `tools/test_m32_rust_sqlite_open_inventory.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-018 |   | R4 — démontrer que le garde main/WAL/SHM résiste aux substitutions contrôlées | `tools/test_m32_g2b_fileid_writer_counterexample.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-019 |   | R4 — qualification en deux processus OS indépendants | `tools/test_m32_shared_ram_other_writer_counterexample.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-020 |   | R4 — établir la frontière atomique ou admettre explicitement la limite | `tools/test_m32_g2b_fileid_writer_counterexample.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-021 |   | R5 — prouver provenance SQLite distincte de integrity_check | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-022 |   | R5 — refuser ATTACH étrangère, migration implicite et reprise ambiguë | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-023 |   | R6 — implémenter une unique session propriétaire avec génération | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-024 |   | R6 — refuser writer concurrent et commandes périmées | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-025 |   | R7 — définir fermeture, checkpoint, crash, restart et transition RECOVERY_REQUIRED | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-026 |   | R7 — tester matrice de crash à phases bornées et restart jetable | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-027 |   | R7 — décider et qualifier séparément la récupération native éventuelle | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-028 |   | R8 — qualifier durée de vie C ABI, VFS et ressources | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-029 |   | R8 — bornage des transactions, lectures et requêtes futures | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-030 |   | R9 — construire dossier d'admission négatif et positif indépendant | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-031 |   | R9 — obtenir une décision explicite et nouvelle avant writer runtime | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-032 |   | Résoudre le témoin production/pre_m24_early_manifest | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-033 |   | Résoudre le témoin acl/original_acls | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-034 |   | Résoudre le témoin acl/pre_repair_json | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-035 |   | Résoudre le témoin production/activation_marker | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-036 |   | Résoudre le témoin m25/isolated_v6 | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-037 | x | Si des preuves historiques authentiques manquent, enregistrer honnêtement cette limite | `tools/test_m32_parallel_documentary_audit.py` | `docs/qualification/M3_2_PARALLEL_DOCUMENTARY_AUDIT_20261111.md` | CLOSED_DOCUMENTARY |
| M32-038 |   | Décider séparément la mise en place d'un baseline prospectif | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-039 |   | G2-B — prouver l'identité de la source et l'absence d'un écrivain concurrent | `tools/test_m32_g2a_writer_gap_model.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-040 |   | G2-C — qualifier accord opérateur de source et de périmètre | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-041 |   | G2-D — examiner quiescence, sidecars, ACL, chemin de backup et préflight | `tools/test_m32_g2a_exact_block_source.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-042 |   | G3 — obtenir une méthode sûre de capture prospective depuis une source prouvée | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-043 |   | G3 — tenir la copie et sa chaîne de conservation | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-044 |   | G4 — vérifier l'image isolée et un vrai test de restauration | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-045 |   | G4 — démontrer absence de modification des originaux | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-046 |   | G5 — formaliser la décision de risque de l'opérateur unique | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-047 |   | G6 — recette isolée du profil admissible et de la lecture v7 | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-048 |   | Avant toute migration 007 — sauvegarde cohérente non écrasante de v6 | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-049 | x | Séparer une éventuelle activation de production de la seule acceptation d'un projet neuf | `tools/test_m32_parallel_documentary_audit.py` | `docs/qualification/M3_2_PARALLEL_DOCUMENTARY_AUDIT_20261111.md` | CLOSED_DOCUMENTARY |
| M32-050 |   | Réconcilier la PR historique #35 sans la fusionner en bloc | `tools/test_m32_legacy_pr_reconciliation.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-051 | x | Documenter le contrat de données v7 existant | `tools/test_m32_parallel_documentary_audit.py` | `docs/qualification/M3_2_PARALLEL_DOCUMENTARY_AUDIT_20261111.md` | CLOSED_DOCUMENTARY |
| M32-052 |   | Rendre le service Rust chronologique accessible derrière la seule autorité admise | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-053 |   | Compléter création et lecture de calendriers par univers | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-054 |   | Compléter création et liste d'événements/ancres | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-055 |   | Compléter édition métier non destructive d'ancre | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-056 |   | Compléter création de précédence « A avant/après B » | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-057 |   | Compléter révocation et correction des précédences | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-058 |   | Traiter les conflits et cycles sur graphe actif | `src/m32WorldOrderComparison.test.tsx` | `docs/qualification/M3_2_P3R_SYNTHETIC_WITNESS_TIEBREAK_POLICY_20261111.md` | OPEN_PARTIAL_ONLY |
| M32-059 |   | Traiter dates et incertitudes en quatre modes | `src/m32ChronologyPreview.test.tsx` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-060 |   | Traiter la comparaison entre calendriers fictifs | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-061 |   | Lier un événement à scène et révision historique immuable | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-062 |   | Gérer plusieurs romans dans un Universe et plusieurs Universes distincts | `src/m32TwoUniverseIsolation.test.tsx` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-063 |   | Garantir transactions atomiques et refus cohérents | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-064 |   | Garantir persistance sur v7 neuve puis réouverture | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-065 |   | Maintenir la v6 restaurée et migration 007 non exécutée sans gate | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-066 |   | Définir le parcours opérateur d'un projet Greenfield réellement neuf | `tools/test_m32_greenfield_first_launch_preflight.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-067 |   | Intégrer à une vraie navigation l'atelier chrono aujourd'hui isolé | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-068 |   | Relier l'UI à des commandes Tauri Rust typées et bornées | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-069 |   | Distinguer visuellement les trois ordres indépendants | `src/m32ChronologyPreview.test.tsx` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-070 |   | Concevoir formulaires calendrier et événement utilisables sans IA | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-071 |   | Concevoir liste/consultation et inspection des sources historiques | `src/m32P3eHistoricalInspection.test.tsx` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-072 |   | Concevoir éditeur humain de précédence avant/après | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-073 |   | Concevoir correction/supersession/révocation réversible | `src/m32P3dReversibleChronology.test.tsx` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-074 |   | Préserver la séparation brouillon/proposé/canon existante | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-075 |   | Garantir accessibilité/échappement et comportement hors ligne | `src/m32P3cFictionalUx.test.tsx` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-076 |   | Ne jamais afficher un faux succès de persistance | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-077 |   | Gérer erreurs de session et de fichiers sans corruption | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-078 |   | Construire une matrice exigences→tests→preuves à jour | `tools/test_m32_requirements_evidence_matrix.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-079 |   | Valider les quatre temporalités sur deux Universes et plusieurs romans | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-080 |   | Valider prévention des cycles et conflits déterministes | `src/m32WorldOrderComparison.test.tsx` | `docs/qualification/M3_2_P3R_SYNTHETIC_WITNESS_TIEBREAK_POLICY_20261111.md` | OPEN_PARTIAL_ONLY |
| M32-081 |   | Valider revocations, corrections et lecture du passé | `src/m32P3dReversibleChronology.test.tsx` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-082 |   | Valider isolation Universe et IDs homogènes | `src/m32TwoUniverseIsolation.test.tsx` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-083 |   | Valider monde/narration/révélation indépendants | `src/m32ChronologyPreview.test.tsx` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-084 |   | Valider tests négatifs de fichiers et des droits Windows | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-085 |   | Valider sauvegarde/restauration à destination neuve et pointeur v6 inchangé | `tools/test_m32_greenfield_backup_restore.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-086 |   | Tester usage hors ligne avec Ollama éteint | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-087 |   | Tester réouverture et récupération selon périmètre autorisé | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-088 |   | Valider intégration Rust–Tauri–React Windows hors laboratoire après gate | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-089 |   | Réaliser une recette opérateur sur un profil NEUF admis | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-090 |   | Réaliser une recette distincte sur copie authentifiée des données historiques si autorisée | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-091 |   | Auditer absence de réseau non voulu et stabilité mémoire/fichiers | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-092 |   | Traiter séparément les alertes Dependabot Vite/launch-editor | `tools/test_m32_vite_817_security_lock.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-093 |   | Traiter le problème glib 0.18.5 de la chaîne Linux GTK3 | `tools/m32_glib_linux_target_audit.py` | `docs/qualification/M3_2_GLIB_ALERT1_UPSTREAM_BLOCKER_20261101.md` | OPEN_PARTIAL_ONLY |
| M32-094 |   | Qualifier Windows et Linux comme deux expositions distinctes | `tools/m32_glib_target_audit.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |
| M32-095 | x | Documenter décisions de sécurité restantes avant distribution | `tools/test_m32_parallel_documentary_audit.py` | `docs/qualification/M3_2_PARALLEL_DOCUMENTARY_AUDIT_20261111.md` | CLOSED_DOCUMENTARY |
| M32-096 | x | Tenir Windows Hello comme confirmation future des actes sensibles | `tools/test_m32_parallel_documentary_audit.py` | `docs/qualification/M3_2_PARALLEL_DOCUMENTARY_AUDIT_20261111.md` | CLOSED_DOCUMENTARY |
| M32-097 |   | Prendre une décision d'admission writer formelle basée sur R1–R9 | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-098 |   | Prendre décisions explicites G2B–G6 et provenance | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-099 |   | Accepter les parcours produit complets, pas seulement un démonstrateur | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-100 |   | Qualifier la PR d'implémentation finale au HEAD exact et sous Protect main | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-101 |   | Effectuer contrôle postmain indépendant de chaque merge | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-102 |   | Fusionner une PR séparée de normalisation documentaire de M3.2 | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-103 |   | Prononcer explicitement M3.2 ACCEPTED + MERGED + NORMALIZED | `NO_TARGETED_TEST` | `NO_ACCEPTANCE_PROOF` | OPEN_UNPROVEN |
| M32-104 |   | Conserver M3.3–M3.6, M4–M9, Ollama créatif, cohérence IA et ComfyUI hors M3.2 | `tools/test_m32_roadmap_traceability.py` | `NO_ACCEPTANCE_PROOF` | OPEN_PARTIAL_ONLY |

**Contrôle CI :** `tools/test_m32_requirements_evidence_matrix.py` recoupe identifiants, titres, cases, chemin des preuves et marqueurs de portée sans ouvrir aucun fichier opérateur.
