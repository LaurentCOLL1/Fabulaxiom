# M3.2 — Lisibilité et accessibilité du laboratoire de chronologie fictive

**2026-10-17. Périmètre : interface web de test isolée, et non Fabulaxiom Tauri installé.**
Autorité initiale : `main=f4da538a5e17ead5cf4ea3b06f2ec6aaf18a1e4a` après fusion protégée de la PR #61. La qualification précédente est [CI Windows #39052427503](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39052427503) : 43/43 étapes réussies, 22 tests ciblés, 23 cas Chromium réels, 123 tests frontend et 100 tests Rust généraux.

## Problèmes traités, sans changement de domaine

Dans `src/M32SyntheticEventExplorer.tsx`, les filtres forment maintenant une région de recherche nommée (`role="search"`). Deux annonces distinctes, atomiques et identifiées par nom accessible indiquent le nombre de résultats/page et les **identifiants** du premier/deuxième événement explicitement choisi. Les boutons de choix portent `aria-pressed` vrai/faux ; l’information ne repose plus seulement sur l’apparence ou le libellé « Premier / Deuxième ». Les états en vigueur et historiques restent des **textes explicites**. Les relations humaines justificatives demeurent une liste ordonnée avec identifiants d'arêtes, direction et raisons.

Le nouveau fichier `src/m32BrowserLab.css` améliore l’espacement, le retour à la ligne, les contrastes de texte/contrôles, l’état actif visible, le focus clavier (`:focus-visible` avec contour de 3 px) et les cibles interactives (minimum 44 px en hauteur). Il s'applique **uniquement** à la page fictive `m32-browser-lab.html`, via `src/m32BrowserLab.tsx` ; `src/App.tsx`, la feuille de style de production et les dépendances/locks sont inchangés. Aucun code de domaine ne dépend du CSS.

Aucun filtrage ou changement de page ne substitue ou n’efface implicitement la paire sélectionnée. Les assertions historiques restent consultables mais jamais sélectionnables comme événements courants. Le validateur complet du graphe actif reste appelé avant chaque affichage, **même lorsque des filtres cachent le cycle**. Les changements UI n’ouvrent aucune source et n’écrivent aucun fichier.

## Qualification attendue sur HEAD exact

- Six tests Vitest supplémentaires (22 → **28**) vérifient la région de recherche, les annonces accessibles et l'état `aria-pressed` sans présélection.
- Six interactions Chromium supplémentaires (23 → **29**) vérifient les rôles accessibles, les sélections déclarées, l’annonce des résultats pendant la saisie, la conservation du focus, le contour `:focus-visible` de 3 px, les cibles >= 44 px, l’absence de débordement du panneau à **375 px**, la conservation d’une preuve sous filtre historique.
- L’étape Windows existante exécute déjà la suite frontend complète, le test ciblé `m32SyntheticEventExplorer.test.tsx`, le navigateur Chromium épinglé éphémère, le build TypeScript/Vite, Rust et tous les refus G3. Aucune suppression ni modification du workflow n’est requise. Une qualification sur l'ancien SHA ne valide pas les nouveaux changements.
- Les mesures en pixels sont **bornées à un navigateur/une largeur**. Ce ne sont ni un audit complet des contrastes/cibles WCAG, ni une étude de lecteur d’écran, de zoom, de navigation réelle Tauri ou de l’installation utilisateur.

## Limitations et autorisations

La page de test n’a aucun import depuis `App.tsx`, aucune commande `invoke`, aucune connexion SQLite, aucun accès aux originaux/sauvegardes v6/v7, aucun service réseau autre que Vite sur `127.0.0.1`. Playwright continue de résider uniquement dans `RUNNER_TEMP` du runner Windows. Le choix visuel d’un événement n’est **pas** une permission d’écriture ou une attestation de provenance.

Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, source G3 réel `STOP_UNAVAILABLE`, G3/G4/G5/G6 réels `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`. Aucune migration 007, modification de marqueur, writer IPC, exécution G3/G4 réelle, M3.3 ou release.

## Références officielles

- [W3C WCAG 2.2 — Focus visible, noms accessibles, cible et messages de statut](https://www.w3.org/TR/WCAG22/)
- [W3C WAI — régions et composants de recherche](https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/)
- [Playwright — locators et rôles](https://playwright.dev/docs/locators)
- [React — rendering lists](https://react.dev/learn/rendering-lists)
