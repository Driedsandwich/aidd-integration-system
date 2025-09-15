# 複数デバイス同期戦略 - ルール改善サイクル

## 概要

Windows環境とMac環境の両方でルール改善サイクルを運用するための同期戦略です。複数デバイス間での一貫したルール管理を実現します。

## 同期戦略の選択肢

### 1. Git同期（推奨）

#### メリット
- **バージョン管理**: 変更履歴の完全な記録
- **競合解決**: 複数デバイスでの編集時の競合処理
- **ブランチ機能**: 実験的なルール変更の安全な管理
- **バックアップ**: 自動的なバックアップ機能

#### セットアップ手順

##### リポジトリの作成
```bash
# 新しいリポジトリの作成（GitHub推奨）
# 1. GitHubで新しいリポジトリを作成
# 2. ローカルで初期化
git init
git add .cursor/rules/
git commit -m "Initial rules setup"
git branch -M main
git remote add origin https://github.com/username/rules-repository.git
git push -u origin main
```

##### 各デバイスでの設定
```bash
# リポジトリのクローン
git clone https://github.com/username/rules-repository.git
cd rules-repository

# ルールファイルのシンボリックリンク作成
ln -s .cursor/rules ~/.cursor/rules
# または
cp -r .cursor/rules ~/project/.cursor/
```

#### 日常的な同期フロー
```bash
# 作業開始時
git pull origin main

# ルール更新後
git add .cursor/rules/
git commit -m "Update rules: [具体的な変更内容]"
git push origin main

# 他のデバイスでの更新取得
git pull origin main
```

### 2. クラウドストレージ同期

#### 対応サービス
- **iCloud Drive**: Mac環境での自動同期
- **OneDrive**: Windows環境での自動同期
- **Google Drive**: クロスプラットフォーム対応
- **Dropbox**: 安定した同期機能

#### セットアップ手順

##### iCloud Drive（Mac）
```bash
# iCloud Driveにプロジェクトを配置
cp -r ~/project ~/Library/Mobile\ Documents/com~apple~CloudDocs/

# シンボリックリンクの作成
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/project/.cursor/rules ~/project/.cursor/rules
```

##### OneDrive（Windows）
```powershell
# OneDriveにプロジェクトを配置
copy -r project C:\Users\username\OneDrive\

# シンボリックリンクの作成（管理者権限が必要）
mklink /D .cursor C:\Users\username\OneDrive\project\.cursor
```

### 3. 手動同期

#### 同期用スクリプトの作成

##### Windows用スクリプト（sync-rules.ps1）
```powershell
# ルールファイルの同期スクリプト
param(
    [string]$RemotePath = "C:\path\to\sync\location"
)

# ルールファイルのコピー
Copy-Item -Path ".cursor\rules\*" -Destination "$RemotePath\.cursor\rules\" -Recurse -Force

# 同期日時の記録
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "Rules synced at: $timestamp"
```

##### Mac用スクリプト（sync-rules.sh）
```bash
#!/bin/bash
# ルールファイルの同期スクリプト

REMOTE_PATH="/path/to/sync/location"

# ルールファイルのコピー
cp -r .cursor/rules/* "$REMOTE_PATH/.cursor/rules/"

# 同期日時の記録
timestamp=$(date "+%Y-%m-%d %H:%M:%S")
echo "Rules synced at: $timestamp"
```

## 推奨される同期戦略

### 1. ハイブリッド戦略（最推奨）

#### 構成
- **メイン同期**: Gitリポジトリ
- **バックアップ同期**: クラウドストレージ
- **緊急時**: 手動同期

#### 実装例
```bash
# 日常的なGit同期
git add .cursor/rules/
git commit -m "Update rules"
git push origin main

# 週次バックアップ
tar -czf rules-backup-$(date +%Y%m%d).tar.gz .cursor/rules/
# クラウドストレージにアップロード
```

### 2. 環境固有の最適化

#### Windows環境
```powershell
# PowerShellプロファイルに追加
function Sync-Rules {
    git pull origin main
    Write-Host "Rules updated from remote"
}

function Update-Rules {
    git add .cursor/rules/
    git commit -m "Update rules from Windows"
    git push origin main
    Write-Host "Rules pushed to remote"
}
```

#### Mac環境
```bash
# .zshrcまたは.bashrcに追加
alias sync-rules='git pull origin main && echo "Rules updated from remote"'
alias update-rules='git add .cursor/rules/ && git commit -m "Update rules from Mac" && git push origin main && echo "Rules pushed to remote"'
```

## 同期時の注意事項

### 1. 競合の回避

