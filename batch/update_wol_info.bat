@echo off

cd ../

REM .env ファイルの読み込み
for /f "tokens=1,2 delims==" %%a in ('findstr /r "^" .env') do set %%a=%%b

REM MongoDBの接続URIの設定
set MONGO_URI=%MONGO_URI%

REM MongoDBに接続してwol_infoコレクションのドキュメントを更新
mongosh %MONGO_URI% batch/js/update_wol_info.js

pause
