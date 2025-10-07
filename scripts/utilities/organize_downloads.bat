@echo off
echo ========================================
echo ダウンロードフォルダ整理ツール
echo ========================================
echo.

REM Pythonがインストールされているか確認
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pythonがインストールされていません
    echo Python 3.7以上をインストールしてから再実行してください
    pause
    exit /b 1
)

echo 📋 ステップ1: ダウンロードフォルダを分析中...
echo.
py download_folder_analyzer.py
if errorlevel 1 (
    echo ❌ 分析に失敗しました
    pause
    exit /b 1
)

echo.
echo 📋 ステップ2: 整理のプレビュー（DRY RUN）
echo.
py download_folder_organizer.py --dry-run
if errorlevel 1 (
    echo ❌ プレビューに失敗しました
    pause
    exit /b 1
)

echo.
echo ⚠️ 実際に整理を実行しますか？
echo ファイルは移動のみで削除は行いません
echo.
set /p confirm="続行しますか？ (y/N): "
if /i not "%confirm%"=="y" if /i not "%confirm%"=="yes" (
    echo ❌ 処理を中止しました
    pause
    exit /b 0
)

echo.
echo 📋 ステップ3: 実際の整理を実行中...
echo.
py download_folder_organizer.py
if errorlevel 1 (
    echo ❌ 整理に失敗しました
    pause
    exit /b 1
)

echo.
echo ✅ 整理が完了しました！
echo 📁 ダウンロードフォルダを確認してください
echo.
pause
