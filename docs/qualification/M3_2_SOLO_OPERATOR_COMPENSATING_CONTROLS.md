# M3.2 — SOLO_OPERATOR_COMPENSATING_CONTROLS (proposition de gouvernance)

**Situation actuelle (2026-10-16) : politique prospectivement acceptée par l'opérateur via PR #39 fusionnée, puis réconciliée et fusionnée par PR #37 ; aucune opération Windows autorisée par cette adoption.** Les paragraphes ci-dessous sont le texte historique de la proposition, à lire avec ce préambule et le [plan G2](M3_2_G2_WINDOWS_SOURCE_IDENTITY_PREFLIGHT_PLAN.md).

**État lors de la proposition initiale : PROPOSED_NOT_EFFECTIVE. AUCUNE autorisation nouvelle.** 15 octobre 2026. Ce libellé est une proposition propre à Fabulaxiom, ni norme officielle, ni certification, ni revue humaine indépendante.

## 1. Situation et autorités non contournables

Un seul développeur/opérateur est disponible ; aucune personne compétente indépendante n'est disponible. Le document `M3_2_INDEPENDENT_REVIEW_DECISION_RECORD.md` de la PR [#37](https://github.com/LaurentCOLL1/Fabulaxiom/pull/37) conserve son verdict **AWAITING_INDEPENDENT_REVIEW**. **La présente proposition ne satisfait pas ni ne supprime cette condition.** Seul un changement de gouvernance **distinct, explicitement approuvé et réconcilié** pourrait instaurer une exception limitée, jamais rétroactive.

