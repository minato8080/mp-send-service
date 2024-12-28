@echo off
REM .env ファイルの読み込み
for /f "tokens=1,2 delims==" %%a in ('findstr /r "^" .env') do set %%a=%%b

REM MongoDB の接続 URI と更新者の設定
set MONGO_URI=%MONGO_URI%

REM MongoDB に接続して target_flag の bool_value を True に更新
mongosh %MONGO_URI% update_flag.js

pause
