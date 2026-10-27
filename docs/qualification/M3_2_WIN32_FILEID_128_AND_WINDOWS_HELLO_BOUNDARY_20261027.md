# M3.2 — identité FileId 128 bits de fixture et place éventuelle de Windows Hello

**Deux questions distinctes ; seule la première fait l'objet d'un nouveau test CI. AUCUNE authentification Windows Hello n'est implémentée.** État vivant re-fetch du 27 octobre : [PR #195](https://github.com/LaurentCOLL1/Fabulaxiom/pull/195) MERGED, source `f84f3035170baa4830879796230675ad8b328a2c`, [CI exacte #40516204731](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40516204731) **SUCCESS**, squash protégé `main=1ab320f7834086ac587ce2fdaa8638d7c29d61f5`, [postmain #40518270685](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40518270685) **SUCCESS** indépendante, [issue #38 terminale #6444458042](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6444458042) ; **153 Rust, 7 Greenfield, 34 gardes, 126 contrats** à ces seuls SHA. Le dépôt vivant prime sur cette observation datée. PR #35 reste OPEN/DRAFT.

## A. Suite technique expérimentale — vrais handles, FileId 128 bits

Le `GetFileInformationByHandle` précédent compare un index fichier **64 bits** et un volume **32 bits**. Microsoft prévient que l'identifiant 64 bits n'est **pas nécessairement unique sous ReFS**. Le test ajouté ne change pas le runtime : `GetFileInformationByHandleEx(..., FileIdInfo=0x12, ...)` récupère le `FILE_ID_INFO` Windows (numéro de volume 64 bits, FileId 128 bits) depuis :

1. le handle du fichier de fixture, créé avec `create_new(true)` ;
2. le handle natif réellement ouvert par SQLite après son `xOpen`, via `SQLITE_FCNTL_WIN32_GET_HANDLE` déjà qualifié dans #195.

Le nouveau test `m32_windows_sqlite_fileid_128_matches_claim_but_cannot_prevent_prior_swap` possède **deux** sous-cas : identité égale sur fixture neuve avec claim retenu ; puis, dans **une deuxième racine jetable**, précheck des parents positif, libération du claim, déplacement de l'original, création d'un autre fichier au même nom, `xOpen` suivant ce nom et FileId 128 bits du fichier **déjà substitué**. La comparaison au FileId initial doit montrer le désaccord. Le marqueur d'activation reste absent, les deux fichiers test sont vides et préservés, aucune requête métier n'est lancée sur le fichier substitué.

**Cibles et non résultat anticipé** : 154 Rust (+1 Windows), 7 Greenfield inchangées, 35 gardes d'inventaire (+1), 127 contrats de continuité (+1). Occurrences textuelles connues du module Rust de test : `(20,4,3,2,0,8,0)` (+1 RW fichier jetable). Aucun changement `Cargo.lock`, SQL, Tauri runtime, migration 007, workflow ou profil opérateur.

**Limite de l'incrément A :** FileId 128 bits améliore le *format de mesure* et le risque de collisions 64 bits ReFS, **pas** l'atomicité du passage du nom à `xOpen`. Une identité peut être réutilisée après disparition d'un fichier, et les opérations VFS avant comparaison ne sont pas exclues. Pas de preuve sur ACL, tous les ascendants du vrai profil, reparse/junctions, droits de noms, sidecars WAL/SHM/journaux, adversaire même utilisateur, ni sauvegarde/réouverture.

