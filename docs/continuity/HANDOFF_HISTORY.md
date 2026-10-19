# M3.2 — Historique condensé des qualifications (référence, pas CI réutilisable)

Les détails exhaustifs restent dans [STATE.md](STATE.md) et les PR GitHub. **Toujours re-fetch les HEAD ; CI d'un commit A non transférable à B.**

| Tranche | Avancée fusionnée | Preuve et limite |
| --- | --- | --- |
| [#79](https://github.com/LaurentCOLL1/Fabulaxiom/pull/79) | Modèle source-only des capabilities Tauri | fenêtre fictive `m32-fiction` distincte de `main`, sans ACL runtime |
| [#80](https://github.com/LaurentCOLL1/Fabulaxiom/pull/80) | Matcher `RuntimeAuthority` natif sur ACL fictive | aucune fenêtre opérateur |
| [#81](https://github.com/LaurentCOLL1/Fabulaxiom/pull/81) | `Resolved::resolve` natif sur manifeste inventé | pas la vraie ACL Core |
| [#82](https://github.com/LaurentCOLL1/Fabulaxiom/pull/82) | Manifestes Core produits par `tauri-build` en CI | aucune exécution Tauri/WebView2 |
| [#83](https://github.com/LaurentCOLL1/Fabulaxiom/pull/83) | Registre d'autorité historique 21/3/2 et tests de refus | statut documentaire |
| [#84](https://github.com/LaurentCOLL1/Fabulaxiom/pull/84) | Proposition inerte G2-A, tests de consentement | aucune commande fournie |
| [#85](https://github.com/LaurentCOLL1/Fabulaxiom/pull/85) | Bloc PowerShell exact en Markdown, parser AST uniquement | exécuté manuellement ensuite : STOP PROCESS_NAMES |
| [#86](https://github.com/LaurentCOLL1/Fabulaxiom/pull/86) | Correction de détection WebView2 rattaché à SearchHost | tests synthétiques et syntaxe CI ; **nouveau bloc non exécuté** |

L'échec du premier G2-A ne doit pas être « corrigé » en arrêtant la recherche Windows. Les relations parent/enfant changent avec le temps ; les PID visibles dans une ancienne capture ne sont pas une liste blanche. Microsoft note que les PID peuvent être réutilisés et que les horodatages aident à détecter les relations incohérentes.

Les blocages externes (issues #36/#38) demeurent. Les détails techniques de la préparation du snapshot SQLite et du contrôle d'ACL ne sont **pas** requalifiés par ce registre condensé.
