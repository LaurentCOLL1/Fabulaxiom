# M3.2 — Proposition de consentement G2-A (NON EXÉCUTABLE)

**STATUT : PROPOSAL_ONLY. AUCUN SCRIPT, AUCUNE COMMANDE WINDOWS, AUCUNE AUTORISATION DE LANCEMENT.**

Cette proposition clarifie ce que l'opérateur pourrait autoriser un jour dans une observation G2-A strictement non invasive. Elle ne lance rien et ne collecte ni chemin, ACL, empreinte, base SQLite, contenu narratif, secret ou identifiant Windows. Le contrat est dans [M3_2_G2A_OPERATOR_REVIEW_PROPOSAL.json](M3_2_G2A_OPERATOR_REVIEW_PROPOSAL.json) ; les tests `tools/test_m32_g2a_consent_contract.py` en vérifient la nature non exécutable. La CI vérifie uniquement le **contrat**, et non la sécurité de toute future commande concrète.

## Portée proposée, sans exécution

| Observation future envisagée | Donnée admissible | Refus |
| --- | --- | --- |
| Jeton Windows courant | Niveau d'intégrité uniquement, sans élévation | SID, identité personnelle, ACL privée, UAC |
| Session PowerShell | Version, sans écriture | Script non revu, profil exécuté de façon imprévue |
| Horloge | Date, fuseau, sans accès SQLite | Horodatage présenté comme preuve historique |
| Processus | Présence possible d'une application, sans arrêt | Fermeture forcée de Fabulaxiom/Tauri/Ollama |
| GitHub public | Commit `main`, état PR/check/ruleset via vérification distante indépendante | `git fetch` ou autre commande réseau locale non expressément approuvée |

Ces cinq informations sont des **intentions de revue** et non des observations effectuées. Les données privées ne doivent jamais figurer dans GitHub.

## Préalables à tout bloc Windows G2-A ultérieur

1. Re-fetch GitHub et fixer le SHA de la future proposition. Écrire un bloc PowerShell `& { ... }` exact et séparé, **non présent dans cette PR**, puis inspecter sa totalité, ses API, ses fichiers, sa collecte et ses effets.
2. Prévenir l'opérateur avant exécution de tout caractère interactif (`q`, Entrée), élévation/UAC, fenêtre ouverte, arrêt éventuel de processus, accès disque ou réseau et éventuelle journalisation. À ce stade, le cahier des charges exige **zéro interaction, élévation, arrêt ou écriture locale** ; un script qui ne peut tenir ce contrat est STOP.
3. Obtenir l'accord **spécifique du propriétaire** sur le code exact, son empreinte, le périmètre, la machine et les effets. Le simple « Continue » du développement ou une CI verte ne vaut pas cet accord.
4. Exécuter seulement à cette étape future approuvée ; rapport privé minimal `PASS|FAIL|NOT_ASSESSED` pour chaque vérification ; en cas d'inconnu, **STOP**. Aucun déblocage implicite de G2-B, G2-C, G2-D, G3–G6.

**ATTENTION :** l'état des sidecars `-wal`/`-shm` et des ACL est réservé à des étapes futures spécifiquement autorisées ; elles nécessiteront une revue des effets des API d'ouverture et des chemins privés, sans présumer que `mode=ro` est sans effet. Le [plan G2](M3_2_G2_WINDOWS_SOURCE_IDENTITY_PREFLIGHT_PLAN.md) conserve ses seuils et refus. Les opérations Win32 `CreateFileW` et leurs drapeaux de partage/réparse exigent une analyse par handle avant toute confiance dans une identité de chemin. Un `Get-Item` ponctuel ou un chemin textuel ne constitue pas une fixation stable de l'identité. <NEVER_RUN_THIS_DOCUMENT>

## Verdict du document

`G2-A=PROPOSAL_ONLY/NOT_ASSESSED`. `G2-B/C/D=NOT_AUTHORIZED`. Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT et issues #36/#38 OPEN. `M32_SECURITY_PREFLIGHT_STOP` ; `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`. Pas de fusion #35, migration 007, writer IPC, M3.3 ou release.

Références techniques : https://www.sqlite.org/wal.html ; https://www.sqlite.org/backup.html ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew .
