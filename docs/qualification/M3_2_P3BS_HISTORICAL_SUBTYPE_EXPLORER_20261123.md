# P3bs — distinguer révocation et remplacement dans l'explorateur fictif (23/11/2026)

**SOURCE_ONLY_CANDIDATE_UNQUALIFIED — NO_RUNTIME_ADMISSION.** Parent protégé `main=8fca3130315803309ddcfa0a4f82369f5044a005`, PR #421 MERGED, CI Windows source #45111836510 completed/SUCCESS sur HEAD exact `74ffebf461fb86a44cca13a64522e7e224413906`. Postmain #45202139946 event push SHA exact parent a été observée IN_PROGRESS à la préparation : **PENDING_UNQUALIFIED**, ne pas anticiper le résultat.

## Fonctionnalité isolée

L'explorateur `src/M32SyntheticEventExplorer.tsx`, monté uniquement dans `m32BrowserLab.tsx` (fixture), connaissait les filtres `all`, `current` et `historical`. P3bs ajoute les filtres explicites `revoked` et `superseded` sans modifier les trois filtres précédents ni les identités de révision exactes. Les événements historiques ne deviennent jamais sélectionnables pour une comparaison active et l'ancienne sélection explicite de deux ancres courantes reste valide même si des filtres la cachent.

La validation globale du graphe, la prévention des cycles et l'isolement d'Univers interviennent **avant** le filtrage de présentation. Tri Unicode scalaire, pagination à huit, refus d'un statut non reconnu, échappement React et `can_write=false` sont conservés. Aucune conversion automatique de dates, provenance de scène/roman ou succès de persistance n'est déduit.

## Preuve candidate et limites

Sept scénarios Vitest dans `src/m32ExplorerHistoricalSubtypeFilter.test.tsx` : partition des statuts, composition d'un filtre de révision exact, conservation du témoin humain de comparaison, rejet de cycle masqué, refus inter-Univers/statut/sélection obsolète, noms accessibles et absence d'écriture, échappement + non-mutation. La suite doit passer Windows `pull_request` CI sur **HEAD exact candidat** puis revue du diff, Protect main strict, squash attendu et postmain indépendante.

**M32-071 [ ] / M32-075 [ ] / M32-078 [ ] / M32-081 [ ] restent OPEN_NOT_ACCEPTED** : il s'agit d'une amélioration de l'atelier synthétique non monté dans l'application, sans interface Tauri de production ni preuve d'acceptation utilisateur. Checklist 104 : **13 CLOSED_SCOPED / 91 OPEN_NOT_ACCEPTED**. M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif), PRODUCT_FIRST_PARALLEL_SAFETY.

**STOP** Writer/R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED, R2 STOP/R3 partiel/D3c conception/D3b-4/5 et D3b-5 STOP, live SQLite main/WAL/SHM WAL-index et ABA NOT_PROVEN, glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
