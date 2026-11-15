# M3.2 P3ad — corrections/révocations de précédences fictives en lot (15/11/2026)

## Portée source candidate

Parent protégé après #366 : `main=533350934590ea367982b50e845154dbdfcb82da`, #366 source CI Windows #43665202152 terminal SUCCESS au HEAD exact `ef32a510d472414f703d97bd715afdb230d22a32`. Postmain #366 [#43667623908](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43667623908) **NON QUALIFIÉE au moment de la préparation**. Aucun droit supplémentaire.

La PR P3ad ajoute un **lot de 1–16 décisions humaines explicitement choisies** pour révoquer une précédence active, avec remplacement facultatif par une *nouvelle* précédence. La relation révoquée reste dans la projection et l'audit, jamais effacée ni remplacée sur place. Chaque remplacement a ses propres ancres actives et son motif humain ; aucune correction n'est calculée depuis l'ordre des romans, scènes ou calendriers. Tous les choix sont validés sur le graphe fictif entier, et une erreur tardive refuse globalement le lot sans altérer la version source. La prévisualisation est séparée de la confirmation ; la confirmation réévalue toute la base et l'intégralité des propositions, refusant les previews périmées ou modifiées. Retour d'état strictement en RAM.

## Cas Vitest candidats

14 cas nouveaux dans `src/m32FictionalHumanOrderRepair.test.tsx` :
1. prévisualisation immuable et refus d'autoriser une écriture ;
2. confirmation explicite obligatoire ;
3. remplacement donnant nouvelle identité tout en conservant l'ancienne relation ;
4. refus d'un cycle introduit par remplacement ;
5. refus des révocations dupliquées/historiques ;
6. refus d'IDs étrangers, anciens, absents ou réflexifs ;
7. refus des lots vides/surplombants, motifs invalides et champs de contournement ;
8. refus des confirmations périmées ou de propositions altérées ;
9. refus de preuve candidat forgée et d'un indicateur writer falsifié ;
10. conservation ordre des audits, narration et révélation ;
11. redéclaration explicite d'un même arc avec nouvel ID ;
12. refus de fausse provenance d'une base opérateur ;
13. contrôles React visibles et aucune fausse réussite de sauvegarde ;
14. échappement HTML des identifiants de relation inventés.

Les cas sont **CANDIDATS** tant que CI Windows au HEAD exact, Protect main, revues et postmain indépendante ne sont pas qualifiés. Ils ne prouvent **aucune** transaction SQLite, aucun undo réel, ni l'absence de R1–R9.

## Exigences et gates

- M32-057, M32-073, M32-081 : preuves partielles, cases [ ].
- M32-056/058/063/072/078/080 restent [ ] ; pas de promotion à l'acceptation.
- R4 M32-017/019/020 restent [ ], absence de capture atomique main/WAL/SHM et ABA invisible non prouvé.
- Checklist 104 = **9 clôtures ciblées / 95 ouvertes**, M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 %).
- `PRODUCT_FIRST_PARALLEL_SAFETY` maintenu ; writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; R2 STOP, R3 partiel ; D3c conception, D3b-4/5 et D3b-5 STOP.
- `glib #160` OPEN_NOT_REMEDIATED ; aucune modification de lock.
- Interdiction d'ouvrir v6/v7, `M:\\Fabulaxiom`, Greenfield, backups, IPC writer, migration 007, Hello ou recovery.
- `Protect main` ACTIVE strict `bypass=[]`, CI au HEAD exact, reviews/threads, guarded squash avec `expected_head_sha`, nouveau postmain indépendant et issue #38 append-only obligatoires.

Aucune intégration dans `App.tsx`, aucune commande Tauri, aucun accès réseau/fichier, aucune migration ou réécriture SQLite. L'UI de laboratoire React demeure exclusivement fictive, non montée dans l'application opérateur.
