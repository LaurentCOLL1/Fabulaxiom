# P3aq — désélection de la source fictive après confirmation en RAM (17 novembre 2026)

## Bénéfice produit et périmètre
Après confirmation **réussie** d'une correction d'ancre exclusivement fictive en RAM, le laboratoire React efface la cible corrigée (qui appartient désormais à l'historique), la scène, sa révision et le drapeau de détachement. L'ancienne revue est invalidée et un nouveau choix manuel est exigé avant toute nouvelle correction. Le nettoyage n'est déclenché que si la fonction de confirmation retourne une copie contrôlée sans exception ; un refus maintient l'état de saisie et affiche une erreur. La source historique, l'audit et la version superseded restent présents dans le brouillon RAM. Aucun montage productif, aucune écriture dans SQLite, IPC, sauvegarde, Hello ou recovery.

## Tests candidats
Vitest de contrat #34 : explication explicite et interdiction de prétendre à une persistance. Chromium #104 : sélectionner D, associer scène s1/révision inventée `invented-rev-B`, prévisualiser, confirmer RAM, vérifier sélection corrigée/source effacées, révision absente, confirmation réinitialisée, prévisualisation et détachement désactivés, audit `anchor_superseded` conservé et message « aucune sauvegarde ». **CANDIDAT NON QUALIFIÉ** avant nouvelle CI Windows sur HEAD exact ; Chromium 104/104 attendu avec CSP strict.

## Autorité vérifiée et frontières
Parent protected `main=3e705b6d04b1a00f20cd1c773e6c1683869ea731`, #384 MERGED sous Protect main ACTIVE strict bypass=[], source CI Windows #44125836232 completed/SUCCESS au HEAD exact `10fd450f0d66099dc97834874184b81600defca2` (Chromium 103/103, CSP 98/98, Rust 332/332), postmain indépendante #44130888195 completed/SUCCESS au SHA exact `3e705b6d04b1a00f20cd1c773e6c1683869ea731`. Checklist 104 : 9 closes/95 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif), PRODUCT_FIRST_PARALLEL_SAFETY. Writer/R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, R2 STOP/R3 partiel/D3c conception/D3b-4/5/D3b-5 STOP ; main/WAL/SHM, live WAL-index, ABA NOT_PROVEN, glib #160 OPEN_NOT_REMEDIATED. Aucun STOP levé par un test fictif.

## Suite
DRAFT/STOP MERGE tant que CI P3aq non terminale SUCCESS au HEAD exact. Diff/reviews/threads, Protect main ACTIVE strict bypass=[], READY puis squash gardé expected_head_sha, postmain indépendante et issue #38 append-only.
