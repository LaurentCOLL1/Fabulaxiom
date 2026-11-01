# Fabulaxiom — glib Dependabot #1 ouvert : compatibilité Tauri / GTK3

**1er novembre 2026. Constat sécurité, PAS CORRECTION.** Le propriétaire a transmis une capture d'écran de l'alerte modérée (CVSS v4 6,9) [GHSA-wrw7-89jp-8q8g](https://github.com/advisories/GHSA-wrw7-89jp-8q8g) / [RUSTSEC-2024-0429](https://rustsec.org/advisories/RUSTSEC-2024-0429.html), toujours **OPEN** pour `src-tauri/Cargo.lock` : `glib=0.18.5`, affectée `>=0.15,<0.20`, première version corrigée `0.20.0`. Bug `VariantStrIter::impl_get` : pointeur C de sortie transmis avec mutabilité incorrecte ; comportement indéfini / plantage possible en build optimisée.

## Éléments vérifiés dans le dépôt vivant

- `Cargo.toml` : `tauri="2"`, pas de `glib` direct. `Cargo.lock` observé sur `main=6346ebd405345e1cc2447cd28fa679bef7f19490` : `tauri=2.12.1`, `wry=0.57.0`, `gtk=0.18.2`, `gio=0.18.4`, `webkit2gtk=2.0.2`, `glib=0.18.5`.
- CI du projet a déjà des audits `tools/m32_glib_target_audit.py` (graphe cible Windows **sans GTK/GLib sélectionnés**) et `tools/m32_glib_linux_target_audit.py` (**graphe Linux exposé**, `OPEN_NOT_REMEDIATED`). Ces constats ne prouvent PAS qu'aucun appel indirect Linux n'atteint `VariantStrIter`.
- Remplacer uniquement `glib 0.18` par `glib 0.20` dans Cargo.lock est **incompatible avec les contraintes semver de la famille GTK3 0.18** ; ne pas faire de faux patch ni ignorer la dépendance.
- Recherche amont au 1er novembre : [gtk-rs-core PR #2009](https://github.com/gtk-rs/gtk-rs-core/pull/2009) proposant un backport `glib 0.18.6` **CLOSED / NON MERGED**, [gtk-rs-core issue #2010](https://github.com/gtk-rs/gtk-rs-core/issues/2010) pour release 0.18.6 **CLOSED**, [tauri #12564](https://github.com/tauri-apps/tauri/issues/12564) **CLOSED/not_planned**, migration GTK4 plutôt envisagée dans l'écosystème Tauri 3. **Aucune version compatible corrigée n'a été établie** lors de cette analyse.

## Action réelle et conditions de sortie

**Garder l'alerte et [issue #160](https://github.com/LaurentCOLL1/Fabulaxiom/issues/160) ouvertes ; aucun Dismiss/ignore/false-positive sans preuve.** Surveiller une release officielle `glib 0.18.x` corrigée et reconnue par l'advisory, ou une migration Tauri/WRY compatible vers GTK4 avec `glib>=0.20`, puis produire un Cargo.lock authentique par Cargo (ne pas l'éditer à la main), audit `cargo tree --locked` Windows et Linux, Rust Windows exact-head CI, et vérifier que Dependabot marque l'alerte **CLOSED FIXED**. Tant que non atteint : afficher **OPEN_NOT_REMEDIATED** sans le dissimuler.

Poursuivre la stratégie choisie **PRODUCT_FIRST_PARALLEL_SAFETY** sur fixtures Windows nouvelles ; si exposition Windows ou risque remettant en cause l'isolation se révèle, **informer le propriétaire avant de recommander un changement d'orientation**, avec options et conséquences. Ne jamais convertir « non sélectionné par Windows » en « l'alerte a disparu » ni prétendre que l'installation GitHub des paquets est sûre en Linux.

**STOP M3.2 IN_PROGRESS_NOT_ACCEPTED, writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; aucune SQLite opérateur ou writer IPC.**
