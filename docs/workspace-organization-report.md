# ワークスペース整理報告書

**作成日**: 2025年10月7日  
**対象**: C:\AI\workspaces\cursor-aidd-sandbox  
**目的**: 散乱したディレクトリ構造の整理と再発防止策の提案

---

## 📊 現状分析

### 発見された問題点

#### 1. **プロジェクト構造の不明確さ**
現在のワークスペースには、**3つの独立したプロジェクト**が混在しています：

| プロジェクト | 説明 | ファイル数 |
|------------|------|-----------|
| **aidd-integration-system** | AI駆動開発の統合システム（メインプロジェクト） | 約40ファイル |
| **hackathon-2025** | Steppyアプリ（ハッカソンプロジェクト） | 173ファイル |
| **pims-template** | PIMSテンプレート（テンプレートリポジトリ） | 約10ファイル |

これらが全てルートレベルに配置され、境界が不明確です。

#### 2. **ルートレベルの散乱ファイル**

**一時ファイル（.gitignoreで除外済み）**:
- `organize_log_*.txt` (3ファイル)
- `download_analysis_report.json`
- `downloaded_files.txt`
- `temp_config.json`
- `tatus --porcelain` ← コマンドのタイポ？

**ドキュメント（重複・未整理）**:
- `サブPC Cursor導入プロンプト集.md` (2バージョン)
- `サブPC ハッカソン応用編プロンプト.md`
- `マルチデバイス*.md` (3ファイル)
- `統合*.md` (2ファイル)
- `整理完了報告.md`
- `Issue管理システム設計.md`

**スクリプト（用途不明）**:
- `download_folder_analyzer.py`
- `download_folder_organizer.py`
- `organize_downloads.bat`
- `README_download_organizer.md`

#### 3. **ディレクトリの重複・不統一**

| ディレクトリ | 場所 | 内容 |
|------------|------|------|
| `docs/` | ルート | メインドキュメント (11ファイル) |
| `development-docs/` | ルート | 開発ドキュメント (9ファイル) |
| `aidd-integration-system/docs/` | サブディレクトリ | 同じ内容 (7ファイル) |
| `hackathon-2025/docs/` | サブディレクトリ | ハッカソン用 |
| `archive/` | ルート | 過去のドキュメント (16ファイル) |
| `aidd-integration-system/archive/` | サブディレクトリ | 同じ内容 (12ファイル) |
| `examples/` | ルート | テンプレート (2ファイル) |
| `aidd-integration-system/examples/` | サブディレクトリ | 同じ内容 |
| `templates/` | ルート | Cursorルール (5ファイル) |
| `aidd-integration-system/templates/` | サブディレクトリ | 同じ内容 |

#### 4. **Git管理状態の問題**

**未追跡ファイル**（重要なファイルが未コミット）:
- `.cursor/` ← Cursor設定
- `.taskmaster/` ← Taskmaster設定
- `aidd-integration-system/` ← **サブディレクトリ全体**
- `hackathon-2025/` ← **サブディレクトリ全体**
- `pims-template/` ← **サブディレクトリ全体**

**変更されたファイル**（未コミット）:
- `.cursorrules`
- `.gitignore`
- `README.md`
- その他GitHubテンプレート

#### 5. **謎のディレクトリ**

- `%APPDATA%\Cursor\mcp\...` ← システムディレクトリへの参照？
- `contents/japanese/` (32 mdファイル) ← 用途不明
- `project-files/` (4 mdファイル) ← GitHub関連手順書

---

## 🎯 整理手法の提案

### アプローチ1: モノレポ構造への移行（推奨）

**概要**: 現在の3つのプロジェクトを明確に分離し、モノレポとして管理

```
cursor-aidd-sandbox/
├── projects/                          # 各プロジェクトを格納
│   ├── aidd-integration-system/      # メインプロジェクト
│   ├── hackathon-2025/               # ハッカソンプロジェクト
│   └── pims-template/                # テンプレート
├── docs/                             # 共通ドキュメント
│   ├── guides/                       # ガイド類
│   ├── references/                   # リファレンス
│   └── archive/                      # 過去のドキュメント
├── scripts/                          # 共通スクリプト
│   └── utilities/                    # ユーティリティ
├── .cursor/                          # Cursor設定
├── .taskmaster/                      # Taskmaster設定
├── .github/                          # GitHub設定
├── README.md                         # ワークスペース全体の説明
└── package.json                      # ワークスペース設定
```

**実行手順**:

1. **バックアップ作成**
   ```bash
   # Gitで現在の状態をコミット（セーフティネット）
   git add -A
   git commit -m "chore: 整理前のスナップショット"
   git tag workspace-before-cleanup
   ```

