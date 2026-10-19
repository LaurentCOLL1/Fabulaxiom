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

## Sécurité opérateur

Aucune étape Windows locale sous-entendue par « Continue ». Toute nouvelle commande doit être présentée **en entier**, mentionner Entrée/`q`/UAC/risque d'arrêt, réseau, écriture/sidecars, et être approuvée spécifiquement avant lancement. Les journaux locaux sensibles restent privés. L'absence de relecteur humain indépendant ne permet pas d'en simuler un.

Une vérification PowerShell AST seule ne certifie pas la sécurité OS de l'exécution. L'ancestralité PID/`SearchHost.exe` est une observation informative, pas une preuve cryptographique de signature, ni une attestation d'absence d'écrivain SQLite.

Les scripts et fichiers de handoff ne **créent jamais** une autorisation ; un changement de champ JSON ne peut pas débloquer G2–G6.
