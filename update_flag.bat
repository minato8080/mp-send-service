@echo off
REM .env ファイルの読み込み
for /f "tokens=1,2 delims==" %%a in ('findstr /r "^" .env') do set %%a=%%b

REM MongoDB の接続 URI と更新者の設定
set MONGO_URI=%MONGO_URI%
set UPDATED_BY=%UPDATED_BY%

REM MongoDB に接続して target_flag の bool_value を True に更新
mongo %MONGO_URI% --eval "db.target_flags.updateOne({\"key\": \"target_flag\"}, {\$set: {\"bool_value\": true, \"updated_at\": new Date(), \"updated_by\": \"%UPDATED_BY%\"}})"

REM 更新完了のメッセージ
echo Flag updated to True successfully.
pause
