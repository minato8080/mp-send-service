from pymongo import MongoClient
from wakeonlan import send_magic_packet
from datetime import datetime, timezone
import time
import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数から設定を取得
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
TARGET_MAC_ADDRESS = os.getenv("TARGET_MAC_ADDRESS")
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", 10))
UPDATED_BY = os.getenv("UPDATED_BY")


def get_bool_value_and_process():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    try:
        # データベースからbool値を取得
        document = collection.find_one({"key": "target_flag"})
        if document and document.get("bool_value") == True:
            print("True値を検出、マジックパケットを送信します。")
            send_magic_packet(TARGET_MAC_ADDRESS)
            
            # MongoDBのドキュメントを更新
            update_result = collection.update_one(
                {"key": "target_flag"},
                {"$set": {
                    "bool_value": False,
                    "updated_at": datetime.now(timezone.UTC),
                    "updated_by": UPDATED_BY
                }}
            )
            if update_result.modified_count > 0:
                print("MongoDBのドキュメントが正常に更新されました。")
            else:
                print("MongoDBのドキュメント更新に失敗しました。")
        else:
            print("bool_valueはFalse、何もしません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        client.close()

# 定期実行ループ
if __name__ == "__main__":
    while True:
        get_bool_value_and_process()
        time.sleep(INTERVAL_SECONDS)
