import json
import random
from datetime import datetime

def handler(request):
    try:
        filepath = "api/kuruppo_timed_full.jsonl"

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            kuruppo_data = [json.loads(line) for line in lines]

        now = datetime.utcnow().hour + 9  # JST
        if 5 <= now < 10:
            time_label = "morning"
        elif 10 <= now < 17:
            time_label = "day"
        elif 17 <= now < 22:
            time_label = "evening"
        elif 22 <= now < 24:
            time_label = "night"
        else:
            time_label = "midnight"

        candidates = [k["text"] for k in kuruppo_data if k["time"] == time_label]
        return {
            "statusCode": 200,
            "body": random.choice(candidates) if candidates else "くるっぽー（該当メッセージなし）"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"くるっぽー（エラー発生）: {str(e)}"
        }
