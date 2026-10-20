# M3.2 — Atelier manuel fictif de chronologie (création / correction / révocation)

**Travail fonctionnel sur fixtures, uniquement navigateur isolé. Aucun contrôle Windows opérateur ni extension G2-B/G3.** Dérivé de `main=a839953f73f17379aa7c5ccde69d807b5b99a2f6` après fusion de PR #97, CI post-fusion #39428345389 terminale SUCCESS. Re-fetch le dépôt et la CI de cette nouvelle PR avant fusion.

## Livrable précis

`src/m32FictionalManualChronology.ts` : réducteur de projet chronologique **entièrement en mémoire** basé sur `M32ChronologyProjection`. Il accepte uniquement des Univers avec préfixe `fiction-`. Pas d'API SQL, pas de disque ni d'IPC Tauri. Les entrées exactes exigent un calendrier fictif + une étiquette, les approximatives un calendrier fictif + une description d'incertitude, et les inconnues/relatives n'inventent pas de date. Toutes les modifications créent une nouvelle valeur en mémoire, jamais de mutation du tableau initial.

Actions humaines fictives :
- Ajouter une ancre temporelle `exact / approximate / relative / unknown` par identifiant créé localement.
- Déclarer `A avant B` avec justification humaine, en refusant auto-référence, identité manquante, ancre historique, doublon ou **cycle transitif**. Aucune comparaison totalisée ou conversion grégorienne.
- Corriger une ancre par **supersession append-only** : l'ancienne conserve son ID et `source_revision_id`, la nouvelle reçoit un ID distinct. Un lien actif à l'ancienne interdit sa correction jusqu'à **révocation explicite**.
- Révoquer un lien en conservant sa raison précédente et en enregistrant séparément l'explication humaine dans un journal fictif de session.
- Préserver le tableau de narration (plusieurs romans possibles) et l'ordre de révélation `not_authored`, distincts de l'ordre du monde.

`src/M32ManualChronologyLab.tsx` présente ces opérations à travers des formulaires React. Le [laboratoire navigateur fictif](../../src/m32BrowserLab.tsx) offre un **troisième mode** « atelier manuel fictif » avec réinitialisation à chaque changement de scénario. Un scénario cyclique initial est refusé sans afficher le formulaire. Ce laboratoire browser distinct **n'est pas** le `App.tsx` de production et ne peut ni lire l'ordinateur de l'opérateur ni émettre des IPC.

## Tests et limites

`src/m32ManualChronologyLab.test.tsx` : 13 tests Vitest pour les quatre formes temporelles, refus des champs manquants, cycles, liens invalides ou doubles, conservation des révisions immuables, révocations avant correction, narration multiromans, refus d'un Univers étranger, volumes bornés et rendu des commandes fictives. Ils rejoignent le `npm run test:ci` existant et le contrôle `npm run build` de la CI Windows.

**Ce n'est pas l'acceptation produit de M3.2** : aucun transfert vers une SQLite réelle ni vers le M3.1 isolé v7, aucun lien à une scène/révision **nouvelle** depuis un formulaire, aucune écriture applicative, aucun test d'UI Windows opérateur, aucun backup de source privée ou procédure de création/restauration. Le mot « CRUD » du plan M3.2 demandera un contrat de revocation/supersession durable et une persistance isolée autorisée séparément. Les tests sont un incrément utilisateur fictif, pas une preuve de réalisation complète.

Le contrôle du graphe est réalisé **en mémoire sur les seuls nœuds actifs**, en refusant un chemin bouclé avant d'autoriser la relation. Il complète, sans remplacer, l'[exemple officiel SQLite des CTE récursives pour parcours de graphe](https://www.sqlite.org/lang_with.html), utile pour une future traduction SQL qualifiée.

## Traçabilité des exigences

| Exigence roadmap M3.2 | Preuve proposée | Statut |
| --- | --- | --- |
| Quatre types de temporalité | Tests Vitest 01–03 | SYNTHETIC_ONLY |
| Deux Univers et plusieurs romans | Scénarios navigateur + test 09 | SYNTHETIC_ONLY |
| Relation avant/après saisie manuelle | Tests 04–05, formulaire | SYNTHETIC_ONLY |
| Refus cycles, auto-liens, doublons | Tests 04–05, 10, 13 | SYNTHETIC_ONLY |
| Correction sans perte des assertions et révisions | Tests 06–08 | SYNTHETIC_ONLY |
| Monde / narration / révélation distincts | Composants de consultation existants + test 09/12 | SYNTHETIC_ONLY |
| CRUD persistant, UI locale Windows qualifiée, conservation des originales | Aucune nouvelle preuve | **NOT_ACCEPTED** |
| CI exact-head, acceptance indépendante, normalisation | CI de cette PR à vérifier ; acceptation non établie | **NOT_ACCEPTED** |

## Barrières intactes

G2-A `PASS_METADATA_ONLY_OWNER_REPORTED` après accord unique consommé ; `PROCESS_WRITER_ABSENCE=NOT_PROVEN` ; G2-B/C/D, G3–G6 `NOT_AUTHORIZED`, réel G3 `STOP_UNAVAILABLE`. Historique 21/3/2 non attesté, prospective NOT_STARTED, PR #35 DRAFT. Aucun accès aux bases v6 production/v7 isolée, WAL/SHM/journaux, ACL, sauvegardes, marqueur, migration 007, writer IPC, M3.3, ComfyUI ou release.

**Pas de commande PowerShell ; tout nouveau geste opérateur exige le script exact, description des effets et autorisation spécifique nouvelle.**
