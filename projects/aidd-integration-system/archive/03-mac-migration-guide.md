# Mac移行ガイド - ルール改善サイクル

## 概要

Windows環境で構築したルール改善サイクル（`.cursor/rules`構造）をMac環境に移行するためのガイドです。

## 移行前の準備

### 1. 現在のルール構造の確認

#### Windows環境での確認
```powershell
# ルールファイルの一覧確認
ls .cursor/rules/

# 各ファイルの内容確認
cat .cursor/rules/general.mdc
cat .cursor/rules/environment.mdc
cat .cursor/rules/implementation.mdc
cat .cursor/rules/github.mdc
cat .cursor/rules/knowledge.mdc
```

#### バックアップの作成
```powershell
# ルールディレクトリ全体のバックアップ
copy -r .cursor .cursor.backup
```

### 2. 移行用ファイルの準備

#### アーカイブ作成
```powershell
# tar.gz形式でアーカイブ作成
tar -czf cursor-rules-backup.tar.gz .cursor/
```

## Mac環境での移行手順

### ステップ1: Cursorのインストール

#### Homebrewを使用したインストール（推奨）
```bash
# Homebrewが未インストールの場合
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cursorのインストール
brew install --cask cursor
```

#### 手動インストール
1. [Cursor公式サイト](https://cursor.sh/)からMac版をダウンロード
2. .dmgファイルをマウントしてアプリケーションにコピー

### ステップ2: プロジェクトの移行

#### Gitリポジトリを使用する場合（推奨）
```bash
# リポジトリのクローン
git clone <your-repository-url>
cd <project-directory>

# ルールファイルの確認
ls -la .cursor/rules/
```

#### 手動移行の場合
```bash
# プロジェクトディレクトリの作成
mkdir -p ~/Projects/<project-name>
cd ~/Projects/<project-name>

# アーカイブの展開
tar -xzf cursor-rules-backup.tar.gz
```

### ステップ3: 環境固有のルール調整

#### environment.mdcの更新

**Windows用（移行前）**:
```markdown
## 環境固有の設定
- Windows環境ではPowerShellコマンドを使用してください
- パスの区切り文字は環境に応じて適切に選択してください
```

**Mac用（移行後）**:
```markdown
## 環境固有の設定
- Mac環境ではBash/Zshコマンドを使用してください
- パスの区切り文字は `/` を使用してください
- Homebrewを使用したパッケージ管理を推奨します
```

#### 更新手順
```bash
# environment.mdcの編集
nano .cursor/rules/environment.mdc

# または
code .cursor/rules/environment.mdc
```

### ステップ4: 開発環境の設定

#### Python環境の設定
```bash
# Pythonのインストール確認
python3 --version

# 仮想環境の作成（venv）
python3 -m venv .venv

# 仮想環境の有効化
source .venv/bin/activate

# 仮想環境の有効化確認
which python
```

#### uvのインストール（推奨）
```bash
# uvのインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# シェルの再読み込み
source ~/.zshrc  # または source ~/.bashrc

# uvの動作確認
uv --version
```

### ステップ5: ルールの動作確認

#### Cursorでの確認
1. Cursorを起動
2. プロジェクトを開く
3. チャット機能でルールの確認

#### 確認コマンド
```bash
# ルールファイルの権限確認
ls -la .cursor/rules/

# ファイルの文字エンコーディング確認
file .cursor/rules/*.mdc

# ファイルサイズの確認
wc -l .cursor/rules/*.mdc
```

## 環境固有の調整

### 1. シェルコマンドの違い

#### Windows PowerShell → Mac Bash/Zsh
```bash
# Windows
copy file1 file2
dir
del file

# Mac
cp file1 file2
ls
rm file
```

### 2. パス表記の違い

#### Windows → Mac
```bash
# Windows
C:\Users\username\project\.cursor\rules\general.mdc

# Mac
/Users/username/project/.cursor/rules/general.mdc
```

### 3. 仮想環境の違い

#### Windows
```powershell
# 仮想環境の有効化
.\.venv\Scripts\Activate.ps1

# 仮想環境の無効化
deactivate
```

#### Mac
```bash
# 仮想環境の有効化
source .venv/bin/activate

# 仮想環境の無効化
deactivate
```

## 移行後の検証

### 1. 基本機能のテスト

#### ルールファイルの読み込み確認
```bash
# 各ルールファイルの内容確認
head -5 .cursor/rules/general.mdc
head -5 .cursor/rules/environment.mdc
head -5 .cursor/rules/implementation.mdc
head -5 .cursor/rules/github.mdc
head -5 .cursor/rules/knowledge.mdc
```

#### Cursorでの動作確認
1. 新しいチャットセッションを開始
2. 「ルールを確認してください」と入力
3. 適切にルールが読み込まれているか確認

### 2. 開発環境のテスト

#### Python環境のテスト
```bash
# 仮想環境でのPython実行
python -c "import sys; print(sys.executable)"

# パッケージのインストールテスト
pip install requests
python -c "import requests; print('OK')"
```

#### uv環境のテスト
```bash
# uvでのプロジェクト初期化
uv init test-project
cd test-project

# パッケージの追加
uv add requests
uv run python -c "import requests; print('OK')"
```

## トラブルシューティング

### 1. よくある問題

#### ファイルの権限エラー
```bash
# 権限の確認と修正
ls -la .cursor/rules/
chmod 644 .cursor/rules/*.mdc
```

#### 文字エンコーディングの問題
```bash
# 文字エンコーディングの確認
file .cursor/rules/*.mdc

# UTF-8への変換（必要に応じて）
iconv -f SHIFT_JIS -t UTF-8 file.mdc > file_utf8.mdc
```

#### パスの問題
```bash
# 絶対パスの確認
pwd
realpath .cursor/rules/general.mdc
```

### 2. Cursor固有の問題

#### ルールが認識されない
1. Cursorの再起動
2. プロジェクトの再読み込み
3. `.cursor/rules/`ディレクトリの権限確認

#### パフォーマンスの問題
1. ルールファイルのサイズ確認（500行未満）
2. 不要なルールの削除
3. ルールの統合

## 移行完了チェックリスト

### 基本移行
- [ ] Cursorのインストール完了
- [ ] プロジェクトの移行完了
- [ ] ルールファイルの移行完了
- [ ] 環境固有の調整完了

### 開発環境
- [ ] Python環境の設定完了
- [ ] 仮想環境の動作確認完了
- [ ] uv環境の設定完了（オプション）

### 動作確認
- [ ] Cursorでのルール読み込み確認完了
- [ ] 基本的な開発作業のテスト完了
- [ ] ルール改善サイクルの動作確認完了

### 最適化
- [ ] 環境固有のルール調整完了
- [ ] パフォーマンスの確認完了
- [ ] バックアップの作成完了

## 移行後の運用

### 1. 定期的な同期

#### Gitを使用した同期
```bash
# 変更の確認
git status

# 変更のコミット
git add .cursor/rules/
git commit -m "Update rules for Mac environment"

# リモートへのプッシュ
git push origin main
```

#### 手動同期
```bash
# ルールファイルのバックアップ
tar -czf cursor-rules-mac-$(date +%Y%m%d).tar.gz .cursor/
```

### 2. 継続的な改善

#### 環境固有の知見の蓄積
```markdown
### Mac環境関連（追加）
- 失敗例：Homebrewのパスが通っていない
- 再発防止ルール：シェルプロファイルの確認を必須とする
- 効率的な処理方法：brew doctorでの環境チェック
```

## まとめ

Mac環境への移行は、以下の手順で安全に実行できます：

1. **準備**: 現在のルール構造の確認とバックアップ
2. **移行**: Cursorのインストールとプロジェクトの移行
3. **調整**: 環境固有のルール調整
4. **検証**: 動作確認とテスト
5. **最適化**: 継続的な改善

この移行により、WindowsとMacの両方で同じルール改善サイクルを活用できます。

---

*作成日: 2025年9月12日*
*対象環境: Windows → Mac*
*移行方法: Git同期推奨*
