## 26/11/2026 — M32-073 motif humain de supersession candidat

Parent 9fffd70cb07acbe466fb49afa64986aa22d961dd ; #431 CI #45706491192 SUCCESS exact HEAD 9bae11d937221236c3435ff0e1eff44315d1027c ; postmain #45755296134 PENDING au contrôle initial. Motif humain obligatoire pour le formulaire de remplacement, lié à la prévisualisation et au journal RAM ; abandon explicite avant confirmation sans suppression, 4 Vitest candidats, scénarios Chromium existants adaptés (pas encore attestés). Appels historiques de fixtures préservés, aucun writer/runtime admis. M32-073 [ ] : preuve Chromium dédiée et annulation compensatoire après confirmation restent à examiner. 18/86 ; M32-078 [ ] ; IN_PROGRESS_NOT_ACCEPTED ; PRODUCT_FIRST_PARALLEL_SAFETY.

### Résultats de #432 et suite de M32-073

La CI Windows #45857121460 a réussi sur le HEAD `9c8b436d7768b0890e7e93a6465035e7749f9cf4` (job #140038295559). La première exécution #45755554493 avait échoué au scénario 45 sur `bb2f7263b2368de3368718d2f551e6b7877a00f2`. Le parcours corrigé exige un motif, abandonne un premier aperçu puis confirme le second. Le journal conserve uniquement le motif confirmé. CI push #45859162191 sur le commit fusionné `fb36a2f5e7857d09e3e461cb8d3a2b84c3cfe57e`, en cours au contrôle initial. Registre #38, commentaire #7197708103.

Le candidat ajoute un lien explicite entre une ancre remplacée et sa nouvelle version dans le journal fictif. Pour annuler une correction, l’auteur reprend les valeurs de la version précédente, saisit un nouveau motif et confirme une troisième version. Le scénario 113 vérifie le calendrier, la date, la révision source, les trois lignes et les deux changements de statut. Le scénario 114 vérifie qu’une relation révoquée reste visible après la création motivée d’une nouvelle relation sur la même paire.

Vérification locale Linux du candidat : 681 tests Vitest réussis, TypeScript et scénarios Chromium 45, 113 et 114 réussis. La qualification Windows propre au candidat reste à établir. M32-073 et M32-078 restent ouvertes.
