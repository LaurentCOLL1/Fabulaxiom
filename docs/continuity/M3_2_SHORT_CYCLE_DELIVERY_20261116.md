# M3.2 — développement en cycles courts (16 novembre 2026)

**Objet :** accélérer le travail sans allonger les chaînes d'actions GitHub et sans promouvoir un résultat non qualifié. Ce protocole n'autorise jamais l'accès opérateur, le writer ou un bypass Protect main.

## Règles de cycle
1. Re-fetch main/PR/CI/ruleset avant une décision ; conserver les SHA/run exacts. Lectures groupées avec au plus trois requêtes simultanées ; ne pas relire une source inchangée pour le même SHA.
2. Regrouper les modifications cohérentes en une PR. Préparer et tester en parallèle les tâches indépendantes ; sérialiser toute écriture dans un chemin commun et toute fusion.
3. CI en cours : consigner `PENDING_UNQUALIFIED`, run + HEAD, puis poursuivre une tâche indépendante sur branche séparée en DRAFT ; ne pas interroger Actions en boucle.
4. Échec CI : identifier le job et l'assertion, confirmer l'état de branche, effectuer un correctif minimal ; aucun doublon de PR/commit/fusion et aucun report de la réussite précédente sur un nouveau SHA.
5. Fusion seulement après parent postmain SUCCESS SHA exact, source CI Windows terminal SUCCESS HEAD exact, diff/reviews/threads, Protect main ACTIVE bypass=[], PR READY, squash `expected_head_sha` ; nouveau main et postmain indépendants ; issue #38 append-only.
6. Actualiser les deux prompts, HANDOFF MD/JSON, STATE, NEXT, gate, roadmap et checklist après chaque vraie validation, en gardant les 104 IDs uniques, les non prouvés ouverts et les STOP inchangés.

## État initial
PR #377 P3aj MERGED `main=a9c2cd7cd095ec8fb7f0ecad9ede66428dfed991` ; CI source #43908932749 SUCCESS au HEAD `6f60dfdd158fbfa93d75cb95116417c8d8de6c6b` ; postmain indépendante #43913712275 PENDING_UNQUALIFIED au checkpoint. M3.2 IN_PROGRESS_NOT_ACCEPTED ; 9/104 closes, 95 ouvertes ; PRODUCT_FIRST_PARALLEL_SAFETY. R1–R9/writer NOT_PROVEN, P4/G2B/G2C/G3 STOP, R4 main/WAL/SHM/ABA NOT_PROVEN, glib #160 OPEN.

## Pistes parallèles autorisées
Produit : laboratoire fictif non monté, sans persistance et sans App.tsx ; sécurité : expériences R4 jetables et tests de refus ; gouvernance : checklist/source CI/documentation. STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, migration 007, Hello, recovery.

## Reprise
Lire le prompt court et la tête de HANDOFF_CURRENT.json ; ne relire le long historique que pour une dépendance technique non encore validée. À chaque fin de cycle noter réalisés, SHA/PR, CI confirmées et PENDING, cases vraiment clôturées, reste, prochaine action.
