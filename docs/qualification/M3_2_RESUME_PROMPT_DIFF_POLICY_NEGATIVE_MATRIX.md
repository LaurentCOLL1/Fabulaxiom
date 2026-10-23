# Fabulaxiom M3.2 — matrice négative du garde des prompts de reprise (23 octobre 2026)

**SOURCE-ONLY / NO OPERATOR SQLITE / NO WINDOWS EXECUTION BY USER.**

## Objectif

Le dépôt utilise deux niveaux de reprise :
- `docs/continuity/RESUME_PROMPT_SHORT.md`, copie rapide vers une nouvelle conversation ChatGPT ;
- `docs/continuity/RESUME_PROMPT.md`, reprise exhaustive et liens vers les documents d'autorité.

La règle de PR ne doit pas accepter une modification de documentation qui oublie un prompt ; une PR de code, d'audit ou de workflow doit également actualiser les deux handoffs canoniques. L'ancienne vérification PowerShell du diff a été extraite en `tools/m32_resume_pr_diff_policy.py`, appelée sur **la liste des chemins** produite par la CI Windows contre la base Git de la PR, puis qualifiée par `tools/test_m32_resume_pr_diff_policy.py` utilisant **uniquement des listes de chemins inventés**.

## Scénarios attendus

- Docs-only avec les deux prompts : PASS
- Code/modification matérielle avec deux prompts + les deux handoffs : PASS
- Un seul prompt, aucun prompt, diff vide : STOP
- Code sans les deux handoffs ou avec un seul handoff : STOP
- Modification d'un workflow ou d'une pièce de qualification sans handoffs : STOP
- Chemin qui imite le prompt court sans correspondance exacte : STOP
- Doublons ou fichiers supplémentaires sans prompt court : STOP

**Limite :** la règle vérifie les fichiers modifiés, pas la véracité du contenu. Les checks de handoff contrôlent séparément la concision, les liens, le statut M3.2 et les barrières. Une future CI source au SHA exact est indispensable ; une CI sur un ancien SHA ne qualifie pas un commit différent.

## Checkpoint vérifié

PR #142 source `f17a5c62fb6cc5fcb6259138b4f529b8f07bc581`, CI source #39930833733 SUCCESS, fusion `main=98216aa5f5045d6faa4202b76709507b61027534`, CI post-fusion #39932102283 SUCCESS. Cette nouvelle matrice est **candidate** tant que sa propre CI n'a pas réussi au HEAD exact et qu'elle n'est pas fusionnée.

**Gates inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; source `PARTIAL_LOCAL_IDENTITY_ONLY` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT.
