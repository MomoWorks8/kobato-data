import json
import random
from datetime import datetime
from pathlib import Path

def handler(request):
    try:
        filepath = Path(__file__).resolve().parent / "kuruppo_timed_full.jsonl"

        with filepath.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            kuruppo_data = [json.loads(line) for line in lines]

        now = datetime.utcnow().hour + 9  # JSTに変換（UTC+9）

        if 5 <= now < 10:
            time_label = "morning"
        elif 10 <= now < 17:
            time_label = "day"
        elif 17 <= now < 20:
            time_label = "evening"
        elif 20 <= now < 24:
            time_label = "night"
        else:
            time_label = "midnight"

        candidates = [d for d in kuruppo_data if d["time"] == time_label]

        if not candidates:
            return {
                "statusCode": 200,
                "body": json.dumps({"text": "くるっぽ〜…今は静かに羽を休める時間みたい🕊️"})
            }

        selected = random.choice(candidates)
        return {
            "statusCode": 200,
            "body": json.dumps({"text": selected["text"]})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
