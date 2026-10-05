**parse.py**
Python script for easy extraction of departure times.
Only works with schedules coming from https://transport.obshtinaruse.bg/Schedule/DisplaySchedulesForRouteLine?lineName=<n> where <n> is a valid line number.

Use:
1. Save (Ctrl + S) only HTML of selected line
2. Open command prompt in the (or navigate to) folder where the script is
3. Enter the following: `python parse.py saved_line.html output.json`
4. The JSON file will be created in the same folder the script is

**build_manifest.py**
Python script for building manifest.json.
Run after adding or removing files in lines folder.
(or just update the file manually, it's not hard)