2. **projects/ディレクトリを作成し、プロジェクトを移動**
   ```bash
   mkdir projects
   git mv aidd-integration-system projects/
   git mv hackathon-2025 projects/
   git mv pims-template projects/
   ```

3. **ドキュメントを統合**
   ```bash
   # development-docs/ を docs/ に統合
   mkdir -p docs/development
   git mv development-docs/* docs/development/
   rmdir development-docs

   # 重複ファイルを削除
   # aidd-integration-system/docs/ は既に projects/ 配下にあるので維持
   ```

4. **一時ファイル・スクリプトを整理**
   ```bash
   # scriptsディレクトリへ移動
   mkdir -p scripts/utilities
   git mv download_folder_analyzer.py scripts/utilities/
   git mv download_folder_organizer.py scripts/utilities/
   git mv organize_downloads.bat scripts/utilities/
   git mv README_download_organizer.md scripts/utilities/README.md

   # 一時ファイルは削除（.gitignore済み）
   rm organize_log_*.txt
   rm download_analysis_report.json
   rm downloaded_files.txt
   rm temp_config.json
   rm "tatus --porcelain"
   ```

5. **ルートのmdファイルを整理**
   ```bash
   # 古いプロンプト集をarchiveへ
   mkdir -p docs/archive/prompts
   git mv "サブPC Cursor導入プロンプト集.md" docs/archive/prompts/
   git mv "サブPC Cursor導入プロンプト集（更新版）.md" docs/archive/prompts/
   git mv "サブPC ハッカソン応用編プロンプト.md" docs/archive/prompts/

   # マルチデバイス関連をarchiveへ
   mkdir -p docs/archive/multi-device
   git mv "マルチデバイス・マルチアカウントシステム完成報告.md" docs/archive/multi-device/
   git mv "マルチデバイス・マルチアカウントシステム導入案.md" docs/archive/multi-device/
   git mv "マルチデバイス実装ガイド.md" docs/archive/multi-device/

   # その他
   git mv "整理完了報告.md" docs/archive/
   git mv "統合知見蓄積システム.md" docs/archive/
   git mv "統合運用実証結果.md" docs/archive/
   git mv "Issue管理システム設計.md" docs/archive/
   ```

6. **contents/とproject-files/を整理**
   ```bash
   # contents/japanese/ の内容を確認して適切な場所へ
   # （内容次第でdocs/へ統合または削除）

   # project-files/ はarchiveへ
   git mv project-files docs/archive/
   ```

7. **不要なディレクトリを削除**
   ```bash
   # 重複するexamples/, research/, templates/
   # aidd-integration-systemのものを残し、ルートレベルは削除
   git rm -rf examples/
   git rm -rf research/
   git rm -rf templates/
   ```

8. **README.mdを更新**
   ```markdown
   # AI駆動開発ワークスペース

   このワークスペースには、AI駆動開発（AIDD）に関する複数のプロジェクトが含まれています。

   ## 📁 プロジェクト構成

   ### メインプロジェクト
   - **[aidd-integration-system](projects/aidd-integration-system/)** - AI駆動開発の統合システム
   - **[hackathon-2025](projects/hackathon-2025/)** - Steppyアプリ（ハッカソンプロジェクト）
   - **[pims-template](projects/pims-template/)** - PIMSテンプレート

   ### ドキュメント
   - **[docs/](docs/)** - 共通ドキュメント・ガイド
   - **[scripts/](scripts/)** - 共通スクリプト・ユーティリティ

   ## 🚀 クイックスタート

   各プロジェクトの詳細は、それぞれのREADME.mdを参照してください。
   ```

9. **コミット**
   ```bash
   git add -A
   git commit -m "chore: ワークスペース整理 - モノレポ構造へ移行

   - projects/配下に3つのプロジェクトを整理
   - ドキュメントをdocs/に統合
   - 一時ファイル・重複ファイルを削除
   - スクリプトをscripts/に集約"
   ```

**メリット**:
- ✅ プロジェクト境界が明確
- ✅ 各プロジェクトを独立して管理可能
- ✅ 共通ドキュメント・スクリプトの一元管理
- ✅ Gitでの変更追跡が容易

**デメリット**:
- ⚠️ パスが変わるため、既存のスクリプト・設定を修正する必要がある

---

### アプローチ2: マルチリポジトリ化（代替案）

**概要**: 3つのプロジェクトをそれぞれ独立したGitリポジトリに分離

**実行手順**:

1. **各プロジェクトを別リポジトリとして作成**
   ```bash
   # aidd-integration-systemを独立リポジトリ化
   cd aidd-integration-system
   git init
   git remote add origin <new-repo-url-1>
   git add -A
   git commit -m "chore: 独立リポジトリとして初期化"
   git push -u origin main

   # hackathon-2025も同様に
   # pims-templateも同様に
   ```

