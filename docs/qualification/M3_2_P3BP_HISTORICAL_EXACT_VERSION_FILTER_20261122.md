# P3bp — numéro exact de version dans l'historique fictif (22/11/2026)

Dans l'atelier React fictif **non monté**, un filtre permet de choisir **toutes les versions** ou un numéro de version explicite existant (1, 2, etc.). La recherche renvoie uniquement les identifiants opaques d'événements. Le numéro exact et tous les autres filtres (ancre, source, date, temporalité, champ modifié) doivent coïncider sur la **même version** ; aucune union d'anciennes versions ni exposition implicite du texte, des notes et des motifs.

La version 0 signifie « toutes les versions » dans l'API de filtrage, jamais une version persistée. Argument négatif, fractionnaire, infini ou NaN refusé. Changement de filtre : sélection et pagination réinitialisées. Aucune écriture, pas de réseau, SQLite, Tauri ni accès opérateur.

Vitest #53 : versions 1/2/3, champs modifiés et contradictions interversions, invalides et immutabilité. Vitest #54 : rendu SSR des seuls numéros, notes et justifications historiques masquées. **CANDIDATS avant CI Windows HEAD exact**, aucun passage du gate M3.2.

Parent protected `main=3b30e12e3337e71e5bfa571fb2d6424e17addc18` ; #411 CI source #44962625083 SUCCESS HEAD exact e759cd82dbbd139ff68bc5aa37a69d9fac964220 ; postmain #44973406392 PENDING_UNQUALIFIED. Checklist 104 : 12 CLOSED_SCOPED/92 OPEN_NOT_ACCEPTED, M32-071/078/081 [ ], PR35/215 DRAFT NON_ACCEPTED ; PRODUCT_FIRST_PARALLEL_SAFETY ; STOP Writer/R1–R9, P4, G2B/G2C/G3, WAL/SHM/ABA, glib #160 OPEN.
