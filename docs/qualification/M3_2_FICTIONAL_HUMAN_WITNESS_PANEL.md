# M3.2 — Consultation des preuves humaines du temps fictif (candidat)

**CANDIDATE_NOT_CI_QUALIFIED — uniquement navigateur de test inventé.** La comparaison `M32WorldOrderComparison` existe déjà : cette tranche la rend consultable depuis l'atelier manuel `M32ManualChronologyLab` sans dupliquer l'algorithme.

## Comportement

- Deux identifiants d'ancres courantes explicitement sélectionnés. Aucune sélection par intitulé ni connexion au canon.
- Le moteur de preuve déjà validé inspecte exclusivement le graphe de précédences humaines en vigueur. Il renvoie une chaîne déterministe d'identifiants et de motifs humains en cas de précédence directe/transitive, le sens inverse, la même assertion, ou l'absence de preuve.
- Les liens `revoked` ou `superseded` ne justifient plus d'ordre courant. Après une révocation *manuelle explicite*, la consultation React se met à jour sans effacer les anciens liens.
- La position des scènes dans un roman, les titres et les dates littéraires ne créent **aucune** précédence du monde. Révélation du lecteur non renseignée.
- Aucune écriture depuis ce panneau, aucun `App.tsx`, aucune commande Tauri, aucun SQLite réel.

## Contrôles demandés

Six tests Vitest supplémentaires, total attendu **48** dans l'atelier : lien direct, chaîne transitive déterministe, ordre inverse, exclusion des relations révoquées, refus d'identifiant étranger et absence de mutation, présence des sélecteurs. Trois scénarios Chromium, total attendu **44 par mode** : chaîne humaine fictive, lien historique exclu, révocation explicite et réévaluation immédiate ; exécuter les modes normal et précompilé sous CSP stricte, avec vérification d'absence de requête réseau hors loopback. Les chiffres ne sont pas des PASS avant CI terminale au HEAD exact.

**Gates inchangés :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT ; G2A metadata-only accord consommé ; absence d'écrivain SQLite non prouvée ; G2B à G6 interdits, vrai G3 STOP. Ne toucher à aucune base originale v6/v7, ACL, sauvegarde, journal, marqueur, migration 007, writer IPC, M3.3 ou release. Aucune commande opérateur Windows autorisée.