2. **元のワークスペースをクリーンアップ**
   ```bash
   # プロジェクトディレクトリを削除
   rm -rf aidd-integration-system
   rm -rf hackathon-2025
   rm -rf pims-template

   # README.mdにリンクを追加
   ```

**メリット**:
- ✅ 各プロジェクトの独立性が最大限に保たれる
- ✅ 異なる権限・ワークフロー管理が可能

**デメリット**:
- ❌ 横断的な検索・操作が困難
- ❌ 共通ファイルの管理が複雑化

---

## 🛡️ 再発防止策

### 1. **Cursor Rulesへの追加**

`.cursorrules`または`.cursor/rules/workspace-organization.mdc`に以下を追加：

```markdown
---
description: ワークスペース整理ルール - プロジェクト構造の維持
alwaysApply: true
---

## ワークスペース構造の維持

### **禁止事項**

1. **ルートレベルへの無秩序なファイル配置**
   - ❌ 一時ファイルをルートに作成しない
   - ❌ 新しいmdファイルを安易にルートに配置しない
   - ❌ スクリプトをルートに配置しない

2. **重複ディレクトリの作成**
   - ❌ 既存の`docs/`, `scripts/`と同じ目的のディレクトリを作らない
   - ❌ プロジェクト外に`examples/`, `templates/`を作らない

### **推奨事項**

1. **新規ファイルの配置先**
   ```
   ✅ ドキュメント → docs/
   ✅ スクリプト → scripts/
   ✅ 一時ファイル → .gitignore + ルート外
   ✅ プロジェクト固有ファイル → projects/<project-name>/
   ```

2. **新規プロジェクトの作成**
   ```bash
   # 必ずprojects/配下に作成
   mkdir projects/new-project
   cd projects/new-project
   # プロジェクト初期化
   ```

3. **定期的なクリーンアップ**
   - 月次で`git status`を確認
   - 未追跡ファイルを整理
   - 一時ファイルを削除
```

### 2. **Git Hooksの活用**

`.git/hooks/pre-commit`にチェックスクリプトを追加：

```bash
#!/bin/bash
# ルートレベルに危険なファイルがないかチェック

echo "🔍 ワークスペース整理チェック..."

# ルートレベルの.mdファイルをチェック（README.mdを除く）
root_md_files=$(git diff --cached --name-only --diff-filter=A | grep '^[^/]*\.md$' | grep -v '^README\.md$')

if [ ! -z "$root_md_files" ]; then
  echo "⚠️  警告: ルートレベルに新しい.mdファイルが追加されています:"
  echo "$root_md_files"
  echo ""
  echo "これらのファイルは docs/ または projects/<project-name>/ に配置することを推奨します。"
  echo "続行しますか？ (y/N)"
  read -r response
  if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ コミットを中止しました。"
    exit 1
  fi
fi

# ルートレベルの.pyファイルをチェック
root_py_files=$(git diff --cached --name-only --diff-filter=A | grep '^[^/]*\.py$')

if [ ! -z "$root_py_files" ]; then
  echo "⚠️  警告: ルートレベルに新しい.pyファイルが追加されています:"
  echo "$root_py_files"
  echo ""
  echo "これらのファイルは scripts/ または projects/<project-name>/src/ に配置することを推奨します。"
  echo "続行しますか？ (y/N)"
  read -r response
  if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ コミットを中止しました。"
    exit 1
  fi
fi

echo "✅ チェック完了"
exit 0
```

### 3. **.gitignoreの強化**

既存の`.gitignore`に追加：

```gitignore
# ワークスペース整理用
# ルートレベルの一時ファイル
/*.tmp
/*.temp
/*.bak
/*_backup.*
/*_old.*

# ログファイル（ルートレベル限定）
/*.log

# ダウンロードフォルダ関連
/downloads/
/Download*/
```

### 4. **READMEへの明示**

ルートの`README.md`に**ワークスペース規約**を追加：

```markdown
## 📋 ワークスペース規約

### ファイル配置ルール

| ファイルタイプ | 配置先 | 例 |
|--------------|--------|-----|
| プロジェクトコード | `projects/<project-name>/` | `projects/aidd-integration-system/src/` |
| 共通ドキュメント | `docs/` | `docs/guides/`, `docs/references/` |
| 共通スクリプト | `scripts/` | `scripts/utilities/` |
| プロジェクト固有ドキュメント | `projects/<project-name>/docs/` | `projects/hackathon-2025/docs/` |
| 一時ファイル | `.gitignore` + プロジェクト外 | ❌ ルートに配置しない |

### 禁止事項

- ❌ ルートレベルへの`.md`, `.py`, `.js`等の直接配置（README.md除く）
- ❌ 既存の`docs/`, `scripts/`と重複するディレクトリの作成
- ❌ 一時ファイルのコミット

### クリーンアップコマンド

```bash
# 未追跡ファイルの確認
git status --short

