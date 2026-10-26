import pathlib,subprocess,json,tarfile,io,hashlib
r=pathlib.Path(__file__).parent
repo=pathlib.Path('F:/Github-PR/inspection/resume-20261026-js-fast-glob')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
(r/'final-head.txt').write_text(head)
entries=[]
with tarfile.open(r/'final-source.tar','w') as tar:
 for row in subprocess.check_output(['git','ls-tree','-r','HEAD'],cwd=repo,text=True).splitlines():
  meta,name=row.split('\t',1);mode,kind,blob=meta.split();data=subprocess.check_output(['git','cat-file','blob',blob],cwd=repo)
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
  e={'path':name,'mode':mode,'blob':blob,'sha256':hashlib.sha256(data).hexdigest()};entries.append(e)
  info=tarfile.TarInfo(name);info.mode=int(mode[-3:],8);info.size=len(data)
  if mode=='120000':info.type=tarfile.SYMTYPE;info.linkname=data.decode();info.size=0
  tar.addfile(info,io.BytesIO(data) if mode!='120000' else None)
(r/'final-manifest.json').write_text(json.dumps(entries,indent=2))
print(json.dumps({'head':head,'files':len(entries),'tar_sha256':hashlib.sha256((r/'final-source.tar').read_bytes()).hexdigest()}))
