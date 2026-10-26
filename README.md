# Repeated leading dot segment validation

Product commit: `8c3f11b200a5f54a543f4c513c558ae498cc2bf7`  
Base: `bfe4a68733806774da2cc7a558d3f017cc471db7`  
Source branch: `fix/repeated-leading-dot-segments`

Patterns such as `././root.txt` omit existing files through fast-glob's public sync, async and stream APIs. The two-file patch collapses redundant leading `./` segments to one before task preparation. Interior and parent segments remain intact, and a single prefix retains existing output formatting.

## Completed checks

- New official E2E cases: original production source 36 failed / 12 passed; candidate 48 passed. Separate native filesystem proof: baseline 24 failed / 24 passed, candidate 48 passed.
- Fresh standard `npm install` succeeds for canonical baseline and candidate with identical resolutions. Full build (TypeScript, ESLint, 288 unit tests) plus each configured API E2E suite passes on Linux Node 22.13.0, 22.23.4, 24.14.0 and 26.12.1, and native Windows Node 24.14.0. Each API reports 476 passed / 3 existing pending (1,428 / 9 total per runtime).
- All 15 configured Node26 benchmark commands completed with exact defaults of 100 warmups and 300 runs: 3 product, 9 regression (3 APIs × default/objectMode/absolute options), and 3 overhead. All 78 expected suites have start and finish records. Two commands ran concurrently; timing numbers are retained as raw measurements, not a claim of comparative performance improvement.
- The initial dependency workaround changed only lint-package versions relative to the recovered current plain install. All 393 other physical packages match versions, resolved URLs, integrity and all 12,273 package files. All 174 compiled files and all 15,259 fixture filesystem entries match. The long default benchmarks therefore use identical benchmark/runtime dependencies, compiled product code and glob-scanned paths; current lint packages were exercised by the fresh matrix.
- All 132 final canonical Git blobs/modes match before and after final Linux tests and benchmarks. Windows canonical source bytes match before and after its fresh gates. The frozen product source is retained across final runs; no dependency, workflow, snapshot or timeout changes are included in the patch.
- The exact 25,875-byte npm package has SHA256 `f310b714278332f5c77dd418aa63f193107c9a58545d516301bd89acb685be41`. All 59 files match independent Linux/Windows installs, which each pass all 48 public package-export native-filesystem cases. Fresh current-resolution packing reproduces the same archive byte-for-byte; the archive is included.

`FINAL-RECEIPT.json` records commands and gate bindings. `final-evidence/` contains actual default benchmark logs and completion receipts. `install-probe-reports/` and `windows-fresh-*` contain current standard-install gates. The local scripts retain their actual workspace paths and can be adapted to another checkout.

## Retained earlier attempts and limits

An initial plain install returned a registry tarball 404; subsequent fresh plain installs succeeded. Initial split E2E commands omitted the workflow's `SNAPSHOT_SKIP_PRUNING=1`, pruning 14 tracked snapshots; these results are excluded and canonical snapshots were restored before final tests. An initial final Windows sync run timed out in an existing Errors case; unchanged commands with the default timeout subsequently passed. The raw attempts and snapshot-byte audit are retained; no unsupported cause is asserted. The interrupted pre-freeze benchmark was excluded; all 15 final commands were run to completion.

macOS execution and hosted CodeQL were unavailable locally. The configured GitHub CI/Benchmark/CodeQL workflows can be checked after PR submission and are not represented as already passed here.

Only the explicit allowlist in `manifest.json` is published. Every copied input, output, archive, log and manifest retains its original bytes, including Windows CRLF. No path sanitization or newline normalization was applied; `sha256`, raw Git blob IDs and byte counts can be checked against the published files. `* -text` prevents Git from changing those bytes. No unrelated workspace files, caches, credentials or full parent directory were copied. AI assistance was used for implementation, review and validation; no human testing or approval is claimed.
