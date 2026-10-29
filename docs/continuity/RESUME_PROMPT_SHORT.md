# Fabulaxiom — reprise courte (29 octobre 2026)

**Reprise obligatoire :** consulter d'abord [RESUME_PROMPT.md](RESUME_PROMPT.md), puis HANDOFF_CURRENT.md, HANDOFF_CURRENT.json, HANDOFF_PROTOCOL.md, HANDOFF_HISTORY.md, STATE.md, NEXT.md, M3_2_GATE_DECISION_CURRENT.md et les deux roadmaps. Re-fetch main, PR, issues, CI, ruleset Protect main. Les états GitHub actuels priment sur les SHA historiques.

**Point GitHub vérifié :** main `90142d8c78dd8a84ee3f0ee1676a753c8521d78e` ; PR [#215](https://github.com/LaurentCOLL1/Fabulaxiom/pull/215) OPEN/DRAFT, HEAD `8203b7323877edc87ffabaad1694c52d2523023d` ; Windows CI [#40793962533](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40793962533) completed/SUCCESS au HEAD exact. D3a ancien HEAD `a7323ab80f12372aa83b2be48019806be212eb32` CI #40764117809 SUCCESS 220 Rust/7 Greenfield/41 gardes/151 contrats. **Inspecter les logs D3b exacts avant de déclarer 224/7/41/152 qualifiés.**

**D3b autorisé uniquement sur fixtures Windows CI jetables :** 4 tests de crash/restart, WAL commit/pending, mutex WAIT_ABANDONED ou disparu, SQLITE_BUSY ; après crash, REFUS `RECOVERY_REQUIRED_NOT_AUTHORIZED`, aucune réouverture ni récupération SQLite. Conception et code expérimental dans la PR #215 et [D3b](../qualification/M3_2_V7_P1_D3B_DISPOSABLE_WINDOWS_CRASH_RESTART_REFUSAL_FIXTURE_20261028.md) sur sa branche, **pas sur main**. Ne pas fusionner #215 en assimilant des tests à l'admission writer.

**STOP :** M3.2 IN_PROGRESS_NOT_ACCEPTED ; A0 EXISTING_PROFILE STOP ; writer/R1–R9 production NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2) ; prospective NOT_STARTED ; PR #35 OPEN/DRAFT. Aucun accès SQLite opérateur, backup, ACL, WAL/SHM, marqueur persistant, récupération réelle, S3/S4, migration 007, IPC, Hello ou Ollama runtime. Respecter #38 append-only, CI exacte SHA, reviews/threads, expected_head_sha, postmain et ruleset sans bypass.

**Windows :** code `M:\\Fabulaxiom` ; profil Greenfield `%LOCALAPPDATA%\\com.fabulaxiom.greenfield.v1` ; ne pas ouvrir la base opérateur. Objectif : application locale utilisable pour création littéraire, mémoire narrative, chronologie et Ollama local, sans cloud ni API payante.

**Suite :** poursuivre qualification D3b sur #215 sans déployer ; préparer les preuves restantes R1–R9 sur fixtures, puis décision architecturale explicite. Ce handoff documentaire ne constitue ni preuve de production ni autorisation de fusion de #215.
