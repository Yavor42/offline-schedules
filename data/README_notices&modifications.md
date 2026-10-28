# Notices and Modifications - Data Format

(AI generated and human reviewed!)
This document explains how to structure `data/notices.json` and `data/modifications.json` for the Offline Transit (OTP) application.

Both files are optional. If a file is missing, its feature remains disabled. Updates are checked at startup, when the tab becomes visible, and approximately every five minutes. The service worker uses network-first caching, with a cached copy available offline.

## 1. Notices (`data/notices.json`)

Notices communicate information to passengers and can optionally override the schedule type.

### Structure

```json
{
  "updatedAt": "2026-10-26",
  "notices": [
    {
      "id": "notice1",
      "type": "INFORMATION",
      "forDev": false,
      "title": "Service information",
      "message": "Please check your departure time.",
      "titleBG": "",
      "messageBG": "",
      "validityPeriod": {
        "start": {
          "year": 2026,
          "month": 10,
          "day": 28,
          "hour": 8,
          "minute": 0
        },
        "end": {
          "year": 2026,
          "month": 10,
          "day": 28,
          "hour": 18,
          "minute": 0
        }
      },
      "affectedEntities": {
        "lineID": ["T2"]
      }
    }
  ]
}
```

### Fields

| Field | Description |
|---|---|
| `updatedAt` | Informational timestamp; ignored by the app. |
| `id` | Identifier used in error messages. |
| `type` | Notice type. |
| `forDev` | Developer-related metadata; ignored by the app. |
| `title`, `message` | English title and message. The message may be empty. |
| `titleBG`, `messageBG` | Optional Bulgarian translations. Each field independently falls back to English when empty or missing. |
| `validityPeriod` | Start and end date/time, using the device's local time. |
| `affectedEntities` | Defines which lines, directions, stations, or vehicle categories the notice affects. |
| `overrideScheduleType` | Used by `SCHEDULE_OVERRIDE` notices: `"workday"` or `"holiday"`. |

The end minute is inclusive.

### Notice types

- `INFORMATION` — Blue informational banner.
- `FREE_TRANSIT` — Dark green free-transit banner.
- `SCHEDULE_OVERRIDE` — Amber banner that can change the timetable type while valid.

Unknown types are ignored.

### Affected entities

The following fields accept arrays of IDs:

- `stationID`, `excludeStationID`
- `directionID`, `excludeDirectionID`
- `lineID`, `excludeLineID`

An inclusion list containing `"*"` matches everything. Exclusion lists cannot contain `"*"`.

Additional boolean filters:

- `municipalOnly` — Buses and trolleybuses.
- `busOnly` — Buses.
- `trolleybusOnly` — Trolleybuses.
- `intercityOnly` — Lines of type `intercity`. (none exist of this type at the moment)
- `specialOnly` — Special lines.

Inclusion criteria are combined as a union, and exclusions are then subtracted. An exclusion without an inclusion applies to everything except the excluded entities. A station exclusion takes precedence at that station.

Notices can appear on station screens, line/direction selection screens, and trip screens.

### Validity and schedule overrides

Notices begin appearing **three days before their start time**, with a “Starts” label. They disappear after their validity ends.

A `SCHEDULE_OVERRIDE` changes affected directions to the specified workday or holiday timetable only during the actual validity period, not during the three-day advance-notice period.

- A manually selected Workday or Holiday schedule takes precedence.
- If multiple overrides overlap, the first matching entry in the file wins.
- Station-only overrides do not change schedules.

Invalid validity periods or conflicting entity filters can prevent a notice from displaying. Problems are reported on the home screen and in the console.

---

## 2. Modifications (`data/modifications.json`)

Modifications describe actual changes to the service. They can alter departures, routes, or the available lines.

### Structure

```json
{
  "modifications": [
    {
      "id": "modification1",
      "type": "CANCELLATION",
      "forDev": false,
      "title": "Cancelled service",
      "message": "This service will not operate.",
      "titleBG": "",
      "messageBG": "",
      "validityPeriod": {
        "start": {
          "year": 2026,
          "month": 10,
          "day": 28,
          "hour": 8,
          "minute": 0
        },
        "end": {
          "year": 2026,
          "month": 10,
          "day": 28,
          "hour": 18,
          "minute": 0
        }
      },
      "affectedEntities": {
        "A28": {}
      }
    }
  ]
}
```

Each modification is an entry in the `modifications` array. The common fields follow the same conventions as notices.

### Modification types