# 一時ファイルの削除
git clean -fd --dry-run  # プレビュー
git clean -fd            # 実行
```
```

### 5. **Taskmaster統合**

Taskmasterで定期的な整理タスクを作成：

```bash
# 月次整理タスクを追加
task-master add-task \
  --prompt="ワークスペースのクリーンアップ: 未追跡ファイルの整理、一時ファイルの削除、ディレクトリ構造の確認" \
  --priority=medium

# 週次レビュータスクを追加
task-master add-task \
  --prompt="git statusで未追跡ファイルを確認し、適切な場所に移動またはgitignore追加" \
  --priority=low
```

### 6. **自動化スクリプト**

`scripts/utilities/workspace-check.sh`:

```bash
#!/bin/bash
# ワークスペース健全性チェック

echo "🔍 ワークスペース健全性チェック開始..."

# 1. ルートレベルのファイル数をチェック
root_files=$(ls -1 | wc -l)
echo "📊 ルートレベルのファイル数: $root_files"

if [ $root_files -gt 20 ]; then
  echo "⚠️  警告: ルートレベルのファイルが多すぎます（20個以上）"
fi

# 2. 未追跡ファイルのチェック
untracked=$(git status --porcelain | grep '^??' | wc -l)
echo "📊 未追跡ファイル数: $untracked"

if [ $untracked -gt 5 ]; then
  echo "⚠️  警告: 未追跡ファイルが多すぎます"
  echo ""
  git status --porcelain | grep '^??'
fi

# 3. 一時ファイルのチェック
temp_files=$(find . -maxdepth 1 -type f \( -name "*.tmp" -o -name "*.temp" -o -name "*.log" \) | wc -l)
echo "📊 一時ファイル数: $temp_files"

if [ $temp_files -gt 0 ]; then
  echo "⚠️  警告: 一時ファイルが残っています"
  find . -maxdepth 1 -type f \( -name "*.tmp" -o -name "*.temp" -o -name "*.log" \)
fi

echo ""
echo "✅ チェック完了"
```

---

## 📅 実行スケジュール

### 即時対応（今日）
1. ✅ このレポート作成
2. ⏳ バックアップ作成（Gitタグ）
3. ⏳ アプローチ1（モノレポ化）の実行開始

### 短期（1週間以内）
1. ⏳ Cursor Rulesへの追加
2. ⏳ Git Hooksの設定
3. ⏳ README更新
4. ⏳ 自動化スクリプト作成

### 中期（1ヶ月以内）
1. ⏳ Taskmaster統合（定期タスク設定）
2. ⏳ ワークスペース規約の周知
3. ⏳ 月次チェックの実施

---

## 🎯 期待される効果

### 短期的効果
- ✅ プロジェクト境界の明確化
- ✅ ファイル検索の高速化
- ✅ Git操作の簡素化

### 長期的効果
- ✅ 新規プロジェクト追加時の混乱防止
- ✅ チーム開発時の混乱回避
- ✅ メンテナンス工数の削減

---

## 📝 補足: contents/とproject-files/の処理

### contents/japanese/ (32ファイル) ⚠️
**内容**: 「⿻（多元性）」に関する日本語書籍のコンテンツ
- `0-1-著者紹介.md`, `0-2-自分の道を見つける.md`
- `1-0-多元性を見る.md`～`7-1-結論.md`まで32章

**判断**: **このワークスペースとは無関係な別プロジェクトの内容**

**推奨処理**:
```bash
# Option 1: 完全削除（他の場所にバックアップがある場合）
git rm -rf contents/

# Option 2: 別リポジトリへ移動（書籍プロジェクトとして独立管理）
mkdir ../plurality-book-japanese
git mv contents/japanese/* ../plurality-book-japanese/
cd ../plurality-book-japanese
git init
git add .
git commit -m "初期コミット: ⿻（多元性）日本語訳プロジェクト"

# Option 3: archiveへ移動（保存だけしておく）
mkdir -p docs/archive/external-content
git mv contents/japanese docs/archive/external-content/
git rm -rf contents/
```

**推奨**: Option 1（完全削除） または Option 2（独立リポジトリ化）

### project-files/ (4ファイル)
**内容**: GitHub関連の手順書
- `GitHubアップロード手順書.md`
- `GitHubリポジトリ作成手順.md`
- `リポジトリアップロード計画.md`
- `リポジトリ設計案.md`

**推奨処理**:
```bash
# docs/archive/github-setup/へ移動
mkdir -p docs/archive/github-setup
git mv project-files/* docs/archive/github-setup/
rmdir project-files
```

**理由**: 歴史的価値はあるが、現在はアクティブではない

---

**次のステップ**: この報告書を確認後、アプローチ1（モノレポ化）の実行を開始しますか？

