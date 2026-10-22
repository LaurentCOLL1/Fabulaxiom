# M3.2 — Consultation fictive de l'historique des corrections

**Source candidate, 22 octobre 2026.** En attente de qualification CI au HEAD exact; sans autorisation d'utilisation Windows.

Ce petit panneau React expérimental affiche une lignée de corrections explicitement révoquées ou encore actives sur **des données inventées en mémoire**. Il est séparé de `App.tsx`, n'importe aucun module Tauri, SQLite ni adaptateur réseau, et ne contient aucun contrôle de modification. Le validateur `auditM32FictionalCorrectionChain` refuse les erreurs d'univers, les cycles, les racines multiples, les enfants sans parent retiré, les bifurcations et les révocations incomplètes. L'affichage conserve tous les prédécesseurs pour l'inspection; il ne prétend pas déduire une chronologie totale.

À ce stade, ni la source, ni les tests n'ont été qualifiés sur Windows : ne pas déclarer le jalon accepté. Toute évolution devra conserver la séparation entre cette démonstration et l'application normale. Aucune connexion à une SQLite opérateur ou au service réel de chronologie.

**Gates toujours fermés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Pas de migration 007, writer IPC, sauvegarde, activation réelle, M3.3, ComfyUI ni release.

## Laboratoire navigateur fictif

Un onglet isolé « Afficher l'historique fictif des corrections » présente trois générations fictives sur le premier univers, aucun événement sur le deuxième et un refus explicite pour le scénario d'ascendance cyclique. Trois nouveaux cas Playwright sont ajoutés au parcours Chromium normal et CSP strict : le total **candidat** passe de 50 à 53 pour chaque mode, sous réserve d'une qualification CI fraîche. Aucune modification de `App.tsx`, aucun IPC ni import réseau.

## Source manifest strict et refus des imports externes

CI #39748895327 a initialement refusé l'import du nouveau composant parce que le manifeste Git fictif contenait exactement dix fichiers. L'ajout est **limité à un seul fichier** `src/M32FictionalCorrectionHistory.tsx` dans `tools/m32_ci_fixture_stage.cjs` et dans `tools/m32_ci_git_source_binding.cjs`, portant l'inventaire strict à onze. Le bind reste fondé sur les blobs du commit exact, refuse tout import hors de l'inventaire, `App.tsx`, les symlinks et les écarts de bytes. Le test de longueur a été adapté à onze, sans supprimer de test négatif. La nouvelle CI complète au nouveau HEAD est obligatoire.

## Tranche suivante — lien explicite au prédécesseur, source-only (22 octobre 2026)

Le tableau de consultation du laboratoire fictif affiche, après validation stricte de la chaîne, le prédécesseur immédiat de chaque correction et son assertion humaine précédente (`avant/après`). Cela décrit uniquement une ascendance explicitement déclarée ; ni la succession éditoriale des corrections ni la position des scènes ne crée une date ou un ordre global du monde. Le premier élément n'invente aucun prédécesseur. Un historique invalide reste rejeté entièrement, sans fuite du contenu partiel, et le deuxième univers reste vide.

Seuls `src/M32FictionalCorrectionHistory.tsx`, ses assertions Vitest déjà existantes et le cas Chromium existant 51 sont modifiés. Le nombre de tests reste huit pour ce composant et 53 scénarios Chromium par mode ; ces nombres ne deviennent des résultats que si la CI du **nouveau SHA** les démontre. Aucun `App.tsx`, Tauri, IPC, SQLite, réseau, stockage ou Windows opérateur n'est concerné. M3.2 demeure `IN_PROGRESS_NOT_ACCEPTED`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`.
