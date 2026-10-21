# M3.2 — Comparateur fictif des trois ordres : candidature de qualification

**Statut : CANDIDATE_NOT_CI_QUALIFIED.** Cette fiche décrit une prochaine PR, ne prouve aucune réussite CI et n'autorise aucune opération Windows ou SQLite réelle.

## Périmètre produit

Dans `src/M32ManualChronologyLab.tsx`, deux listes sélectionnent des **identifiants de scènes inventées**, pas leurs titres. `previewFictionalThreeOrders` (fonction pure) renvoie trois explications distinctes en lecture seule :

- **Narration** : ordre des chapitres/scènes seulement à l'intérieur du **même roman** ; égalité de position pour deux scènes différentes = indéterminée ; scènes dans des romans différents = indéterminées ; scène absente = refus.
- **Monde** : toujours indéterminé par ces choix de position manuscrite, même si des ancres humaines existent ailleurs. Aucun tri temporel inféré.
- **Révélation au lecteur** : non renseignée, aucune exposition ou connaissance déduite du texte ou de la narration.

Pas d'enregistrement, mutation, révision de scène, résolution `head` ni propagation de canon ; l'historique et les relations temporelles restent inchangés.

## Preuve à exiger sur un SHA nouveau

Six nouveaux Vitest (**42 tests atelier attendus**) : position intra-roman dans les deux sens, romans distincts, même scène, références absentes/étrangères, collision de position dans un roman, non-mutation même si des précédences existent. Trois nouveaux scénarios Chromium (**41 par mode attendus**) : scène première/suivante dans un roman, romans distincts, second Univers fictif sans scènes. Vérifier les modes navigateur normal et précompilé strict CSP, l'absence d'accès réseau externe, et le contrôle de provenance exacte de fixture CI.

Toute CI appartient exclusivement à son commit. Ni une CI verte antérieure ni cette fiche ne prouvent un produit accepté.

## STOP toujours applicable

**M3.2 = IN_PROGRESS_NOT_ACCEPTED.** PR #35 DRAFT. G2-A PASS métadonnées seulement (autorisation unique consommée), `PROCESS_WRITER_ABSENCE=NOT_PROVEN`, G2-B/C/D–G6 `NOT_AUTHORIZED`, réel G3 `STOP_UNAVAILABLE`. Historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucune originale SQLite v6/v7, backup, WAL/SHM/journal, ACL, marqueur, migration 007, writer IPC, App.tsx, M3.3, ComfyUI ni release. Aucun script Windows opérateur demandé ou exécuté.
