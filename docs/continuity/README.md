# Fabulaxiom — Point d'entrée pour reprendre les discussions ChatGPT

Ce dossier constitue la **mémoire de travail versionnée du projet**. Lire en priorité, dans cet ordre :

1. [HANDOFF_CURRENT.md](HANDOFF_CURRENT.md) : état opérationnel concis, dernier checkpoint vérifié et prochaine action.
2. [HANDOFF_CURRENT.json](HANDOFF_CURRENT.json) : mêmes barrières de sécurité en format vérifiable par CI, sans autorité d'exécution.
3. [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) : règles permanentes de reprise et de mise à jour.
4. [HANDOFF_HISTORY.md](HANDOFF_HISTORY.md) : étapes déjà fusionnées, pour éviter de refaire les mêmes audits.
5. [NEXT.md](NEXT.md), puis [STATE.md](STATE.md) : historique détaillé et plans antérieurs (certains en-têtes anciens ont un statut « en attente » depuis clos).
6. [M3_2_GATE_SNAPSHOT.md](M3_2_GATE_SNAPSHOT.md) : photographie **datée** de la preuve et des STOP.
7. [bloc historique PR #86](../qualification/M3_2_G2A_EXACT_BLOCK_REVIEW.md) : **déjà exécuté sur Windows une fois, résultat STOP_WEBVIEW2_PARENTAGE** ; ne pas relancer.
8. [nouveau candidat G2-A PID 0](../qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md) : **texte non exécuté et non autorisé** ; relecture et approbation distincte indispensables.

Pour une nouvelle conversation, copier seulement le [prompt court](RESUME_PROMPT.md). Le dépôt GitHub réel prévaut sur tout texte ou souvenir du modèle. Les SHA inscrits ici sont des **repères historiques**, jamais la preuve que GitHub n'a pas changé entre-temps.

Les PR qui modifient le code ou les procédures de M3.2 doivent aussi mettre à jour `HANDOFF_CURRENT.md` et `HANDOFF_CURRENT.json` ; un garde-fou CI refusera leur omission. Ce garde-fou ne met pas les fichiers à jour automatiquement : **le développeur doit inscrire une preuve juste, datée et vérifiable**. Seule une fusion réussie les rendra disponibles dans `main`.
