# Offline Transit

Vibe-coded personal project.
A phone-first Progressive Web App (PWA) for offline of browsing public transport schedules. Data is from Municipal Transport Ruse (https://transport-ruse.com/)
View the app here: https://yavor42.github.io/offline-schedules/

## Features

- **Route search** - Browse lines by direction.
- **Station search** - Find stops by name, number, aliases, or Bulgarian and English spellings.
- **Upcoming departures** - View departure times and countdowns, with filtering, sorting, and favourites.
- **Interactive transit map** — Offline map of the transport network.
- **Service updates** - Display notices, cancellations, reduced or additional services, diversions, and temporary special lines.
- **Delay warnings** - Flag departures that may be delayed because of short turnaround times.
- **Vehicle tracking (experimental)** — Estimate where a vehicle should be along its route by calculating its progress from scheduled departure times and stop-to-stop travel durations. This is schedule-based estimation, not live GPS tracking.
- **English and Bulgarian interfaces** - Switch languages directly in the app. (some translations may be missing)
- **Offline support** - Cache the application, schedules, and map for use without mobile data.
- **Installable PWA** - Add the app to your phone's home screen.

## Getting Started

1. Host the repository using GitHub Pages (or over HTTPS).
2. Open the published URL while online.
3. Allow the app to load and cache its files.
4. Add it to your phone's home screen.
5. Open it whenever you need to check transit schedules, including offline.

## Project Structure

- `index.html` - Application interface and logic.
- `sw.js` - Service worker and offline caching.
- `manifest.webmanifest` - PWA configuration.
- `data/manifest.json` - Lists the route files to load.
- `data/stations/` - Station information.
- `data/lines/` - Routes, stops, travel durations, and schedules.
- `data/notices.json` - Service notices and schedule overrides.
- `data/modifications.json` - Cancellations, additional services, diversions, and special lines.
- `data/lang_bg.json` - Bulgarian interface translations.
- `data/aliases.json` - Search synonyms.
- `tiles/` and `lib/` - Offline map tiles and Leaflet assets.

## Data and Updates

Schedules and station information are maintained in JSON files. Optional notices, service modifications, translations, and search aliases can be updated independently.
When changing the application HTML, update the service-worker cache version in `sw.js` so installed devices can receive the latest version.

## Limitations

Vehicle positions are estimated from published schedules and configured travel durations, not obtained from live vehicle GTFS. Accuracy depends on the quality of the schedule data and actual traffic conditions.
