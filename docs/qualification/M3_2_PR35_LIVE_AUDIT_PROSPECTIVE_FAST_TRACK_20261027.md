# M3.2 — Audit vivant de PR #35 et voie prospective courte (27 octobre 2026)

**Observation source-only, non autorisante.** Ce constat photographie le GitHub au
`main=009fa1723b3fc9a574e867a28759adff42e255d0`. Re-fetch avant toute
nouvelle action. Aucun système Windows opérateur, aucune SQLite privée ni aucun
artefact historique n'a été examiné ou modifié pour cet audit.

## Audit comparatif, sans fusion automatique

| Critère | Résultat GitHub daté |
| --- | --- |
| PR | [#35](https://github.com/LaurentCOLL1/Fabulaxiom/pull/35), `OPEN/DRAFT` |
| HEAD de #35 | `41ce7b915e76d22785d53d7fffe288d113dd0bf5` |
| Base ancestrale de #35 | `f7eabfea74480d307b52d4b053730021efc95352` |
| Comparaison `main...#35` | `diverged`, 47 commits ahead, **645 behind** |
| Fusionabilité GitHub | `mergeable=false`, `mergeable_state=dirty` |
| Fichiers du diff #35 | 84 (6 mêmes blobs dans `main`, 10 blobs différents, 68 chemins absents du `main` courant) |
| Revues et threads #35 | Aucune revue et aucun thread enregistré au contrôle ; non substituable à une revue future |

Les **six** blobs exactement repris dans `main` sont les SQL candidats
`m3_2_{active_precedence,chronology_decisions,recursive_chain,restatement_revocations,restatement_successors,successor_revocations}_candidate.sql`.
Ils ne sont **pas** des migrations de production : les exercices sont des
fixtures v7 neuves. Le service `src-tauri/src/m32_manual_chronology.rs` a lui
aussi été porté, puis modifié sur `main` : il reste compilé seulement sous
`#[cfg(test)]`, et non appelé par les commandes Tauri de production. Les vues
`M32ChronologyPreview.tsx` et leurs tests ont été durcis dans `main`, tandis
que `M32ManualChronologyLab.tsx` demeure fictif, non monté dans `App.tsx`.

Les **10 chemins existants mais divergents** sont le workflow CI, `README.md`,
`STATE.md`, `NEXT.md`, `Cargo.toml`, `build.rs`, `lib.rs`, le service Rust,
`M32ChronologyPreview.tsx` et ses tests. Leur version de #35 ne doit jamais
écraser les garde-fous plus récents de `main`. Les **68 absences de chemins**
comprennent des notes, scripts et essais antérieurs, notamment le préflight
M3.2 expérimental et un test de concurrence SQLite. Ni nécessité fonctionnelle,
ni innocuité, ni équivalence d'implémentation ne sont inférées de ces comptages.

**Décision :** ne pas rebaser brutalement, ne pas fusionner ni supprimer #35.
Conserver la PR comme archive révisable et porter seulement d'éventuels
manques démontrés en branches **nouvelles**, courtes, depuis `main` revérifié.

## Sortie productive la plus courte : Greenfield neuf en priorité

**Attention : la prospective historique n'offre aucune garantie de déblocage.**
G2B peut encore refuser l'identité et l'absence d'écrivain, et G3 rester
indisponible. Il ne faut pas conditionner indéfiniment **toute** chronologie
manuelle à cette voie incertaine.

La cible fonctionnelle recommandée est donc une **qualification M3.2
Greenfield limitée aux nouveaux projets**, dans le profil Tauri **existant**
`com.fabulaxiom.greenfield.v1`. Une SQLite v7 **nouvelle, de test, créée
exclusivement dans une racine jetable du runner** peut exercer le modèle
chronologique complet sans migrer aucune base v6 opérateur. L'éventuelle
activation/transition des projets neufs sur Windows demande une conception et
une autorisation séparées : un succès de CI n'autorise pas de toucher à la
SQLite Greenfield active ni d'exécuter la migration 007. Le projet n'a pas
encore accepté de faire de cette qualification bornée une clôture formelle du
jalon historique M3.2 : la décision doit rester explicite et traçable.

1. **Écart fonctionnel** : relier explicitement exigences M3.2 et couverture
   existante des tests Rust et React fictifs (quatre temporalités, deux
   Universes, romans multiples, ordres monde/narration/révélation, révisions
   immuables, corrections/révocations et cycles). Ne pas ajouter un test-jouet
   redondant là où la fonction et son test existent déjà.
2. **Service Greenfield réel, sous barrière distincte** : définir une interface
   transactionnelle persistante M3.2 et ses refus sur **bases v7 nouvelles
   uniquement**, avec rejeu/rollback, garde de l'identité Tauri et revue des
   chemins. Préparer les contrats par CI sur fixtures. La compilation et les
   tests ne constituent pas une autorisation de writer Windows réel.
3. **UX réelle, après preuve** : relier l'interface au service validé sur une
   base *neuve* explicitement admissible, avec affichage séparé des trois ordres,
   conflits compréhensibles, références de scène/révision exactes et contrôle
   de préservation de la source. Aucune promotion d'un brouillon React isolé
   en GUI acceptée.
4. **Réception Greenfield bornée** : CI terminale sur le SHA exact, revue des diffs/threads,
   fusion protégée avec `expected_head_sha`, CI `push` postmain indépendante,
   qualification Windows sur **nouveau stockage projet** selon le périmètre
   autorisé puis PR de normalisation distincte. Ne pas étendre cette réception
   aux historiques. Le jalon global demeure `IN_PROGRESS_NOT_ACCEPTED`
   jusqu'à une décision explicite et des preuves de produit complètes.

## Provenance : ne plus confondre historique et prospective

La [politique prospective SOLO](M3_2_PROSPECTIVE_TRUST_BASELINE_DECISION.md)
et son [runbook non exécutable](M3_2_PROSPECTIVE_BASELINE_WINDOWS_RUNBOOK_DRAFT.md)
existent déjà. Le chemin privilégié **n'exige pas d'inventer cinq attestations
anciennes** : une *nouvelle* chaîne de confiance peut être instruite pour un
usage futur borné. L'[issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36)
conserve les cinq lacunes historiques en `PENDING_EXTERNAL_ATTESTATION(21/3/2)`.
Le statut de la nouvelle référence reste `NOT_STARTED` avant une cérémonie
réelle, consignée dans l'[issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38).
**Cette voie est un travail parallèle optionnel pour l'accès aux sources
historiques, pas une garantie de M3.2** ; la voie Greenfield neuve sépare
l'avancement des fonctionnalités de cette incertitude.

Pour avancer, il faut **dans l'ordre** : G2B identité/propriétaire/source
non migrante et tous écrivains/journaux réellement maîtrisés ; décision G2C
distincte ; G3 capture cohérente sans écrasement ni ouverture migrante ; G4
preuves croisées et restauration isolée ; G5 décision de risque SOLO explicite
(jamais `INDEPENDENTLY_REVIEWED`) ; G6 runtime isolé en lecture seule,
autorisé séparément. Une source froide non prouvée et une connexion propriétaire
non authentifiée restent des STOP, même si toutes les fixtures sont vertes.

Le profil de **nouveaux projets** `com.fabulaxiom.greenfield.v1` doit rester
unique et intact. Son succès propriétaire d'archivage 5/5 et les tests de
sauvegarde/restauration CI ne qualifient pas l'historique v6/v7 ; aucune nouvelle
destination Tauri n'est requise. Aucune migration 007, writer IPC, marqueur,
ACL, backup, SQLite active/historique, `-wal`/`-shm`/journal ni release n'est
autorisé par cette décision. Aucune commande Windows opérateur n'est fournie
ou exécutée ici ; tout éventuel PowerShell futur sera entièrement sous `& { ... }`.

## Vérification à chaque incrément

Maintenir les deux prompts, les deux handoffs, roadmap, continuité et un
commentaire append-only dans #38. Refetch `main`/PR/CI/`Protect main` ; ne
jamais transférer la CI #40455683237 / #40456835489 du SHA de #189 à un
nouveau commit. La source seule ne peut ni accorder l'accès Windows ni signer
une preuve prospective ; si G2B/G3 sont encore indisponibles, la progression
autorisée reste code/fixtures et non exécution opérateur.
