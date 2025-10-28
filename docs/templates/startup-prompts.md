# 🚀 実開発開始プロンプト（ユーザー用）

**作成日**: 2025-10-12  
**基盤**: aidd-integration-system完了  
**用途**: 新しいチャット/セッションで実開発を開始

---

## 🎯 使い方

1. **新しいCursorチャットを開く**
2. **以下のプロンプトをコピー&ペースト**
3. **[  ]部分を自分の情報に置き換え**
4. **送信して開始**

---

## 📝 Option A: 小規模タスクで基盤確認（初回推奨）

### **コピー&ペーストするプロンプト**

```
# 小規模タスクで基盤確認

## 背景
- 基盤リポジトリ（aidd-integration-system）で確立したルール・運用システムを実開発で試用
- 30分〜1時間で完結する小規模タスクから開始
- 基盤の動作確認と改善点の発見

## 実施したいタスク
[ここに具体的なタスクを記載]

例:
- 簡単なPythonスクリプト作成（データ処理、API呼び出し等）
- 既存コードのリファクタリング
- 技術調査とドキュメント作成

## 要求事項

### 1. 新規リポジトリ作成
```bash
gh repo create [task-name] --private
git clone https://github.com/[your-username]/[task-name]
cd [task-name]
```

### 2. 基盤からルールコピー
```bash
# Windows PowerShell
Copy-Item -Recurse ..\aidd-integration-system\.cursor .
Copy-Item ..\aidd-integration-system\.cursordocs .

# Mac/Linux
cp -r ../aidd-integration-system/.cursor .
cp ../aidd-integration-system/.cursordocs .
```

### 3. README作成
```markdown
# [タスク名]

## 目的
[タスクの目的]

## 参照基盤
このプロジェクトは、aidd-integration-systemのルール・運用システムを活用します。
```

### 4. GitHub Issue管理
- **最初のIssue作成**（5分以内）:
  - タイトル: [タスク名]
  - 目的: [一文]
  - 成果基準: [完了条件]
  
### 5. 実行
- タスク実行（Cursor + AI活用）
- 進捗をIssueコメントに記録（任意）

### 6. 完了
- Issue Close（1分）
- 重要な学習があれば.cursor/rules/knowledge.mdcに1-2行追記

## 時間配分
- 記録: 8分以内
- 実開発: 22-52分

## 期待される成果
- 基盤ルールの動作確認
- Issue管理の実践
- @Docs活用の体験
- 改善点の発見

## 次のステップ
- 基盤に改善が必要 → aidd-integration-systemのknowledge.mdcに追記
- 問題なし → 修士論文製作または個人開発プロダクトに進む
```

---

## 🎓 Option B: 修士論文製作開始

### **コピー&ペーストするプロンプト**

```
# 修士論文製作プロジェクト開始

## 背景
- 基盤リポジトリ（aidd-integration-system）のルール・運用システムを活用
- 修士論文製作を体系的に管理
- AI（Cursor、ChatGPT、ClaudeCode等）を活用した効率的な執筆

## 論文情報
- **タイトル**: [論文タイトル（仮）]
- **研究分野**: [分野名]
- **提出期限**: [YYYY-MM-DD]
- **現在の進捗**: [未着手/調査中/執筆中/...]

## 要求事項

### 1. リポジトリセットアップ
```bash
gh repo create master-thesis-2025 --private
git clone https://github.com/[your-username]/master-thesis-2025
cd master-thesis-2025

# ルールコピー（Windows PowerShell）
Copy-Item -Recurse ..\aidd-integration-system\.cursor .
Copy-Item ..\aidd-integration-system\.cursordocs .

# ルールコピー（Mac/Linux）
cp -r ../aidd-integration-system/.cursor .
cp ../aidd-integration-system/.cursordocs .
```

### 2. プロジェクト構造作成
```
master-thesis-2025/
├── README.md
├── .cursor/rules/
├── thesis/
│   ├── chapters/
│   ├── figures/
│   └── references/
├── code/（実験コード）
├── data/（データセット）
└── notes/（調査メモ）
```

### 3. 初期Issue作成（5分）
- **Issue #1**: 論文構成の策定
  - タイトル: 論文構成とチャプター計画
  - 本文:
    - 目的: [研究目的]
    - 背景: [研究背景]
    - 各章の概要: [章1]、[章2]、...
    - 成果基準: 構成確定、章タイトル決定
  - ラベル: planning, structure

### 4. GitHub Issue活用
- 章ごとにIssue作成
- 進捗・発見をコメント記録
- 完了時にClose
- 重要な研究知見はknowledge.mdcに追記

### 5. AI活用戦略
- **Cursor**: 論文執筆、LaTeX編集
- **ChatGPT**: 文献調査、アイデア整理
- **@Docs**: 参考文献・技術ドキュメント参照

### 6. 時間配分
- 記録: 10%以下
- 執筆・研究: 90%以上

## 期待される成果
- 体系的な論文執筆プロセス
- AI活用による効率化
- 進捗の可視化
- 研究知見の蓄積

## 次のステップ（提案してください）
- 論文構成の詳細化
- 文献調査計画
- 実験計画（必要に応じて）
```

