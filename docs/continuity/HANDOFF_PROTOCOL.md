# Contrat permanent de reprise et de mise à jour — Fabulaxiom

## Principe

Un nouveau fil ChatGPT ne doit pas reconstruire M3.2 à partir de milliers de lignes de conversation. Il doit commencer par [HANDOFF_CURRENT.md](HANDOFF_CURRENT.md), puis [HANDOFF_CURRENT.json](HANDOFF_CURRENT.json), [HANDOFF_HISTORY.md](HANDOFF_HISTORY.md), [NEXT.md](NEXT.md) et [STATE.md](STATE.md). Re-fetch GitHub ensuite **avant tout write**, et re-fetch encore avant toute fusion. En cas de divergence, la réalité GitHub prime ; ne jamais convertir une supposition de continuité en preuve.

## Obligations à chaque tranche

1. **Avant travail :** vérifier `main`, branches, PRs/issues, SHA du dernier commit, règle Protect main, CI valide au HEAD exact. Conserver le SHA initial.
2. **Développement :** branche de travail dédiée, diff borné, aucune mutation des bases privées (prod v6, isolée v7), backups, ACL, markers, sept worktrees locaux ; pas de migration 007 ni IPC writer sans autorisation distincte.
3. **Avant PR :** mettre à jour `HANDOFF_CURRENT.md` et `HANDOFF_CURRENT.json` dans **la même PR** avec les faits du nouveau checkpoint et les STOP inchangés. Ajouter une entrée `HANDOFF_HISTORY.md` lorsqu'une étape est terminée. Garder `NEXT.md` et `STATE.md` alignés. Un contrôle CI sur le diff refuse les PR M3.2 significatives sans mise à jour des deux fichiers de handoff.
4. **Validation :** tests adversariaux, nouvelle CI au nouveau SHA ; examiner les logs et les attestations annoncées, pas seulement le badge vert.
5. **Fusion :** relire re-fetch main/heads/workflows/threads/reviews/ruleset, puis fusion protégée `expected_head_sha` uniquement après réussite des checks exigés. **Ne pas déclarer fusionnée une PR encore ouverte.**
6. **Après fusion :** revérifier le nouveau SHA `main`; corriger dans un commit ultérieur toute information datée devenue périmée (les empreintes historiques ne sont jamais des autorisations vivantes). Rapport succinct dans l'issue #38.
7. **Arrêt et nouvelle conversation :** le prompt du prochain fil ne contient que le lien du dépôt, les chemins des fichiers et une demande de re-fetch. Éviter d'empiler les anciennes PR/CI/chemins privés.

## Deux niveaux de prompts de reprise — obligation à CHAQUE PR (23 octobre 2026)

- **Court :** [RESUME_PROMPT_SHORT.md](RESUME_PROMPT_SHORT.md) est le point d'entrée directement copiable dans une nouvelle conversation, sans avoir à demander à ChatGPT de régénérer le prompt. Format volontairement concis, avec lien vers le prompt long et vers les fichiers de continuité, les barrières STOP réelles et le dernier checkpoint *vérifié* à la rédaction.
- **Long :** [RESUME_PROMPT.md](RESUME_PROMPT.md) reste le prompt de reprise **détaillé**, comprenant les dépendances, qualifications, état produit, règles GitHub/CI, archives de preuve et mesures de sécurité. Le prompt court le cite explicitement ; un nouvel assistant doit le lire avant toute modification.
- **Synchronisation obligatoire :** chaque **nouvelle PR**, y compris docs-only, doit inclure une modification réelle des **DEUX** chemins `docs/continuity/RESUME_PROMPT_SHORT.md` et `docs/continuity/RESUME_PROMPT.md` dans son diff, ainsi que des deux handoffs dans les PR matérielles. Actualiser `STATE.md`, `NEXT.md`, `HANDOFF_HISTORY.md` et la roadmap selon les faits nouveaux ; préserver les checkpoints historiques au lieu de les réécrire.
- **Garde-fou automatique :** le job Windows `M3.2 require both resume prompts on every pull request` vérifie les deux chemins contre la base exacte de la PR. Si l'un manque, il échoue et empêche la fusion grâce au contexte requis `Windows frontend and Rust checks`. Le contrat Python vérifie l'existence, le renvoi du court vers le long, les barrières et les informations du checkpoint, ainsi que la concision. Aucun job ne prétend créer ou actualiser les documents automatiquement.
- **Limite structurelle :** une PR ne peut pas documenter à l'avance son propre numéro attribué après création, sa CI future ou son commit de fusion. Le texte doit mentionner uniquement les états observés, le travail candidat et la nécessité de re-fetch ; les résultats terminaux sont inscrits plus tard, séparément, dans l'issue #38 et une PR de continuité si nécessaire. Ne jamais promouvoir une CI `IN_PROGRESS_AT_CHECKPOINT` en réussite par anticipation.