#### ルール更新のタイミング
- **作業開始時**: 必ず最新のルールを取得
- **作業終了時**: 変更を即座にコミット
- **長時間の作業**: 定期的な同期

#### 競合発生時の対応
```bash
# 競合の確認
git status

# 競合の解決
git mergetool

# 解決後のコミット
git add .cursor/rules/
git commit -m "Resolve merge conflict"
```

### 2. 環境固有の調整

#### 環境識別の追加
```markdown
# general.mdcに追加
## 環境識別
- このルールは[Windows/Mac]環境で更新されました
- 更新日時: [日付]
- 更新者: [デバイス名]
```

#### 環境固有のルール分離
```
.cursor/rules/
├── general.mdc
├── environment-windows.mdc
├── environment-mac.mdc
├── implementation.mdc
├── github.mdc
└── knowledge.mdc
```

## 同期の自動化

### 1. Git Hooksの活用

#### pre-commit hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# ルールファイルの構文チェック
for file in .cursor/rules/*.mdc; do
    if ! grep -q "^#" "$file"; then
        echo "Error: $file does not start with header"
        exit 1
    fi
done

echo "Rules validation passed"
```

#### post-commit hook
```bash
#!/bin/bash
# .git/hooks/post-commit

# 同期の自動プッシュ
git push origin main
echo "Rules automatically synced"
```

### 2. 定期同期の設定

#### Windows Task Scheduler
```powershell
# 毎日午前9時に同期
$action = New-ScheduledTaskAction -Execute "PowerShell" -Argument "-File C:\path\to\sync-rules.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Sync Cursor Rules"
```

#### Mac cron
```bash
# crontabの編集
crontab -e

# 毎日午前9時に同期
0 9 * * * cd /path/to/project && git pull origin main
```

## トラブルシューティング

### 1. 同期エラーの対応

#### Git関連
```bash
# リモートとの差分確認
git fetch origin
git log HEAD..origin/main

# 強制同期（注意: ローカルの変更が失われます）
git reset --hard origin/main
```

#### クラウドストレージ関連
```bash
# 同期状況の確認
# iCloud: システム環境設定 > Apple ID > iCloud
# OneDrive: タスクバーのアイコンをクリック
# Google Drive: アプリの同期状況を確認
```

### 2. データの整合性確認

#### チェックスクリプト
```bash
#!/bin/bash
# rules-integrity-check.sh

echo "Checking rules integrity..."

# ファイルの存在確認
for file in general.mdc environment.mdc implementation.mdc github.mdc knowledge.mdc; do
    if [ ! -f ".cursor/rules/$file" ]; then
        echo "ERROR: $file is missing"
        exit 1
    fi
done

# ファイルサイズの確認
for file in .cursor/rules/*.mdc; do
    lines=$(wc -l < "$file")
    if [ $lines -gt 500 ]; then
        echo "WARNING: $file is too large ($lines lines)"
    fi
done

echo "Rules integrity check completed"
```

## 運用フロー

### 1. 日常的な運用

#### 作業開始時
```bash
# 1. 最新のルールを取得
git pull origin main

# 2. ルールの整合性確認
./rules-integrity-check.sh

# 3. 作業開始宣言
echo "Starting work with latest rules"
```

#### 作業終了時
```bash
# 1. ルールの更新
git add .cursor/rules/
git commit -m "Update rules: [具体的な変更]"

# 2. リモートへの同期
git push origin main

# 3. バックアップの作成
tar -czf rules-backup-$(date +%Y%m%d).tar.gz .cursor/rules/
```

### 2. 週次メンテナンス

#### 月曜日の作業
```bash
# 1. 全デバイスの同期確認
git log --oneline -10

# 2. 不要なルールの整理
# 3. ルールの効果測定
# 4. 同期戦略の見直し
```

## まとめ

複数デバイスでのルール改善サイクル運用には、以下の要素が重要です：

### 推奨構成
1. **メイン同期**: Gitリポジトリ
2. **バックアップ**: クラウドストレージ
3. **自動化**: Git Hooksと定期同期
4. **監視**: 整合性チェックスクリプト

### 運用のポイント
1. **作業開始時の同期**: 必ず最新ルールを取得
2. **作業終了時のコミット**: 変更を即座に反映
3. **定期メンテナンス**: 週次での整理と確認
4. **環境固有の調整**: Windows/Macの違いを考慮

この戦略により、複数デバイス間で一貫したルール改善サイクルを維持できます。

---

*作成日: 2025年9月12日*
*対象環境: Windows + Mac*
*同期方式: Git + クラウドストレージ*