---

## 💻 Option C: 個人開発プロダクト開始

### **コピー&ペーストするプロンプト**

```
# 個人開発プロダクト開始

## 背景
- 基盤リポジトリ（aidd-integration-system）のルール・運用システムを活用
- 個人開発プロダクトを体系的に管理
- AI駆動開発による効率的な実装

## プロダクト情報
- **プロダクト名**: [名前]
- **概要**: [一文で説明]
- **技術スタック**: [言語/フレームワーク/データベース等]
- **ターゲットユーザー**: [誰が使うか]
- **目標**: [MVP/本番リリース/...]

## 要求事項

### 1. リポジトリセットアップ
```bash
gh repo create [product-name] --private
# または公開する場合: gh repo create [product-name] --public
git clone https://github.com/[your-username]/[product-name]
cd [product-name]

# ルールコピー（Windows PowerShell）
Copy-Item -Recurse ..\aidd-integration-system\.cursor .
Copy-Item ..\aidd-integration-system\.cursordocs .

# ルールコピー（Mac/Linux）
cp -r ../aidd-integration-system/.cursor .
cp ../aidd-integration-system/.cursordocs .
```

### 2. プロジェクト構造作成（技術スタック次第）
```
[product-name]/
├── README.md
├── .cursor/rules/
├── src/（ソースコード）
├── docs/（ドキュメント）
├── tests/（テスト）
└── [package.json/requirements.txt/etc]
```

### 3. 初期Issue作成（5分）
- **Issue #1**: プロダクト要件定義とMVP計画
  - タイトル: 機能要件とMVP計画
  - 本文:
    - 目的: [なぜ作るか]
    - ターゲットユーザー: [誰が使うか]
    - 主要機能: [機能1]、[機能2]、...
    - MVP範囲: [最小限の機能]
    - 成果基準: 要件確定、MVP計画完成
  - ラベル: planning, mvp

### 4. GitHub Issue活用
- 機能ごとにIssue作成
- 実装・テスト結果をコメント記録
- 完了時にClose
- 技術知見はknowledge.mdcに追記

### 5. AI活用戦略
- **Cursor**: コード実装、リファクタリング
- **ChatGPT**: アーキテクチャ設計、API設計
- **ClaudeCode**: 複雑な実装、デバッグ
- **@Docs**: フレームワーク・ライブラリドキュメント参照

### 6. 時間配分
- 記録: 10%以下
- 実装: 90%以上

## 期待される成果
- MVP（Minimum Viable Product）の完成
- AI活用による開発速度向上
- 体系的な開発プロセス
- 技術知見の蓄積

## 次のステップ（提案してください）
- 要件定義の詳細化
- アーキテクチャ設計
- 技術スタック選定（未定の場合）
- MVP実装計画
```

---

## 🎯 プロンプト使用ガイド

### **新しいチャットでの開始手順**

1. **Cursorで新しいチャットを開く**

2. **プロンプトを選択**:
   - 初回 → Option A（小規模タスク）
   - 論文 → Option B
   - 開発 → Option C

3. **[  ]部分を置き換え**:
   - [your-username]
   - [タスク名/プロダクト名/論文タイトル]
   - その他の具体的情報

4. **プロンプトを送信**

5. **AIの提案に従って実行**

---

## ✅ 重要な原則

### **基盤リポジトリ（aidd-integration-system）**
- ✅ 待機状態（基盤改善時のみ活用）
- ✅ 実開発は行わない
- ✅ ルール・テンプレートの保管庫

### **実開発リポジトリ**
- ✅ 論文ごと、プロダクトごとに完全分離
- ✅ 基盤からルールをコピー
- ✅ GitHub Issueで管理
- ✅ 記録10%、実開発90%

### **記録の最小化**
- ✅ Issue作成: 5分
- ✅ Issue Close: 1分
- ✅ knowledge.mdc: 2分（重要時のみ）
- ❌ 報告書: 作成しない

---

## 📎 参照情報

**基盤リポジトリ**: https://github.com/Driedsandwich/aidd-integration-system  
**ルールファイル**: `.cursor/rules/`  
**テンプレート**: `.cursor/templates/`、`docs/templates/`  
**運用方針**: `docs/2025-10-12-session-status.md`

