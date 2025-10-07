# 環境変数設定ガイド

> APIキー・機密情報の安全な管理方法

## 🚨 重要: 機密情報の取り扱い

**絶対に守ること:**
1. ✅ APIキーは `.env` ファイルに記載
2. ✅ `.env` は `.gitignore` で除外済み（確認必須）
3. ❌ `.env` は**絶対にGitにコミットしない**
4. ❌ コード内に直接APIキーを書かない

---

## セットアップ手順

### 1. .env ファイルを作成

プロジェクトルートに `.env` ファイルを作成:

```bash
# Windowsの場合
type nul > .env

# Mac/Linuxの場合
touch .env
```

### 2. APIキーを記入

以下のテンプレートを `.env` にコピーして、実際のキーを記入:

```env
# ====================================
# AI プロバイダー APIキー
# ====================================

# Anthropic (Claude) - Cursor等で使用
# 取得: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# OpenAI (GPT-4等)
# 取得: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# Perplexity (研究用) - Taskmaster researchで使用
# 取得: https://www.perplexity.ai/settings/api
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxx

# Google (Gemini)
# 取得: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=

# その他のプロバイダー
MISTRAL_API_KEY=
XAI_API_KEY=
OPENROUTER_API_KEY=

# Azure OpenAI
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=

# Ollama (ローカルLLM)
OLLAMA_BASE_URL=http://localhost:11434/api

# ====================================
# Taskmaster 設定
# ====================================

# ログレベル (debug, info, warn, error)
TASKMASTER_LOG_LEVEL=info

# ====================================
# その他
# ====================================

# アプリケーション設定
NODE_ENV=development
PORT=3000

# データベース（使用する場合）
DATABASE_URL=

# GitHub Token（Actions等で使用）
GITHUB_TOKEN=
```

### 3. .gitignore を確認

`.gitignore` に以下が含まれているか確認:

```gitignore
# 環境変数
.env
.env.local
.env.*.local

# APIキー・機密情報
*.key
*.pem
**/secrets/
```

### 4. 動作確認

環境変数が正しく読み込まれるか確認:

#### Node.js (JavaScript/TypeScript)

```javascript
// dotenvを使用
require('dotenv').config();

console.log('API Key loaded:', process.env.ANTHROPIC_API_KEY ? '✓' : '✗');
```

#### Python

```python
# python-dotenvを使用
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"API Key loaded: {'✓' if api_key else '✗'}")
```

---

## プロバイダー別: APIキー取得方法

### 🤖 Anthropic (Claude)

**Cursor/Windsurf等で必須**

