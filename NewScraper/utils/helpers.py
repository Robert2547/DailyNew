import json
from pathlib import Path
from datetime import datetime, timedelta
import pytz
def save_to_json(data, output_file: Path):
    if not output_file.exists():
        with output_file.open("w", encoding="utf-8") as f:
            json.dump([], f)

    with output_file.open("r", encoding="utf-8") as f:
        existing_data = json.load(f)

    existing_data.append(data)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

def is_within_last_24_hours(time_str):
    try:
        now = datetime.now()
        if 'ago' not in time_str.lower():
            return False
        
        time_parts = time_str.split()
        number = int(time_parts[0])
        unit = time_parts[1]

        if unit.startswith("hour"):
            delta = timedelta(hours=number)
        elif unit.startswith("minute"):
            delta = timedelta(minutes=number)
        elif unit.startswith("second"):
            delta = timedelta(seconds=number)
        elif unit.startswith("day"):
            delta = timedelta(days=number)
        else:
            return False

        return delta <= timedelta(hours=24)
    except Exception as e:
        print(f"Error in is_within_24_hours: {e}")
        return False