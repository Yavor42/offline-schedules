const C='transit-v12';
self.addEventListener('install',e=>{e.waitUntil((async()=>{
  const c=await caches.open(C);
  await c.addAll(['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./lib/leaflet.js','./lib/leaflet.css','./data/manifest.json']);
  const m=await (await fetch('./data/manifest.json',{cache:'no-store'})).json();
  await c.addAll(['./data/'+m.stations,...m.lines.map(f=>'./data/lines/'+f)]);
  await Promise.all(['./OTP.png'].map(u=>c.add(u).catch(()=>{}))); // optional logo; don't fail install if missing
  try{const r=await fetch('./tiles/meta.json',{cache:'no-store'});if(r.ok){const t=await r.json();await c.addAll(['./tiles/meta.json',...t.files.map(f=>'./tiles/'+f)])}}catch(e){} // map tiles (optional)
  self.skipWaiting();})())});
self.addEventListener('activate',e=>e.waitUntil((async()=>{
  for(const k of await caches.keys())if(k!==C)await caches.delete(k);
  await clients.claim();})()));
// cache-first, refresh in background when online
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;
  e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(hit=>{
    const net=fetch(e.request).then(r=>{if(r.ok)caches.open(C).then(c=>c.put(e.request,r.clone()));return r}).catch(()=>hit);
    return hit||net;}))});