## Règle permanente — paralléliser les travaux indépendants quand c'est possible

**Objectif :** gagner du temps de développement **sans accélérer artificiellement un gate** et sans risquer de perte de données. À chaque reprise, établir des tâches distinctes, leurs dépendances, leurs entrées immuables (HEAD Git exact) et leurs conditions STOP avant de les exécuter.

1. **À exécuter en parallèle lorsque les sources et destinations sont indépendantes :** lectures/re-fetch GitHub et vérifications de CI, audit de roadmap/exigences, recherche publique de provenance historique, revue du code, analyses de risques et tests adversariaux sur **fixtures inventées**. Des changements de code indépendants peuvent avancer sur **branches ou worktrees de développement séparés**, avec responsables/périmètres identifiés, sans partager de répertoire mutable.
2. **À garder séquentiel ou exclusif :** écritures sur le même fichier ou la même branche/ref ; rebase/merge/commit qui se disputent une HEAD ; modifications des handoffs canoniques ; qualifications dépendant de commits ; fusion dans `main` ; opérations sur une destination ou un état de sécurité partagé. La vérification finale du `main` et du HEAD de la PR précède **immédiatement** chaque fusion protégée, avec `expected_head_sha` et CI terminale **sur ce HEAD exact**. Tout commit nouveau invalide la qualification précédente de la PR.
3. **Dépendances et validation :** organiser plusieurs flux (A : produit/source et tests fictifs ; B : références historiques #36 ; C : sûreté G2/G3 source-only et décision prospective #38 ; D : tests CI et documents de continuité) puis intégrer **un flux après l'autre** sur `main` avec re-fetch, vérification des différences/reviews/ruleset, CI fraîche et checkpoint cohérent. Des analyses parallèles ne remplacent ni attestation indépendante ni essai opérateur.
4. **Barrières absolues :** ne jamais ouvrir, lire, écrire, migrer, sauvegarder, restaurer ou manipuler en parallèle les originaux SQLite v6, v7 isolée, journaux/sidecars, ACL, activation marker ou backups protégés. Aucun lancement Windows opérateur, migration 007, writer IPC, promotion de G2B–G6, M3.3 ni release sans **autorisation distincte et explicite** ; le simple `Continue` ne suffit pas.
5. **Arbitrage automatique :** privilégier le parallèle seulement si les tâches sont réellement indépendantes, les risques et sources exactes connus et les protections maintenues. Sinon, sérialiser et documenter le blocage plutôt que créer une course ou réduire les contrôles. Noter à chaque reprise les sous-tâches parallèles, leur HEAD, leur résultat et les actions restées interdites.

**Preuve documentaire uniquement :** cette règle organise le travail GitHub et les fixtures, mais ne crée aucun droit d'accès ni aucune preuve d'absence d'écrivain concurrent SQLite.

## Sécurité opérateur

Aucune étape Windows locale sous-entendue par « Continue ». Toute nouvelle commande doit être présentée **en entier**, mentionner Entrée/`q`/UAC/risque d'arrêt, réseau, écriture/sidecars, et être approuvée spécifiquement avant lancement. Les journaux locaux sensibles restent privés. L'absence de relecteur humain indépendant ne permet pas d'en simuler un.

Une vérification PowerShell AST seule ne certifie pas la sécurité OS de l'exécution. L'ancestralité PID/`SearchHost.exe` est une observation informative, pas une preuve cryptographique de signature, ni une attestation d'absence d'écrivain SQLite.

Les scripts et fichiers de handoff ne **créent jamais** une autorisation ; un changement de champ JSON ne peut pas débloquer G2–G6.