Références vérifiées lors de la rédaction, **à re-fetch avant toute décision** : protected `main=f7eabfea74480d307b52d4b053730021efc95352` ; PR [#35](https://github.com/LaurentCOLL1/Fabulaxiom/pull/35) DRAFT `41ce7b915e76d22785d53d7fffe288d113dd0bf5` (CI [38672905255](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38672905255), 44/44) ; PR [#37](https://github.com/LaurentCOLL1/Fabulaxiom/pull/37) DRAFT `fdaa34b85145b36509253d06bd79dd81f8dc8a90` (CI [38759612398](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38759612398), 23/23). Ces CI ne qualifient pas les données Windows.

**Preuves historiques** [issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) : `PENDING_EXTERNAL_ATTESTATION`, 21 rôles ancrés / 3 SHA observés seulement / 2 non ancrés. Les cinq rôles restent non attestés historiquement : `production/pre_m24_early_manifest`, `acl/original_acls`, `acl/pre_repair_json`, `production/activation_marker`, `m25/isolated_v6`. Les nouvelles mesures **ne les promeuvent jamais**. La baseline prospective = `NOT_STARTED` et M3.2 réel = `NOT_AUTHORIZED`. Le schéma SQLite actif restauré demeure v6, distinct de la copie v7 isolée M3.1.

## 2. Changement de politique proposé et condition d'entrée en vigueur

**Option dérogatoire limitée** : permettre ultérieurement une nouvelle référence de confiance **prospective** avec double qualification technique reproductible et acceptation explicite du risque par l'opérateur, sans prétendre à une revue humaine indépendante.

**Conditions cumulatives, toutes nécessaires avant l'exception** : (1) approbation explicite du propriétaire de *cette politique uniquement*, avec SHA exact, diff limité et CI terminale ; (2) **PR ultérieure distincte de réconciliation** corrigeant explicitement les exigences incompatibles de la DRAFT PR #37, le formulaire indépendant, les issues #36/#38 et les documents d'autorité — sans supprimer la vérité historique ; (3) enregistrement authentifié d'une acceptation personnelle du risque portant sur un périmètre et une durée déterminés ; (4) autorisation spécifique **avant chaque phase d'opération Windows**. La fusion de cette PR documentaire ne suffit à aucun de ces quatre points.

États proposés **uniquement après adoption** : `SOLO_CONTROLS_VERIFIED`, `OWNER_RISK_ACCEPTED_FOR_SCOPE`, `ACCEPTED_SOLO_FOR_LIMITED_FUTURE_REFERENCE`. Ne jamais utiliser `INDEPENDENTLY_REVIEWED` pour qualifier l'opérateur, l'assistant, la CI ou sa signature. Conserver séparément `AWAITING_INDEPENDENT_REVIEW` si aucun humain indépendant n'est intervenu.

## 3. Contrôles compensatoires à démontrer, non présumés

| Contrôle | Preuve obligatoire | Limite / refus |
| --- | --- | --- |
| Source exacte et provenance | Re-fetch SHA/CI, versions, rôles, trace de l'outil et de l'OS, verdicts et log privés minimisés | SHA changeant / rôle incertain = STOP |
| Vérification double, techniquement diversifiée | Deux implémentations ou méthodes indépendantes dans leur logique lorsque faisable (par exemple Rust/SQL et Python/audit) sur **nouvelles copies**, avec oracles explicites | Moteur SQLite éventuellement commun ; **pas** d'indépendance humaine ; désaccord = STOP |
| Vérification contradictoire | Cas positifs et négatifs déterministes : mauvais rôle, manifest falsifié, digest faux, révision altérée, FK invalide, v6/v7 inversées, collision, données manquantes, WAL incertain | Test négatif accepté ou non exécuté = STOP |
| Répétition isolée | Deux environnements/sorties propres distincts et résultats rapprochés ; **réexamen différé** après gel des premières preuves | Répétition du même code ≠ témoin humain indépendant ; divergence = STOP |
| Garantie SQLite logique | Sur copies nouvelles : `PRAGMA integrity_check` exactement `ok`, `foreign_key_check` sans ligne, tables/schema/comptes, historique immuable des révisions et digests canoniques versionnés | Un hash physique ne démontre ni intégrité logique ni provenance ; échec = STOP |
| Préservation et restauration | Empreintes SHA-256 + tailles des nouveaux outputs ; restauration isolée neuve puis seconde validation et preuves source avant/après sans altération | Sauvegarde incomplète, manque de test de restauration ou source altérée = STOP |
| Conservation/authenticité | Manifest prospectif daté, rôles/versions/digests, emplacements privés séparés et politique de rétention, signature honnêtement attribuée au propriétaire | Signature auto-produite ≠ attestation indépendante ; jamais de données privées sur GitHub |
| Arrêt strict | Chaque critère obligatoire avec verdict `PASS`, `FAIL` ou `NOT_ASSESSED`, preuves et code de sortie | `FAIL` ou `NOT_ASSESSED` = aucun franchissement de barrière |

Les oracles attendus doivent être fixés **avant** de voir les valeurs contrôlées. Ne pas « valider » un hash attendu obtenu du même fichier inconnu. Les tests contradictoires utilisent des **fixtures nouvelles**, jamais une altération de fichiers protégés.

## 4. Séparation des autorisations — phases proposées

- **G0 — politique proposée (cette PR)** : documentation seule, aucune approbation implicite et aucune opération locale.
- **G1 — changement d'autorité** : consentement explicite de l'auteur/propriétaire à la politique et **réconciliation formelle** avec la PR #37 et les issues. Sinon, la règle de revue indépendante reste bloquante.
- **G2 — observation Windows** : nouveau plan SHA-pinné, autorisé séparément, lecture uniquement après examen du comportement des ouvertures, token standard, ACL, 7 worktrees, fichiers/roles v6/v7 et marqueur M1.5 ; absence de garantie zéro mutation des originaux = STOP.
- **G3 — capture prospective** : plan/source/destination et droit de **création de sorties nouvelles seulement** autorisés distinctement. SQLite Online Backup API ou équivalent expertisé, **jamais copie brute** d'une source live. WAL/SHM sans suppression/checkpoint/écriture non autorisée, jamais `immutable=1` supposé sur source mutable. Le backup peut écraser son fichier cible : une réservation nouvelle atomique / création exclusive et la protection de l'identité cible de bout en bout sont obligatoires ; `exists()` et `Test-Path` seuls ne suffisent pas. Refuser junctions/reparse points, symlinks et collisions. Des snapshots de deux bases ne prouvent pas un instantané atomique multi-bases.
- **G4 — tests et restauration isolés** : copies nouvelles, vérifications diversifiées/adversariales, restauration dans un **troisième emplacement neuf**, contrôle avant/après de l'original, réexamen différé et journal privé ; aucune restauration par la fonction qui bascule le marqueur M1.5.
- **G5 — risque résiduel personnel** : décision signée **comme propriétaire non indépendant**, preuve/rôle/durée/périmètre/contre-indications, possibilité de révocation. Alors seulement une demande de label `ACCEPTED_SOLO_FOR_LIMITED_FUTURE_REFERENCE` pourrait être examinée.
- **G6 — intégration limitée** : nouvel accord **distinct** pour tests React/Tauri/SQLite v7 **en lecture seule sur une copie isolée**, CI sur son propre SHA et qualification Windows hors IA avec audit post-sortie.

**Hors périmètre et interdits sans de nouvelles décisions spécifiques** : migration normale production `007`, changement du pointeur M1.5, GUI writer et IPC writer, fusion PR #35, M3.3, déplacement/remplacement/nettoyage des sept worktrees, SQLite originales, ACL, sauvegardes, manifestes, WAL/SHM, archives et données privées. Aucun script Windows n'est livré ni autorisé ici.

## 5. Risque résiduel et veto

Risque **ÉLEVÉ** pour la provenance passée, l'absence de jugement humain indépendant et l'erreur systémique commune ; risque **MODÉRÉ À ÉLEVÉ** pour la nouvelle copie prospective jusqu'à démonstration des contrôles. Il est **impossible** de remplacer une revue humaine indépendante ou de reconstituer les témoins historiques manquants par CI, ChatGPT, auto-signature ou hash actuel.

Veto si : référence changée ; autorisation absente ; identité/ACL/token/processus/chemin incertains ; ouverture source pouvant produire un sidecar ou altérer WAL ; destination préexistante/non exclusive ; capacité ou permission insuffisante ; backup interrompu/LOCKED/BUSY ; schéma/intégrité/FK/digest/revisions non conformes ; test adversarial incorrect ; restauration ou réexamen différé absent ; divergence inexpliquée ; secret exposé. Arrêt **sans nettoyage automatique des originaux** ; seule une sortie **nouvelle et identifiée** peut éventuellement être mise en quarantaine après autorisation spécifique.

## 6. Fiche de décision et documentation officielle

La [fiche de décision personnelle](M3_2_SOLO_OPERATOR_RISK_DECISION_TEMPLATE.md) reste **non remplie**. Une approbation de politique ne vaut pas consentement à lire, sauvegarder, restaurer ni exécuter une application. Aucun protocole de signature personnel ne devient indépendance de garde.

Références : [NIST SSDF 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) ; [SQLite Online Backup](https://www.sqlite.org/backup.html), [WAL](https://www.sqlite.org/wal.html), [URI immutable](https://www.sqlite.org/uri.html), [PRAGMA](https://www.sqlite.org/pragma.html) ; [Microsoft CreateFile CREATE_NEW](https://learn.microsoft.com/en-us/windows/desktop/FileIO/creating-and-opening-files) ; [GitHub artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations) (provenance des builds, non preuve rétroactive de bases locales).

**Fin : PROPOSÉ / NON APPROUVÉ / NON ACTIVÉ / AUCUNE OPÉRATION WINDOWS.**
