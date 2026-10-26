import pathlib,subprocess,json,hashlib,os,time,tarfile
r=pathlib.Path(__file__).parent;repo=r/'fresh-native-source';repo.mkdir()
with tarfile.open(r/'final-source.tar') as tar:tar.extractall(repo,filter='data')
head=(r/'final-head.txt').read_text().strip();expected=json.loads((r/'final-manifest.json').read_text());states=[];env=os.environ.copy();env['SNAPSHOT_SKIP_PRUNING']='1';env.pop('npm_config_before',None);env.pop('NPM_CONFIG_BEFORE',None)
def audit(label):
 actual=[]
 for e in expected:
  b=(repo/e['path']).read_bytes();actual.append({'path':e['path'],'blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
 assert len(actual)==132 and all(a['blob']==e['blob'] for a,e in zip(actual,expected))
 (r/('windows-fresh-'+label+'-manifest.json')).write_text(json.dumps({'head':head,'actual':actual},indent=2))
audit('before')
for args,label in [(['install'],'install'),(['run','build'],'build'),(['run','test:e2e:sync'],'sync'),(['run','test:e2e:async'],'async'),(['run','test:e2e:stream'],'stream')]:
 start=time.time()
 with (r/('windows-fresh-'+label+'.log')).open('wb') as out:p=subprocess.run(['cmd.exe','/d','/c','npm',*args],cwd=repo,env=env,stdout=out,stderr=subprocess.STDOUT)
 states.append({'head':head,'command':'npm '+' '.join(args),'code':p.returncode,'seconds':round(time.time()-start,2)});(r/'windows-fresh-summary.json').write_text(json.dumps(states,indent=2));print(states[-1],flush=True);assert p.returncode==0
audit('after')
tree=subprocess.run(['cmd.exe','/d','/c','npm','ls','--json','--all'],cwd=repo,env=env,capture_output=True);(r/'windows-fresh-dependencies.json').write_bytes(tree.stdout);(r/'windows-fresh-dependencies.stderr.log').write_bytes(tree.stderr);assert tree.returncode==0
(r/'windows-fresh-physical-lock.json').write_bytes((repo/'node_modules/.package-lock.json').read_bytes())
