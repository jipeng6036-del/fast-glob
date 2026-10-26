import pathlib,subprocess,json,hashlib,os,time
r=pathlib.Path(__file__).parent
repo=pathlib.Path('F:/Github-PR/inspection/resume-20261026-js-fast-glob')
head=(r/'final-head.txt').read_text().strip()
manifest=json.loads((r/'final-manifest.json').read_text())
def verify(label):
 actual=[]
 for e in manifest:
  b=(repo/e['path']).read_bytes();actual.append({'path':e['path'],'blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()})
 (r/('windows-final-'+label+'-manifest.json')).write_text(json.dumps({'head':head,'actual':actual},indent=2))
 wrong=[e for e,w in zip(actual,manifest) if e['blob']!=w['blob']]
 assert not wrong,wrong
verify('before');states=[];env=os.environ.copy();env['SNAPSHOT_SKIP_PRUNING']='1'
for name in ['build','test:e2e:sync','test:e2e:async','test:e2e:stream']:
 start=time.time()
 with (r/('windows-final-'+name.replace(':','-')+'.log')).open('wb') as out:
  p=subprocess.run(['cmd.exe','/d','/c','npm','run',name],cwd=repo,env=env,stdout=out,stderr=subprocess.STDOUT)
 states.append({'head':head,'command':'npm run '+name,'code':p.returncode,'seconds':round(time.time()-start,2)})
 (r/'windows-final-summary.json').write_text(json.dumps(states,indent=2));print(states[-1],flush=True)
 assert p.returncode==0
verify('after')
