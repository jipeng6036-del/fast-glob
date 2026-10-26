import hashlib,json,pathlib,re,shutil,subprocess
r=pathlib.Path(__file__).parent;dest=r/'public-proof';dest.mkdir(exist_ok=True)
receipt=json.loads((r/'FINAL-RECEIPT.json').read_text());head=receipt['head'];assert head=='8c3f11b200a5f54a543f4c513c558ae498cc2bf7'
allow=[
 'FINAL-RECEIPT.json','FINAL-CHECKLIST.md','final-head.txt','final-manifest.json','codeql-availability.json',
 'fast-glob-4.0.0.tgz','package-final-audit.json','windows-package-final-audit.json',
 'fastglob-baseline-dot.json','fastglob-candidate-dot.json','fastglob-packed-proof.json','windows-packed-proof.json',
 'fastglob-baseline-dot-regression.log','fastglob-candidate-dot-regression.log','fastglob-install.log','fastglob-install-before.log',
 'fastglob-source-and-package-verification.json','fastglob-base-manifest.json','invalid-snapshot-pruning-audit.json',
 'fastglob-linux-matrix.json','fastglob-linux-22.13.0-full.log','fastglob-linux-22.23.4-full.log','fastglob-linux-24.14.0-full.log',
 'windows-final-summary.json','windows-final-build.log','windows-final-test-e2e-sync.log','windows-final-v2-summary.json',
 'windows-final-v2-before-manifest.json','windows-final-v2-after-manifest.json',
 'windows-fresh-summary.json','windows-fresh-before-manifest.json','windows-fresh-after-manifest.json','windows-fresh-dependencies.json','windows-fresh-physical-lock.json',
 'recover-runner.mjs','fresh-install-probe.mjs','fresh-matrix.mjs','fresh-proof.mjs','benchmark-dependency-audit.mjs',
 'fastglob-dot-proof.mjs','fastglob-packed-proof.mjs','freeze.py','collect-final.py','windows-final.py','windows-final-v2.py','windows-fresh.py','prepare-raw-proof.py',
 'fast-glob-258-files.json','fast-glob-402-files.json',
]
allow += ['windows-final-v2-test-e2e-'+api+'.log' for api in ['sync','async','stream']]
allow += ['windows-fresh-'+label+'.log' for label in ['install','build','sync','async','stream']]
bench_ids=[kind+'-'+api for kind in ['product','overhead'] for api in ['async','stream','sync']]+['regression-'+option+'-'+api for option in ['default','object','absolute'] for api in ['async','stream','sync']]
allow += ['final-evidence/'+name+'.log' for name in bench_ids]
allow += ['final-evidence/linux-'+version+'.log' for version in ['22.13.0','22.23.4','24.14.0','26.12.1']]
allow += ['final-evidence/'+name+'-manifest.json' for name in ['before','after-22.13.0','after-22.23.4','after-24.14.0','after-26.12.1','after-benchmarks']]
allow += ['final-evidence/status.json','final-evidence/done.json']
fresh_names=['base-dependencies.json','base-npm-install.log','candidate-dependencies.json','candidate-npm-install.log','status.json','done.json','benchmark-dependencies-byte-audit.json','benchmark-fixture-tree-comparison.json','fresh-before-manifest.json','fresh-base-native-proof.json','fresh-base-native-proof.log','fresh-baseline-build.log','fresh-baseline-source-audit.json','fresh-candidate-native-proof.json','fresh-candidate-native-proof.log','fresh-compiled-comparison.json','fresh-matrix-done.json','fresh-matrix-status.json','fresh-pack.json','fresh-proof-done.json','fresh-physical-lock.json','historical-physical-lock.json','physical-lock-comparison.json','resolution-comparison.json']
fresh_names += ['fresh-after-'+v+'-manifest.json' for v in ['22.13.0','22.23.4','24.14.0','26.12.1']]
fresh_names += ['fresh-linux-'+v+'.log' for v in ['22.13.0','22.23.4','24.14.0','26.12.1']]
allow += ['install-probe-reports/'+name for name in fresh_names]
remote_names=['repository-open-prs.json','default-tree.json','policy-.github__CONTRIBUTING.md','policy-.github__PULL_REQUEST_TEMPLATE.md','summary.json','semantic-disposition.json','freshness-before-publication.json','history-repeated.json','history-leading.json','history-dot-segments.json']
remote_names += ['owner-default-'+name+'-error.txt' for name in ['CONTRIBUTING.md','.github__CONTRIBUTING.md','AI_POLICY.md','AGENTS.md']]
remote_names += ['open-pr-'+str(n)+'-files.json' for n in [374,393,460,508,514,516,517,523,526,527,529,531,536,537,539,540,541]]
allow += ['final-remote-gates/'+name for name in remote_names]
assert len(allow)==len(set(allow))
(r/'proof-allowlist.json').write_text(json.dumps(allow,indent=2),encoding='utf8',newline='\n')
files={}
for name in allow:
 source=r/name;assert source.is_file() and source.resolve().is_relative_to(r.resolve())
 raw=source.read_bytes()
 if source.suffix!='.tgz':assert not re.search(rb'(?<![A-Za-z0-9])(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|sk-(?:proj-)?[A-Za-z0-9_-]{20,})',raw),name
 target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);assert target.read_bytes()==raw
 files[name]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'mode':'100644'}
readme=f'''# Repeated leading dot segment validation

Product commit: `{head}`  
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
'''
for name,raw in [('README.md',readme.encode()),('.gitattributes',b'* -text\n')]:
 (dest/name).write_bytes(raw);files[name]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'mode':'100644'}
manifest={'productHead':head,'productTree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd='F:/Github-PR/inspection/resume-20261026-js-fast-glob',text=True).strip(),'base':receipt['base'],'packageSha256':receipt['packageSha256'],'allowlist':allow,'bytePolicy':'All copied files retain exact original bytes; no sanitization or newline normalization. Manifest excludes its own hash.','files':files}
(dest/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8',newline='\n')
print(json.dumps({'files':len(files)+1,'bytes':sum(p.stat().st_size for p in dest.rglob('*') if p.is_file()),'directory':str(dest)}))
