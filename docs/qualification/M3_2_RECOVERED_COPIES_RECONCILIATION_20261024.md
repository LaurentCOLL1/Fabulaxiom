# M3.2 — Rapprochement expurgé des copies récupérées (24 octobre 2026)

**STATUT : OBSERVATION PRIVÉE, LECTURE SEULE, SANS ATTESTATION EXTERNE.** Marqueur : `DONNEES_PRIVEES_NON_PUBLIEES`.
Aucun octet des pièces, aucune base SQLite, aucune ACL, aucun chemin privé, aucun SID, aucune empreinte de la base SQLite isolée **nouvellement calculée**, et aucun contenu d’artefact utilisateur ne sont publiés ici. Le rapport détaillé intégral et ses empreintes existent uniquement dans un dossier privé téléchargeable depuis la conversation, pas dans ce dépôt public.

## Portée concrète de la comparaison

Le propriétaire a retrouvé puis transmis **six copies détachées** : les **cinq rôles** de l'[issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) ainsi qu’un **deuxième manifeste M2.4** attendu et historiquement distinct.

| Rôle de garde | Constat sur la copie reçue | Autorité inchangée |
| --- | --- | --- |
| `production/pre_m24_early_manifest` | Copie de l'ancien manifeste : SHA-256 égal à l'empreinte **déjà consignée publiquement** dans la matrice historique | `OBSERVED_SHA256`, non authentifié |
| `acl/original_acls` | Copie d'export ACL : SHA-256 égal à l'empreinte publique observée, structure cohérente avec une sauvegarde, sans restauration | `OBSERVED_SHA256`, non authentifié |
| `acl/pre_repair_json` | Copie du JSON : SHA-256 égal à l'observation publique ; document interne référant 11 objets déclarés, non relus | `OBSERVED_SHA256`, non authentifié |
| `production/activation_marker` | Copie du marqueur : contenu cohérent avec le nom de base restaurée M1.5 ; SHA égal au champ du JSON pré-réparation fourni | `UNANCHORED_OBSERVED`, pas de témoin indépendant |
| `m25/isolated_v6` | Copie candidate `fabulaxiom.sqlite3` : en-tête brut SQLite cohérent ; provenance M2.5 et schéma logique non vérifiés | `UNANCHORED_OBSERVED`, pas de preuve d'identité historique |

Le **deuxième** manifeste M2.4 (ultérieur) a un SHA correspondant au rôle historique distinct **`production/pre_m24_manifest` déjà `PINNED_SHA256`**. Les deux JSON déclarent deux chemins de sauvegarde v5 distincts, à deux heures auto-déclarées, avec le **même SHA de contenu de sauvegarde** et le même tableau de vérification logique. Les sauvegardes SQLite compagnons ne font PAS partie des pièces reçues : leur empreinte ni leur intégrité ne sont qualifiées par ce constat. Ne pas dédupliquer les sauvegardes ou supprimer le manifeste ancien.

Le champ de SHA du marqueur dans le JSON fournit un **lien documentaire auto-rapporté**, pas une attestation cryptographique tierce historiquement antérieure. La base isolée transmise est une **copie détachée**, pas la démonstration d'une identité Win32, de l'absence de writer, de la situation des journaux ou d'un lien authentifié avec le conteneur local M2.5. L'en-tête SQLite de 100 octets n'atteste ni la version de migration Fabulaxiom, ni l'intégrité de pages, ni le contenu des tables.

## Distinctions impératives

- **Pièces retrouvées : oui**, sur copies fournies ; **attestations historiquement indépendantes retrouvées : NON (0/5)**.
- Les quatre correspondances de SHA déjà publiés (trois observations et le second manifeste épinglé) prouvent la concordance **avec les empreintes de référence**, pas l'origine indépendamment datée. Le lien supplémentaire du marqueur passe par le JSON provenant du même dossier opérateur et n'est pas une cinquième attestation.
- Les rapports de création publiés dans [PR #33](https://github.com/LaurentCOLL1/Fabulaxiom/pull/33#issuecomment-6113135812) et [PR #35](https://github.com/LaurentCOLL1/Fabulaxiom/pull/35#issuecomment-6133818636) comportent des **dates de commentaire GitHub**, mais pas une preuve indépendante antérieure du contenu exact de chacun des cinq rôles.
- Les téléchargements hors du système original, les copies fournies en chat et le contrôle de format **ne constituent pas** une opération G2B, G2C ou G3 réalisée sur le Windows de l'opérateur. Aucun programme SQLite n'a ouvert les copies ou les originaux. Aucun appel au réseau ne contenait des octets des fichiers privés.

## Suite gouvernée

1. **Préserver** les six originaux et les deux paires sauvegarde/manifeste M2.4 (si présentes) dans leurs emplacements actuels. Ne pas restaurer les ACL ni activer un marqueur.
2. Conserver les constats détaillés **uniquement dans le dossier privé de l'opérateur** ; n'archiver ici ni les fichiers eux-mêmes ni leurs nouveaux digests privés.
3. Sur la voie historique, rechercher **uniquement** de possibles preuves externes indépendantes **antérieures** ; leur absence persistante doit être expressément documentée sans inventer d'attestation.
4. Sur la voie prospective de [l'issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38), préparer ensuite un **protocole séparé de référence de confiance nouvelle**, incluant auteur/opérateur, chaîne de garde, identités et journaux, writer, procédure sans écrasement, restauration isolée et revue contradictoire avant approbation spécifique. Cette voie ne rétro-authentifie jamais les artefacts historiques.
5. **Aucun changement des STOP** : M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 **OPEN/DRAFT**. Aucun geste Win32, SQLite original, ACL, marqueur, sauvegarde, migration 007 ou IPC writer.

**Précision chronologique :** le checkpoint précédent est [PR #166](https://github.com/LaurentCOLL1/Fabulaxiom/pull/166) (source CI #40107790950, squash `c1fee9638c343c51e2e0bdab6ac8fccf2340104b` et postmain #40108674282 : tous TERMINAL SUCCESS indépendamment, 79 étapes Windows et 100 contrats). Ce document et cette PR restent de la qualification documentaire ; toute nouvelle CI doit réussir sur le SHA exact de sa propre branche.
