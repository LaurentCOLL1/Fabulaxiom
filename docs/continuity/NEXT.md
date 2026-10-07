# Fabulaxiom — Next Authorized Work

## Immediate objective

Merge and normalize completed M0.

## M0

**COMPLETE**

Terminal qualified implementation SHA:

`6fbea03be2b6058aa14d1cddcaffc7f840ebf81c`

Terminal deterministic CI:

- workflow: `M0 CI`;
- run: `37561269046`;
- conclusion: `success`.

## Required sequence

1. run exact-head CI on this completion-documentation commit;
2. if and only if it is fully successful, mark PR #2 ready;
3. re-fetch PR #2 and verify exact head/mergeability;
4. merge PR #2 using expected-head protection;
5. re-fetch live `main`;
6. create post-merge continuity normalization;
7. run exact-head CI for normalization;
8. merge normalization;
9. re-fetch live `main`;
10. only then authorize M1.

## M1

**NOT AUTHORIZED YET**

Do not yet add:

- SQLite persistence;
- Universe/Series/Novel/Chapter/Scene CRUD;
- text version history;
- backup/restore;
- manuscript generation;
- vector search;
- rich-text editor.
