# 🚀 クイックスタートプロンプト（コピペ用）

**最終更新**: 2025-10-12  
**用途**: 新チャットで修士論文製作・個人開発を即座に開始

---

## ⚡ 最速スタート（小規模タスク推奨）

### **このプロンプトをコピー&ペーストして開始**

```
AI駆動開発の基盤（aidd-integration-system）が確立済みです。

【実施タスク】
[ここにタスクを記載。例: Pythonでデータ分析スクリプト作成]

【要求】
1. 新規リポジトリ作成: [task-name]
2. 基盤からルールコピー:
   - Windows: Copy-Item -Recurse ..\aidd-integration-system\.cursor .
   - Mac: cp -r ../aidd-integration-system/.cursor .
3. GitHub Issue #1作成（5分以内）
4. 実開発実行
5. 完了後Issue Close（1分）

【時間配分】
- 記録: 8分以内
- 実開発: 90%以上

【参照】
- 基盤: https://github.com/Driedsandwich/aidd-integration-system
- ルール: .cursor/rules/general.mdc, knowledge.mdc
- 運用: docs/2025-10-12-session-status.md

技術的合理性に基づき、ハルシネーションを回避しながら進行してください。
```

---

## 🎓 修士論文製作用

### **このプロンプトをコピー&ペーストして開始**

```
AI駆動開発の基盤（aidd-integration-system）を活用して修士論文製作を開始します。

【論文情報】
- タイトル: [仮タイトル]
- 分野: [研究分野]
- 期限: [提出期限]
- 進捗: [現在の状況]

【要求】
1. リポジトリ作成: master-thesis-2025
2. 基盤からルールコピー
3. プロジェクト構造:
   thesis/chapters/
   thesis/figures/
   thesis/references/
   code/（実験コード）
   data/
   notes/
4. Issue #1作成: 論文構成とチャプター計画（5分）
5. AI活用:
   - Cursor: 執筆、LaTeX
   - ChatGPT: 文献調査
   - @Docs: 参考文献参照

【時間配分】
- 記録: 10%
- 研究・執筆: 90%

【参照】
基盤: https://github.com/Driedsandwich/aidd-integration-system

次のステップを提案してください。技術的合理性に基づき、ハルシネーションを回避すること。
```

---

## 💻 個人開発プロダクト用

### **このプロンプトをコピー&ペーストして開始**

```
AI駆動開発の基盤（aidd-integration-system）を活用して個人開発を開始します。

【プロダクト情報】
- 名前: [プロダクト名]
- 概要: [一文で]
- 技術: [言語/フレームワーク]
- ターゲット: [ユーザー]
- 目標: [MVP/リリース/...]

【要求】
1. リポジトリ作成: [product-name]
2. 基盤からルールコピー
3. プロジェクト構造（技術スタック次第）
4. Issue #1作成: 機能要件とMVP計画（5分）
5. AI活用:
   - Cursor: 実装、リファクタリング
   - ChatGPT: 設計、API設計
   - ClaudeCode: 複雑実装
   - @Docs: ライブラリドキュメント

【時間配分】
- 記録: 10%
- 実装: 90%

【参照】
基盤: https://github.com/Driedsandwich/aidd-integration-system

要件定義とMVP計画を提案してください。技術的合理性に基づき、ハルシネーションを回避すること。
```

---

## 🎯 推奨開始順序

```
1. 【まず】Option A: 小規模タスク（30分-1時間）
   ↓ 基盤動作確認
   ↓
2. 【次に】Option B or C: 本格的プロジェクト
   ├─ 修士論文製作
   └─ 個人開発プロダクト
```

---

## ⚠️ 注意事項

### **絶対に守ること**
- ❌ 基盤リポジトリ（aidd-integration-system）で実開発しない
- ✅ 新規リポジトリを作成
- ✅ 基盤からルールをコピー
- ✅ リポジトリごとに完全分離

### **時間管理**
- 記録: 最小限（8分/タスク）
- 実開発: 最大限（90%以上）

### **基盤改善**
- 基盤に問題発見 → aidd-integration-systemのIssue作成
- 重要な学習 → knowledge.mdcに1-2行追記

---

## 📞 トラブル時

**基盤リポジトリに戻る**:
```
cd ../aidd-integration-system
# 新しいチャットで以下を送信:
「基盤リポジトリ（aidd-integration-system）のセッションを再開します。
docs/2025-10-12-session-status.mdを確認し、状況を報告してください。」
```

---

## ✅ 成功の定義

**小規模タスク**:
- リポジトリ作成完了
- Issue管理実践
- タスク完了
- 基盤動作確認

**本格プロジェクト**:
- 要件定義完了
- 初期Issue作成
- 開発開始
- AI活用開始

