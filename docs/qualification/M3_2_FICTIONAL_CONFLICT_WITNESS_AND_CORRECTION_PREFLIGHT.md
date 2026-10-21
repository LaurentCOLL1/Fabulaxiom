# M3.2 — Aperçu des conflits avant validation (chronologie fictive)

**21 octobre 2026 — incrément exclusivement source-only dans le laboratoire navigateur inventé.** Point de départ vérifié : `main=205a328150c90bf1fb4f52abd7fb8c04f3959468`, PR #99 fusionnée, CI obligatoire de PR #39480662913 **SUCCESS 74/74**, CI post-fusion #39482419125 **SUCCESS**. Aucun droit G2-B/G3 ni accès opérateur n'en découle.

## Objectif produit M3.2

La roadmap [M3_TIME_KNOWLEDGE_RELATIONSHIPS.md](../roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md) exige une saisie *humaine* d'une **chronologie partielle**, des refus de contradictions déterministes, une histoire conservée et des références aux révisions immuables des scènes. Après PR #99 (liaison scène/révision fictives), le laboratoire propose maintenant deux **prévisualisations explicatives avant toute modification**.

### 1. Relation avant/après

`previewFictionalPrecedence(draft, before, after)` vérifie le graphe actif d'un seul Univers imaginaire. Réponses typées : `unselected`, `allowed` ou `blocked`. Si un lien `A avant B` est envisagé, un parcours **BFS déterministe** vérifie s'il existe déjà un chemin **B → ... → A**. Si oui, ajouter A → B créerait un cycle : le prévisualiseur restitue les identifiants exacts des ancres et des relations préexistantes constituant le témoin. Il refuse aussi une auto-référence, une ancre inconnue/historique ou un lien direct doublé. Il n'invente ni date grégorienne, ni ordre complet, ni nouvelle assertion canonique ; il n'ajoute aucune relation au brouillon.

La commande réelle *fictive* `createFictionalPrecedence` fait passer la proposition par **le même contrôle** et refuse atomiquement en cas de blocage, même si un appelant contourne la prévisualisation de l'interface. Les témoins portent sur les seuls liens `status=current` ; un lien révoqué ne crée pas de conflit vivant.

### 2. Correction d'une ancre et sa révision de scène

`previewFictionalCorrection(draft, id)` donne les identifiants ordonnés des relations `current` qui dépendent de l'ancre ainsi que son `source_revision_id` **historique** (s'il existe). Une correction ne peut pas retirer ces dépendances implicitement. L'utilisateur doit explicitement révoquer les liens concernés, avec sa raison, avant que la correction par *supersession append-only* devienne possible. La commande `supersedeFictionalAnchor` réemploie exactement le contrôle et préserve l'ancien ID et sa révision de scène immuable.

L'interface `M32ManualChronologyLab.tsx` affiche en direct deux zones `role=status` accessibles : « Vérification avant/après fictive » et « Vérification de correction fictive ». En cas de veto, le bouton de validation appelle toujours le réducteur et remonte une erreur explicite : **la prévisualisation n'est pas une autorisation d'écriture**.

## Qualification requise sur la branche de PR

- **10 nouveaux tests Vitest**, soit **32 au total** dans `src/m32ManualChronologyLab.test.tsx` : preuve de chemin cyclique, refus déterministe, doublon, absence de fausse chronologie, révocation explicite, conservation de source historique et observation sans mutation.
- **2 nouveaux scénarios Chromium**, soit **36 au total** : témoin des liens `human-ab` et `human-bc` avant C→A, puis révocation explicite de `human-ab` mettant à jour le refus de correction de A.
- CI à qualifier au nouveau **HEAD exact** ; ne jamais recycler une CI d'un commit antérieur.
- Pas de nouveaux modules JS importés : les neuf objets Git de la fixture, ses manifestes exact-source, la CSP, le sandbox navigateur et les commandes Tauri autorisées restent inchangés.

## Limites et décisions

C'est une démonstration **entièrement fictive**, en mémoire du navigateur jetable. Ce n'est ni la GUI Windows de production, ni la persistance SQLite autorisée, ni une preuve de préservation des bases de l'opérateur. M3.2 reste **IN_PROGRESS_NOT_ACCEPTED**, PR #35 **OPEN/DRAFT**, M3.3–M9 non autorisés. G2-A `PASS_METADATA_ONLY_OWNER_REPORTED` (accord unique consommé), `PROCESS_WRITER_ABSENCE=NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, réel G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`.

Aucune commande locale Windows n'a été demandée. Production SQLite v6, base v7 isolée, journaux WAL/SHM, sauvegardes, ACL, activation marker, migration 007, writer IPC, PR #35 merge, M3.3, ComfyUI et release restent interdits.

**Conception de l'UI :** ne pas muter les tableaux d'état React ([documentation officielle](https://react.dev/learn/updating-arrays-in-state)). Le contrôle du DAG reste source-only ; il ne prétend pas remplacer les futures contraintes SQLite et validations transactionnelles.
