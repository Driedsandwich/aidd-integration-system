---
name: PDCA - オーバーエンジニアリング監査
about: 複雑性の監査と簡素化を記録するテンプレート
title: "[PDCA] オーバーエンジニアリング監査と簡素化"
labels: pdca-cycle, simplification, audit
---

## 🎯 目的・背景

**目的**: AI駆動開発の動画思想からの逸脱を検出し、過剰実装を撤収してシンプル運用に回帰する

**背景**:
- 2024年6月27日公開の動画「AI駆動開発を10倍快適にする」の思想を基に構築
- 約3ヶ月経過後、エンタープライズレベルの複雑性に膨張
- 非エンジニアユーザーにとって理解困難・運用不可能な状態

**成功基準**:
- [ ] ルール構成を800行 → 400行以下に削減
- [ ] 非エンジニアでも理解可能な構造
- [ ] 動画の中核思想（RuleOps + Issue管理）への回帰
- [ ] 手戻りなし（Git履歴による安全性確保）

---

## 📋 Plan（計画）

### 監査で検出された過剰実装

#### 🔴 レベル3: 即座撤収
1. **problem_detection_system.mdc** (86行)
   - メタ管理システム（管理のための管理）
   - 成功指標95%、Phase 1-3実装計画
   - 動画思想にない概念

2. **SubChat並行開発システム** (knowledge.mdc内)
   - 統括役、最大5チャット並行
   - ChatGPTのような対話から乖離

3. **Notion統合PIMS** (docs/ops/: 9ファイル、33KB)
   - ポストモーテム、SLO評価、監査ログ
   - エンタープライズレベル（個人開発に過剰）
   - **判断**: MCP経由の読み書き機能のみ保持、運用体制は撤収

#### 🟡 レベル2: 簡素化
4. **knowledge.mdc** (200行 → 50行)
   - SubChat/統括役/マルチデバイス/ハッカソン関連削除

5. **Git運用ルール** (396行 → 100行)
   - git-workflow.mdc + github.mdc を統合
   - Taskmaster言及削除

#### Taskmaster評価
- **有用な設計思想**: PRD駆動、MVP vs Production
- **処理**: `.disabled/`へ移動、思想は他ルールに反映

### 実行計画（段階的・手戻り防止）

**Phase 1**: 現状スナップショット取得 ✅
- Git commit済み

**Phase 2**: 評価と抽出
- Taskmasterの有用要素抽出
- 各ルールの技術的評価

**Phase 3**: 撤収実行
1. Taskmaster → .disabled/
2. problem_detection_system.mdc削除
3. knowledge.mdc簡素化
4. Git運用ルール統合
5. docs/ops/ → .disabled/

**Phase 4**: 新ルール反映
- implementation.mdcに有用思想を統合
- 動画思想の明文化

**Phase 5**: 検証・完了
- ルール総行数確認
- 動作確認
- 完了報告

---

## 🛠️ Do（実行）

### 実行ログ

#### 2025-10-12 開始

**実行者**: Cursor AI Agent
**作業環境**: Windows, Cursor 1.7.44

**Step 1**: 監査実施 ✅
- 全ルールファイルの読み込み・分析
- 行数・複雑性の定量化
- 報告書作成: `docs/over-engineering-audit-report.md`

**Step 2**: スナップショット取得 ✅
```bash
git add docs/
git commit -m "docs: add comprehensive analysis reports before simplification"
# Commit: 05a9805
```

**Step 3**: Taskmaster移動（進行中）
```bash
mkdir -p .cursor/rules/.disabled
# git mv .cursor/rules/taskmaster .cursor/rules/.disabled/
# → ユーザーが中断（Issue作成を優先）
```

**Step 4**: GitHub Issue作成 ✅
- Issue #47作成
- PDCAテンプレート作成

---

## ✅ Check（検証）

### 検証項目

#### 数値目標
- [ ] ルールファイル数: 9個 → 7個以下
- [ ] 総行数: 約800行 → 約400行以下
- [ ] knowledge.mdc: 200行 → 50行以下
- [ ] Git運用: 396行 → 100行以下

