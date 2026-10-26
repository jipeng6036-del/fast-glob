import pathlib,subprocess,tarfile,json,hashlib,datetime
r=pathlib.Path(__file__).parent
repo=pathlib.Path('F:/Github-PR/inspection/resume-20261026-js-fast-glob')
container='ghpr-resume-js-fastglob'
subprocess.run(['docker','exec',container,'tar','-C','/ram/final-evidence','-cf','/tmp/final-evidence-final.tar','.'],check=True)
subprocess.run(['docker','cp',container+':/tmp/final-evidence-final.tar',str(r/'final-evidence-final.tar')],check=True)
with tarfile.open(r/'final-evidence-final.tar') as tar:tar.extractall(r/'final-evidence',filter='data')
head=(r/'final-head.txt').read_text().strip();expected=json.loads((r/'final-manifest.json').read_text())
status=json.loads((r/'final-evidence/status.json').read_text());done=json.loads((r/'final-evidence/done.json').read_text())
assert done['head']==head and done['code']==0
assert status['head']==head
assert len(status['states'])==19 and all(s.get('code')==0 for s in status['states'])
assert sum(s['kind']=='configured-benchmark' for s in status['states'])==15
assert status['warmup']==100 and status['runs']==300
expected_bench_ids={kind+'-'+api for kind in ['product','overhead'] for api in ['async','stream','sync']}|{'regression-'+option+'-'+api for option in ['default','object','absolute'] for api in ['async','stream','sync']}
assert {s['id'] for s in status['states'] if s['kind']=='configured-benchmark'}==expected_bench_ids
benchmark_suites=0
for s in [s for s in status['states'] if s['kind']=='configured-benchmark']:
 text=(r/'final-evidence'/(s['id']+'.log')).read_text(encoding='utf8')
 kind=s['id'].split('-')[0];api=s['id'].split('-')[-1];task='bench:'+kind+':'+api
 assert 'unset WARMUP_COUNT RUNS_COUNT CONCURRENCY' in s['command']
 parts=['flatten','deep'] if kind=='overhead' else ['flatten','extension_flatten','deep','extension_deep','partial_flatten','partial_deep']
 for part in parts:
  assert text.count('Starting '+task+':'+part+'\n')==1,(s['id'],part)
  assert text.count('Finished '+task+':'+part+' in ')==1,(s['id'],part)
  benchmark_suites+=1
 assert 'Completed '+task+' in ' in text
assert benchmark_suites==78
for p in sorted((r/'final-evidence').glob('*-manifest.json')):
 actual=json.loads(p.read_text());assert actual['head']==head
 assert len(actual['actual'])==len(expected)
 assert all(a['blob']==e['blob'] and a['mode']==e['mode'] for a,e in zip(actual['actual'],expected)),p
for label in ['before','after']:
 actual=json.loads((r/f'windows-final-v2-{label}-manifest.json').read_text());assert actual['head']==head
 assert len(actual['actual'])==len(expected)
 assert all(a['blob']==e['blob'] for a,e in zip(actual['actual'],expected))
windows=json.loads((r/'windows-final-v2-summary.json').read_text());assert len(windows)==3 and all(s['code']==0 for s in windows)
windows_build=json.loads((r/'windows-final-summary.json').read_text())[0];assert windows_build['command']=='npm run build' and windows_build['code']==0
for name in ['fastglob-packed-proof.json','windows-packed-proof.json']:
 proof=json.loads((r/name).read_text());assert proof['passed']==48 and proof['failed']==0
for name in ['package-final-audit.json','windows-package-final-audit.json']:
 audit=json.loads((r/name).read_text());assert audit['head']==head and not audit['wrong'] and len(audit['installed'])==59
fresh=r/'install-probe-reports'
fresh_install=json.loads((fresh/'status.json').read_text());assert len(fresh_install)==2 and all(s['code']==0 and s['noLock'] and s['emptyCache'] for s in fresh_install)
fresh_linux=json.loads((fresh/'fresh-matrix-status.json').read_text());assert len(fresh_linux)==4 and all(s['code']==0 for s in fresh_linux)
for p in fresh.glob('fresh-*-manifest.json'):
 actual=json.loads(p.read_text());assert actual['head']==head and len(actual['actual'])==132
 assert all(a['blob']==e['blob'] and a['mode']==e['mode'] for a,e in zip(actual['actual'],expected))
byte_audit=json.loads((fresh/'benchmark-dependencies-byte-audit.json').read_text());assert not byte_audit['wrong'] and byte_audit['unchangedPackages']==393 and byte_audit['comparedFiles']==12273
compiled=json.loads((fresh/'fresh-compiled-comparison.json').read_text());assert not compiled['diff'] and compiled['files']==174
fixture_tree=json.loads((fresh/'benchmark-fixture-tree-comparison.json').read_text());assert not fixture_tree['diff'] and fixture_tree['oldEntries']==fixture_tree['freshEntries']==15259
fresh_proof=json.loads((fresh/'fresh-proof-done.json').read_text());assert fresh_proof['head']==head and fresh_proof['code']==0
windows_fresh=json.loads((r/'windows-fresh-summary.json').read_text());assert len(windows_fresh)==5 and all(s['code']==0 for s in windows_fresh)
for label in ['before','after']:
 actual=json.loads((r/f'windows-fresh-{label}-manifest.json').read_text());assert actual['head']==head and len(actual['actual'])==132
 assert all(a['blob']==e['blob'] for a,e in zip(actual['actual'],expected))
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==head
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo,text=True).strip()
subprocess.run(['git','diff','--check','HEAD^','HEAD'],cwd=repo,check=True)
hashes=[]
for p in sorted((r/'final-evidence').iterdir()):
 if p.is_file():hashes.append({'path':'final-evidence/'+p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
report={'head':head,'base':'bfe4a68733806774da2cc7a558d3f017cc471db7','collectedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceFiles':len(expected),'linuxHistoricalResolutionAndDefaultBenchmarks':status,'freshStandardInstall':fresh_install,'freshLinuxGates':fresh_linux,'freshWindowsGates':windows_fresh,'benchmarkDependencyEquivalence':{k:v for k,v in byte_audit.items() if k!='matched'},'compiledEquivalence':compiled,'windowsHistoricalResolutionBuild':windows_build,'windowsHistoricalResolutionE2E':windows,'packageSha256':'f310b714278332f5c77dd418aa63f193107c9a58545d516301bd89acb685be41','packageFiles':59,'realFsPackageCases':{'Linux26':48,'Windows24':48},'initialWindowsFinalTimeout':'Retained in windows-final-test-e2e-sync.log; exact unchanged default-timeout rerun passed; cause not established.','localMacOS':'not available; upstream CI only','evidence':hashes}
(r/'FINAL-RECEIPT.json').write_text(json.dumps(report,indent=2));print(json.dumps({'head':head,'configuredBenchmarksPassed':15,'linuxRuntimesPassed':4,'windowsPassed':True,'files':len(expected),'evidenceFiles':len(hashes)}))
