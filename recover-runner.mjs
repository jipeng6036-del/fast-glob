import fs from 'node:fs';
import crypto from 'node:crypto';
import {spawn, spawnSync} from 'node:child_process';
const root='/ram/candidate', report='/ram/final-evidence';
fs.mkdirSync(report,{recursive:true});
const expected=JSON.parse(fs.readFileSync('/tmp/final-manifest.json','utf8'));
const head=fs.readFileSync('/tmp/final-head.txt','utf8').trim();
function verify(label){
 const actual=expected.map(e=>{const p=root+'/'+e.path,s=fs.lstatSync(p),b=s.isSymbolicLink()?Buffer.from(fs.readlinkSync(p)):fs.readFileSync(p);return {path:e.path,mode:s.isSymbolicLink()?'120000':(s.mode&0o111)?'100755':'100644',blob:crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex'),sha256:crypto.createHash('sha256').update(b).digest('hex')};});
 fs.writeFileSync(report+'/'+label+'-manifest.json',JSON.stringify({head,actual},null,2));
 const wrong=actual.filter((e,i)=>e.mode!==expected[i].mode||e.blob!==expected[i].blob);
 if(wrong.length)throw new Error('Source mismatch '+JSON.stringify(wrong));
}
let states=[];
function save(){fs.writeFileSync(report+'/status.json',JSON.stringify({head,updatedAt:new Date().toISOString(),warmup:100,runs:300,states},null,2));}
async function command(id,cmd,extra={}){
 const entry={id,command:cmd,startedAt:new Date().toISOString(),...extra};states.push(entry);save();
 const out=fs.openSync(report+'/'+id+'.log','w');
 const code=await new Promise((resolve,reject)=>{const child=spawn('/bin/sh',['-c',cmd],{cwd:root,env:{...process.env,SNAPSHOT_SKIP_PRUNING:'1'},stdio:['ignore',out,out]});child.on('error',reject);child.on('close',resolve);});
 fs.closeSync(out);entry.code=code;entry.finishedAt=new Date().toISOString();save();return code;
}
try{
 verify('before');
 // Preserve the interrupted run, but wait for its exact process before rebuilding.
 while(fs.existsSync('/proc/836'))await new Promise(r=>setTimeout(r,1000));
 for(const [version,bin] of [['22.13.0','/ram/node22min/node_modules/node/bin'],['22.23.4','/ram/runtime22/bin'],['24.14.0','/ram/runtime24/bin'],['26.12.1','/usr/local/bin']]){
  const cmd=`export PATH=${bin}:$PATH; node --version; npm run build && npm run test:e2e:sync && npm run test:e2e:async && npm run test:e2e:stream`;
  if(await command('linux-'+version,cmd,{version,kind:'configured-ci'}))throw new Error('Matrix failure '+version);
  verify('after-'+version);
 }
 const queue=[];
 for(const api of ['async','stream','sync'])queue.push({id:'product-'+api,script:'bench:product:'+api,options:null});
 for(const [name,options]of [['default','{}'],['object','{"objectMode":true}'],['absolute','{"absolute":true}']])for(const api of ['async','stream','sync'])queue.push({id:'regression-'+name+'-'+api,script:'bench:regression:'+api,options});
 for(const api of ['async','stream','sync'])queue.push({id:'overhead-'+api,script:'bench:overhead:'+api,options:null});
 async function worker(){while(queue.length){const item=queue.shift();const cmd=(item.options===null?'unset BENCHMARK_OPTIONS; ':`export BENCHMARK_OPTIONS='${item.options}'; `)+`unset WARMUP_COUNT RUNS_COUNT CONCURRENCY; node --run ${item.script}`;await command(item.id,cmd,{kind:'configured-benchmark',options:item.options});}}
 await Promise.all([worker(),worker()]);
 verify('after-benchmarks');
 fs.writeFileSync(report+'/done.json',JSON.stringify({head,code:states.every(s=>s.code===0)?0:1,finishedAt:new Date().toISOString()},null,2));
}catch(error){fs.writeFileSync(report+'/error.json',JSON.stringify({head,error:String(error),stack:error.stack},null,2));process.exitCode=1;}