1. [Anthropic Console](https://console.anthropic.com/) にアクセス
2. アカウント作成・ログイン
3. 「API Keys」セクションへ
4. 「Create Key」をクリック
5. キーをコピーして `.env` に貼り付け

**料金**: 従量課金（クレジット事前購入）

### 🧠 OpenAI (GPT-4)

1. [OpenAI Platform](https://platform.openai.com/api-keys) にアクセス
2. 「Create new secret key」をクリック
3. キーをコピー（**再表示不可なので注意**）
4. `.env` に貼り付け

**料金**: 従量課金

### 🔍 Perplexity (研究用)

**Taskmaster の `research` コマンドで使用**

1. [Perplexity Settings](https://www.perplexity.ai/settings/api) にアクセス
2. 「Generate API Key」をクリック
3. キーをコピー
4. `.env` に貼り付け

**料金**: 無料枠あり + 従量課金

### 🌐 OpenRouter (複数モデル対応)

1. [OpenRouter Keys](https://openrouter.ai/keys) にアクセス
2. 「Create Key」をクリック
3. キーをコピー
4. `.env` に貼り付け

**特徴**: 1つのAPIで複数のモデルにアクセス可能

### 🏠 Ollama (ローカルLLM)

**料金不要・オフライン動作可能**

1. [Ollama公式サイト](https://ollama.ai/) からインストール
2. モデルをダウンロード:
   ```bash
   ollama pull llama2
   ollama pull codellama
   ```
3. `.env` に追加:
   ```env
   OLLAMA_BASE_URL=http://localhost:11434/api
   ```

---

## Cursor / Windsurf での設定

### Cursor

APIキーは `.env` ではなく、Cursor設定に直接入力:

1. `Ctrl/Cmd + Shift + P` → 「Cursor Settings」
2. 「Models」セクション
3. 「API Key」に入力

または `.cursor/mcp.json` に記載:

```json
{
  "mcpServers": {
    "taskmaster": {
      "command": "npx",
      "args": ["-y", "task-master-ai", "mcp"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-xxxxxxxxxxxxx",
        "PERPLEXITY_API_KEY": "pplx-xxxxxxxxxxxxx"
      }
    }
  }
}
```

### Windsurf

同様に設定画面から入力、または設定ファイルに記載。

---

## Taskmaster での環境変数

### CLI使用時

`.env` ファイルから自動的に読み込まれます:

```bash
task-master research "最新のReact Query情報"
# PERPLEXITY_API_KEY を .env から読み込み
```

### MCP (Cursor統合) 使用時

`.cursor/mcp.json` の `env` セクションに記載:

```json
{
  "mcpServers": {
    "taskmaster": {
      "env": {
        "ANTHROPIC_API_KEY": "実際のキー",
        "PERPLEXITY_API_KEY": "実際のキー",
        "OPENAI_API_KEY": "実際のキー"
      }
    }
  }
}
```

**注意**: `.cursor/mcp.json` は通常 `.gitignore` で除外されます。

---

## セキュリティベストプラクティス

### ✅ やるべきこと

1. **環境変数を使用**
   ```javascript
   const apiKey = process.env.ANTHROPIC_API_KEY;
   ```

2. **定期的にキーをローテーション**
   - 3〜6ヶ月ごとに新しいキーに更新

3. **最小権限の原則**
   - 必要最小限の権限を持つキーを使用

4. **チーム共有は .env.example で**
   - 実際のキーは各自で取得

5. **本番環境では環境変数を直接設定**
   - Heroku, Vercel等のダッシュボードから設定

### ❌ やってはいけないこと

1. **コード内にハードコーディング**
   ```javascript
   // ❌ 絶対にやらない
   const apiKey = "sk-ant-xxxxxxxxxxxxx";
   ```

2. **Gitにコミット**
   - `.env` をコミットしない
   - コミット履歴に残さない

3. **Slackや他ツールで共有**
   - 平文でAPIキーを送らない

4. **スクリーンショットに含める**
   - デモ動画・画像で晒さない

---

## トラブルシューティング

### APIキーが読み込まれない

#### 確認1: .env ファイルの場所
- プロジェクトルート（package.jsonと同じ階層）にあるか確認

#### 確認2: dotenv のインストール
```bash
npm install dotenv
```

#### 確認3: 読み込みコード
```javascript
require('dotenv').config();
```

#### 確認4: キーの形式
- 余分なスペースがないか
- 引用符で囲んでいないか（不要）

### キーが無効と表示される

1. **キーを再確認**
   - コピペミスがないか
   - 期限切れでないか

2. **プロバイダーのダッシュボードで確認**
   - キーが有効化されているか
   - 使用制限に達していないか

3. **新しいキーを発行**
   - 古いキーを無効化
   - 新しいキーを `.env` に記入

---

## 漏洩してしまった場合の対処

### 即座に実行

1. **キーを無効化**
   - プロバイダーのダッシュボードで即座に無効化

2. **新しいキーを発行**

3. **Gitの履歴から削除**（すでにコミットした場合）
   ```bash
   # 最後のコミットを取り消し（まだプッシュしていない場合）
   git reset HEAD~1
   
   # すでにプッシュした場合（高度な操作）
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

4. **リポジトリを確認**
   - GitHub等で `.env` が表示されていないか確認
   - 表示されている場合、リポジトリを削除して作り直すことを検討

5. **請求を監視**
   - 不正利用がないか定期的にチェック

---

## まとめ

### チェックリスト

- [ ] `.env` ファイルを作成
- [ ] APIキーを `.env` に記入
- [ ] `.gitignore` に `.env` が含まれているか確認
- [ ] 環境変数が正しく読み込まれるか動作確認
- [ ] チームメンバーには構造のみ共有（実際のキーは共有しない）
- [ ] 定期的にキーをローテーション

### 重要な原則

> 「APIキーはパスワードと同じ。  
> 絶対に共有せず、安全に管理する。  
> 漏洩したら即座に無効化。」

---

**関連ドキュメント**
- [Git/GitHub初心者ガイド](./git-github-beginner-guide.md)
- [Git運用ルール](.cursor/rules/git-workflow.mdc)
- [Taskmaster設定ガイド](.cursor/rules/taskmaster/taskmaster.mdc)



