OFFLINE TRANSIT
1. Host this folder over HTTPS once (GitHub Pages, Netlify, or any static host). Service workers don't run from file://.
2. Open it on your phone, then "Add to Home Screen" (iOS: Share > Add to Home Screen; Android: menu > Install app).
3. Open it once while online - everything is cached and works offline after that.
Adding a line: drop its JSON into data/lines/, run `python3 build_manifest.py`, and bump CACHE name ('transit-v1') in sw.js.
