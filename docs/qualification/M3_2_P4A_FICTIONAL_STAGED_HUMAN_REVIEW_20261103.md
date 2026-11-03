# M3.2 — P4a revue humaine d'une proposition fictive (candidate test-only)

**3 novembre 2026 — CANDIDAT NON QUALIFIÉ.** Base protégée `main=62ec182ba963c4da3fc2db3dfbd55d99f987c70b`; PR #268 R4 région-1 source #41660006467 et postmain indépendant #41664658305 au SHA exact **completed/SUCCESS** : 303 Rust, 7 Greenfield, 68 inventaire SQLite, 183 continuité, Chromium 85/85 normal et CSP stricte. Cet addendum est historique de qualification des fixtures, pas preuve R4 globale.

## Produit — préparation du gate P4, sans l'ouvrir

P1/P2a/P2b/P3a–P3e ont déjà produit une chronologie inventée, ses révisions, ses liens humains, le refus des cycles et l'historique des corrections. La nouvelle étape **P4a** fournit une **revue avant confirmation** sans modifier l'état d'origine : `stageP4aFictionalPlan` calcule une projection avant/après d'une seule commande P3, l'inventaire des ancres créées/remplacées et des liens créés/révoqués, ainsi que les identifiants des révisions narratives conservées. `confirmP4aFictionalPlan` exige une raison humaine explicite et rejette un état d'origine devenu périmé ou une proposition modifiée. Elle recalcule la commande via le moteur P3 existant : **seule une nouvelle valeur RAM fictive est renvoyée**.

- `src/m32P4aFictionalReview.ts` : contrat pur, aucune écriture; comparaison d'images JSON comme détecteur de périmption dans une seule session, **pas une preuve de sécurité cryptographique**.
- `src/M32P4aFictionalReview.tsx` : interface React de revue autonome, explicitement absente de `App.tsx`, non reliée aux données Windows, à Rust ni aux IPC.
- `src/m32P4aFictionalReview.test.tsx` : six Vitest inventés : avant/après non destructif, motif obligatoire, refus d'état périmé, refus d'un résultat falsifié, univers/cycle/identifiants invalides et rendu HTML isolé.
- Aucun changement des modules Rust, du VFS par défaut, de SQLite production, de Cargo, des capacités Tauri, de `App.tsx`, d'IPC, des profils ou de migrations. Aucun serveur ou accès réseau.
- Les tests **n'ouvrent PAS le gate P4** : aucune authentification de provenance/source, aucun contrôle de writer réel ni garantie cryptographique; même une confirmation acceptée reste strictement fictive.

## Qualification distincte

CI Windows obligatoire sur SHA exact de la PR : **303 Rust / 7 Greenfield / 68 inventaire / 183 continuité / Chromium 85/85 normal et CSP stricte ATTENDUS NON QUALIFIÉS**, plus six Vitest; audit diff, reviews/threads, Protect main active strict bypass=[], squash `expected_head_sha`, CI indépendante postmain et #38 append-only. P4 réel demeure un gate séparé, non franchi par une UI de revue fictive. La recherche sur SQLite WAL documente l'usage des méthodes xShmMap et xShmLock dans un VFS NORMAL (https://sqlite.org/wal.html), mais n'autorise aucune conclusion sur la garde atomique des handles Win32.

**Stratégie ACTIVE : PRODUCT_FIRST_PARALLEL_SAFETY**, avertir propriétaire AVANT changement. R4–R9 en parallèle; main/WAL/SHM custody, SHM pages >0 hors bornes 0..1, écrivains adversariaux même SID, crash/ABA restent NOT_PROVEN. glib 0.18.5 Linux GTK3 GHSA-wrw7-89jp-8q8g / issue #160 **OPEN_NOT_REMEDIATED**.

**STOP inchangés :** M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; D3b-4/5 STOP. Aucune donnée v6/v7 opérateur, profil Greenfield préexistant, journaux/sauvegardes, IPC writer, migration 007 runtime, Hello natif, marqueur ou recovery. Les fixtures ne sont ni autorisation P4 ni admission G3.
