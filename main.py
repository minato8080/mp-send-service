from pymongo import MongoClient
from wakeonlan import send_magic_packet
from datetime import datetime, timezone, timedelta
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
TARGET_MACHINE = os.getenv("TARGET_MACHINE")
LOG_PATH=os.getenv("LOG_PATH")


def get_current_time():
    current_time = (
        datetime.now(timezone.utc)
        .astimezone(timezone(timedelta(hours=9)))
        .strftime("%Y-%m-%d %H:%M:%S")
    )
    return current_time

def write_log(message):
    current_time = get_current_time()
    print(f"{current_time} {message}")
    with open(LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(f"{current_time} {message}\n")

def watch_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    current_time = get_current_time()

    try:
        # データベースからwolフラグを取得
        document = collection.find_one({"_id": TARGET_MACHINE})
        if document and document.get("wol_switch") == True:
            write_log("Detected True value, sending magic packet.")
            send_magic_packet(TARGET_MAC_ADDRESS)

            # MongoDBのドキュメントを更新
            update_result = collection.update_one(
                {"_id": TARGET_MACHINE},
                {
                    "$set": {
                        "wol_switch": False,
                        "updated_time": current_time,
                        "updated_name": UPDATED_BY,
                    }
                },
            )
            if update_result.modified_count > 0:
                write_log("MongoDB document was successfully updated.")
            else:
                write_log("Failed to update MongoDB document.")
    except Exception as e:
        write_log(f"An error occurred: {e}")
    finally:
        client.close()


# 定期実行ループ
if __name__ == "__main__":
    write_log("Service started.")
    while True:
        watch_db()
        time.sleep(INTERVAL_SECONDS)
