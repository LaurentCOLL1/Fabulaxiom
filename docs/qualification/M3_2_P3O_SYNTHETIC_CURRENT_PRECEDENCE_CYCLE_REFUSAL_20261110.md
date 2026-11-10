# M3.2 — P3o : refus des cycles de précédence dans l'aperçu fictif isolé

**10 novembre 2026 — CANDIDAT, NON QUALIFIÉ avant CI HEAD exacte et postmain.**
Parent `main=e997a239f71d726c67880dd4acc07dfcda80482e` ;
PR #335 fusionnée, CI source #42875150735 SUCCESS, CI postmain #42877389890
attempt 1 completed/SUCCESS au SHA exact. Protect main actif, strict, bypass=[].

## Écart et changement ciblé

L'audit historique PR #35 (`M3_2_PR35_PER_PATH_DISPOSITION_20261110.md`)
appelle une comparaison sélective des refus de graphes de précédence. Dans
`src/M32ChronologyPreview.tsx`, le décodeur rejetait les références étrangères
et les liens réflexifs mais ne rejetait pas un cycle de deux précédences
**en vigueur**, malgré l'affichage explicite de « avant/après — assertions humaines ».

Le changement ajoute une validation de graphe dirigé bornée (Kahn) **uniquement**
sur les relations `current` après contrôle strict des identifiants. Si les
relations actives sont cycliques, la projection entière est refusée sans révéler
les données du snapshot. Les relations `revoked`/`superseded` restent consultables
comme témoignages historiques et **ne créent pas de cycle actif**.

Le test Vitest couvre (a) deux assertions courantes contraires, (b) le refus
d'affichage complet, (c) la conservation du témoignage historique révoqué.
Ce refus ne suppose **aucune** conversion de dates fictives ni chronologie globale
entre romans. Il ne réécrit aucun service Rust ni aucune migration.

## Portée et suivi de checklist

- `M32-007 [ ]` : les 84 chemins #35 ont été triés ; ce témoin P3o ne
  prouve pas l'équivalence totale aux 20 références Python anciennes.
- `M32-058 [ ]` et `M32-080 [ ]` : preuve **partielle / fixture-only**
  côté aperçu TS. Rust, Windows réel et l'admission opérateur restent distincts.
- Checklist vivante : **104 obligations, 2 closes, 102 ouvertes** ;
  **AUCUNE case nouvelle clôturée**.
- CI source et postmain du lot P3o : **À VÉRIFIER après création de PR**.
  Les SHA et runs ne doivent jamais être anticipés.

## Limites de sécurité maintenues

`PRODUCT_FIRST_PARALLEL_SAFETY`, prévenir AVANT tout changement ;
`IN_PROGRESS_NOT_ACCEPTED` (~45 % d'estimation) ;
writer/R1–R9 `NOT_PROVEN`, P4 réel STOP, G2B `NOT_ACCEPTED`,
G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`,
historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`,
main/WAL/SHM/ABA `NOT_PROVEN`, glib #160 `OPEN_NOT_REMEDIATED`.
Aucune ouverture de v6/v7 opérateur, Greenfield, backups, `M:\\Fabulaxiom`,
IPC writer, migration 007, Windows Hello ni recovery. CI fictive ≠ admission.
