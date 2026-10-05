import json
import re
import sys
from bs4 import BeautifulSoup

def parse_transport_schedule(html_file_path, output_json_path=None):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    line_name = None
    directions = []

    # Find all h3 headings that define line directions
    h3_elements = soup.find_all('h3')

    for h3 in h3_elements:
        text = h3.get_text(strip=True)
        if not text or ':' not in text:
            continue

        # Extract Line Name (e.g., "29")
        line_part, rest = text.split(':', 1)
        if not line_name:
            line_name = line_part.strip()

        # Clean display name by stripping trailing date ranges if present
        display_name = re.sub(r'\s*\d{2}\.\d{2}\.\d{4}\s*г\.\s*до\s*\d{2}\.\d{2}\.\d{4}\s*г\.', '', rest).strip()

        # Locate the schedule table corresponding to this direction
        table = h3.find_next('table')

        schedules = {
            "workday": [],
            "holiday": []
        }

        if table:
            theads = table.find_all('thead')
            for thead in theads:
                header_text = thead.get_text(strip=True).lower()
                tbody = thead.find_next_sibling('tbody')
                if not tbody:
                    continue

                # Extract departure times as plain strings
                buttons = tbody.find_all('button')
                departures = [btn.get_text(strip=True) for btn in buttons if btn.get_text(strip=True)]

                # Categorize schedule type
                if 'делнич' in header_text:
                    schedules["workday"] = departures
                elif any(kw in header_text for kw in ['събота', 'неделя', 'празник', 'празнич']):
                    schedules["holiday"] = departures

        directions.append({
            "id": None,  # Field present for future direction IDs
            "display_name": display_name,
            "schedules": schedules
        })

    data = {
        "line_name": line_name,
        "total_directions": len(directions),
        "directions": directions
    }

    # Save output to JSON file
    if output_json_path:
        with open(output_json_path, 'w', encoding='utf-8') as out_f:
            json.dump(data, out_f, ensure_ascii=False, indent=2)

    return data


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "29.html"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "schedule_29.json"

    parsed_data = parse_transport_schedule(input_file, output_file)
    print(f"Successfully exported {parsed_data['total_directions']} directions to {output_file}")