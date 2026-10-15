# M3.2 — Baseline prospective : protocole réconcilié pour opérateur unique

**Statut actualisé le 2026-10-16 : protocole documentaire prospectif réconcilié et fusionné via PR #37, mais G2–G6 réels non exécutés/non autorisés ; la baseline est toujours `NOT_STARTED`.** Le [plan G2 détaillé](M3_2_G2_WINDOWS_SOURCE_IDENTITY_PREFLIGHT_PLAN.md) prépare la prochaine observation sans exécuter de commande locale.

**Statut antérieur au moment de rédaction de PR #37 : PROTOCOLE EN RÉCONCILIATION, non opérationnel jusqu'à la CI du HEAD exact et la fusion protégée de cette PR.** La politique `SOLO_OPERATOR_COMPENSATING_CONTROLS` de la [PR #39](https://github.com/LaurentCOLL1/Fabulaxiom/pull/39) a été fusionnée dans `main=86d1773ff32e710b719ed0ec35fb7a734de3cd75` avec 23/23 étapes Windows PASS sur son SHA. L'utilisateur a explicitement autorisé le principe d'exécuter les quatre phases de déblocage, mais **n'a pas approuvé les paramètres inconnus d'une commande Windows précise**, et il ne dispose pas de relecteur humain indépendant.

## Portée de la nouvelle autorité prospective

Le protocole antérieur imposait systématiquement un relecteur humain indépendant. Pour la **seule construction d'une référence nouvelle**, cette exigence est désormais **proposée comme remplacée**, après fusion de cette PR de réconciliation, par les vérifications contradictoires, tests adversariaux, restauration isolée, gel des preuves et acceptation **personnelle** du risque définis dans [la politique opérateur unique](M3_2_SOLO_OPERATOR_COMPENSATING_CONTROLS.md). Ce mode n'est ni une revue humaine indépendante ni une attestation indépendante. Tout veto objectif reste impératif.

Les conditions d'attestation indépendante *historique* restent inchangées. [Issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) : `PENDING_EXTERNAL_ATTESTATION` 21 rôles épinglés historiquement / 3 empreintes seulement observées / 2 non ancrées. Les cinq rôles `production/pre_m24_early_manifest`, `acl/original_acls`, `acl/pre_repair_json`, `production/activation_marker`, `m25/isolated_v6` ne sont **pas** réparés, promus, re-signés ni déclarés intacts historiquement par une signature actuelle. L'ancienne fiche de revue indépendante reste **AWAITING_INDEPENDENT_REVIEW** en tant que dossier non exécuté : elle ne devient pas PASS.

## Statuts séparés et sans promotion automatique

- `historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)` — inchangé, même si la future prospective est acceptée.
- `prospective=NOT_STARTED` — aucun backup/manifest de référence prospective créé.
- `solo_protocol=APPROVED_POLICY_ONLY` **uniquement après** qualification et fusion de cette réconciliation documentaire ; cela ne signifie pas que les tests sur les données réelles sont réussis.
- `owner_windows_execution=NOT_AUTHORIZED`, `real_M3_2=NOT_AUTHORIZED`, `production_007=NOT_AUTHORIZED`, `writer_IPC=NOT_AUTHORIZED`.

Les autorités techniques restent protégées : 7 worktrees Windows, schéma actif M1.5 restauré v6, M3.1 v7 seulement en copie isolée, sauvegardes/ACL/manifests/marqueur et journaux historiques. Aucun secret, récit ou chemin privé ne doit entrer dans GitHub.

## Barrières d'autorisation à franchir dans l'ordre

| Gate | Action bornée | Décision minimale et état actuel |
| --- | --- | --- |
| G0 | Adoption de politique SOLO sans opération locale | PR #39 fusionnée ; modification d'autorité de PR #37 à qualifier sur son SHA avant entrée en vigueur |
| G1 | Acceptation des règles réconciliées et des risques connus | Accord de principe de l'opérateur ; aucun risque sur fichier réel accepté sans preuve |
| G2 | Lecture de préflight uniquement | **Non autorisée** sans bloc exact, rôles/chemins privés confirmés, vérification de l'absence de sidecars et accord spécifique |
| G3 | Nouvelle capture SQLite cohérente | **Non autorisée** sans destination neuve, garantie d'exclusion de collision, méthode de source-open revue, capacité/ACL et approbation spécifique |
| G4 | Vérifications contradictoires et restauration isolée | **Non autorisée** sans G3 valable, nouvelles copies séparées et nouveaux dossiers de preuve |
| G5 | Acceptation formalisée du risque prospectif | **Non signée** ; jamais « revue indépendante » |
| G6 | Test applicatif M3.2 en lecture seule sur copie isolée | **Non autorisé** avant acceptation G5 et sa propre décision de périmètre/test |
| G7 | Interface d'écriture/production ou PR #35 merge | **HORS PÉRIMÈTRE**, doit faire l'objet d'une nouvelle décision explicite et de tests réels |

Une phase non commencée n'est **pas** en échec technique ; elle est simplement **non autorisée / non qualifiée**. Chaque étape possède son propre accord et une procédure d'abandon qui ne supprime jamais un original.

## Invariants SQLite vérifiables

Une connexion déclarée read-only ne garantit pas à elle seule zéro modification annexe ; les sidecars `-wal`/`-shm` doivent être analysés **sans** les supprimer, reconstituer ni checkpoint. Pas de `immutable=1` sur une source potentiellement modifiable. L'Online Backup API fournit un snapshot cohérent mais **peut remplacer sa destination** : réservation exclusive, identité de fichier et absence de course doivent être démontrées au niveau Windows, pas seulement via `exists()` ou `Test-Path`. Jamais de copie brute d'un SQLite actif WAL, ni de présomption d'atomicité multi-base.

Sur les **nouvelles copies uniquement**, vérifier : `PRAGMA integrity_check` = exactement `ok`, `PRAGMA foreign_key_check` = zéro ligne, version/schema/tables/compteurs, lineage des scènes/revisions/sources, digests logiques canoniques et SHA256 des nouveaux fichiers, test de restauration séparé. Deux contrôles techniques diversifiés autant que réalisable, jeux négatifs artificiels et second examen temporel distinct ; tous les critères obligatoires `PASS`. Tests de faux hash, mauvaise source, collision, FK, corruption, WAL incertain, processus écrivain, missing/changed SHA : **fail closed**.

Une signature du propriétaire et un horodatage prospectif aident à suivre une décision et la chaîne de conservation **à partir de la nouvelle date**, pas avant. Aucun SHA actuel ne répare le passé.

## Prochain livrable technique permis par la seule gouvernance

Concevoir **sans lire des fichiers opérateur** un outil/test de laboratoire limité aux SQLite synthétiques, avec code exact et CI ; puis préparer un runbook Windows exact à faire approuver séparément avant toute lecture locale. Le [runbook réconcilié](M3_2_PROSPECTIVE_BASELINE_WINDOWS_RUNBOOK_DRAFT.md) est délibérément **non exécutable**. Le [modèle de décision propriétaire](M3_2_SOLO_OPERATOR_RISK_DECISION_TEMPLATE.md) est encore vierge.

**Non autorisé :** migration `007` de production, copie/move/reset/cleanup des anciens fichiers, modification du marqueur, writer IPC, fusion #35, passage M3.3, divulgation des données privées ou utilisation de l'application sur ses données actives pendant cette cérémonie.
