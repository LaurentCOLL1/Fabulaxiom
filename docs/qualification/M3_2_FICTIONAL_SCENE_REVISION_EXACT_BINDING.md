# M3.2 — référence manuelle à une révision immuable de scène (laboratoire inventé)

**20 octobre 2026. Développement produit source-only, laboratoire navigateur isolé, sans lecture d'un document, fichier SQLite ou IPC opérateur.** Source vérifiée avant cette tranche : `main=7477001cd0ebc69d4701f21eddbda898f94c79c5`, PR #98 fusionnée, CI PR #39447951647 **SUCCESS 74/74** au HEAD exact et CI post-fusion #39449601527 **SUCCESS**.

## Fonction utilisateur fictive

Dans « Atelier manuel fictif » : l'utilisateur peut choisir une **scène inventée** par identifiant stable, puis sa **révision exacte** dans une liste de révisions immuables déclarées littéralement. Il peut créer une ancre temporelle en la rattachant à ce couple précis, ou corriger l'ancre précédente par supersession. Le nom affiché de la scène est informatif, jamais utilisé comme clé. Ni le `scene_revision_head` courant ni le contenu textuel ne sont lus. Si l'utilisateur ne modifie pas ce choix pendant une correction, la nouvelle assertion **hérite de la même révision historique**, tandis que l'ancienne conserve son ID/source.

Ce lien complète le modèle de M3.2 existant `M32ChronologyProjection` dont une ancre mémorise `source_revision_id`. Le nouveau catalogue de test dans `src/m32FictionalManualChronology.ts` contient des associations `universe_id / novel_id / scene_id / revision_id / revision_label` de **fixtures explicitement fournies par l'appelant**. Le réducteur vérifie :

- un seul Univers fictif dont l'identifiant commence par `fiction-`, et un catalogue borné à 128 entrées ;
- les identifiants de scène/roman existent dans les métadonnées de narration du même Univers ;
- aucun doublon d'identifiant de révision, aucune révision appartenant à un autre Univers/roman/scène ;
- toutes les ancres déjà liées à une révision ne citent que des IDs présents dans ce catalogue ;
- une nouvelle paire `source_scene_id` + `source_revision_id` correspond **exactement** à une entrée ; aucune sélection par nom de scène, date actuelle ou `latest head`.

Les objets d'entrées sont clonés au démarrage du brouillon ; ni la scène d'origine ni ses révisions ne sont mutées lors d'une action. Les quatre types temporels, les précédences, la révocation explicite et le refus des cycles de PR #98 restent inchangés.

Le catalogue de la **page navigateur** `src/m32BrowserLab.tsx` est littéralement constitué de deux révisions fictives de `s1` dans `fiction-world-one`, dont une ancienne `invented-rev-A` et une seconde `invented-rev-B`. Le deuxième Univers fictif n'expose **aucune** révision du premier. Changement de scénario = nouvelle session sans sauvegarde. **Aucune persistance, import de source réelle, lecture SQLite ou accès Tauri**.

## Preuves à qualifier sur la nouvelle CI SHA exact

- 9 nouveaux tests Vitest dans `src/m32ManualChronologyLab.test.tsx` : ancien ID choisi au lieu du head, refus de mélange scène/révision, mauvais Univers/roman, révision inconnue/dupliquée, conservation historique par supersession, isolation des objets de catalogue et rendu explicite du contrôle UI ; 13 tests précédents préservés, soit **22 tests dans ce fichier**.
- 2 tests d'interaction réelle Chromium ajoutés au pilote `tools/m32_browser_interaction.cjs` : choix explicite d'une révision historique puis création d'ancre, et deuxième Univers sans aucune révision étrangère. Total annoncé : **34 scénarios de navigateur**.
- Les manifestes de staging et d'objets Git conservent les **mêmes neuf modules autorisés**, pas de nouveau paquet, de fichier exécutable ou de voie vers `App.tsx`. La CI conserve ses contrôles de refus de changement Git, CSP réseau, origines hostiles et tests Rust généraux.

**Limites produit :** les révisions du catalogue sont inventées et déclarées dans le code de fixture. Elles ne sont pas des données M1 ou M2 attestées. Aucun contenu de scène ni révision réelle n'a été consulté, aucune copie de base n'a été créée ; les comportements de lecture/persistance via Tauri/SQLite ne sont ni implémentés ni validés par ces tests. Aucun apport à M3.3/ComfyUI.

## Position roadmap et arrêt opérateur

M3.1 `COMPLETE_MERGED_NORMALIZED` (PR #33 et #34), M3.2 `IN_PROGRESS_NOT_ACCEPTED` (PR #35 toujours DRAFT), M3.3–M3.6, M4–M9 et ComfyUI `NOT_STARTED_NOT_AUTHORIZED` ou `PROPOSAL_ONLY`. G2A `PASS_METADATA_ONLY_OWNER_REPORTED` (exécution unique et accord consommé), `PROCESS_WRITER_ABSENCE=NOT_PROVEN`, G2B/C/D, G3–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`. Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucun accès aux originaux v6/v7, WAL/SHM, backups, ACL, marqueurs, migration 007 ou writer IPC ; aucun script opérateur Windows. La PR #35 et la release restent interdites à fusion/publication.

**Fondements de conception publics :** [Référence React : arrays en état immuable](https://react.dev/learn/updating-arrays-in-state), [SQLite : clés étrangères et relations d'existence](https://www.sqlite.org/foreignkeys.html). Aucune de ces références ne remplace les preuves ou gates locales.
