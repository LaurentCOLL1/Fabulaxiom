# M3.2 — Contrat d'interface et d'acceptation de chronologie manuelle

**PLAN DOCUMENTAIRE UNIQUEMENT — aucun code de production, aucune interface modifiée, aucune autorisation d'écriture ou de migration.**

## Sources de vérité et statut

- Feuille de route : docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md, section M3.2 Manual chronology and ordering UX.
- Schéma existant : src-tauri/sql/m3_1_world_time_v7_candidate.sql, **candidat v7 isolé uniquement**, non enregistré dans les migrations automatiques de la production.
- Prédécesseur qualifié : PR #35 HEAD 5839d3d23d04ee8bab8a7af1a7f50bb45582cf1a, CI Windows exacte #38506803238, 31/31 SUCCESS dont 33 tests synthétiques de provenance.
- Contrôle réel Stage 18.1 : 26/26 éléments de conservation, SHA historiques 21/21 et observations récentes 3/3, intégrité et clés étrangères SQLite isolé v7 PASS ; sept migrations, 14 tables historiques STRICT, trois nouvelles tables STRICT vides, empreinte logique v6 conforme, SHA de la copie v7 inchangé avant/après.
- Autorité historique : trois observations récentes (premier manifeste M2.4 et deux archives ACL) et deux éléments sans empreinte d'origine indépendante (marqueur d'activation M1.5 et copie isolée M2.5 v6). Aucun témoin historique supplémentaire authentifié.
- Le résultat global reste PENDING_EXTERNAL_ATTESTATION ; il ne devient pas READY sous l'effet d'un document, d'une référence HTTPS déclarée ou d'une réussite de CI.

## Trois dimensions temporelles impérativement distinctes

| Dimension | Source et interprétation | Ce qu'il ne faut pas inférer |
|---|---|---|
| Chronologie du monde | Assertions humaines : événement exact, approximatif, relatif ou inconnu dans un Univers fictif | Aucun calendrier grégorien automatique, aucune date Unix, aucun ordre total implicite |
| Ordre du récit | Organisation existante roman / chapitre / scène et référence textuelle immuable | Une modification de la chronologie ne doit jamais déplacer une scène |
| Ordre de révélation au lecteur | Dimension distincte planifiée pour un jalon ultérieur | Ne jamais l'inventer depuis le texte, le temps fictif ou un mot-clé |

Sans correspondance de calendrier explicitement créée sous autorisation distincte, les dates de calendriers fictifs différents sont incomparables. Une relation humaine A avant B peut contraindre leur ordre relatif sans les convertir.

## Contrat réel des trois tables v7 immuables

- fictional_calendars : identifiant, Univers, nom, definition_text, created_at_utc. Aucun calendrier par défaut.
- world_time_anchors : identifiant, Univers, calendrier facultatif, événement facultatif, révision textuelle immuable facultative, time_kind (exact, approximate, relative, unknown), exact_label, window_start_text, window_end_text, precision_text, created_at_utc.
- world_time_precedences : identifiant, Univers, before_anchor_id, after_anchor_id, raison non vide, révision textuelle facultative, created_at_utc.
- Pour exact : calendrier et étiquette non vide obligatoires, aucune borne approximative. Pour approximate : calendrier, précision explicite et au moins une borne textuelle non vide, mais n'inventer ni début ni fin manquant. Pour relative et unknown : pas de calendrier, date, fenêtre ou précision ; seuls les liens d'ordre explicites peuvent établir des contraintes temporelles.
- Identités et révisions : les mêmes noms affichés ne fusionnent jamais deux IDs. Chaque source_revision_id doit désigner une révision historique précise dans le même Univers, pas la dernière révision courante. Une entité d'événement doit être de type event.
- Ordre partiel : interdiction des boucles, liens A→A et doublons ; jamais de tri total caché. Les ancres non comparables doivent rester visibles comme telles.
- Les triggers v7 **refusent les UPDATE et DELETE** sur les trois tables. Un éditeur prétendant corriger directement un ancien enregistrement serait mensonger. Une proposition de supersession/rectification **append-only** doit faire l'objet d'une conception, de tests et d'une autorisation distinctes avant de revendiquer un CRUD complet.

## Proposition UX future — aucune fonctionnalité livrée ici

1. Sélection explicite de l'Univers ; plusieurs romans d'un même Univers peuvent fournir des révisions sources historiques. Aucun accès transversal automatique.
2. Panneau Chronologie du monde : présenter chaque assertion humaine avec son type, sa précision brute, ses IDs immuables et les relations avant/après ; afficher « ordre indéterminé » quand aucune contrainte ne tranche.
3. Panneau Ordre narratif : affichage indépendant de romans/chapitres/scènes sans déplacement et sans réécriture de leurs révisions.
4. Panneau Révélation lecteur : explicitement « non encore disponible », sans exposition implicitement calculée.
5. Sous le statut PENDING, les actions de création, édition, suppression et liaison M3.2 doivent rester indisponibles. Ne montrer aucun succès fictif ni écriture optimiste.
6. Après autorisation distincte, chaque mutation devra être transactionnelle et retourner un conflit reproductible sur source invalide, erreur d'Univers, cycle ou relation contradictoire, sans supprimer les assertions existantes.

## Matrice de tests synthétiques pour une future implémentation autorisée

| Cas | Situation d'essai | Résultat exigé |
|---|---|---|
| A | Deux Univers, plusieurs romans, deux événements de même nom | Identifiants distincts et cloisonnement strict |
| B | Étiquette fictive exacte « troisième cloche » | Texte inchangé, aucune conversion grégorienne |
| C | Fenêtre approximative avec borne manquante et précision déclarée | Ne pas inventer la borne absente |
| D | Date inconnue, ancre relative et relation A avant B | Aucun ordre implicite ajouté |
| E | Ancres non reliées | Résultat explicitement incomparable |
| F | A avant B, B avant C, puis C avant A | Refus déterministe, aucune modification précédente |
| G | Relation A avant A ou double A avant B | Refus atomique |
| H | Calendrier, événement, révision ou lien d'un autre Univers | Refus et conservation des données |
| I | Source renvoyant vers la mauvaise ou une ancienne révision | Révision historique exacte conservée, pas de substitution |
| J | UPDATE/DELETE d'une ancre ou précédence historique | Refus conforme aux triggers, aucune réussite prétendue |
| K | Ordre du récit différent de la chronologie fictive | Panneaux séparés ; révélation lecteur indisponible |
| L | Fermeture et restauration lors d'une future cérémonie isolée | Intégrité SQLite, backups et pointeur M1.5 intacts |

Ces scénarios sont des spécifications, pas des tests Windows réels ni une autorisation de les exécuter sur les bases originales.

## Conditions incontournables avant implémentation

Conserver la production restaurée M1.5 v6, les sept worktrees, la copie M3.1 v7 isolée et toutes les sauvegardes. Ne jamais enregistrer la migration 007 dans le démarrage normal sans cérémonie distincte, sauvegarde SQLite cohérente non écrasante, manifeste de référence et tests opérateur. Ne pas convertir des observations contemporaines en preuves historiques antérieures. Aucune interface d'écriture M3.2, aucune fusion de PR #35, aucun M3.3 tant que ces portes demeurent fermées.

Le présent texte pourra être qualifié par CI sur son SHA exact mais cette qualification **ne vaut que pour la documentation**.
