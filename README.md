# README

Raspberry piとMongoDBを使用してWake-on-LAN(WoL)機能を管理するスクリプトです。

- `main.py`: MongoDBからWoLフラグを監視し、フラグが立っている場合に指定されたMACアドレスにマジックパケットを送信します。また、フラグをリセットし、更新情報をMongoDBに記録します。
- `batch/update_wol_info.bat`: MongoDBに接続し、`wol_info`コレクションのドキュメントを更新するためのバッチスクリプトです。

## 環境設定

### ラズパイ側
1. リポジトリをクローンし、以下のコマンドを実行して必要なライブラリをインストールしてください。
   ```
   pip install .
   ```
2. プロジェクトのルートディレクトリに`.env`ファイルを作成し、以下の内容を記述してください。
   ```
   MONGO_URI=mongodb+srv://<username>:<password>@<collection>.tjzrd.mongodb.net
   DB_NAME=<dbname>
   COLLECTION_NAME=wol_info
   TARGET_MACHINE=hogehoge
   TARGET_MAC_ADDRESS= 00:11:22:33:44:55
   INTERVAL_SECONDS=10
   UPDATED_BY=hugahuga
   LOG_PATH=wol.log
   ```
3. `crontab`を使用して、起動時に自動実行されるように設定します。以下のコマンドを実行してください。
   ```
   crontab -e
   ```
   次の行を追加してください。`sleep`は安定性を確保する理由で入れています。
   ```
   @reboot sleep 60 && /usr/bin/python3 /home/pi/mp-send-service/main.py
   ```

### クライアント側Windows機
1. リポジトリをクローンし、プロジェクトのルートディレクトリに`.env`ファイルを作成してください。
2. [mongosh](https://www.mongodb.com/ja-jp/docs/mongodb-shell/)をインストールし、システムのパスに追加してください。

## 使用手順
1. 各Windows機でZeroTierを起動し、ネットワークに参加してください。
2. ラズパイを電源に接続してください。
3. `update_wol_info.bat`を実行し、Wake On LAN用のフラグをONに設定してください。
4. リモートデスクトップを使用してホスト側に接続してください。
