# M3.2 — Matrice de résolution des preuves historiques externes

**15 octobre 2026 — décision documentaire, sans attestation nouvelle et sans action sur la machine de l'opérateur.**

## Décision en vigueur

`PENDING_EXTERNAL_ATTESTATION` demeure obligatoire. Le Stage32 de la PR #35 a passé la CI Windows exacte #38671745786 (44/44) au SHA `ac40fb29944f2f2293003bca4eb932eded496c37`, mais qualifie **des références synthétiques** ; il ne confère aucune autorisation de lecture/écriture des fichiers opérateur. Les autorisations, l'attestation historique et la qualification Windows sont des contrôles indépendants. La PR #35 reste ouverte DRAFT et non fusionnée.

Les sources applicables sont `tools/m3_2_independent_authority_gate.py` (`PINNED_SHA256`, `OBSERVED_SHA256`, `UNANCHORED_OBSERVED`, `EXACT_PATHS`), `tools/m3_2_provenance_triage.py`, `docs/continuity/STATE.md`, `docs/continuity/NEXT.md` et la section M3.2 de la roadmap. Re-fetch les sources live **avant toute éventuelle décision** ; les empreintes et comptes ci-dessous décrivent uniquement l'état vérifié au SHA Stage32.

## Cinq rôles sans preuve historique suffisante

| Rôle exact (racine, clé) | Statut | Empreinte observée SHA-256 (NON une preuve historique) | Correspondance logique | Action de preuve extérieure attendue |
| --- | --- | --- | --- | --- |
| `production / pre_m24_early_manifest` | `OBSERVED_SHA256` | `372f4ed68942a85f35a7a11a6c030589f9ff5b95d352899e00b154c99964b47d` | Manifeste `operator-qualification/m2_4/<nom ancien snapshot>.manifest.json` | Retrouver une copie/attestation **antérieure**, horodatée et conservée par une source indépendante qui associe ce chemin/rôle au digest |
| `acl / original_acls` | `OBSERVED_SHA256` | `bed23c954f720b7aca398290dfd9bed127a316687a383d21f428ae233fa54e83` | `original-acls.txt` | Pièce indépendante datée d'origine, identifiant et contexte d'export ACL, empreinte correspondante |
| `acl / pre_repair_json` | `OBSERVED_SHA256` | `5fcc1d1baec1fd4b3cb39ddbd1c866e5c6328bfd0a60c95faa23b23d1163e86e` | `pre-repair-evidence.json` | Pièce indépendante antérieure à la réparation, chaîne de garde, digest/identité du rôle |
| `production / activation_marker` | `UNANCHORED_OBSERVED` | **AUCUNE empreinte originelle ancrée** | `database/activations/activation-00000000000001791428210523732000-0000025660-0000000002.active` | Rechercher un enregistrement authentifié **contemporain de l'activation**, liant cette identité à son contenu/empreinte d'origine |
| `m25 / isolated_v6` | `UNANCHORED_OBSERVED` | **AUCUNE empreinte originelle ancrée** | `database/fabulaxiom.sqlite3` de l'espace isolé M2.5 | Rechercher la preuve de création/qualification originelle par une source indépendante, avec identité et digest d'alors |

Il y a **21** rôles `PINNED_SHA256`, **3** rôles `OBSERVED_SHA256` ci-dessus et **2** rôles `UNANCHORED_OBSERVED`. Les cinq rôles ne deviennent pas fiables sous l'effet d'une nouvelle mention dans GitHub, d'un même fichier recopié ou d'une comparaison avec le digest d'aujourd'hui.

## Politique de recevabilité — examen manuel indépendant obligatoire

Chaque proposition de preuve doit documenter explicitement :

