import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
const dir='/ram/install-probe-reports';fs.mkdirSync(dir,{recursive:true});
const results=[];
for(const [name,tar]of [['base','/tmp/base.tar'],['candidate','/tmp/final-source.tar']]){
 const cwd='/ram/install-probe-'+name;fs.mkdirSync(cwd,{recursive:true});
 let p=spawnSync('tar',['-xf',tar,'-C',cwd]);if(p.status!==0)throw Error(String(p.stderr));
 if(fs.existsSync(cwd+'/package-lock.json')||fs.existsSync(cwd+'/node_modules'))throw Error('Not fresh');
 const env={...process.env,npm_config_cache:'/ram/install-probe-cache-'+name};delete env.npm_config_before;delete env.NPM_CONFIG_BEFORE;
 const out=fs.openSync(dir+'/'+name+'-npm-install.log','w');
 const start=new Date().toISOString();p=spawnSync('npm',['install'],{cwd,env,stdio:['ignore',out,out]});fs.closeSync(out);
 const result={name,command:'npm install',startedAt:start,finishedAt:new Date().toISOString(),code:p.status,node:process.version,emptyCache:true,noLock:true};results.push(result);fs.writeFileSync(dir+'/status.json',JSON.stringify(results,null,2));
 const ls=spawnSync('npm',['ls','--json','--all'],{cwd,env,encoding:'utf8'});fs.writeFileSync(dir+'/'+name+'-dependencies.json',ls.stdout);fs.writeFileSync(dir+'/'+name+'-dependencies.stderr.log',ls.stderr);result.dependencyTreeCode=ls.status;fs.writeFileSync(dir+'/status.json',JSON.stringify(results,null,2));
}
fs.writeFileSync(dir+'/done.json',JSON.stringify({results,finishedAt:new Date().toISOString()},null,2));
