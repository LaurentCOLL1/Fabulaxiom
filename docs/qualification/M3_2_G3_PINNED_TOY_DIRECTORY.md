# M3.2 G3 — Win32 pinned toy-directory handle, namespace negatives

**DRAFT — SYNTHETIC-ONLY EXPERIMENT. NO OPERATOR FILE PERMISSION.**

Starting from protected \`main=5c8c8f11f23a6dda105ffdea267fdef61ae3a143\`, PR #45 is merged with terminal exact-head Windows CI #38926252403 **27/27 PASS, 15/15 toy tests**. It reads a disposable toy SQLite using a single held Win32 source handle and validates the physical image via SQLite RAM deserialization.

## Additional fixture controls in this PR

A separate directory HANDLE is opened via \`CreateFileW(FILE_READ_ATTRIBUTES, FILE_SHARE_READ | FILE_SHARE_WRITE, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT)\` on the disposable **temporary fixture root** only. Since \`FILE_SHARE_DELETE\` is omitted, Windows should deny new rename/delete opens on the pinned directory while this handle is held. The fixture obtains a volume/file-index identity from \`GetFileInformationByHandle\` and compares it to a separate temporary handle lookup of the toy root path before and after reading. The source HANDLE from PR #45 remains open for the entire physical byte read and in-memory SQLite audit. This PR adds fixture negatives for renaming the pinned toy directory, renaming a held source file, injected directory path identity mismatch, symlink fixtures, journal sentinels and writer conflicts. CI runs on Windows only.

**Not established even if 13/13 tests pass:** This pins only the toy directory, *not all of the real path's ancestors*. The check-then-open of a final source path still has a race if an ancestor above the pinned directory is swapped. Same-user adversarial rename mechanisms, filters, hard links, network FS and ACL or reparse mutation are not comprehensively covered. Directory/file IDs are local observations, not an independent attestation of a historic source. No guarantee exists for live SQLite without full journal and writer handling.

The fixture test does not create a real prospective destination, merge G3 with G4, touch protected original v6/v7, change an activation marker, migrate production 007, or expose writer IPC. The tested file naming and root constraints are **not** secure authentication of arbitrary operator paths; the CLI accepts only \`--self-test\`.

## Next barriers

Before **any** real G3, separately prove actual Windows custody source identity/ACL (including all ancestor handles and no reparse/rename races), writer quiescence, source consistency and a new-only destination directory/file with a private manifest. Then an operator-specific, disclosed Windows runbook needs distinct approval. Until such proof, \`prospective=NOT_STARTED\`, \`historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)\`, PR #35 OPEN/DRAFT, and actual G3/G4/G5/G6 NOT_AUTHORIZED.

Documentation: https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew ; https://learn.microsoft.com/en-us/windows/win32/fileio/obtaining-a-handle-to-a-directory ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandle ; https://www.sqlite.org/lockingv3.html .
