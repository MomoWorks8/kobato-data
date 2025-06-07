import json
import random
from datetime import datetime
from pathlib import Path

def handler(request):
    try:
        filepath = Path(__file__).parent / "kuruppo_timed_full.jsonl"
        with filepath.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            kuruppo_data = [json.loads(line) for line in lines]

        now = datetime.utcnow().hour + 9  # JST変換
        if 5 <= now < 10:
            time_label = "morning"
        elif 10 <= now < 17:
            time_label = "day"
        elif 17 <= now < 22:
            time_label = "evening"
        elif 22 <= now < 25:
            time_label = "night"
        else:
            time_label = "midnight"

        filtered = [item["text"] for item in kuruppo_data if item["time"] == time_label]
        message = random.choice(filtered) if filtered else "くるっぽ〜（データがないよ）"

        return {
            "statusCode": 200,
            "body": message
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"エラーが発生したぽぽ！: {str(e)}"
        }
