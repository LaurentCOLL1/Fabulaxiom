# M3.2 — P3p : refus des extrémités historiques et des liens actifs dupliqués

**10 novembre 2026 — CANDIDAT SOURCE/CI À QUALIFIER.**
Parent protected `main=7660c96cf9b3eab3a8a958253f35726356420ee4`.
PR #336 P3o fusionnée : HEAD source `8a3d0c8e23ae3077fbfd8afd010d640dda08f279`,
CI Windows #42894263560 attempt 1 completed/SUCCESS au HEAD exact (89 étapes),
postmain #42896536877 attempt 1 completed/SUCCESS sur main exact
(job #130111014880, 88 SUCCESS, 1 étape PR-only SKIPPED).
Protect main actif, strict, `bypass_actors=[]`.

## Écart ciblé et analogie historique #35

Le service Rust `src-tauri/src/m32_manual_chronology.rs` possède déjà les tests
`retired_anchors_cannot_receive_new_edges` et
`successor_active_graph_rejects_raw_cycles_and_duplicates`, sur DB fictive
`#[cfg(test)]`. Le précédent P3o couvrait le cycle de précédences actives dans
l'aperçu TypeScript isolé ; il ne vérifiait **pas** les deux scénarios suivants :

1. Une précédence `current` utilisant une ancre `revoked` ou
   `superseded` est acceptée à tort par le décodeur de l'aperçu, même si la
   relation devrait être invalide en tant qu'assertion présente.
2. Deux précédences `current` ayant des ID distincts mais la même paire
   orientée d'ancres sont acceptées alors qu'elles redoublent un fait actif.

## Correctif minimal : validation de projection seulement

Le contrôle de frontières TypeScript crée une table `ancre → statut` après
validation des ancres. Pour chaque relation **`current` seulement**, il
refuse les extrémités non `current`, puis les duplications de paire
`(before_anchor_id, after_anchor_id)` indépendamment de l'ID de relation.
Les relations historiques `revoked` et `superseded` restent visibles et
n'invalident pas les ancres retirées qu'elles décrivent. Le refus entier
précède toute sortie React : aucune projection partiellement trompeuse.

Nouveaux témoins Vitest : refus côté source et destination, ancre révoquée,
pas de divulgation de texte lors du refus, paire active dupliquée avec ID
et motifs différents, acceptation d'une paire active et d'une ancienne
assertion révoquée. P3o et sa détection de cycles restent intacts.

**Aucun accès** au filesystem opérateur, SQLite réel, v6/v7, Tauri IPC,
migrations, writer, Windows Hello ou recovery ; l'aperçu n'est toujours pas
monté dans `App.tsx`. Ce test ne prouve pas la cohérence d'un runtime complet.

## Checklist et limites

**104 obligations, 2 closes (M32-001 et M32-002), 102 ouvertes ;
AUCUNE case nouvelle clôturée.** `M32-007 [ ]`, `M32-058 [ ]`,
`M32-080 [ ]` : couverture supplémentaire *fixture-only* dans le chantier
de réconciliation #35, sans clôturer les obligations de production.
CI P3p HEAD et postmain **NON QUALIFIÉES au checkpoint initial**, à vérifier
sur les vrais SHA et runs sans anticipation. Journal issue #38 append-only.

Stratégie `PRODUCT_FIRST_PARALLEL_SAFETY` inchangée ; prévenir AVANT
tout changement. M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % estimés),
writer/R1–R9 `NOT_PROVEN`, P4 réel STOP, G2B `NOT_ACCEPTED`,
G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique
`PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`,
main/WAL/SHM et ABA invisible `NOT_PROVEN`, glib #160
`OPEN_NOT_REMEDIATED`. CI fictive ≠ admission.
