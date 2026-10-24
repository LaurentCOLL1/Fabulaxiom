# M3.2 / dépendances — GHSA-wrw7-89jp-8q8g dans glib 0.18.5

**Qualification ciblée, Windows uniquement, au 24 octobre 2026. Ni correctif Rust ni dispense de sécurité.**

## Autorité observée
[PR #161](https://github.com/LaurentCOLL1/Fabulaxiom/pull/161) fusionnée `main=6cf1dd175431f19cde7a347a44d1d53f29ffecb2`, CI source #40071869911 SUCCESS, CI postmain #40072779652 SUCCESS indépendantes. Elle utilise Vite 8.1.6 pour **cinq alertes npm** ; fermeture Dependabot à confirmer dans l'interface. `src-tauri/Cargo.lock` contient toujours `glib 0.18.5` et sa chaîne `gtk 0.18.2` / `webkit2gtk 2.0.2`.

L'avis officiel [GHSA-wrw7-89jp-8q8g](https://github.com/advisories/GHSA-wrw7-89jp-8q8g) confirme que `glib >=0.15,<0.20` est affecté et `0.20.0` corrigé. Le bug `VariantStrIter` peut provoquer un comportement indéfini. **Il n'est pas corrigé dans ce dépôt.** La migration amont [wry GTK4/WebKit6 #1767](https://github.com/tauri-apps/wry/pull/1767) et [wry #1474](https://github.com/tauri-apps/wry/issues/1474) n'est pas un changement trivial pour Tauri 2 / GTK3. Forcer `glib=0.20` dans ce lock sans aligner tout l'écosystème est interdit.

## Nouvelle preuve source-only proposée

Ajouter à la CI Windows, **après** le test Rust et **avant** le check Rust, un appel :
```text
python tools/m32_glib_target_audit.py
```

Le programme vérifie que `Cargo.lock` conserve l'unique `glib=0.18.5` (contrôle de dérive). Sur le runner, `cargo tree --manifest-path src-tauri/Cargo.toml --locked --offline --target x86_64-pc-windows-msvc --edges normal,build --prefix none --format {p}` produit le graphe de dépendances normales et de build **sélectionnées pour la cible Windows** sans compiler ni exécuter l'application. Le parseur exige la racine `fabulaxiom` et un graphe suffisamment renseigné, puis échoue fermement si `glib`, `gtk`, `gdk`, `gio`, `webkit2gtk` ou leurs variantes -sys sont présentes.

**Ce que cela prouve en cas de PASS :** pour le manifeste et les options inspectées, Cargo ne sélectionne pas la famille GTK/GLib pour le graphe Windows examiné. **Ce que cela ne prouve PAS :** une absence générale de vulnérabilité, une preuve de non-atteignabilité formelle, le bon comportement d'un build Linux, ou l'absence d'alerte dans le lock multi-plateforme. L'avis Rust reste **OPEN_NOT_REMEDIATED** et aucune alerte ne doit être fermée artificiellement.

Le test de continuité #96 inclut des cas synthétiques positifs/négatifs (graphe incomplet, glib accidentellement présent, gtk accidentellement présent, version de lock conservée), l'ordre exact des étapes et les preuves terminales de PR #161. Ce correctif CI ajoute une étape Windows : 78 contre 77 historiques. Il ne modifie pas `Cargo.lock`, `Cargo.toml`, la production, les IPC, ni la machine opérateur. Ne pas activer de cache Cargo par ce changement.

## Décision et suivi

- En cas de FAIL : **STOP**, étudier le graphe réel, ne pas masquer le paquet ni ignorer Dependabot.
- En cas de PASS : documenter la limitation de risque **Windows uniquement** ; maintenir l'[issue sécurité #160](https://github.com/LaurentCOLL1/Fabulaxiom/issues/160) ouverte pour la correction glib Linux en amont.
- Avant intégration : nouvelle CI terminale sur SHA exact, diff/reviews/threads, `Protect main`, squash `expected_head_sha`, CI postmain indépendante. Aucun résultat anticipé : seuils attendus 96 contrats, 96 Vitest carnet inventé, Chromium 82/82 dans les deux modes, Rust 132, 78 étapes Windows.
- Contrôles de sécurité M3.2 inchangés : `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucune SQLite originale v6/v7, sauvegarde, ACL, sidecar, marqueur, migration 007 ni writer IPC.

**IMPORTANT : ni mise à jour de glib ni clôture de l'alerte ne sont réalisées par cette qualification.**
