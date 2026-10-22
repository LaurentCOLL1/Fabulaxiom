# M3.2 — Consultation fictive de l'historique des corrections

**Source candidate, 22 octobre 2026.** En attente de qualification CI au HEAD exact; sans autorisation d'utilisation Windows.

Ce petit panneau React expérimental affiche une lignée de corrections explicitement révoquées ou encore actives sur **des données inventées en mémoire**. Il est séparé de `App.tsx`, n'importe aucun module Tauri, SQLite ni adaptateur réseau, et ne contient aucun contrôle de modification. Le validateur `auditM32FictionalCorrectionChain` refuse les erreurs d'univers, les cycles, les racines multiples, les enfants sans parent retiré, les bifurcations et les révocations incomplètes. L'affichage conserve tous les prédécesseurs pour l'inspection; il ne prétend pas déduire une chronologie totale.

À ce stade, ni la source, ni les tests n'ont été qualifiés sur Windows : ne pas déclarer le jalon accepté. Toute évolution devra conserver la séparation entre cette démonstration et l'application normale. Aucune connexion à une SQLite opérateur ou au service réel de chronologie.

**Gates toujours fermés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Pas de migration 007, writer IPC, sauvegarde, activation réelle, M3.3, ComfyUI ni release.
