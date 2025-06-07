
import json
import random
from datetime import datetime
from pathlib import Path

def get_time_category(hour):
    if 5 <= hour < 10:
        return "morning"
    elif 10 <= hour < 18:
        return "day"
    elif 18 <= hour < 21:
        return "evening"
    elif 21 <= hour < 24:
        return "night"
    else:
        return "midnight"

def load_kuruppo_data():
   filepath = Path(__file__).resolve().parent.parent / "kuruppo_timed_full.jsonl"
    with filepath.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]
        filepath = Path(__file__).resolve().parent.parent / "kuruppo_timed_full.jsonl"

def handler(request):
    try:
        hour = datetime.utcnow().hour + 9  # JST変換
        category = get_time_category(hour)
        kuruppo_data = load_kuruppo_data()
        filtered = [k for k in kuruppo_data if k["time"] == category]
        message = random.choice(filtered)["text"] if filtered else "ぽぽぽ…今日は静かな日っぽ。"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

