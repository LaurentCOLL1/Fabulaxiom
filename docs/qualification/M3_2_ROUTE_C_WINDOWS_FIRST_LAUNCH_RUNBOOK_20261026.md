# Fabulaxiom — voie C / premier lancement Windows « projets neufs » (proposition contrôlée)

**26 octobre 2026 — PREPARED_NOT_EXECUTED_ON_OPERATOR_WINDOWS.**
Voie C uniquement : création d'histoires **nouvelles**, sans import, migration historique, restauration ou accès aux originales M1.5 v6, M3.1 v7, ACL, backups anciens, journaux/sidecars, marqueur d'activation et IPC writer. La qualification source est [PR #181](https://github.com/LaurentCOLL1/Fabulaxiom/pull/181) : CI source #40277924539 et postmain #40278919705 indépendamment SUCCESS ; base Rust v6 sur nouveaux fichiers du runner jetable. Le vrai lancement Windows opérateur **n'a pas eu lieu**. Le consentement général exprimé dans la conversation du 26 octobre vaut pour la **préparation** de ce bloc ; le script n'est pas un moteur d'autorisation à lui seul et aucune autorisation historique ne découle de la voie C.

## Pourquoi deux phases

Le profil Tauri supplémentaire `src-tauri/tauri.greenfield.conf.json` utilise l'identifiant `com.fabulaxiom.greenfield.v1`, à distinguer du normal `com.fabulaxiom.desktop` ; Tauri lie normalement `appLocalDataDir` à `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` lorsque les répertoires ne sont pas surchargés. Un nom différent ne prouve **ni** l'absence d'entrée préalable ni l'absence de junction/reparse, ni des droits corrects, ni l'absence de course après inspection. Microsoft documente notamment le bit `FILE_ATTRIBUTE_REPARSE_POINT`. Références : https://v2.tauri.app/reference/javascript/api/namespacepath/#applocaldatadir et https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-point-operations.

Le préflight `tools/greenfield_first_launch_preflight.ps1` ne fait que lire l'identité du checkout, les sources Tauri, les noms **immédiats** sous la racine de données et les attributs de ses ascendants. Il n'utilise pas d'ouvre-base ni de commande d'écriture. Un affichage `GREENFIELD_PREFLIGHT_METADATA_ONLY_CANDIDATE` signifie **observé à un instant**, sans réservation atomique ni preuve native d'identité par handle ; toute ambiguïté vaut STOP. La CI peut l'exercer dans une **racine temporaire GitHub jetable**, jamais sur Windows opérateur.

## Prérequis humains (pas d'installation automatique)

1. Poste Windows local accessible par le propriétaire ; terminal PowerShell ordinaire **non administrateur**. Aucun UAC accepté pendant l'essai ; s'il apparaît, STOP.
2. Checkout Git distinct et propre, dont le HEAD est **exactement le SHA de `main` revalidé à l'instant de l'essai** (à copier depuis l'issue #38/le checkpoint terminal ultérieur). Le chemin local réel du checkout doit être fourni par l'opérateur, pas inventé dans une réponse. Le script calcule son propre répertoire Git depuis `$PSScriptRoot`.
3. Git, Node/npm, Rust/cargo, Microsoft C++ Build Tools (`Desktop development with C++`), Microsoft Edge WebView2. Tauri documente ces deux prérequis Microsoft et Rust pour développer sous Windows : https://v2.tauri.app/start/prerequisites/. Le script constate seulement l'existence de commandes ; **il ne certifie pas** l'installation/configuration de C++ Build Tools ou de WebView2.
4. Au moins 2 Gio disponibles sur le volume du dossier local. Toute redirection/liaison de la racine ou de ses ancêtres, entrée Greenfield existante, instance Fabulaxiom active ou identité inconnue : STOP, **ne pas forcer ou réutiliser**.
5. Ne présenter aucun original, ni sauvegarde historique, ni destination liée aux anciens profils ne doit être présentée à ce test ; ne jamais le résoudre en mode admin.

## Bloc A — lecture des métadonnées, STOP strict

Dans un PowerShell **non administrateur**, placé manuellement à la racine d'un checkout Git Fabulaxiom propre (chemin choisi et contrôlé par l'opérateur) :

```powershell
# Remplacer uniquement par le SHA de main confirmé après la dernière PR.
$ApprovedHead = 'SHA_MAIN_EXACT_A_REMPLACER'
& .\tools\greenfield_first_launch_preflight.ps1 -ExpectedHead $ApprovedHead
if ($LASTEXITCODE -ne 0) { throw 'STOP Greenfield : aucun lancement autorisé' }
```

Effets : uniquement interrogation des commandes disponibles, lecture du checkout et de son état, des deux fichiers JSON Tauri, des attributs des ascendants de `%LOCALAPPDATA%`, et des noms des entrées de **ce dossier uniquement** ; contrôle de présence de processus et d'espace libre. Aucun fichier SQLite, journal, marqueur, backup, ni ACL originale n'est ouvert. Le script ne crée **rien dans le profil Greenfield** et n'appelle pas Tauri. Une politique d'exécution PowerShell qui bloque ce fichier est un **STOP** à examiner, pas une invitation à contourner la politique par `-ExecutionPolicy Bypass`.

Conserver dans le compte rendu le **statut et le chemin candidat**, en masquant l'identité nominative de l'utilisateur si partage public. Si la cible n'est pas absente ou qu'un attribut est douteux : STOP. Le test ne prouve pas qu'un tiers ne modifie pas la destination ensuite.

## Bloc B — construction et premier essai DEV, effets créateurs

Ce bloc est **distinct du préflight**. À lancer manuellement **seulement** après le bloc A vert, revue visuelle du chemin candidat, validation des prérequis C++/WebView2, et décision humaine de poursuivre sur cette destination neuve. Le fait que l'utilisateur autorise la voie C n'étend pas le test aux anciens fichiers.

```powershell
# Toujours à la racine du checkout propre, sans UAC.
npm ci
if ($LASTEXITCODE -ne 0) { throw 'STOP dépendances' }
# réexécuter l'échantillon metadata-only immédiatement avant toute création.
& .\tools\greenfield_first_launch_preflight.ps1 -ExpectedHead $ApprovedHead
if ($LASTEXITCODE -ne 0) { throw 'STOP cible non neuve ou préflight expiré' }
if (-not (Test-Path -LiteralPath '.\node_modules\.bin\tauri.cmd' -PathType Leaf)) {
    throw 'STOP binaire Tauri local absent'
}
.\node_modules\.bin\tauri.cmd dev --config src-tauri/tauri.greenfield.conf.json
```

Effets à accepter : `npm ci` peut accéder au registre réseau, télécharger des dépendances verrouillées, écrire `node_modules` et exécuter les scripts de dépendances ; `tauri dev` peut télécharger des sources Rust verrouillées, compiler et écrire `src-tauri/target`, démarrer Vite sur l'interface locale `localhost:1420`, ouvrir la fenêtre « **PROJETS NEUFS** » et, au premier accès base, créer sous la nouvelle racine `database/fabulaxiom.sqlite3`, ses dossiers, éventuels journaux et migrations ordinaires **001–006**. Aucun bundle/release autorisé (configuration `bundle.active=false`). Le processus se termine via fermeture de la fenêtre et/ou `Ctrl+C` dans le terminal. Aucun `npx` (risque de résolution/téléchargement implicite si CLI local absent).

**Contrôle de fenêtre obligatoire :** si le titre n'indique pas `PROJETS NEUFS`, si une ancienne histoire apparaît, si un chemin est inattendu, si UAC apparaît ou si des écritures anormales sont observées : **STOP immédiatement**, pas de récupération/renommage/migration forcée.

## Session fonctionnelle minimale, créations neuves uniquement

- Créer un **univers fictif**, une série, un roman, un chapitre et une scène, avec deux révisions de texte ; noter uniquement les identifiants fictifs et un verdict d'interface, pas de contenu privé.
- Fermer complètement, relancer **le même** profil Greenfield et contrôler la persistance, la sélection de version, l'entité, un fait sourcé et une revue humaine explicitement déclenchée. Le préflight initial refusera désormais l'entrée existante : **c'est voulu** ; ne pas contourner ce garde après coup, ni relancer la première cérémonie.
- Générer une **sauvegarde de ces seuls nouveaux projets** et constater sa présence via l'interface. **AUCUNE restauration** dans cette première session : l'API actuelle active une copie restaurée **dans la racine active**, alors que la qualification de restauration complète prévoit une **autre destination vierge** (VM ou compte séparé) et une procédure exacte distincte.
- Fermer le processus et noter : SHA source, statut/chemin du préflight, compte non admin, absence UAC, prérequis, actions M1/M2, redémarrage, sauvegarde, erreurs et constat de fermeture. Ne publier aucun journal personnel ou chemin nominatif complet.

## Limites, résultat attendu et non-autorités

- Un contrôle de noms/attributs **n'est pas** une preuve de réservation atomique, d'ACL native, de provenance ni de quiescence. Pour une assurance forte contre une création concurrente, il faudra une ouverture créatrice native à identité vérifiée et une revue sécurité spécifique.
- Le profil Greenfield et la CI Rust ne sont **pas** M3.2 G2B/G3. Aucun opérateur Windows observé dans cette PR ; une future réponse du propriétaire restera `OWNER_REPORTED` tant que non attestée indépendamment.
- L'issue #38 reçoit seulement de nouveaux checkpoints datés. STOP inchangés : M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, écrivain historique `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective historique `NOT_STARTED`, #35 OPEN/DRAFT.
