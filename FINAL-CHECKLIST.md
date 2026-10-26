# Fast-glob repeated leading dot segments

- Checkout: `F:/Github-PR/inspection/resume-20261026-js-fast-glob`
- Upstream baseline: `bfe4a68733806774da2cc7a558d3f017cc471db7`
- Frozen candidate: `8c3f11b200a5f54a543f4c513c558ae498cc2bf7`
- Branch: `fix/repeated-leading-dot-segments`
- Scope: normalize 2+ leading `./` segments to one during task preparation. The supported public sync, async and stream APIs otherwise omit existing files for `././root.txt` and corresponding dynamic patterns.
- Two changed files, 46 additions / 2 deletions. No package declarations, dependencies, workflow or snapshots changed.

## Completed evidence

- All 132 canonical Git blobs and modes verified against the actual Linux candidate before and after every final configured runtime run. Frozen tar is made from `git cat-file` bytes (not `git archive` and not checkout transformations).
- Final Linux 22.13.0 / 22.23.4 / 24.14.0 / 26.12.1 each: `npm run build` and each configured sync / async / stream E2E command passed. 288 unit; each API 476 passed and 3 existing pending.
- Native filesystem comparison: unchanged production source 24 failed / 24 passed, candidate 48 passed. Official added E2E tests against unchanged production source: 36 failed / 12 passed; candidate 48 passed.
- Native Windows Node24.14.0 final build passed (288 unit); unchanged default-timeout sync / async / stream E2E rerun passed, each 476 passing / 3 existing pending. All 132 canonical source files matched before and after the rerun. Initial final sync attempt timed out in an existing Errors case; that attempt is retained and its cause was not established.
- Candidate npm tarball SHA256 `f310b714278332f5c77dd418aa63f193107c9a58545d516301bd89acb685be41`, 25,875 bytes. All 59 packaged files match independently installed Linux and Windows package files. Public package-export real-filesystem reproduction: 48 passed on Linux Node26.12.1 and Windows Node24.14.0.
- Baseline/candidate use the same compatible dependency tree. Unconstrained registry install initially failed on a missing tarball; exact failure logs retained. `npm install --before=2026-10-25T00:00:00Z` recovered within existing version declarations; no dependency or lockfile change is in the patch.
- Standard plain `npm install` later recovered. Separate canonical baseline and candidate source probes, with no preexisting lock/modules and empty caches, both succeeded with identical 793-path dependency trees. All four Linux runtime gates and native Windows24 plain-install/build/full E2E gates subsequently passed in fresh current-resolution environments. The fresh baseline retains all 131 original source blobs, and fresh candidate all 132 final blobs/modes.
- The current resolution changes only 12 lint packages. Other 393 physical packages retain version/resolved URL/integrity and all 12,273 actual package files match the running benchmark environment byte-for-byte. All 174 compiled output files match, and fresh packing reproduces the identical candidate tarball hash. Benchmark/runtime/compiler/test tools and compiled code are therefore unchanged; current lint packages were exercised by the fresh matrix.

## Final pre-publication result

- All 15 unconditional `.github/workflows/benchmark.yml` commands under Node26 finished with exit0, exact default 100 warmups and 300 runs, no reduced counts. Product 3 APIs; regression 3 APIs × `{}`, `objectMode:true`, `absolute:true`; overhead 3 APIs. All 78 expected suites have matching start/finish records. Raw logs, status/done and canonical post-run manifests are exported to `final-evidence/` and validated by `collect-final.py`.
- `FINAL-RECEIPT.json` validates all local requirements and exact clean HEAD. Root and a separate reviewer found no source or policy blocker. Fresh full upstream body/comment/file-patch review covered all 17 open PRs / 58 file patches, and the 18:24:21Z final query confirms unchanged upstream base, PR heads, bodies and comments. No overlap or claim was found.
- Local macOS execution is unavailable; only post-PR upstream CI can execute that OS. No local macOS claim.
- Configured CodeQL uses `github/codeql-action@v4` on the pull-request event with hosted security-event permissions. Local `codeql` CLI is unavailable (`codeql-availability.json`); hosted CodeQL and the full hosted OS matrix can only be checked after PR creation. They are not claimed as locally passed.

## Retained invalid or incomplete attempts

- Initial split E2E runs omitted the configured `SNAPSHOT_SKIP_PRUNING=1` and pruned 14 tracked snapshot files. The pre-correction tar and initial results are retained, excluded from final gates. Canonical snapshots were restored from Git blobs before final testing, and every final runtime source audit is clean.
- Initial registry 404 and initial Windows final sync timeout remain historical attempts. Fresh standard installs succeeded, and all fresh Linux/Windows gates passed with unchanged source and default timeouts. No failure was erased or attributed to a proven cause without evidence.
- Pre-interruption product async benchmark survived as an orphaned Docker exec, but its host log was incomplete and no command receipt survived. It is historical incomplete evidence, excluded from final gates; the final runner waited for that exact process to finish before rebuilding and starts all 15 commands afresh.
