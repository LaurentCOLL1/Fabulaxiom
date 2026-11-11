# M3.2 — P3r : choix déterministe des témoins sur graphe de précédence fictif

**11 novembre 2026 — CANDIDAT / NON QUALIFIÉ jusqu'à CI Windows SHA exact et postmain.** Parent protected `main=ca43ed2012c210c9184b093f6547fb327ee22d46` (#340 documentaire MERGED) ; CI source #340 #42977279125 SUCCESS (90 étapes) ; postmain #42990208545 attempt 1 completed/SUCCESS SHA exact (job Windows #130420945094 : 89 succès, 1 PR-only SKIPPED) ; checkpoint initial réconcilié. Protect main ACTIVE strict `bypass_actors=[]`.

## Contrat et écart constaté

- Prototype Python Stage26 dans PR #35 DRAFT : BFS des précédences actives, départage de chemins de longueur identique par **ordre d'insertion des relations du snapshot source**, donc potentiellement variable pour des listes ordonnées différemment.
- Composant actuel `src/M32WorldOrderComparison.tsx` **non monté**, données exclusivement inventées : BFS sur graphe actif, successeurs triés par **ID de relation**, choisissant une chaîne minimale déterministe indépendamment de la permutation du tableau d'entrée.
- **Décision locale P3r : conserver le tie-break TypeScript par ID et le rendre explicite dans le résultat et à l'écran.** Le champ discriminant `witness_selection_policy: "shortest_active_chain_then_edge_id"` concerne la présentation du témoin fictif, pas une affirmation de chronologie globale ni de vérité canonique. Aucun portage de l'insertion Python, qui n'est pas une garantie de la projection TS.

## Témoins et refus attendus

- Deux chaînes `A→D→C` (ID `z-route`, `z-tail`) et `A→B→C` (ID `a-route`, `a-tail`), de même longueur : TS sélectionne les ID `a-*` même lorsque leur ordre dans la projection est inversé.
- Relation historique révoquée directe `A→C` : ignorée, ne raccourcit jamais le témoin actif ; vérification de non-mutation du snapshot fictif.
- Une relation active directe plus courte reste prioritaire sur le tie-break ; tests historiques de cycle, doublons et sources étrangères continuent de refuser.
- Retour `same` ou `incomparable` : aucun témoin inventé, mais contrat de sélection explicite ; l'UI ne propose ni bouton, ni écriture, ni IPC.

## Limites et autorisations

**P3r NE prouve PAS une équivalence Stage26 globale.** Les filtres Stage25, >512 ancres et la provenance de l'ordre d'insertion ne sont pas représentés comme garanties, pas plus que le writer, P4 réel, le runtime Tauri/SQLite ou une décision canonique automatique. Checklist `M32-007/058/080 [ ]` et `M32-092/093/094 [ ]` ; **104 tâches, 2 closes, 102 ouvertes, aucune case nouvelle cochée**. `PRODUCT_FIRST_PARALLEL_SAFETY` maintenue ; avertir AVANT réorientation. R1–R9/writer NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, main/WAL/SHM/WAL-index live et ABA NOT_PROVEN, glib #160 OPEN_NOT_REMEDIATED. STOP données v6/v7 opérateur, `M:\Fabulaxiom`, profil Greenfield, backups, IPC writer, migration 007, Windows Hello et recovery. CI synthétique ≠ admission.
