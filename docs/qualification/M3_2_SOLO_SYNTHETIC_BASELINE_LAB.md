# M3.2 — Laboratoire de sauvegarde prospectif exclusivement synthétique

**Statut : TECHNICAL_FIXTURES_ONLY / OPERATOR_EXECUTION_NOT_AUTHORIZED.** Cette PR prépare le **G3–G4 synthétique**, sans toucher au monde réel. Le script `tools/m3_2_solo_synthetic_lab.py` n'accepte volontairement **aucun argument `--source` ou `--destination`** ; il ne crée que ses propres bases fictives dans un `TemporaryDirectory`. La CI lance `tools/test_m3_2_solo_synthetic_lab.py`. Aucun chemin opérateur, nom de base réelle, source privée, marqueur d'activation ou ACL d'origine n'est fourni.

## Ce que les fixtures qualifient réellement

- Deux bases **fictives** schéma v6 et v7, identifiants fictifs, deux révisions append-only et un fait (v7 ajoute une ancre temporelle).
- SQLite Online Backup API vers un nom **nouveau** ; restauration distincte dans une sortie neuve ; digests SHA-256 et logique déterministe **sur fixture seulement** ; `integrity_check`, `foreign_key_check`, `user_version`, tables/comptages, lignage.
- Deux modes de comptages techniques différents, **reposant malgré tout sur la même bibliothèque SQLite** ; cela n'atteste pas une indépendance humaine ni une indépendance complète du moteur.
- Tests adversariaux : collision sans écrasement, fausse empreinte, digest différent, version fausse, suppression/changement de révision, FK orpheline, SQLite invalide, table inattendue, compteur de manifest faux, nom de sortie non autorisé.

## Limites majeures — un PASS de CI ne déverrouille PAS G2/G3 sur Windows

La réservation `O_CREAT|O_EXCL` protège contre une collision **au moment de la création du fichier test**. Comme un nouveau handle SQLite est ouvert ultérieurement et que le laboratoire n'emploie pas de protocole Windows complet anti-reparse, de confinement ACL ni une identité persistante de fichier, cette implémentation **NE PROUVE PAS** l'absence de TOCTOU ni de substitution d'un fichier réel. **Ne jamais l'utiliser sur les bases opérateur.**

Une ouverture SQLite `mode=ro` peut créer/modifier WAL/SHM sur certaines configurations et n'est ici autorisée que sur les copies jetables. Le schéma et le digest logique de ces fixtures simplifiées ne sont **pas** ceux des bases réelles M1.5 ou M3.1. Le laboratoire ne gère pas plusieurs bases de manière atomique, ni les historiques d'ACL, ni une clé indépendante, ni le processus Tauri, ni le pointeur M1.5.

**Avant tout travail opérateur réel :** réconciliation de la politique via PR #37 ; méthode safe-open validée sur l'état WAL exact, répertoire neuf privé avec mécanisme anti-écrasement audité au niveau Win32, définition des digests de toutes les tables réelles, inventaire Windows G2 et plan de G3/G4 séparément approuvés. La prospective reste `NOT_STARTED`, historique `PENDING_EXTERNAL_ATTESTATION 21/3/2`, M3.2 réel `NOT_AUTHORIZED`. Aucun `007`, writer IPC, merge #35, M3.3 ni commande sur données Windows depuis ce code.

Sources : https://www.sqlite.org/backup.html , https://www.sqlite.org/wal.html .
