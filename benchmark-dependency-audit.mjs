import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
const old='/ram/candidate',fresh='/ram/install-probe-candidate',report='/ram/install-probe-reports';
const a=JSON.parse(fs.readFileSync(old+'/node_modules/.package-lock.json')),b=JSON.parse(fs.readFileSync(fresh+'/node_modules/.package-lock.json'));
const identity=x=>x&&{version:x.version,resolved:x.resolved,integrity:x.integrity};
const changed=Object.keys({...a.packages,...b.packages}).filter(k=>JSON.stringify(identity(a.packages[k]))!==JSON.stringify(identity(b.packages[k])));
if(changed.some(p=>!p.startsWith('node_modules/@typescript-eslint/')&&!['node_modules/typescript-eslint','node_modules/baseline-browser-mapping'].includes(p)))throw Error('Non-lint dependency changed');
const matched=[];const wrong=[];
for(const pkg of Object.keys(a.packages).filter(k=>!changed.includes(k))){
 const walk=(dir)=>{for(const name of fs.readdirSync(old+'/'+dir)){if(name==='node_modules')continue;const p=dir+'/'+name,one=old+'/'+p,two=fresh+'/'+p,s=fs.lstatSync(one);if(s.isDirectory()){walk(p);continue;}const x=s.isSymbolicLink()?Buffer.from(fs.readlinkSync(one)):fs.readFileSync(one),y=fs.lstatSync(two).isSymbolicLink()?Buffer.from(fs.readlinkSync(two)):fs.readFileSync(two);if(!x.equals(y))wrong.push(p);matched.push({path:p,sha256:crypto.createHash('sha256').update(x).digest('hex')});}};
 walk(pkg);
}
const result={head:fs.readFileSync('/tmp/final-head.txt','utf8').trim(),totalPackages:Object.keys(a.packages).length,unchangedPackages:Object.keys(a.packages).length-changed.length,changedLintPackages:changed,comparedFiles:matched.length,wrong,matched};fs.writeFileSync(report+'/benchmark-dependencies-byte-audit.json',JSON.stringify(result,null,2));console.log(JSON.stringify({...result,matched:undefined}));if(wrong.length)process.exitCode=1;
