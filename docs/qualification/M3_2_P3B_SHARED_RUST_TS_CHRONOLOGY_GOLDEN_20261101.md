# M3.2 P3b — même scénario fictif vérifié indépendamment par Rust et TypeScript

**1er novembre 2026 — CANDIDAT NON QUALIFIÉ, pas d'autorisation opérateur.** Parent PR #261 P3a fusionnée : \`main=f08061c578bce1f631ea41c554da8f03811f2110\`, [CI source #41349001435](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41349001435) et [postmain indépendante #41350139797](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41350139797) completed/SUCCESS **301 Rust/7 Greenfield/68 inventaire/182 continuité**, **85/85 Chromium normal/CSP stricte**.

## Livrable P3b

Une **fixture JSON Git unique**, \`fixtures/m32_p3b_typed_chronology_contract_v1.json\`, décrit un Univers et roman inventés, une scène et ses révisions immuables \`fiction-r2\` historique / \`fiction-r3\` HEAD, trois ancres \`fiction-draft-0001/0002/0004\`, un lien avant/après humain \`fiction-draft-0003\`, une troisième ancre incomparable, quatre contre-exemples, les résultats attendus et trois flags runtime \`false\`. **Ce JSON n'est pas un protocole IPC, un service ni une autorisation.**

- \`src/m32P3bCrossLanguageGolden.test.ts\` : 4 tests Vitest qui lisent le JSON source et exercent le réducteur TS P3a réel, avec IDs déterministes, relation, état immuable si échec, cycle, Univers étranger, mauvaise révision/scène. Aucun appel Rust ni accès au disque depuis l'interface : l'import du fichier est une fixture statique de build/test.
- \`src-tauri/src/m32_p2b_fixture_chronology_actor.rs\` : un test Rust \`#[cfg(test)]\` lit par \`include_str!\` **le même JSON source**, reprend l'acteur P2b réellement exécuté avec une base SQLite **RAM fictive préouverte**, exécute indépendamment les commandes, vérifie IDs/relations/provenance/ordre partiel et les rejets transactionnels. Ne modifie aucun runtime Rust, aucune fonction de production, aucune ouverture de connexion/path, aucune migration runtime.
- On n'exécute pas un aller-retour Rust↔React et on ne prétend ni tester une sérialisation réseau authentifiée, ni prouver la custody atomique main/WAL/SHM. On vérifie seulement un **contrat de comportements commun** sur la même fixture versionnée.

## Qualifications et suites

Avant CI, **302 tests Rust / 7 Greenfield / 68 inventaire SQLite / 183 continuité ATTENDUS NON ACQUIS**, **4 Vitest nouveaux** et **85 scénarios Chromium** attendus. Il faut Windows CI au HEAD SHA exact, logs, diff/reviews/threads, ruleset \`Protect main\` ACTIVE strict bypass=[], squash \`expected_head_sha\` puis postmain indépendante ; en cas d'échec refuser le merge et corriger le code/test. P3c ensuite : améliorer l'expérience ergonomique uniquement dans l'atelier de laboratoire, tandis que R4–R9 traitent la preuve réelle du writer en parallèle. Ne jamais présenter P3b comme l'intégration finale.

Priorité utilisateur **\`PRODUCT_FIRST_PARALLEL_SAFETY\`** ACTIVE et réversible. **Informer et consulter AVANT tout changement de stratégie** si une frontière ne peut plus être tenue. GLIB 0.18.5 \`GHSA-wrw7-89jp-8q8g\` Linux GTK3 demeure \`OPEN_NOT_REMEDIATED\` (issue #160), pas de correctif compatible inventé ni de dismiss. Issues #38/#160 : ajout de commentaire seulement.

**STOP : M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED.** Aucune base/opérateur v6-v7, profil \`%LOCALAPPDATA%\\com.fabulaxiom.greenfield.v1\`, contenu de \`M:\\Fabulaxiom\`, IPC writer, migration 007 runtime, sauvegardes/journaux, Windows Hello natif, marqueur ou recovery.
