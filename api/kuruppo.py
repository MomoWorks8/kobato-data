from pathlib import Path
import json
import random

def load_kuruppo_data():
    filepath = Path(__file__).resolve().parent.parent / "kuruppo_timed_full.jsonl"
    print(f"📂 ファイルパス: {filepath}")  # パス確認用ログ

    messages = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                messages.append(json.loads(line))
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")
        return []

    print(f"✅ 読み込んだメッセージ数: {len(messages)}")
    return messages

# データ読み込み（関数の外に定義して一度だけ読む）
kuruppo_data = load_kuruppo_data()

# メイン関数（Vercelが呼び出す）
def handler(request):
    if not kuruppo_data:
        return {"message": "ぽぽぽ…データが見つからないっぽ！"}

    text = random.choice(kuruppo_data)["text"]
    return {"message": text}
