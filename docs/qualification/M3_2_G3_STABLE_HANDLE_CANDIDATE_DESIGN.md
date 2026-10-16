# M3.2 G3 — Candidat de capture par handle Win32 unique (NON AUTORISÉ SUR LES ORIGINAUX)

**Statut : CONCEPTION À TESTER / SYNTHÉTIQUE SEULEMENT.** Les PR #42 (CI #38914716036, 25/25) et #43 (CI #38917979449, 26/26) sont fusionnées dans `main=b2d8249002cbea8b11edcaedaa9602bd946a62c7`. Leur succès ne couvre que des données fictives. L'opérateur a réalisé le préflight G3 **sans création de destination**, et n'a pas ouvert SQL sur les originales.

## 1. Risque restant avec l'architecture actuelle

Une ouverture SQLite `mode=ro` par le chemin du fichier, même pendant un handle source `CreateFileW` avec `FILE_SHARE_READ`, peut rouvrir un chemin dont un ancêtre a changé. Le test de PR #43 ne prouve pas que le handle de la connexion SQLite interne représente le *même fichier* que le handle Win32 inspecté. La présence éventuelle d'un journal de reprise, même en mode ROLLBACK, peut déclencher une récupération écrivant des fichiers : ce traitement **n'est pas autorisé sur l'original**.

## 2. Nouvelle approche possible, à rejeter si incompatible

1. Sur un répertoire **temporaire de test**, générer les bases fictives v6 et v7, avec `schema_migrations`, sans copie des vraies données, puis fermer intégralement leurs connexions.
2. Vérifier les parents, droits, type, `reparse points` et absence de sidecar ; **les contrôles de chemin seuls restent vulnérables aux courses**. Rejeter une source non locale, identité variable ou tout processus écrivain non exclu.
3. Obtenir le handle par `CreateFileW` avec accès strictement lecture, `OPEN_EXISTING`, `FILE_FLAG_OPEN_REPARSE_POINT`, `FILE_SHARE_READ` sans `SHARE_WRITE/DELETE`. Conserver le handle **pour toute la lecture et la validation source** ; ne pas l'abandonner pour une réouverture par chemin.
4. Obtenir via `GetFileInformationByHandle` l'identité de volume et d'index de fichier (référence locale), la taille, les attributs et la stabilité avant/après. Rejeter les identités non disponibles, dupliquées, incohérentes ou les reparse points. Compléter avec le confinement contre substitution des **ancêtres**, non fourni par ces seules mesures.
5. Lire les octets via **ce même handle**, avec limite mémoire stricte, en-tête ROLLBACK conforme et sidecars absents avant/après. Un hot journal, un WAL, une source ambiguë ou une course détectée = `STOP` ; jamais de checkpoint ou récupération automatique sur original.
6. Charger une **copie en mémoire** via `sqlite3.Connection.deserialize(bytes)` (Python 3.12 si disponible). Effectuer `PRAGMA integrity_check=ok`, `foreign_key_check` sans ligne, migrations réelles sur copies autorisées seulement, tables/comptages et digests canoniques, puis sérialiser la connexion mémorielle. **Ne pas ouvrir SQLite sur le chemin de la source originale.**
7. Écrire seulement un fichier **nouveau** dans un dossier privé nouveau, en gardant l'unique handle de création exclusive pendant l'écriture/fsync (conception de PR #42), puis relire les octets de sortie et tester une restauration isolée dans un **troisième emplacement neuf**. Le répertoire, son ACL et l'identité de fichier nécessitent encore qualification Win32 spécifique.
8. Capturer la preuve prospective datée dans un registre privé : méthode/code exact, version, source et sortie, hash, identité de fichier, métadonnées avant/après, refus et limites. Jamais attribuer l'opérateur à un témoin indépendant.

## 3. Scénarios adversariaux obligatoires

Sur **fixtures synthétiques exclusivement** : écrivain existant/nouveau bloqué, WAL header sans sidecar, hot-journal sentinel, symlink/junction source/ancêtre, chemin remplacé, collision de dossier et fichier sortie, lecture partielle, dépassement du budget mémoire, en-tête altéré, migration de fixture inattendue, FK orpheline, corruption de page, écriture de secours interdite, restauration dans une destination occupée, décalage identité/empreinte avant-après. Évaluer les **limitations de Windows CreateFile** et des filtres de système de fichiers ; ne pas confondre stabilité d'un handle et contrôle complet de l'espace de noms.

## 4. Statuts et limites

Une future CI de fixture pourra vérifier **uniquement** une implémentation de prototype. Même le succès ne suffira pas pour lancer une opération réelle : G3 exige une autorisation séparée portant sur des chemins privés exacts, le nouveau répertoire, un avis préalable sur élévation/interactions/processus, les sidecars, les contraintes ACL, et un contrôle pré/post. Deux bases v6 et v7 séparées ne constituent pas un instantané multi-base atomique.

**Interdit jusqu'à nouvelle autorité :** accès SQLite sur originaux par `open_database`, migration production `007`, changement du marqueur M1.5, nettoyage WAL/SHM, restauration de production, writer IPC, fusion PR #35 et M3.3.

Références officielles :
- https://www.sqlite.org/lockingv3.html — hot rollback journal et récupération
- https://www.sqlite.org/fileformat.html — en-tête et sidecars
- https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandle — identité de volume et fichier
- https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew — partage et ouverture
- https://docs.python.org/3.12/library/sqlite3.html — `deserialize`/`serialize` et `backup`

**Vérité : G3 réellement exécuté = NON ; référence prospective = NOT_STARTED ; historicité 21/3/2 non attestée.**