#### 品質目標
- [ ] 動画の4要素を保持
  - [ ] ルール改善サイクル（RuleOps）
  - [ ] Issue管理でPDCA
  - [ ] Docs活用
  - [ ] MCP（必要に応じて）
- [ ] 非エンジニアでも理解可能
- [ ] 自然言語ベースの対話
- [ ] 手戻りなし（Git履歴で確認）

#### 動作確認
- [ ] Cursorでルールが正常に読み込まれる
- [ ] Notion MCP経由のアクセス可能
- [ ] GitHub Issue管理が機能

---

## 🔄 Act（改善・定着）

### 再発防止策

#### ルールOpsへの組み込み

**general.mdcに追加**:
```markdown
## 複雑性の監視

### 定期監査（3ヶ月ごと）
- [ ] ルール総行数の確認（目標: 400行以下）
- [ ] 動画思想との照合
- [ ] 非エンジニア視点でのレビュー

### 複雑性閾値
- ルールファイル: 7個以下
- 単一ファイル: 100行以下（例外: 詳細ガイド）
- 新規概念導入時: 必ず正当性を評価

### 警告サイン
- 「管理のための管理」の出現
- 非エンジニアに説明困難な概念
- 動画思想にない要素の追加
```

#### 新規機能導入の判断基準

**implementation.mdcに追加**:
```markdown
## 新機能導入の判断基準

### 導入前チェック
1. **必要性**: 既存機能で代替不可能か？
2. **複雑性**: 非エンジニアでも理解可能か？
3. **思想整合**: 動画の中核思想に合致するか？
4. **保守性**: 将来の維持コストは妥当か？

### MVP原則
- プロトタイプ: 速度優先、完璧を求めない
- 本番: 必要最小限の品質で開始
- 過剰実装は段階的に削減

### 撤収基準
- 使用頻度が低い（週3回未満）
- 運用負荷が高い
- 複雑性が価値を上回る
```

### 知見の蓄積

**knowledge.mdcに追加**（簡素化後）:
```markdown
### オーバーエンジニアリング監査（2025-10-12）

**失敗例**: 動画思想から逸脱し、エンタープライズレベルに複雑化
- SubChat並行開発システム
- 問題発見自動化システム
- Notion統合PIMS（ポストモーテム/SLO）

**根本原因**:
1. 機能追加の連鎖（問題発見 → 自動化 → 品質管理 → ...）
2. ハッカソン等の特殊プロジェクトの標準化
3. 非エンジニア視点の欠如

**再発防止ルール**:
1. 定期監査（3ヶ月ごと）
2. 新機能導入時の判断基準適用
3. MVP原則の徹底
4. 複雑性閾値の設定

**学習効果**: 
- シンプルさの価値を再認識
- 「管理のための管理」の回避
- 動画思想への回帰の重要性
```

### 完了条件（DoD）

- [ ] すべての撤収作業完了
- [ ] Git commit済み（各Phase）
- [ ] 数値目標達成
- [ ] 動作確認完了
- [ ] 再発防止策の実装
- [ ] knowledge.mdcへの記録
- [ ] Issue #47のクローズ

---

## 📝 進捗メモ

### 2025-10-12 11:00
- 監査開始
- 報告書作成完了
- ユーザー承認取得

### 2025-10-12 11:30
- スナップショットcommit完了
- Issue #47作成
- PDCAテンプレート作成

### 次のアクション
1. Taskmaster移動の再開
2. problem_detection_system.mdc削除
3. （以降の作業を順次記録）

---

## 📚 関連ドキュメント

- [オーバーエンジニアリング監査報告書](../docs/over-engineering-audit-report.md)
- [YouTube動画分析統合報告書](../docs/youtube-video-analysis-integrated-report.md)
- [動画トランスクリプト原文](./video-transcript.md)（作成予定）

---

## 🏷️ ラベル管理

- `pdca-cycle`: PDCAサイクル管理
- `simplification`: 簡素化プロジェクト
- `audit`: 監査
- `over-engineering`: オーバーエンジニアリング
- `refactoring`: リファクタリング

