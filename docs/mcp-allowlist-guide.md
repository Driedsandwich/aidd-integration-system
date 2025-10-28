# MCP Allowlist設定ガイド

このガイドは、MCP（Model Context Protocol）のAllowlist設定について説明します。

> **重要**: Allowlist設定は、MCPサーバー（特にfilesystem）がアクセスできるディレクトリを制限するセキュリティ機能です。

---

## 🎯 Allowlistとは

### 概要

**Allowlist（許可リスト）**:
- MCPサーバーがアクセスできるディレクトリを指定
- セキュリティ保護のため、制限的に設定する
- filesystem MCPサーバーで特に重要

---

### 設定場所

**mcp.jsonのfilesystemサーバー設定**:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\AI\\workspaces",      ← Allowlistディレクトリ（例）
        "C:\\Users\\username\\Documents"  ← 複数指定可能
      ]
    }
  }
}
```

**説明**:
- `args`配列の3番目以降がAllowlistディレクトリ
- 指定したディレクトリとそのサブディレクトリにアクセス可能
- 指定外のディレクトリはアクセス不可

---

## 🔒 セキュリティ考慮事項

### 推奨設定

**最小権限の原則**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\AI\\workspaces\\aidd-integration-system"  ← プロジェクトディレクトリのみ
      ]
    }
  }
}
```

**理由**:
- ✅ 必要最小限のアクセス権限
- ✅ 誤操作による被害を最小化
- ✅ セキュリティリスク低減

---

### 危険な設定

**ルートディレクトリ指定**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/"  ← Windows: C:\, Mac/Linux: / （危険！）
      ]
    }
  }
}
```

**問題**:
- ❌ システム全体にアクセス可能
- ❌ 誤操作でシステムファイル削除の可能性
- ❌ プライバシーリスク（全ファイル閲覧可能）

**推奨**: ❌ **使用しない**

---

## 📋 環境別の推奨設定

### 個人利用（単一プロジェクト）

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\AI\\workspaces\\aidd-integration-system"
      ]
    }
  }
}
```

**特徴**: プロジェクトディレクトリのみアクセス

---

### 個人利用（複数プロジェクト）

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\AI\\workspaces"  ← workspacesディレクトリ全体
      ]
    }
  }
}
```

**特徴**: 複数プロジェクト間で移動可能

---

### 組織利用（共有プロジェクト）

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Projects\\shared-project"  ← 共有プロジェクトのみ
      ]
    }
  }
}
```

**特徴**: 共有プロジェクト以外にアクセス不可

---

## 🔄 マルチデバイス同期の考慮

### Allowlist設定の扱い

**結論**: ✅ **デバイスごとに個別設定が推奨**

**理由**:
- パスがデバイスごとに異なる（Windows: `C:\`, Mac: `/Users/`）
- 環境ごとに必要なディレクトリが異なる
- mcp.jsonは`.gitignore`で除外（Git管理外）

---

### 推奨運用

**各デバイスでの設定**:

**メインPC（Windows）**:
```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\AI\\workspaces"]
```

**サブPC（Windows）**:
```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", "D:\\Projects"]
```

**MacBook**:
```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Projects"]
```

**同期不要**: 各デバイスのパス構造に合わせて個別設定

---

## 💡 ベストプラクティス

### 1. プロジェクトディレクトリのみ指定

```json
"args": [
  "-y",
  "@modelcontextprotocol/server-filesystem",
  "C:\\AI\\workspaces\\aidd-integration-system"
]
```

**メリット**:
- ✅ セキュリティ最高
- ✅ 誤操作リスク最小
- ✅ プライバシー保護

**デメリット**:
- プロジェクト外のファイルにアクセス不可

---

### 2. workspacesディレクトリを指定

```json
"args": [
  "-y",
  "@modelcontextprotocol/server-filesystem",
  "C:\\AI\\workspaces"
]
```

**メリット**:
- ✅ 複数プロジェクト間で移動可能
- ✅ 柔軟性高

**デメリット**:
- セキュリティリスク若干増加（workspaces内全体）

---

### 3. 読み取り専用ディレクトリの追加

```json
"args": [
  "-y",
  "@modelcontextprotocol/server-filesystem",
  "C:\\AI\\workspaces\\aidd-integration-system",
  "C:\\AI\\reference"  ← 読み取り専用（参考資料等）
]
```

**メリット**:
- ✅ 参考資料にアクセス可能
- ✅ プロジェクト外のリソース活用

**注意**: 書き込みも可能なため、誤操作に注意

---

## ❓ よくある質問

### Q1: Allowlistは必須ですか？

**A**: filesystem MCPサーバーを使用する場合は必須です。

**理由**:
- filesystemサーバーはAllowlistなしで起動できない
- セキュリティ保護のための仕様

---

### Q2: Allowlistは何個まで指定できますか？

**A**: 制限なし（複数指定可能）

**例**:
```json
"args": [
  "-y",
  "@modelcontextprotocol/server-filesystem",
  "C:\\AI\\workspaces",
  "C:\\Projects",
  "C:\\Documents"
]
```

**推奨**: 2-3個以内（管理の簡便性）

---

### Q3: デバイスごとにAllowlistが違っても大丈夫？

**A**: はい、問題ありません。

**理由**:
- mcp.jsonは`.gitignore`で除外（各デバイス固有）
- パス構造はデバイスごとに異なるのが正常
- ルールファイル（`.cursor/rules/`）のみ同期される

---

### Q4: Allowlistを変更したら再起動が必要？

**A**: はい、Cursorの再起動が必要です。

**手順**:
1. `.cursor/mcp.json` を編集
2. Cursorを再起動
3. MCP設定が反映される

---

## 🔗 関連ドキュメント

- [QUICK_START.md](../QUICK_START.md) - セットアップ手順
- [environment-setup-guide.md](environment-setup-guide.md) - 環境セットアップ詳細
- [mcp-configuration.mdc](../.cursor/rules/mcp-configuration.mdc) - MCP設定ルール

---

## 📝 テンプレート

### 個人利用向けテンプレート

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "<YOUR_PROJECT_PATH>"  ← ここを編集
      ]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "fetch-mcp", "stdio"]
    }
  }
}
```

**YOUR_PROJECT_PATH の例**:
- Windows: `C:\\AI\\workspaces\\aidd-integration-system`
- Mac: `/Users/username/Projects/aidd-integration-system`

---

**最終更新**: 2025-10-21  
**対象**: Allowlist設定を理解したい全ユーザー
