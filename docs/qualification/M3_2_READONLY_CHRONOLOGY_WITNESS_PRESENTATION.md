# M3.2 — Stage 27 : présentation synthétique des justifications chronologiques

**Prototype de DTO Python entièrement en mémoire, en lecture seule. Ce n'est ni une fenêtre React, ni un IPC Tauri/Rust, ni une lecture SQLite réelle ou une autorisation de modification.**

## Prédécesseur exact et autorité

- GitHub `main=f7eabfea74480d307b52d4b053730021efc95352`, PR #35 toujours ouverte et DRAFT.
- Stage26 accepté au SHA exact `a960520d8022544259bd3c4bfb6f26ca53bf21b5`, workflow Windows [#38630895947](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38630895947) terminal `completed/success`, **38/38 étapes** dont 32 tests de justification.
- Les trois dimensions demeurent indépendantes : ordre du monde par précédences humaines, ordre narratif de manuscrit et révélations au lecteur non disponibles dans la projection synthétique. Aucun ordre temporel total, aucune conversion de dates fictives.
- La réussite du Stage26 ne qualifie aucun nouveau commit Stage27.

## Contrat du DTO Stage27

`present_world_order_witness(snapshot, universe, left_id, right_id, filters=...)` **recalcule** l'explication Stage26 via la sélection Stage25, au lieu de consommer une preuve arbitraire transmise par un appelant. Les deux extrémités doivent appartenir au même Univers, être actives et correspondre aux filtres. L'indication « avant/après » n'est fondée que sur les relations humaines explicites, éventuellement transitives ; « identique » correspond au même ID actif ; « incomparable » reste un ordre non établi, jamais une impossibilité prétendue.

`WorldOrderWitnessPanel` et `WitnessDisplayStep` sont des dataclasses figées. Le DTO renvoie la relation et une clé de message non interprétative, les étapes numérotées **dans la chaîne de justification seulement**, les IDs historiques d'ancres et de liens, et un état explicite d'absence de preuve. Pour `after`, les étapes suivent toujours le sens du monde déclaré « avant → après », même si la sélection se lit droite-à-gauche. Pour `same`, aucune précédence n'est inventée ; pour `incomparable`, aucune chaîne n'est fabriquée.

La sortie ne reprend pas les textes bruts des dates, calendriers, révisions ou les champs des ancres intermédiaires. Les IDs intermédiaires peuvent ne pas satisfaire les filtres de texte des extrémités ; une véritable application devra appliquer **son propre contrôle d'accès**, car ces filtres synthétiques ne prouvent pas une permission. Les numéros de lien ne sont ni des dates, ni une chronologie numérotée, ni un ordre narratif. `witness_panel_json` est déterministe, mais n'est ni une attestation d'archive, ni une signature, ni un contrat de transport activé.

## Qualification nouvelle requise — non acquise avant CI

`tools/test_m3_2_chronology_witness_presentation_reference.py` ajoute **30 tests synthétiques** : chemins directs, inversés, transitifs, concurrents, chaîne la plus courte, identiques/incomparables, calendriers fictifs, isolation multi-Univers, filtres textuels, rejets d'assertions historiques, 513 ancres, confidentialité des seuls IDs, déterminisme, immutabilité et indisponibilité des commandes d'édition. Le workflow doit désormais être **39/39 SUCCESS sur le SHA exact** ; Stage26 et les autres suites ne peuvent pas le remplacer.

Statut opérateur global inchangé : `PENDING_EXTERNAL_ATTESTATION` (21 empreintes historiques, 3 observations récentes, 2 rôles non ancrés). Préserver les sept worktrees Windows, la production restaurée M1.5 v6, la copie isolée M3.1 v7, les ACL, archives et sauvegardes. Pas de migration `007` normale, de writer IPC, de fusion PR #35, ni de M3.3.
