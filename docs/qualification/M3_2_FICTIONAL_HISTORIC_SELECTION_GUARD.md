# M3.2 — Sélections historiques après correction (atelier fictif)

**CANDIDATE_NOT_CI_QUALIFIED** — seulement tests sur données imaginaires, sans intégration à App.tsx ni persistance.

## Comportement

Une correction humaine remplace une ancre active par une nouvelle identité, en conservant l'ancienne comme `superseded`. Si une comparaison de précédence avait sélectionné l'ancien identifiant, le formulaire annonce **« Sélection historique »**, affiche l'ancien identifiant comme option désactivée et **ne montre plus de preuve d'ordre courant**. Il faut choisir deux ancres actives. Les liens humains historiques ne sont ni effacés ni promus. Dans le navigateur de laboratoire, changer d'Univers réinitialise intégralement la sélection ; aucun identifiant d'autre Univers n'est admis.

La règle est une prévalidation de présentation pure `fictionalSelectionIsHistorical`, pas une nouvelle logique de temps. Le moteur existant `compareM32WorldOrder` continue de refuser les ancres historiques lui-même. Ordre de narration et révélation lecteur toujours indépendants.

## Qualification attendue

Trois nouveaux tests Vitest (**51 au total**) : refus d'ancienne ancre, provenance immuable et état de révélation, garde pure d'IDs courants. Deux nouveaux scénarios Chromium (**46 dans chacun des modes**) : après supersession, plus de preuve tant qu'un nouvel ID courant n'est pas choisi ; changement d'Univers fictif sans contamination. Vérifier mode navigateur normal et précompilé sous CSP stricte, et un **nouveau SHA de CI** avant toute fusion. Ces chiffres ne sont pas encore une réussite.

## STOP non négociable

M3.2 IN_PROGRESS_NOT_ACCEPTED ; PR #35 OPEN/DRAFT. G2-A PASS metadata-only, autorisation ponctuelle consommée, écrivain SQLite réel NOT_PROVEN ; G2-B/C/D et G3–G6 NOT_AUTHORIZED, REAL_G3 STOP_UNAVAILABLE. Ne toucher à aucune originale v6/v7, sauvegarde, WAL/SHM, ACL, activation, migration 007, IPC writer, M3.3, ComfyUI ou release. Aucune commande Windows opérateur exécutée ou autorisée.
