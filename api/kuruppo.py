import json
import random
from datetime import datetime
from pathlib import Path

def kuruppo_handler(request):
    try:
        print("🟢 handler開始")
        
        filepath = Path(__file__).parent / "kuruppo_timed_full.jsonl"
        print(f"📁 ファイルパス: {filepath}")

        with filepath.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            print(f"📄 読み込み行数: {len(lines)}")

            kuruppo_data = [json.loads(line) for line in lines]
            print("✅ JSON読み込み成功")

        now = datetime.utcnow().hour + 9  # JST変換
        print(f"⌚ 現在のJST時刻: {now}")

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
        
        print(f"⏰ ラベル: {time_label}")

        filtered = [item["text"] for item in kuruppo_data if item["time"] == time_label]
        print(f"🕊️ メッセージ候補数: {len(filtered)}")

        message = random.choice(filtered) if filtered else "くるっぽ〜（データがないよ）"
        print(f"📤 選ばれたメッセージ: {message}")

        return {
            "statusCode": 200,
            "body": message
        }

    except Exception as e:
        print(f"🔥 エラー発生: {e}")
        return {
            "statusCode": 500,
            "body": f"エラーが発生したぽぽ！: {str(e)}"
        }

# 🛠️ ここがミソ！
handler = kuruppo_handler