1. L'identité précise (`root`, `role` et, si disponible, le chemin d'origine) et **le contenu couvert** ; pour les fichiers observés, confronter le digest historique signé à l'observation enregistrée.
2. La provenance **extérieure et antérieure** à la modification/au déplacement pertinent : dépositaire indépendant, date et identifiant de l'enregistrement, origine de l'horodatage, chaîne de conservation et méthode de récupération.
3. La possibilité de **vérification indépendante** de l'authenticité et de l'intégrité (ex. signature réellement vérifiable, archive tierce datée, journal distant immuable établi à l'époque). Une URL HTTPS seule, un champ JSON `custodian`, une capture d'écran non authentifiée ou une déclaration de l'auteur ne suffisent pas.
4. La correspondance stricte de rôle, l'absence d'ambiguïté entre copies (production / M2.5 / M3.1), l'indépendance du témoin et la chaîne entre la pièce et l'objet protégé. Vérifier les dates par rapport à la cérémonie initiale ; ne pas déduire l'antériorité d'une date saisie manuellement.
5. Le compte-rendu d'un relecteur humain indépendant **distinct** du créateur de la pièce. Une éventuelle modification d'autorité devra être une décision explicite et traçable dans une PR séparée, puis une nouvelle CI SHA exacte ; aucune commande de diagnostic ne doit auto-promouvoir un rôle.

**GitHub peut fournir une piste, pas une promotion automatique.** Les runs/actions, commits, archives ou attestations de build ne constituent une preuve utile que s'ils existent **depuis l'époque pertinente**, s'ils lient réellement le digest du bon fichier local au rôle, et si leur authenticité est vérifiable. Une attestation GitHub produite aujourd'hui pour un build ne prouve **pas rétroactivement** l'état historique des données Windows. Les artefacts/actions ont des politiques de rétention ; un artefact absent ne doit pas être inventé.

Documentation de contexte (non autorisante) : https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts ; https://docs.github.com/en/rest/actions/artifacts ; https://docs.github.com/en/rest/actions/permissions .

## Parcours opérateur et décisions sans raccourci

**Étape A — recherche documentaire, sans exécution locale** : inventorier d'éventuels originaux/exports antérieurs, journaux indépendants, sauvegardes tierces et preuves archivées. La recherche de métadonnées dans GitHub peut guider le travail ; elle ne prouve pas à elle seule le fichier local. Ne pas déplacer, renommer, remplacer ou ouvrir en écriture une base, un manifeste, un marqueur d'activation ou une archive ACL.

**Étape B — réception facultative de pistes de provenance** : le script déjà présent `tools/m3_2_provenance_triage.py --claims-json ... --dry-run` ne peut accepter qu'une liste stricte des cinq rôles et ne valide que la forme et certaines empreintes observées. Son code de sortie reste non autorisant ; même avec cinq URLs valides, `independently_verified_historical_claims=0`, `historical_promotions=0`, `m32_staging_authorized=false` et `PENDING_EXTERNAL_ATTESTATION`. **Ne pas lui confier de secrets, de base de production ou d'emplacements sensibles**, ni placer le fichier de claims sous un répertoire protégé. Un exemple synthétique de test n'est pas une pièce réelle.

**Étape C — examen contradictoire des cinq pièces** : une preuve manquante ou une provenance invérifiable entraîne `BLOCKED` pour la promotion historique. Conserver alors les observations comme observations, sans créer de fausse preuve. Si la pièce d'origine n'existe plus, envisager uniquement une **nouvelle voie de référence de confiance**, autorisée séparément, avec une sauvegarde cohérente non destructive ; elle peut établir une **nouvelle baseline** mais **ne prouve jamais l'histoire ancienne**.

**Étape D — préparation Windows après autorisation indépendante** : vérifier de nouveau les sept worktrees, HEAD exact, terminal CI, identité Tauri isolée, jeton Windows standard, application arrêtée, ACL, manifestes, sauvegardes, deux bases v6/v7 et empreintes avant/après en lecture seule. La qualification opérateur M3.2 doit rester distincte de la CI synthétique. Ne PAS générer ici de commandes PowerShell automatiques ni lancer l'application.

**Étape E — livraison produit seulement si les barrières sont levées** : concevoir, tester et autoriser séparément l'affichage React/Tauri/SQLite en lecture seule. Un éditeur de chronologie, les écritures IPC, la migration normale `007`, une fusion de PR #35, le passage à M3.3 et tout effet sur les historiques nécessitent chacun les autorisations gouvernées applicables ; aucun n'est implicitement permis par ce document.

## Critères de fermeture de ce blocage

- Les **cinq** rôles disposent d'une décision documentée : source réellement indépendante **vérifiée** ou manque de preuve explicitement reconnu, sans fausse promotion.
- Un relecteur autorisé a statué sur la chaîne de conservation, les empreintes et l'origine ; les états ne peuvent pas être réétiquetés depuis `OBSERVED` à l'aide d'un JSON de déclaration.
- Les vérifications de sécurité Windows et la qualification sur les données autorisées sont effectuées **après** l'étape d'attestation et la nouvelle autorisation.
- Tant que ces conditions ne sont pas vérifiées dans l'ordre, statut maintenu : **`PENDING_EXTERNAL_ATTESTATION`** et **aucune mise en production M3.2**.

> Ce plan ne contient, ne génère et ne valide **aucune** pièce historique indépendante. Il traite le blocage réel sans le contourner.
