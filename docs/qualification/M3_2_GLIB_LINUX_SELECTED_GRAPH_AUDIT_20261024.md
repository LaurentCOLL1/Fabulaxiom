# M3.2 — Audit d'exposition GLib/GTK dans le graphe Cargo sélectionné pour Linux

**Précision runner CI :** le runner Windows ne dispose pas initialement de l'archive du crate Linux `atk 0.18.2`. Un `cargo fetch --locked --target x86_64-unknown-linux-gnu` est donc requis **sur le runner GitHub seulement**, avant `cargo tree --locked --offline` : téléchargement de sources avec checksums de `Cargo.lock`, **sans compilation, sans script, sans écriture d'un nouveau verrou ni contact avec le Windows de l'opérateur**. Le premier run de cette candidate a STOP par absence d'archives offline ; aucun résultat antérieur n'est réutilisable.


**Candidat source-only du 24 octobre 2026.** Ni correction Rust, ni revue de runtime Linux, ni accès Windows de l'opérateur.

## Autorité antérieure revalidée

[PR #162](https://github.com/LaurentCOLL1/Fabulaxiom/pull/162) source `3d7c517561457add580d33151fc0bd10db3e519b`, [CI source #40085001106](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40085001106) `completed/SUCCESS` ; fusion protégée `main=b5d97648cc18597b23f9fece67fd78b094743abb`, [CI postmain #40085871815](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40085871815) `completed/SUCCESS` vérifiée indépendamment. Chaque run : 78 étapes Windows, 96 contrats, 96 tests du carnet fictif, 82/82 Chromium normal et CSP strict, 132 Rust PASS. L'ancienne qualification Windows `M32_GLIB_WINDOWS_TARGET_AUDIT_PASS` montre 247 paquets retenus pour la cible `x86_64-pc-windows-msvc` et aucune sélection GTK/GLib à ce niveau de sélection. Ce n'est **PAS** une dispense de l'alerte Rust/Linux.

## Avis officiel

[GHSA-wrw7-89jp-8q8g](https://github.com/advisories/GHSA-wrw7-89jp-8q8g) affecte `glib >=0.15,<0.20` ; la première version corrigée est `0.20.0`. L'implémentation de `VariantStrIter` présente un comportement indéfini susceptible d'entraîner des plantages. `src-tauri/Cargo.lock` retient `glib 0.18.5`, `gtk 0.18.2`, `webkit2gtk 2.0.2` dans le graphe multiplateforme Tauri 2.12.1 / WRY. Le correctif `glib=0.20.0` n'est **pas** un remplacement compatible direct de la famille GTK3 0.18. **Ne pas le forcer** ; ne pas supprimer ou dismiss l'alerte #1.

## Contrôle proposé

Après le contrôle ciblé Windows, ajouter dans la CI Windows un script purement observateur `python tools/m32_glib_linux_target_audit.py` :

```text
cargo tree --manifest-path src-tauri/Cargo.toml --locked --offline --target x86_64-unknown-linux-gnu --edges normal,build --prefix none --format {p}
```

Le graphe est filtré par cible **Linux**, mais la commande tourne sur un runner Windows ; **elle ne réalise aucune compilation cross-platform**. Elle doit constater les versions exactes `glib=0.18.5`, `gtk=0.18.2`, `webkit2gtk=2.0.2` et produire un marqueur `M32_GLIB_LINUX_EXPOSURE_AUDIT_PASS` indiquant `linux_risk_status=OPEN_NOT_REMEDIATED`, `real_g3=STOP_UNAVAILABLE`. Les composants sont sélectionnés par un parseur qui exige `fabulaxiom` et un graphe complet ; toute absence, dérive ou erreur Cargo conduit à STOP, **et non** à l'affirmation de sécurité. Cette observation ne prouve pas qu'un appel applicatif atteint `VariantStrIter` ; elle renforce uniquement la traçabilité de l'alerte.

L'audit utilise `shell=False`, `timeout=180`, aucune modification de `Cargo.toml`, `Cargo.lock`, `App.tsx`, `src-tauri`, aucun nouveau cache ni permission, aucune exécution sur l'ordinateur de l'opérateur. Il ne fait pas d'appels externes lorsque les métadonnées Cargo sont disponibles `--offline`.

## Qualification exigée

Nouveau contrat de continuité #97 : preuve terminale PR #162, séquence des étapes, refus graphe incomplet, `glib` absent ou mis à une nouvelle version, `gtk` ou `webkit2gtk` absents, protection des prompts et de `Protect main`. Attendus **non anticipés** sur nouveau HEAD : **79** étapes Windows, 97 contrats, 96 Vitest fictifs, 82/82 Chromium par mode et 132 Rust sans régression. Nouvelle CI source au SHA final, revue diff/reviews/threads, fusion protégée `expected_head_sha` et CI postmain indépendante. Consigner l'observation dans l'[issue #160](https://github.com/LaurentCOLL1/Fabulaxiom/issues/160) et l'issue de garde #38 en préservant les anciens checkpoints.

Les cinq alertes npm corrigées par Vite 8.1.6 **ne sont pas encore attestées CLOSED dans l'interface privée Dependabot** ; demander au propriétaire de vérifier le compteur. L'alerte glib reste **OPEN_NOT_REMEDIATED**.

## Gates non modifiés

M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, absence d'écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucune SQLite v6/v7 originale, backup, ACL, marqueur, sidecar, migration 007, IPC writer, M3.3, ComfyUI ou release.
