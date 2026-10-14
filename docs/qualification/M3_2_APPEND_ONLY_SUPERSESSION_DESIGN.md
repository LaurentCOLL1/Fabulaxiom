# M3.2 — Stage 20 : rectification append-only des ancres temporelles

**DESIGN + TESTS SYNTHÉTIQUES SEULEMENT. Aucune migration, aucun IPC ou éditeur, aucune autorisation d'écriture.**

## Checkpoint et bases réelles

- PR #35, prédécesseur `e7e20e08f761b9f9d572b3580714ac9cdfe401c2`, exact-head Windows CI #38570448347 **31/31 SUCCESS** ; main `f7eabfea74480d307b52d4b053730021efc95352` inchangée.
- Le contrat `docs/qualification/M3_2_MANUAL_CHRONOLOGY_UX_CONTRACT.md` distingue chronologie du monde, ordre du récit et ordre de révélation.
- Le schéma M3.1 v7 candidat `src-tauri/sql/m3_1_world_time_v7_candidate.sql` bloque UPDATE et DELETE sur les calendriers, ancres et précédences et refuse les cycles du **graphe historique entier**.
- Le contrôle réel Stage 18.1 de la copie v7 isolée a réussi (conservation 26/26 ; empreintes historiques 21/21, observations récentes 3/3 ; 2 éléments non ancrés ; intégrité et clés étrangères, schéma et empreinte logique v6). Le statut global reste **PENDING_EXTERNAL_ATTESTATION** : aucune attestation historique indépendante nouvelle.
- La production restaurée M1.5 demeure SQLite v6, et les sept worktrees opérateur restent intacts.

## Pourquoi une correction doit préserver l'ancienne assertion

Une assertion erronée demeure une trace historique authentique de ce qui avait été saisi. Pour la rectifier, on propose une **nouvelle ancre dotée d'un nouvel ID**, puis un événement de supersession reliant l'ancienne ancre à la nouvelle avec raison humaine non vide. L'ancienne ancre, son ID, sa révision immuable, ses textes de calendrier et sa date de création restent conservés. Une rétractation est un événement sans nouvel ID, jamais un DELETE.

Les vues « actuelle », « remplacée » ou « retirée » sont des **projections de l'historique append-only**, pas une mutation des tables v7. Les trois ordres (monde/récit/révélation) restent distincts ; le retrait d'une assertion ne réordonne jamais les scènes, et aucun temps fictif n'est converti en date grégorienne.

## Schéma futur proposé — non créé

Une future table de supersession des **ancres uniquement**, à gouverner dans un jalon de schéma séparé, devrait au minimum inclure :

| Champ conceptuel | Contrat |
|---|---|
| `id` | ID immuable unique de la rectification |
| `universe_id` | Identique à l'Univers des deux ancres |
| `old_anchor_id` | ID historique qui demeure physiquement présent |
| `new_anchor_id` | Nouvel ID d'ancre, ou NULL pour rétractation |
| `reason` | Justification humaine non vide |
| `source_revision_id` | Révision historique facultative ; contrôle d'Univers obligatoire via les jointures scène/chapitre/roman |
| `created_at_utc` | Temps de l'assertion humaine, **pas** calendrier fictif |

À prévoir : FKs composites ancre/Univers, unicité de `old_anchor_id` pour interdire les successeurs concurrents, ID nouveau réellement frais, lignée sans cycle, contraintes d'immuabilité sur les événements, transaction Rust et revalidation de l'ancienne tête active. **Pas de INSERT OR REPLACE**, pas de suppression ou d'UPDATE des tables v7. Aucune colonne/table/migration n'est effectivement ajoutée par Stage 20.

## Blocage réel sur les précédences

Le déclencheur v7 `world_time_precedences_guard` évalue le **graphe historique complet**. Ainsi, même après une « rétractation » logique de A→B, une future insertion B→A dans cette table serait rejetée comme cycle. Désactiver le déclencheur serait un contournement inacceptable.

Remplacer une ancre A qui figure dans une relation historique soulève aussi la question de re-lier ou non la relation à A'. **Décision conservatrice Stage 20 : toute ancre ayant une quelconque précédence historique entrante ou sortante est non rectifiable et non rétractable.** Corrections de précédences et de calendriers restent **hors périmètre** jusqu'à un nouveau schéma de projection de graphe actif, ses contraintes et des tests SQLite entièrement jetables approuvés.

## Référence exécutable synthétique

- `tools/m3_2_supersession_reference.py` : modèle Python pur, **sans import SQLite, Tauri, accès au disque ou au réseau**. Un `SyntheticSnapshot` contient des tuples immuables ; `propose_replacement` et `propose_withdrawal` retournent un nouvel objet et ne touchent jamais l'ancien. Ce code est un simulateur de contrat, pas un moteur applicatif.
- `tools/test_m3_2_supersession_reference.py` : **25 tests synthétiques** : remplacements/rétractations historiques, correction en chaîne, refus de fourches, doublons et ID réutilisés, mauvaises appartenances d'Univers, formes exact/approximative/inconnue, fenêtres approximatives partielles, historique des révisions, ordre partiel, cycle, précédence croisée, correction d'ancre reliée interdite et conservation de l'état d'origine après un veto.
- Limite explicite : les objets synthétiques ne valident pas l'existence des vrais calendriers, événements, révisions et l'ensemble des FKs et des triggers Rust/SQLite. La validation réelle imposera une transaction, la vérification indépendante des sources et une cérémonie opérateur séparée.

## Contrat UI futur — rien de livré ici

1. Afficher ID historique, ID successeur, raison et éventuelle source immuable, avec états « retenue / remplacée / retirée » distincts.
2. Ne jamais présenter un bouton « modifier » pour une ligne v7 existante ; le futur parcours proposera éventuellement une nouvelle assertion, sous autorisation.
3. Désactiver tout contrôle d'écriture M3.2 tant que `PENDING_EXTERNAL_ATTESTATION` persiste. Aucune animation de succès avant commit validé.
4. Aucune correction de précédent ou de calendrier avant revue indépendante. Les ancres sans comparabilité explicite demeurent indéterminées.
5. La séparation chronologie du monde / ordre narratif / révélation est stricte. Pas d'IA ni de conversion `Date.parse` fictive.

La CI du nouveau commit doit être terminale `completed/success` sur son SHA exact, avec les 25 cas synthétiques. Elle ne certifie **ni** la future migration **ni** la correction de preuves historiques. Aucune modification de la production v6, de la copie M3.1 v7 isolée, des sauvegardes ACL et des sept worktrees ; aucune fusion PR #35 ou M3.3.

Références : https://www.sqlite.org/lang_createtrigger.html ; https://www.sqlite.org/lang_with.html ; https://www.sqlite.org/lang_savepoint.html ; https://www.sqlite.org/foreignkeys.html .
