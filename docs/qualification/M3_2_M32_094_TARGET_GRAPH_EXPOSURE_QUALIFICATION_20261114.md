# M32-094 — Qualification ciblée des graphes de dépendances Windows et Linux

**14 novembre 2026. Candidate sous Protect main.** Parent `main=ae232eb4dbf79ee25ed39fb2359c4952d51b26a6` après #363, CI source #43611918936 SUCCESS, postmain #43618124255 encore non qualifiée au checkpoint. Statut global M3.2 : IN_PROGRESS_NOT_ACCEPTED.

## Provenance exacte de la preuve

- PR #362 source HEAD `5206bba7f3196c454a22bf85d0d0dca879ee20e3`, [CI Windows #43594666828](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43594666828) completed/SUCCESS, job [#132446512015](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43594666828/job/132446512015), 93 étapes SUCCESS.
- Step 57 `m32_glib_target_audit.py`, graphe Cargo `--locked --offline --target x86_64-pc-windows-msvc` : **247 paquets**, pas de paquets GLib/GTK/WebKit2GTK sélectionnés.
- Step 58 `m32_glib_linux_target_audit.py`, graphe Cargo `--locked --offline --target x86_64-unknown-linux-gnu` : **277 paquets**, versions `glib 0.18.5`, `gtk 0.18.2`, `webkit2gtk 2.0.2`. Avis [GHSA-wrw7-89jp-8q8g](https://github.com/advisories/GHSA-wrw7-89jp-8q8g) OPEN_NOT_REMEDIATED.
- Postmain de #362 [#43610824403](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43610824403) completed/SUCCESS au SHA `8cba5e0bd758a39a501a5ee04c3957deec1ad36c`.
- Reconfirmation CI source #363 [#43611918936](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43611918936) completed/SUCCESS, 93/93 dont étapes 57/58, 495 tests Vitest. Pas d'inférence de statut de la postmain #363.

## Portée permise de M32-094

**Clôture ciblée proposée :** Windows et Linux ont des **graphes Cargo sélectionnés distincts** et la vulnérabilité glib n'est pas sélectionnée dans ce graphe Windows. Cette clôture n'atteste ni la sûreté de l'exécution Windows en général, ni l'exploitabilité ou non-exploitabilité de l'appel `VariantStrIter` sous Linux. Aucun build ou lancement Linux n'a été effectué. **Distribution Linux toujours interdite sans qualification Linux spécifique et décision de risque séparée.**

M32-093 (correctif glib), M32-092 (inventaire complet des alertes Vite/launch-editor) et issue #160 demeurent OPEN. Ne pas mettre à jour Cargo.lock manuellement, ignorer ou masquer l'avis, ou inférer un état Dependabot privé. Les travaux writer R1–R9, G2B/G2C/G3, v6/v7, main/WAL/SHM/ABA, Greenfield, recovery et IPC restent STOP.

## Traçabilité

La matrice de 104 critères et `tools/test_m32_requirements_traceability.py` exigent un enregistrement de preuve avec SHA, CI exacte, job, step, postmain, et les cinq refus `runtime_reachability_proven/linux_build_performed/linux_distribution_authorized/operator_data_access/writer_admission=false`. Liste de clôtures autorisées fixe et contrôlée ; le calcul des compteurs provient de cette liste (ne doit jamais autoriser une case par simple incrément). **9 tâches ciblées candidates closes, 95 ouvertes**, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %).
