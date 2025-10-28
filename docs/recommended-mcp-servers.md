# 推奨MCPサーバー構成ガイド

このガイドは、AIDD Integration Systemで実証済みのMCP（Model Context Protocol）サーバー構成について説明します。

> **設計思想**: 最小構成原則に基づく実証済みMCP構成の共有

---

## 🎯 実証済みMCP構成

### 現在の構成（実測値）

**総MCP数**: 6種類  
**構成期間**: 実証済み（安定運用中）

---

## 📋 MCP構成詳細

### Core MCP（必須）

#### 1. GitHub MCP
**用途**: GitHub操作の完全自動化  
**必要性**: ✅ **必須**（AIDD Integration Systemで必須）

**主要機能**:
- Issue/PRの作成・管理
- リポジトリ操作
- ブランチ管理
- コミット操作

**選定理由**:
- AIDD Integration SystemのGit/GitHub運用で必須
- 自動化により開発効率が大幅向上

---

### Utility MCP（汎用）

#### 2. Fetch MCP
**用途**: Web情報取得・URL処理  
**必要性**: ⏸️ **推奨**（汎用性高）

**主要機能**:
- Webページの内容取得
- URL処理・検証

**選定理由**:
- 最新情報の取得に必須
- リサーチ作業の効率化
- 軽量で安定動作

#### 3. Time MCP
**用途**: 日時操作・タイムゾーン変換  
**必要性**: ⏸️ **推奨**（記録の正確性）

**主要機能**:
- タイムスタンプ生成
- 日時計算
- タイムゾーン変換

**選定理由**:
- 記録の正確性向上
- タイムスタンプの統一
- 軽量で安定動作

#### 4. Filesystem MCP
**用途**: ファイル操作・ディレクトリ管理  
**必要性**: ⏸️ **推奨**（ファイル操作の自動化）

**主要機能**:
- ファイル読み書き
- ディレクトリ操作
- ファイル検索

**選定理由**:
- ファイル操作の自動化
- プロジェクト管理の効率化
- 注意: Allowlist設定必須（セキュリティ）

---

### Specialized MCP（専門）

#### 5. Notion MCP
**用途**: Notionデータベース操作  
**必要性**: ⏸️ **任意**（Notion使用時のみ）

**主要機能**:
- データベース操作
- ページ作成・編集
- プロパティ管理

**選定理由**:
- Notion使用時の効率化
- データ保存・可視化の自動化
- 注意: APIキー設定必須

#### 6. DeepWiki MCP
**用途**: GitHub Wiki解析  
**必要性**: ⏸️ **任意**（Wiki解析時のみ）

**主要機能**:
- GitHub Wiki解析
- 知識ベース構築

**選定理由**:
- GitHub Wiki活用時の効率化
- 知識ベースの自動構築

---

## 🎯 最小構成原則

### 必須構成（Core）
```
GitHub MCP
```
**理由**: AIDD Integration Systemで必須

### 推奨構成（Core + Utility）
```
GitHub MCP
+ Fetch MCP
+ Time MCP
+ Filesystem MCP
```
**理由**: 汎用性が高く、安定動作

### 完全構成（Core + Utility + Specialized）
```
GitHub MCP
+ Fetch MCP
+ Time MCP
+ Filesystem MCP
+ Notion MCP
+ DeepWiki MCP
```
**理由**: 全機能を活用する場合

---

## 📊 構成の特徴分析

### バランス評価
- **総MCP数**: 6種類（適切な規模）
- **構成バランス**: Core(1) + Utility(3) + Specialized(2)
- **過不足**: なし（実証済み）

### 安定性評価
- **運用期間**: 実証済み（安定運用中）
- **エラー率**: 低（安定動作）
- **メンテナンス**: 最小限

### 効率性評価
- **開発効率**: 大幅向上（GitHub操作自動化）
- **学習コスト**: 低（標準的なMCP）
- **設定コスト**: 中（APIキー設定等）

---

## 🔧 設定ガイド

### 基本設定

**mcp.json設定例**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<SET_YOUR_TOKEN>"
      }
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "fetch-mcp", "stdio"]
    },
    "time": {
      "command": "npx",
      "args": ["-y", "mcp-server-time", "--local-timezone=Asia/Tokyo"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "<YOUR_PROJECT_PATH>"
      ]
    }
  }
}
```

### セキュリティ設定

**重要**: Filesystem MCPのAllowlist設定
```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "C:\\AI\\workspaces\\aidd-integration-system"
  ]
}
```

**理由**: セキュリティ保護のため、必要最小限のディレクトリのみ指定

---

## 📈 活用状況の分析

### 高活用（推定）
- **GitHub MCP**: 必須（AIDD Integration Systemで必須）
- **Fetch MCP**: 高（リサーチ作業で頻繁使用）
- **Time MCP**: 高（記録・タイムスタンプで使用）

### 中活用（推定）
- **Filesystem MCP**: 中（ファイル操作時に使用）
- **Notion MCP**: 中（Notion使用時のみ）

### 低活用（推定）
- **DeepWiki MCP**: 低（Wiki解析時のみ）

---

## 🚀 導入推奨順序

### Phase 1: 最小構成
1. **GitHub MCP**を導入
2. 動作確認
3. 基本機能を習得

### Phase 2: 汎用機能追加
1. **Fetch MCP**を追加
2. **Time MCP**を追加
3. 動作確認

### Phase 3: 完全構成
1. **Filesystem MCP**を追加（Allowlist設定注意）
2. **Notion MCP**を追加（APIキー設定）
3. **DeepWiki MCP**を追加（必要に応じて）

---

## 🔍 トラブルシューティング

### よくある問題

#### 1. GitHub MCP認証エラー
**症状**: GitHub操作で認証エラー  
**原因**: APIトークンの設定ミス  
**解決策**: トークンの再生成・設定確認

#### 2. Filesystem MCPアクセスエラー
**症状**: ファイル操作でアクセスエラー  
**原因**: Allowlist設定の不備  
**解決策**: プロジェクトディレクトリのパス確認

#### 3. Notion MCP接続エラー
**症状**: Notion操作で接続エラー  
**原因**: APIキーの設定ミス  
**解決策**: Notion APIキーの再生成・設定確認

---

## 💡 ベストプラクティス

### 1. 段階的導入
- 最小構成から開始
- 動作確認後に追加
- 過度な導入を避ける

### 2. セキュリティ重視
- Allowlist設定を適切に行う
- APIキーは安全に管理
- 必要最小限の権限のみ付与

### 3. 定期監査
- 使用状況の確認
- 不要なMCPの削除
- 設定の最適化

---

## 📚 参考情報

### 公式ドキュメント
- [MCP公式サイト](https://modelcontextprotocol.io/)
- [GitHub MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
- [Notion MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/notion)

### 関連ガイド
- [環境セットアップガイド](environment-setup-guide.md)
- [MCP Allowlist設定ガイド](mcp-allowlist-guide.md)
- [ツール移行ガイド](tool-migration-guide.md)

---

## 🎯 まとめ

### 実証済み構成の特徴
- **総MCP数**: 6種類
- **構成バランス**: 適切
- **安定性**: 実証済み

### 推奨導入方針
1. **最小構成から開始**（GitHub MCP）
2. **段階的に追加**（Utility MCP）
3. **必要に応じて専門MCP追加**

### セキュリティ考慮
- **Allowlist設定必須**（Filesystem MCP）
- **APIキー管理重要**
- **必要最小限の権限**

---

**最終更新**: 2025-10-21  
**対象**: MCP構成を検討する全ユーザー  
**実証環境**: AIDD Integration System
