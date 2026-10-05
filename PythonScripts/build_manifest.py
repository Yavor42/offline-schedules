#!/usr/bin/env python3
"""Run after adding/removing files in data/lines/ -> regenerates data/manifest.json"""
import json, os
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
lines = sorted(f for f in os.listdir(os.path.join(d, "lines")) if f.endswith(".json"))
json.dump({"lines": lines, "stations": "stations/stations_extended.json"}, open(os.path.join(d, "manifest.json"), "w"), indent=1)
print("manifest.json:", len(lines), "line file(s)")
