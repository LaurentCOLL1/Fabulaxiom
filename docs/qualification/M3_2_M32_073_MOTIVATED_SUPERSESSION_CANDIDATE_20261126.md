## 26/11/2026 — M32-073 motif humain de supersession candidat

Parent 9fffd70cb07acbe466fb49afa64986aa22d961dd ; #431 CI #45706491192 SUCCESS exact HEAD 9bae11d937221236c3435ff0e1eff44315d1027c ; postmain #45755296134 PENDING au contrôle initial. Motif humain obligatoire pour le formulaire de remplacement, lié à la prévisualisation et au journal RAM ; abandon explicite avant confirmation sans suppression, 4 Vitest candidats, scénarios Chromium existants adaptés (pas encore attestés). Appels historiques de fixtures préservés, aucun writer/runtime admis. M32-073 [ ] : preuve Chromium dédiée et annulation compensatoire après confirmation restent à examiner. 18/86 ; M32-078 [ ] ; IN_PROGRESS_NOT_ACCEPTED ; PRODUCT_FIRST_PARALLEL_SAFETY.

### Résultats de #432 et suite de M32-073

La CI Windows #45857121460 a réussi sur le HEAD `9c8b436d7768b0890e7e93a6465035e7749f9cf4` (job #140038295559). La première exécution #45755554493 avait échoué au scénario 45 sur `bb2f7263b2368de3368718d2f551e6b7877a00f2`. Le parcours corrigé exige un motif, abandonne un premier aperçu puis confirme le second. Le journal conserve uniquement le motif confirmé. CI push #45859162191 sur le commit fusionné `fb36a2f5e7857d09e3e461cb8d3a2b84c3cfe57e`, en cours au contrôle initial. Registre #38, commentaire #7197708103.

Le candidat ajoute un lien explicite entre une ancre remplacée et sa nouvelle version dans le journal fictif. Pour annuler une correction, l’auteur reprend les valeurs de la version précédente, saisit un nouveau motif et confirme une troisième version. Le scénario 113 vérifie le calendrier, la date, la révision source, les trois lignes et les deux changements de statut. Le scénario 114 vérifie qu’une relation révoquée reste visible après la création motivée d’une nouvelle relation sur la même paire.

Vérification locale Linux du candidat : 681 tests Vitest réussis, TypeScript et scénarios Chromium 45, 113 et 114 réussis. La qualification Windows propre au candidat reste à établir. M32-073 et M32-078 restent ouvertes.


### 26/11/2026 — qualification source et postmain de #433

**Acquis 2026-11-26 — CANDIDAT SCOPED :** CI #45859353900 SUCCESS HEAD exact 02ceec4ea52352d0bd47ca3d0d5c0c85682f85ce, job #140046011093 étape 44 ; postmain #45862982772 SUCCESS SHA exact 0d893d24d3dde94c59421646b199c6b16272e933, job #140058520899. Cas 45, 113, 114 observés chacun deux fois sur les deux jobs (Vite et précompilé), 114/114 deux fois, 681 Vitest. Motif non vide, abandon sans mutation, prévisualisation, confirmation, compensation par nouvelle version et nouvelle relation motivée ; historique et révision source conservés. Périmètre conception du laboratoire RAM fictif NON MONTÉ uniquement ; aucune persistance, writer ni opérateur. Nouvelle CI du registre et postmain nécessaires ; requalifier si intégration réelle.

M32-073 [x] candidat de clôture documentaire ; 19/85 sur branche, 18/86 main. M32-078 [ ] ; M3.2 IN_PROGRESS_NOT_ACCEPTED. Tous STOP maintenus.


### 26/11/2026 — première CI du registre #434, échec conservé

CI #45865551864, HEAD exact `827022d3175b7ab83adc9ec4a3ea9a2d918a6320`, job #140067320828 : FAILURE étape 33, `test_04_master_checklist_not_falsely_closed` (liste historique de 18 IDs non synchronisée, M32-073 seule différence). Étapes 28–32 SUCCESS, dont checklist et matrice/registre ; 40/41 tests de réconciliation historique réussis. Correction ciblée : ajout explicite de M32-073 à la liste de 19 clôtures SCOPED, aucun assouplissement des refus M32-007/M32-078, #35/#215, writer et runtime. Nouvelle CI intégrale requise au HEAD corrigé ; aucun PASS hérité de #45865551864. 19/85 branche candidate, 18/86 main.