Références officielles : [Microsoft `FILE_ID_INFO`](https://learn.microsoft.com/fr-fr/windows/win32/api/winbase/ns-winbase-file_id_info), [`GetFileInformationByHandleEx`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex), [limite 64 bits sur ReFS](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information), [SQLite contrôle natif Win32](https://www.sqlite.org/c3ref/c_fcntl_begin_atomic_write.html).

## B. Réponse produit à Laurent — identification Fabulaxiom / Windows Hello

L'identification peut être **utile** pour une demande volontaire d'accès à l'UI, l'attribution d'une validation chronologique et la confirmation d'une opération sensible. Elle est un **axe de sécurité et d'UX DISTINCT** de la propriété du fichier SQLite et de la preuve d'un écrivain unique.

| Mesure future possible | Ce qu'elle pourrait apporter | Ce qu'elle ne prouve pas |
|---|---|---|
| Vérification `UserConsentVerifier` sur desktop Windows (interop HWND) | Présence/consentement du compte Windows connecté avant une opération sensible | Identité personnelle distincte à plusieurs profils, signature durable d'une décision, isolement d'autres processus du même compte, FileId stable, absence de writer |
| WebAuthn / Windows Hello / passkey avec création de credential et vérification de signature | Authentification cryptographique avec identité de compte *si* protocole, challenge, origine/RP, vérification et récupération correctement conçus | Protection automatique d'un fichier SQLite direct, sécurité de `xOpen`, migration 007 |
| Mot de passe propre à Fabulaxiom (à **ne pas** ajouter par défaut) | Connexion applicative potentielle après enrôlement et garde backend | Chiffrement ou protection de SQLite si le fichier reste lisible directement ; politique de récupération, hashing, stockage et menace à qualifier |
| DPAPI utilisateur Windows (proposition séparée) | Protection de secrets au repos liée en général à l'utilisateur/machine Windows | Distinction entre processus sous la même identité Windows ni unicité writer ; portable/restauration à concevoir |

**Position proposée, sans autorisation implicite d'implémenter :**

1. **Étape d'analyse source uniquement** : poser d'abord des contrats du type `UI_IDENTITY_VERIFIED`, `STORAGE_IDENTITY_VERIFIED`, `WRITER_EXCLUSIVITY_PROVEN` et `HUMAN_DECISION_AUTHORIZED` sans jamais les confondre. Pour l'instant seul l'éventuel premier peut être rendu disponible à terme ; les deux suivants restent **NON PROUVÉS**.
2. Pour Fabulaxiom à utilisateur unique sur Windows, **préférer étudier `UserConsentVerifier`** pour la *confirmation d'opérations sensibles*, si Laurent décide de l'activer. Desktop non-UWP : Microsoft indique la variante `RequestVerificationForWindowAsync(HWND,...)`, pas l'appel UWP ordinaire. Aucun dialogue OS lancé dans cette tranche.
3. **Ne jamais demander le PIN Windows dans un champ Fabulaxiom**, ni lire, enregistrer ou transmettre mot de passe/PIN/biométrie. Windows Hello administre le geste et garde le PIN local ; l'application peut au mieux recevoir un résultat de consentement ou une assertion cryptographique suivant l'API choisie.
4. Si de **véritables comptes multi-utilisateurs**, des signatures d'approbation ou un déverrouillage chiffré sont souhaités, cela réclame une décision de produit séparée sur WebAuthn, identité, récupération, sauvegardes et stockage ; aucun changement de schema, profil Windows, Tauri IPC ou DB n'est autorisé ici.

Sources officielles : [Microsoft `UserConsentVerifier` et interop desktop](https://learn.microsoft.com/en-us/uwp/api/windows.security.credentials.ui.userconsentverifier), [Windows WebAuthn Win32](https://learn.microsoft.com/en-us/windows/win32/webauthn/-webauthn-portal), [Windows Hello for Business / PIN local](https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/faq), [DPAPI `CryptProtectData`](https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata).

## STOP et gouvernance

**Aucun geste Windows opérateur :** l'unique profil `com.fabulaxiom.greenfield.v1` est conservé ; les bases SQLite originales v6/v7, la SQLite neuve hors Git, sidecars actifs, backups, ACL, journaux et marqueur restent intacts. Aucun PIN, compte, secret ou composant Windows Hello n'est utilisé dans les tests. Aucun ouvreur/CRUD/UX v7 réel, migration 007, IPC writer, restauration opérateur ni release. Archivage 5/5 seulement `OWNER_REPORTED_PASS` non indépendant.

M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; writer `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; #35 `OPEN/DRAFT`. Pour toute PR : deux prompts, handoffs MD+JSON, continuité/roadmap, issue #38 append-only, **CI Windows au HEAD exact**, revue du diff/reviews/threads et ruleset actif `Protect main`, squash `expected_head_sha` seulement après check requis terminal, CI postmain `push` indépendante et observation terminale #38. **Une authentification future ne promouvra aucun gate SQLite à elle seule.**
