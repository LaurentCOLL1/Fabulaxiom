# M3.2 / voie C — Profil Fabulaxiom « projets neufs » (SOURCE-ONLY)

**26 octobre 2026 — CANDIDAT DE DÉVELOPPEMENT, NON EXÉCUTÉ.**
Le choix utilisateur est de privilégier une version réellement utilisable sur des histoires **créées après** cette décision. Aucun original M1.5 v6, isolé M3.1 v7, ACL, sauvegarde, journal ou marqueur n'entre dans ce périmètre. Ce profil n'est **pas** la baseline G2–G5 de conservation de fichiers historiques et ne constitue aucune attestation historique.

## Livraison source-only du premier incrément

- Nouvelle surcharge Tauri `src-tauri/tauri.greenfield.conf.json`, chargée **uniquement par choix explicite** : identifiant `com.fabulaxiom.greenfield.v1` distinct du profil habituel `com.fabulaxiom.desktop`, titre visuellement marqué « PROJETS NEUFS », packaging désactivé.
- Réutilisation ciblée du produit déjà présent : univers, séries, romans, chapitres, scènes, révisions de texte, entités, faits sourcés, revue humaine et sauvegarde. **Aucun changement** de l'ouvre-base, de l'IPC writer, de la migration 007, de la configuration principale, des originaux ou du mécanisme d'activation.
- `database::database_path` résout `app.path().app_local_data_dir()` puis `backup::resolve_active_database_path`, lequel reste sous `database/` de cette racine. Tauri documente que le répertoire local applicatif découle de l'**identifiant** ; la surcharge de configuration est appliquée au profil nommé. Le contrat de CI teste la séparation **en source** et plusieurs mutations adversariales en mémoire.
- Aucun profil réel n'est créé, ouvert ou vérifié par cette PR. Un nom d'application différent ne prouve pas à lui seul qu'une destination locale est absente, vide, non redirigée ni exempte de collision : junction/réparse, ACL, instance/processus et racine réelle restent à établir séparément.

## Chemin vers un essai réellement utilisable (nouveaux contenus seulement)

1. **CI au SHA exact** : typecheck, suites préexistantes, garde Python `tools/test_m32_greenfield_profile_contract.py`, Rust et navigateur du runner jetable. CI = validation de source, **pas** acceptation Windows opérateur.
2. **Cérémonie Windows future**, distinctement autorisée : avant toute exécution, documenter le bloc exact, le compte non-administrateur, le répertoire résolu pour `com.fabulaxiom.greenfield.v1`, son inexistence préalablement vérifiée, les parentés/junctions/ACL, disque/espace, WebView2/Ollama et les effets prévisibles. Si un chemin, lien, instance ou ancienne donnée est inconnu : STOP. Ne jamais réutiliser `com.fabulaxiom.desktop`.
3. Sur un emplacement **neuf confirmé** et avec consentement spécifique, lancer uniquement le profil greenfield depuis un checkout propre ; l'ouverture initiale peut **créer des dossiers, une SQLite v6, son journal et appliquer les migrations normales 001–006**. Aucun geste sur la racine historique. Ne pas lancer la commande ici.
4. Essais utilisateur M1/M2 : créer de zéro un univers, roman, chapitre, scène et deux révisions ; redémarrer et vérifier la persistance ; ajouter une entité, un fait et sa revue humaine ; créer une **sauvegarde nouvelle** et exercer une **restauration seulement sur une autre destination neuve**, après revue du parcours existant.
5. Tester sortie/redémarrage, erreurs disque, sauvegarde, restauration, intégrité et perte simulée sur une copie **créée pour le test**, sans original. Décision de qualification produit distincte avant diffusion, activation d'écriture M3.2, M3.3 ou release.


## Deuxième incrément candidat : parcours M1/M2 sur fichiers neufs du runner (pas Windows opérateur)

`src-tauri/src/greenfield_smoke_tests.rs` est uniquement inclus sous `#[cfg(test)]`. Un test d'intégration des services Rust sur un runner Windows jetable doit créer **deux nouvelles racines temporaires exclusives** sous le répertoire temporaire du runner : une pour l'écriture d'histoires neuves et une autre pour la restauration de la sauvegarde construite par le test. Il couvre univers/série/roman/chapitre/scène, deux révisions, entité, fait sourcé à une révision exacte, promotion canon explicite par acteur **fictif**, fermeture/réouverture, conservation intégrale des compteurs et des octets source/backup. Le test n'utilise ni profil Tauri opérateur, ni données historiques, et ne prouve pas le comportement de la WebView native ni l'absence de junctions, writer ou collisions sur la machine opérateur. **Première CI #40277632492** : STOP sur l'inventaire textuel Rust global, car un nouveau module contenant trois appels `database::open_database` n'était pas encore qualifié ; aucun test Rust métier n'avait commencé. Correction source-only à nouveau SHA : inventaire exact `(0,3,0,0,0,0,0)`, contrôle `#[cfg(test)]`, refus d'un quatrième ouvre-base et des IPC ; **nouvelle CI pending**, sans promotion G2B/G3 ni opérateur.

## Troisième incrément : préflight opérateur à la lecture uniquement (PR candidate)

La [procédure de premier lancement](M3_2_ROUTE_C_WINDOWS_FIRST_LAUNCH_RUNBOOK_20261026.md) détaille les **deux phases disjointes** : préflight PowerShell de métadonnées refusant toute entrée existante ou tout ascendant réparse, puis première compilation/GUI après revue sur poste non administrateur. Tests statiques et scénario runner temporaire ne valent **pas** qualification Windows opérateur, sécurité atomique ni autorisation historique. Aucun lancement réel dans cette PR.

## Discipline d'autorisation

Un futur exemple d'invocation du profil, **à ne pas exécuter maintenant**, est `npx tauri dev --config src-tauri/tauri.greenfield.conf.json` depuis la racine du dépôt après installation des dépendances. Ce processus peut lancer une compilation, un serveur de développement et un processus Tauri ; il peut créer un nouveau stockage sur disque. Il n'exécute pas automatiquement le consentement présent. Avant toute commande Windows opérateur, afficher le **bloc exact et tous ses effets** (Entrée/`q`, UAC, accès disque/réseau, processus et arrêt), puis obtenir l'accord spécifique.

**Autorité inchangée :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, absence d'écrivain original `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, baseline prospective historique `NOT_STARTED`, #35 OPEN/DRAFT. Le profil C est uniquement `DEVELOPMENT_ONLY_SOURCE_CANDIDATE` jusqu'aux validations séparées.

Références : [Tauri appLocalDataDir](https://v2.tauri.app/reference/javascript/api/namespacepath/#applocaldatadir), [Tauri CLI configuration](https://v2.tauri.app/reference/cli/), [SQLite pragma/intégrité](https://www.sqlite.org/pragma.html).
