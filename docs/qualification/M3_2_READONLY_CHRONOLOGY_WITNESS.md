# M3.2 — Stage 26 : justification en lecture seule des comparaisons chronologiques

**Prototype Python synthétique et indépendant, uniquement en mémoire. Aucun accès aux données utilisateur, à SQLite, aux archives, à Tauri/React, au réseau ou à Ollama.**

## Autorité vérifiée avant publication

- GitHub `main=f7eabfea74480d307b52d4b053730021efc95352` toujours inchangée ; PR #35 DRAFT et non fusionnée.
- Stage 25 : head exact `857b3025d477c20083bfa2825576174f71c92666`, [workflow Windows pull_request #38628094367](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38628094367) **completed/success, 37/37**. Stage25 comporte 26 tests synthétiques de comparaison et préserve les suites précédentes. Cette ancienne CI **ne qualifie pas** le nouveau Stage26.
- La roadmap M3 exige un ordre partiel explicitement déclaré : ni l'étiquette de calendrier fictif, ni l'ordre d'insertion, ni les IDs de source ne constituent une preuve temporelle.

## Contrat proposé

`tools/m3_2_chronology_witness_reference.py` implémente `explain_filtered_world_order(snapshot, universe, left_id, right_id, filters=...)`, sur les seuls objets `SyntheticSnapshot` Stage20–25. La sélection des deux extrémités passe intégralement par `compare_filtered_anchors` Stage25 : présence dans **un seul Univers**, conformité aux filtres, assertions **actives**, erreurs déterministes si absentes, remplacées ou retirées.

Le DTO figé `WorldOrderWitness` conserve `same/before/after/incomparable` et, uniquement pour `before/after`, renvoie `chain_anchor_ids` et `chain_precedence_ids` d'**un** chemin orienté composé exclusivement des précédences humaines du snapshot. Un parcours en largeur fournit une chaîne avec le **plus petit nombre de liens** ; lorsqu'il existe plusieurs chaînes de même longueur, l'ordre **d'insertion des relations** départage seulement le témoin explicatif choisi, jamais l'ordre chronologique. Pour `after`, la chaîne reste orientée « avant → après » (des IDs dans le sens temporel démontré, et non nécessairement gauche → droite). Pour `same`, seule l'ancre commune apparaît, sans lien ; pour `incomparable`, les deux chaînes sont vides : aucune preuve imaginée.

Les ancres intermédiaires de la chaîne sont nécessairement du **même Univers** et actives, mais peuvent ne pas satisfaire les filtres textuels des **deux extrémités**. La sortie ne fournit que les IDs des ancres intermédiaires et des précédences, jamais leurs champs textuels ou leurs références privées. **Les filtres ne sont pas une autorisation** : dans l'application réelle, un contrôle d'accès Rust/SQLite distinct sera impératif. Le simulateur refuse tout lien historique devenu inactif plutôt que d'en ignorer l'existence. Aucun ID n'est interprété comme valeur de date, révision à jour ou priorité temporelle.

`world_order_witness_json` assure une représentation JSON déterministe en mémoire, et non une signature, un mécanisme de provenance externe, une API applicative ou un registre de preuve historique. Le booléen d'édition demeure `false`, les ordres narratif et lecteur demeurent indisponibles.

## Nouvelle qualification requise — non acquise au moment du commit

Le nouveau fichier `tools/test_m3_2_chronology_witness_reference.py` ajoute **32 tests synthétiques** : chemins directs/inverses/transitifs, chemins concurrents, preuve la plus courte, indétermination explicite, calendriers fictifs, sélection filtrée, cloisonnement, refus des assertions remplacées/retirées, plus de 512 ancres, absence de fuite de texte/revision, JSON déterministe et immutabilité.

Le workflow Windows reçoit une nouvelle étape ; il doit réussir **38/38** sur le **nouveau SHA exact**, incluant les **32 nouveaux tests** et les suites Stage25/24/23/22/21/20a, provenance, Rust, frontend et Tauri. Aucun ancien succès ne peut servir de preuve de cette nouvelle version.

Statut d'archive global inchangé : **`PENDING_EXTERNAL_ATTESTATION`** (21 empreintes historiques, 3 observations récentes, 2 rôles non ancrés). Les sept worktrees opérateur, la production restaurée M1.5 v6, la copie M3.1 v7 isolée, les sauvegardes, les manifestes et les ACL restent intacts. Aucune écriture, migration 007 de production, nouvelle identité, éditeur Tauri/React, fusion de la PR #35 ou progression M3.3.
