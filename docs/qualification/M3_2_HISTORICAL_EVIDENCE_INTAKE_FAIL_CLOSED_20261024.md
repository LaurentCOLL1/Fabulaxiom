# M3.2 — Tri des cinq attestations historiques : seulement métadonnées fictives (24 octobre 2026)

**SOURCE-ONLY ; AUCUN PROCESSUS DE COLLECTE DE PREUVES.** Ce contrôle ne demande, ne télécharge et ne manipule **jamais** les manifestes, bases SQLite, journaux, ACL, sauvegardes, fichiers ou secrets de l'opérateur. Ne publier aucune pièce privée sur GitHub.

## Pourquoi

L'[issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) conserve cinq rôles non authentifiés : `production/pre_m24_early_manifest`, `acl/original_acls`, `acl/pre_repair_json` (SHA observés uniquement) et `production/activation_marker`, `m25/isolated_v6` (non ancrés). Les 21 autres rôles demeurent historiquement distingués ; aucun statut n'est fusionné.

Le module Python `tools/m32_historical_evidence_intake.py` reçoit **uniquement une liste fictive de dictionnaires**. Il vérifie les cinq rôles autorisés, unicité, absence de contenu/chemin supplémentaire, références externes symboliques, forme de digest d'une *notice* et assertions de provenance indépendantes. Il retourne `MISSING_INDEPENDENT_WITNESS`, `REJECTED_UNTRUSTED_METADATA` ou `REVIEW_REQUIRED_NOT_VERIFIED`. Ces catégories ne constituent **jamais** `VERIFIED`.

Même si tous les champs d'un candidat inventé semblent satisfaisants, son attestation reste non vérifiée : un drapeau déclaratif de custodian externe, un digest inventé ou un identifiant symbolique ne prouvent pas la création antérieure, la garde, la liaison de rôle, la signature ni le contenu. Le programme ne vérifie **aucune cryptographie** et n'a pas d'interface de collecte ni de CLI opérateur. Toute véritable décision demanderait un dossier distinct, vérifié indépendamment et autorisé séparément hors des données privées GitHub.

## Durcissement documentaire candidat après PR #165

Une même **référence symbolique** (`EXT-...`) ou le même **SHA de notice fictive** présenté pour plusieurs rôles doit conduire à `STOP`, afin de ne pas simuler l'indépendance par cinq lignes copiées. Le même custodian inventé peut être associé à plusieurs notices **distinctes**, sans authentifier pour autant son indépendance. C'est une règle conservatrice du tri **fictif**, pas une règle juridique de preuve réelle : un dossier historique unique et indépendamment authentifié pourrait légitimement documenter plusieurs rôles, mais cet outil ne sait ni le lire ni le valider. Un contre-exemple inventé avec même token, un autre avec même digest et un scénario avec deux notices distinctes sont couverts par le contrat #100.

**Base vérifiée :** PR #165 source #40105412509 SUCCESS, squash `main=e1faacc909d4c8a693e2552e64dda57b6927473f`, postmain #40106296690 SUCCESS à ce SHA, 79 étapes Windows / 99 contrats / 96 Vitest fictifs / Chromium 82/82 chaque mode / Rust 132. Nouvelle CI de la candidate encore **à qualifier**.

## Qualification source-only

Un nouveau contrat handoff #99 exécute douze contre-exemples inventés, notamment liste vide, candidat synthétique complet, auto-attestation, rôle étranger, doublon, charge utile interdite, hash incorrect, identifiant de custodian insuffisant, fausse chronologie, liaison déclarée absente, réf. dangereuse et trop d'entrées. Il impose en toutes circonstances `G2B=NOT_ACCEPTED`, `writer_absence=NOT_PROVEN`, `G3=STOP_UNAVAILABLE`, `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, `operator_access=False`, `evidence_authenticated=False`. Aucune dépendance supplémentaire ni nouvelle étape workflow ; le test s'exécute dans le contrôle handoff existant (99 contrats attendus, **non encore observés au nouveau HEAD**).

Autorité préalable : [PR #164](https://github.com/LaurentCOLL1/Fabulaxiom/pull/164) source `62868e8ac4103ecaa65d129e6e5551ff3124a99f`, CI #40101820083 SUCCESS ; fusion protégée `main=ac7c61f779c0981d418d8b5b7bb1d4a8a725cdbe`, postmain #40103615181 SUCCESS indépendamment. 79 étapes Windows, 98 tests continuité, 96 tests fictifs, Chromium 82/82 par mode, 132 tests Rust. Ceci n'ouvre aucune autorité réelle.

## STOP

M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, source `PARTIAL_LOCAL_IDENTITY_ONLY`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucune SQLite v6/v7 originale, ACL, sidecar/journal, sauvegarde, marqueur, migration 007, IPC writer, M3.3, ComfyUI, release ni action Windows opérateur.
