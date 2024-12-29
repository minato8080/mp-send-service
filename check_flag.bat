@echo off
REM .env ファイルの読み込み
for /f "tokens=1,2 delims==" %%a in ('findstr /r "^" .env') do set %%a=%%b

REM MongoDBの接続URIの設定
set MONGO_URI=%MONGO_URI%

REM MongoDB に接続して wol_info コレクションのドキュメントを取得
mongosh %MONGO_URI% check_flag.js

pause
