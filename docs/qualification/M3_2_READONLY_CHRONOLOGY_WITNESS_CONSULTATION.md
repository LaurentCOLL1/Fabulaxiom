# M3.2 — Stage 28 : consultation paginée de justifications synthétiques

**Python pur en mémoire, lecture seule. Pas de données opérateur, SQLite réel, accès aux archives, application React/Tauri, IPC, mutation, réseau ou nouvelle identité Windows.**

## Source vérifiée

- GitHub `main=f7eabfea74480d307b52d4b053730021efc95352` inchangée ; PR #35 ouverte DRAFT non fusionnée.
- Prédécesseur Stage27 HEAD `d4fcf5cd2bf051d8dc04655d09d250d551398fa0` : [CI Windows pull_request #38633571290](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38633571290) **completed/success 39/39**. Les 30 tests Stage27 et toutes suites antérieures étaient attachés au SHA exact.
- Les trois coordonnées temporelles restent séparées ; un chemin explicatif ne fabrique pas de tri des dates fictives et ne modifie aucun ordre narratif ou de révélation.

## Nouveau contrat de consultation (non intégré au runtime)

`consult_world_order_witness(snapshot, universe, left_id, right_id, filters=..., page_size=16, cursor=None)` revalide le couple **ACTIF** du même Univers à l'aide de Stage27/26/25, reconstitue **la chaîne complète synthétique en mémoire**, puis ne renvoie que 1 à **64 liens de précédence** par page. Le résultat est un DTO `WitnessConsultationPage` figé, IDs d'ancres et de précédences originaux, numéros **absolus de rang de lien dans ce seul chemin**, `total_evidence_links`, relation `same/before/after/incomparable`, état explicite, curseurs suivants/précédents et `editing_authorized=false`.

Les cas `same` et `incomparable` exposent zéro lien et aucun curseur. Les comparaisons `after` conservent le sens de la preuve humaine `avant → après`. Les extrémités doivent satisfaire les filtres ; les intermédiaires peuvent ne pas y correspondre, et les identifiants intermédiaires exigeraient une autorisation explicite en production. Aucun texte de calendrier, libellé, nom de participant ou révision textuelle ne doit apparaître.

Le curseur réutilise le décodeur strict Stage23. Sa seule empreinte de cohérence inclut la représentation synthétique du snapshot, les filtres **bruts**, l'ordre des deux ID sélectionnés et la largeur de page. Refuser une reprise si un de ces éléments change, si le curseur est d'un autre Univers, non aligné, booléen, négatif, hors plage, dédoublé ou mal encodé. **Ce SHA-256 n'est ni MAC, ni signature, ni permission ni attestation historique**. Le `repr(snapshot)` ne constitue pas un format d'archive reproductible. La pagination ne réduit pas le coût de construction du chemin complet ; aucune revendication de performance à grande échelle n'est faite.

## Qualification proposée et limites

`tools/test_m3_2_chronology_witness_consultation_reference.py` contient **30 tests synthétiques** : 72 liens répartis sur 2 ou 3 pages, reprises avant/arrière, conservations d'IDs, refus de changement de filtre/paire/taille/snapshot/Univers, curseurs malformés et forgés, absence de preuve, non-divulgation de libellés, immutabilité. Un **nouveau** workflow Windows pull_request sur le SHA exact doit réussir **40/40 étapes** (30 tests Stage28 ajoutés ; Stage27 30, Stage26 32, Stage25 26, Stage24 50, autres suites et frontend/Rust/Tauri). Aucun succès historique n'est transféré.

Autorité globale `PENDING_EXTERNAL_ATTESTATION` : 21 empreintes historiquement ancrées, 3 observations récentes, 2 rôles non ancrés. Préserver sept worktrees, production SQLite M1.5 v6, copie M3.1 v7 isolée, ACL, sauvegardes et manifestes. PR #35 DRAFT ; ni migration 007, ni writer IPC, ni fusion, ni M3.3.
