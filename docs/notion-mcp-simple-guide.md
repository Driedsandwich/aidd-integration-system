# Notion MCP シンプル活用ガイド

## 概要

Notionを「MCP経由で読み書き可能なデータベース」として活用します。

### 目的

- GitHubリポジトリ内容の可視化
- プロジェクトメモの保存
- 知見の蓄積
- Cursor/ClaudeCodeからの自然言語アクセス

### 非推奨

- ❌ ポストモーテム運用
- ❌ SLO評価
- ❌ 監査ログ
- ❌ GitHub Actions自動化
- ❌ 手動の双方向同期

---

## セットアップ

### 1. Notion MCP Server のインストール

MCP設定ファイル（`.cursor/mcp.json`または`claude_desktop_config.json`）に追加：

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "your-notion-integration-token"
      }
    }
  }
}
```

### 2. Notion Integration の作成

1. https://www.notion.so/my-integrations へアクセス
2. 「New integration」をクリック
3. 名前を設定（例: "Cursor AI Integration"）
4. Internal Integrationを選択
5. API Keyをコピー

### 3. データベースの共有

Notionのデータベースを作成し、Integrationに共有：

1. Notion でデータベース作成
2. 右上の「Share」をクリック
3. 作成したIntegrationを選択

---

## 使い方

### Cursorから自然言語で操作

**例1: 情報の取得**
```
ユーザー: 「Notionに保存されているプロジェクト一覧を教えて」
Cursor: （Notion MCPを使って情報取得）
```

**例2: 情報の保存**
```
ユーザー: 「このプロジェクトの概要をNotionに保存して」
Cursor: （Notion MCPを使ってページ作成）
```

**例3: リポジトリ内容の確認**
```
ユーザー: 「GitHubの〇〇リポジトリは何のプロジェクト？」
Cursor: （Notionのデータベースを検索）
```

### データ構造の推奨

**シンプルなデータベース構造**:

| Name | Type | GitHub URL | Description | Tags |
|------|------|------------|-------------|------|
| Text | Select | URL | Text | Multi-select |

- **Name**: プロジェクト名
- **Type**: project/learning/experiment等
- **GitHub URL**: リポジトリURL
- **Description**: 簡単な説明
- **Tags**: カテゴリタグ

---

## ユースケース

### 1. プロジェクト管理

```
# GitHubリポジトリとNotionを紐付け
- リポジトリ名
- 目的
- 技術スタック
- 状態（active/archived/frozen）
```

### 2. 知見の蓄積

```
# knowledge.mdcの補完として
- より詳細な失敗事例
- スクリーンショット付きの記録
- 長文のポストモーテム（任意）
```

### 3. アイデア管理

```
# 新しいプロジェクトのアイデア
- 概要
- 技術的な課題
- 参考リンク
```

---

## トラブルシューティング

### MCP接続エラー

**症状**: Cursorから「Notionにアクセスできません」

**原因と対処**:
1. API Keyが正しくない → `.cursor/mcp.json`を確認
2. データベースが共有されていない → Notionで共有設定を確認
3. MCP Serverが起動していない → Cursorを再起動

### 権限エラー

**症状**: 「Permission denied」

**対処**:
1. NotionのIntegration設定で権限を確認
2. データベースの共有設定を再確認
3. 必要に応じてIntegrationを再作成

---

## 参考リンク

- [Notion API公式ドキュメント](https://developers.notion.com/)
- [MCP公式ドキュメント](https://modelcontextprotocol.io/)
- [Cursor MCP統合ガイド](https://docs.cursor.com/mcp)

---

## 関連ドキュメント

- [オーバーエンジニアリング監査報告書](./over-engineering-audit-report.md)
- [YouTube動画分析統合報告書](./youtube-video-analysis-integrated-report.md)

