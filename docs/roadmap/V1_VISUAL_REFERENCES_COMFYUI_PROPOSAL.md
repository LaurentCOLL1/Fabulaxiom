# Fabulaxiom V1 — Atelier de références visuelles et ComfyUI local (proposition)

## Statut et autorité

**PROPOSITION DOCUMENTAIRE — AUCUNE IMPLÉMENTATION AUTORISÉE**

Origine : demande utilisateur d'illustrer les personnages, certains événements et certaines scènes/situations pour explorer des idées et vérifier que le rendu correspond à l'intention narrative.

Issue de suivi : **#19 — atelier visuel local pour personnages, scènes et événements via ComfyUI**.

Ce document propose une extension supplémentaire aux fonctionnalités V1. Il ne remplace pas la roadmap M2 acceptée. **M2.1 reste exclusivement la migration/schema v4 des entités et alias**. Aucun développement ComfyUI ou image n'est autorisé tant qu'une future subdivision explicitement bornée n'a pas reçu les approbations et normalisations habituelles.

## Expérience souhaitée

Fiche **Personnage** :
- galerie de portraits de référence, vues de face/profil, silhouette, vêtements, expressions et versions liées à une époque du récit ;
- variantes visuelles sans altérer l'identité stable du personnage ;
- une ou plusieurs images marquées `référence visuelle approuvée`.

Fiche **Scène / Situation / Événement** :
- proposition d'illustration tirée d'un passage ou d'une description libre ;
- compositions alternatives, plans, ambiance, éclairage, lieu et personnages présents ;
- liaison optionnelle à un `scene_text_revisions.id` immuable, pour comprendre à quelle version du texte l'image répond ;
- vues de comparaison entre texte, références visuelles, variantes et choix.

Autres entités : lieux, objets, organisations ou règles illustrables lorsque pertinent, sans obliger chaque type à avoir une image.

Workflow humain :
1. importer une image existante ou choisir `Générer avec ComfyUI` ;
2. lire/modifier le brief créatif et choisir un workflow disponible ;
3. produire plusieurs variantes et les comparer côte à côte ;
4. approuver une référence visuelle, conserver une piste exploratoire ou rejeter ;
5. réutiliser une référence de personnage pour de nouvelles scènes sans promesse de constance automatique des traits ;
6. aucun changement de fait canonique ou de texte sans confirmation explicite et action séparée.

Une image est une **aide créative**, pas une preuve que des faits ont été établis dans l'histoire. L'approbation d'une image comme référence visuelle ne doit **jamais** promouvoir automatiquement une proposition au statut `canon`.

## Phases proposées (à confirmer par future autorité)

**Phase A — bibliothèque/import local (sans IA)** :
- importer PNG/JPEG/WebP compatibles (formats acceptés à valider) ;
- vérifier signature de fichier, dimensions, taille, chemin canonique et duplication/hash ;
- enregistrer les binaires hors SQLite dans un répertoire applicatif sécurisé ;
- conserver en SQLite des métadonnées et des liens par identifiants stables ;
- lien au sujet narratif et, si pertinent, à la révision immuable d'une scène ;
- images multiples, variantes et statut de sélection distinct du canon ;
- visible/usable avec Ollama et ComfyUI arrêtés.

**Phase B — connecteur ComfyUI local facultatif** :
- configurer une adresse loopback autorisée (exemple `127.0.0.1:8188`, non imposée) ;
- test explicite du serveur/nœuds/workflows disponibles, sans lancer le serveur ni installer de modèle automatiquement ;
- sélectionner/importer des graphes ComfyUI **exportés au format API**, valider les nœuds et paramètres modifiables ;
- `POST /prompt`, suivi des exécutions par `/ws` et/ou `GET /history/{prompt_id}`, téléchargement `GET /view` ;
- contrôler file d'attente, erreur, annulation et absence du serveur sans bloquer le reste de Fabulaxiom ;
- conserver sortie réellement téléchargée et provenance (workflow/digest, modèles identifiables, seed, prompt, date, tâche, sha256 du média).

**Phase C — continuité visuelle et exploration** :
- références de personnage utilisées comme entrée seulement lorsque le workflow prend en charge la méthode ;
- plusieurs poses/vêtements/expression/âges/états narratifs avec suivi des variations ;
- comparaison d'images et version de référence choisie humainement ;
- pas de garantie non fondée sur la cohérence des visages quand les modèles/nœuds correspondants sont absents.

## Invariants de sécurité, stockage et résilience

- Aucun appel ComfyUI sur action de lecture ou ouverture de Fabulaxiom ; uniquement sur action explicite.
- Pas d'API payante ni d'obligation de connexion Internet.
- Connexion strictement loopback et protection contre redirects/SSRF ; ne jamais accepter une URL arbitraire du réseau.
- Les workflows tiers/nœuds personnalisés restent non fiables ; pas d'exécution implicite de commandes externes.
- Les fichiers binaires, métadonnées et vignettes doivent être sauvegardés et restaurés **ensemble**, de façon vérifiable.
- **La sauvegarde SQLite M1.5 actuelle ne suffit pas à restaurer une bibliothèque d'images externes**. Étendre et qualifier d'abord le contrat de sauvegarde/restauration avant de proposer un stockage image permanent.
- Chemins relatifs internes, vérification hash, noms de fichiers contrôlés ; pas d'écrasement destructif.
- Pas de dépendance automatique à un GPU, un checkpoint, un LoRA, IP-Adapter ou ControlNet particulier.
- Le scénario ComfyUI hors ligne doit avoir des erreurs déterministes ; l'import manuel doit toujours rester utilisable.
- Les images exploratoires et versions de prompts ne modifient jamais les sources narratives originales ni les révisions de scène.

## Critères d'acceptation futurs

- un personnage dispose de plusieurs variantes et d'une image de référence sélectionnée ;
- une scène illustrée est associable à sa révision immuable, même après réécriture ;
- un événement peut avoir une ou plusieurs illustrations indépendamment de toute modification du texte ;
- la galerie, l'import et les fiches restent utilisables avec ComfyUI/Ollama OFF ;
- une génération ComfyUI locale réelle suit un workflow autorisé et restitue les images dans l'UI ;
- un workflow absent ou modèle manquant est expliqué, non contourné ;
- la sauvegarde/restauration vérifie binaires + relations SQLite sans liens brisés ;
- tests CI déterministes sans GPU et qualification Windows ComfyUI sur environnement réel ;
- acceptation humaine de la référence visuelle indépendante de toute action de canon narratif ;
- CI exact-head, preuves opérateur, fusion et normalisation post-merge avant subdivision suivante.

## Sources techniques

- [ComfyUI upstream — exemple WebSocket/API](https://github.com/comfyanonymous/ComfyUI/blob/master/script_examples/websockets_api_example.py)
- [Documentation ComfyUI Server Routes](https://docs.comfy.org/development/comfyui-server/comms_routes)

## Gouvernance

La future roadmap devra choisir explicitement le placement des phases dans V1/M2/M5/M8 ou un milestone visuel dédié. Jusqu'à son approbation, cette extension est enregistrée comme besoin produit **non implémentable**. Cette PR ne peut pas autoriser M2.2, M2.6 ou de code ComfyUI.