| Type | Effect |
|---|---|
| `REDUCED_SERVICE` | Cancels specified scheduled departures. |
| `ADDITIONAL_SERVICE` | Adds departures to an existing direction. |
| `CANCELLATION` | Cancels every departure on a line or direction during the validity period. |
| `DIVERSION` | Changes the stops and travel durations along a route. |
| `SPECIAL` | Creates a temporary special line with its own stops and schedules. |

Type matching is case-insensitive; spaces and hyphens are treated as underscores. `SPECIAL_LINE` is also accepted.

### 2.1 Reduced service

The affected direction maps to departure times for each schedule type.

```json
{
  "directionId": {
    "workday": ["05:45", "06:20", "07:10"],
    "holiday": ["06:00"]
  }
}
```

The times must already exist in the base schedule. Matching departures are retained but marked as cancelled. Times that do not exist generate a problem.

### 2.2 Additional service

Uses the same structure as reduced service:

```json
{
  "directionId": {
    "workday": ["23:50"],
    "holiday": ["00:10"]
  }
}
```

The specified departures are added to the schedule. A time already present in the base schedule generates a problem. Times earlier than the first base departure are handled as after-midnight departures.

### 2.3 Cancellation

Cancels every departure belonging to a specified line or direction:

```json
{
  "lineOrDirectionId": {}
}
```

The cancellation applies during the validity period.

### 2.4 Diversion

A diversion changes a segment of a direction's route. The general structure is:

```json
{
  "directionId": {
    "segments": [
      {
        "segmentId": "segment1",
        "startStationId": "StationBeforeDiversion",
        "modifications": [
          {
            "action": "CANCELLED",
            "affectedStations": [
              {
                "stationId": "StationToRemove"
              }
            ]
          },
          {
            "action": "ADDED",
            "affectedStations": [
              {
                "stationId": "ReplacementStation",
                "offsetMinutes": 5
              }
            ]
          }
        ]
      }
    ]
  }
}
```

Important rules:

- `segmentId` is required and is used in error messages.
- `startStationId` is the last unchanged stop before the modified segment.
- Added stops are inserted immediately after the start station.
- `offsetMinutes` specifies the travel time to the next listed stop. The last added stop may omit it.
- Cancelled stops must occur after the start station.
- `previousStationOffsetMinutes` can override the travel time from the start station to the next kept stop. It can be specified at the modification or segment level.
- The last kept stop becomes the effective terminus.
- Multiple diversions on the same direction are applied in file order.

The original route remains available internally, while the application displays the effective route. Cancelled stops are struck through and added stops are marked in green.

### 2.5 Special lines

A `SPECIAL` modification contains a `specialLine` object:

```json
{
  "specialLine": {
    "id": "SPECIAL1",
    "type": "special",
    "color": "#ff8800",
    "displayName": "Special Service",
    "directions": [
      {
        "id": "SPECIAL1_OUT",
        "displayName": "Outbound",
        "smallText": "",
        "stops": [
          {
            "stationId": "StationA",
            "offsetMinutes": 10
          },
          {
            "stationId": "StationB",
            "offsetMinutes": 0
          }
        ],
        "schedules": {
          "workday": ["10:00"],
          "holiday": ["11:00"]
        }
      }
    ]
  }
}
```

Direction objects use the same structure as regular line directions. Optional fields include `displayNameBG`, `smallTextBG`, and `aliases`.

Rules:

- The line ID must not conflict with an existing line ID or direction ID.
- The line exists only during its actual validity period, not during the three-day advance-notice period.
- Departures are limited to the validity window.
- Special lines appear under **Special lines** on the Routes screen and otherwise behave like regular lines.
- Stops should reference valid station IDs. Missing station entries generate home-screen warnings.

---

## 3. Shared behaviour and validation

Both files use the following conventions:

- Dates and times use the device's local time, not UTC.
- Banners appear three days before the start and remain visible through the inclusive end time.
- Bulgarian title and message fields fall back independently to English.
- Modification banners appear before regular notice banners.
- Banners can appear on station screens, line/direction screens, and trip screens, depending on the affected entities and modification type.
- Invalid entries are reported through the app's developer warnings and browser console. Some invalid modification fields are skipped while the remaining valid effects are retained.
- The files are optional and are fetched independently of `data/manifest.json`.

## 4. Editing checklist

Before publishing changes:

1. Use valid JSON syntax, including double quotes and no trailing commas.
2. Confirm that all referenced line, direction, and station IDs exist.
3. Check that each validity period has the intended start and end times.
4. Confirm that reduced-service times exist in the base schedule and additional-service times do not.
5. Verify that diversion offsets connect the intended stops.
6. Check the result in the app, including the home-screen warnings and browser console.

**Important:** Keep `notices.json` for passenger information and schedule overrides. Use `modifications.json` when the service itself changes: departures, stops, routes, or temporary lines.
