# PR #215 — revue assertionnelle des anciens handoff #146/#147 (21/11/2026)

PR historique [#215](https://github.com/LaurentCOLL1/Fabulaxiom/pull/215) DRAFT HEAD `8203b7323877edc87ffabaad1694c52d2523023d`, ancien `tools/test_m32_handoff_contract.py`. Lecture source seule, aucun portage ou exécution. Les tests actuels portant les numéros #146 et #147 concernent D3c/R7 : la numérotation ne prouve ni continuité ni équivalence.

| Ancien cas | Portée des assertions d'origine | Disposition |
| --- | --- | --- |
| 146 | `next_production_writer_custody_design_study_20261028`, `candidate_ci_qualified=false`, `production_writer_authorized=false`, `external_writer_absence=NOT_PROVEN`, compteur historique de 146 contrats, garde writer `#[cfg(test)]` | REVIEW_OLD_ASSERTIONS_NOT_PORTED |
| 147 | `owner_p1_same_sid_ollama_design_decision_20261028`, P1/same-SID/Ollama mémoire seule documentaire, refus direct SQL/auto-canon, `writer=NOT_PROVEN`, `a0_existing_profile_cross_process=STOP` | REVIEW_OLD_ASSERTIONS_NOT_PORTED |

**Aucune équivalence** sémantique attestée ni nouvelle clôture. Les anciens SHAs/compteurs ne doivent jamais être recyclés comme preuves actuelles. Cinq tests #148–152 restant à confronter assertion par assertion ; quatre chemins de PR #215 restent REVIEW ; PR #35 a encore 68 absents. **M32-007 et M32-050 OPEN_NOT_ACCEPTED** ; #35/#215 DRAFT ; nouveau contrat source-only #19 CANDIDAT.

M3.2 IN_PROGRESS_NOT_ACCEPTED ; PRODUCT_FIRST_PARALLEL_SAFETY ; Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; R2 STOP ; R3 partiel ; D3c conception ; D3b-4/5, D3b-5 STOP ; live SQLite WAL-index/ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
