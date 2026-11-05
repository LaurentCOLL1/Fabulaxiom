# M3.2 — P2h : résumé typé de l'impact d'un aperçu chronologique fictif (CANDIDAT NON QUALIFIÉ)

**5 novembre 2026.** Dépendance produit P2g #285 fusionnée sur `main=906ad4103a639eaee94f6cb51e55d96cb87f46e0`, source Windows #41958673635 SUCCESS (317 Rust), postmain indépendante #41967078610 terminal/SUCCESS au SHA exact. Parent documentaire #286 DRAFT à qualifier au SHA `098ebc41b9cd58596876c1159910004e8c2df360`, Windows #42043038180 en cours au checkpoint. **P2h est test-only, 320 Rust attendus (317+3), aucun résultat P2h acquis.**

## Intention produit et frontière
L'auteur doit distinguer rapidement les précédences retirées, ajoutées et maintenues par une correction proposée, sans la confondre avec un engagement durable. P2g présente `active_before` et `active_after` dans la même transaction `IMMEDIATE` terminée par `ROLLBACK`. P2h ajoute le résumé *dérivé* `PreviewImpact {removed,added,unchanged}`, contenant des arêtes typées `PreviewEdgeSummary {id,before_anchor_id,after_anchor_id,origin}`. L'égalité compare toutes les propriétés de l'arête ; une réutilisation d'ID avec extrémités modifiées compte comme retrait + ajout. Aucun ordre total, date automatique ni conversion calendaire inféré. Les vecteurs conservent l'ordre stable des projections P2g.

Implémentation strictement limitée au service fictif `#[cfg(test)]` `src-tauri/src/m32_p2_fixture_chronology_service.rs` (méthode pure `CorrectionPreview::author_impact` sur les copies déjà renvoyées) et aux tests de l'acteur fictif `src-tauri/src/m32_p2b_fixture_chronology_actor.rs`. Aucun SQL, transaction, schéma, runtime writer, Tauri State/IPC, VFS propriétaire, migration 007, vraie base/profil opérateur, sauvegarde/journal, Hello natif, marqueur ou recovery.

## Trois nouvelles preuves Rust proposées, NON ACQUISES
1. Une correction fictive A→B devenue B→A produit exactement une arête retirée, une ajoutée et une autre conservée ; ROLLBACK préserve le graphe initial, aucune décision/reformulation persistée, `PRAGMA integrity_check=ok`.
2. Même ID fictif mais extrémités/origine différentes n'est pas classé comme inchangé.
3. Deux clients de l'acteur RAM : un aperçu rend son résumé, le second ajoute des précédences qui rendent la confirmation obsolète cyclique ; la confirmation échoue sans effacer l'histoire.

**320 Rust attendus, NON QUALIFIÉS** ; 7 Greenfield, 68 inventaire, 183 continuité, six Vitest, Chromium 85/85 normal+CSP stricte, 19 blobs Git fictifs à requalifier sur la CI Windows SHA exact après rebase et parent #286 fusionné. Aucun succès P2g n'est transférable au HEAD P2h.

## STOP de production
**PRODUCT_FIRST_PARALLEL_SAFETY** inchangée, avertir AVANT changement. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, P4 réel/writer/R1–R9 `NOT_PROVEN`, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, vraie custody atomique main/WAL/SHM et écrivain adversarial `NOT_PROVEN`. glib Linux GTK3 0.18.5 issue #160 `OPEN_NOT_REMEDIATED`.

Ne pas fusionner tant que #286 postmain, rebase P2h, CI exacte, diff/reviews/threads, Protect main ACTIVE strict bypass=[], `expected_head_sha`, postmain et #38 append-only ne sont pas qualifiés. **CI fixtures ≠ admission réelle.**
