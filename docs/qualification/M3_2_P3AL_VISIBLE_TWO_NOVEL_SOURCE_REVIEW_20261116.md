# P3al — aperçu des sources d'ancres entre deux romans fictifs (16 novembre 2026)

## Fonction
Étend `m32FictionalAnchorSupersessionPreview.ts` : `old_source` et `new_source` sont calculées uniquement par recherche du `revision_id` exact dans le catalogue inventé et validation du `universe_id`, `novel_id` et `scene_id` dans la narration du même univers. La source absente reste `null` ; source introuvable ou étrangère : REFUS. Copies séparées et revalidation complète avant confirmation, y compris refus d'une prévisualisation avec roman/scène falsifiés.

`M32ManualChronologyLab.tsx` affiche les identifiants exacts des roman et scène historiques et envisagés avant la confirmation RAM ; sans date grégorienne ni ordre global déduits. Cinq tests Vitest nouveaux n°20–24 : changement de roman, conservation, détachement, absence de source et métadonnées forgées.

## État et limites
Base protégée `main=83111ef207d5e585f993dbf5efd8ad4fbddd1527`, PR #379 P3ak MERGED, source Windows CI #43930211771 completed/SUCCESS exact `42cc82a79d35067352e1b48dc65a51b5d5c1275a` ; postmain #43938092253 PENDING_UNQUALIFIED lors de la préparation. **P3al CANDIDAT, sans preuve de CI propre avant exécution.** Aucun App.tsx runtime, écriture, Tauri IPC, base originale, profil opérateur, backup, migration, Hello ou recovery. Checklist M3.2 104=9 closes/95 ouvertes, M32-055/059/061/073/075/076/079/081 toujours [ ] PARTIELS ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % estimés), PRODUCT_FIRST_PARALLEL_SAFETY, writer/R1–R9 NOT_PROVEN, P4/G2B/G2C/G3 STOP, R4 main/WAL/SHM/ABA NOT PROVEN, glib #160 OPEN.
