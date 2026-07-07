> 📦 **アーカイブ済み（2026-07-08）** — 全プロジェクト棚卸しにより正式クローズ。開いているIssue/PRは同日整理済み。経緯の記録は本人管理のprivate台帳（claudecode-workspace/task_rescue_closeouts_2026-07-08.md）参照。再開する場合は Settings から unarchive してください。

# AI駆動開発（AIDD）ワークスペース

**AI駆動開発を10倍快適にする**実践ワークスペースです。YouTubeの動画思想に基づき、シンプルで強力な開発環境を提供します。

> 「最強のルールを探す」のではなく、「使えば使うほど改善する仕組み」を作る

---

## 🚀 導入方法（2分で開始）

### 方法1: Cursorに任せる（推奨・最速）

**Cursorのチャットに入力**:

```
このリポジトリを導入してください：
https://github.com/Driedsandwich/aidd-integration-system

私の環境はWindowsです。
手順を教えてください。
```

Cursorが自動で実行します：
- ✅ リポジトリFork
- ✅ ローカルClone
- ✅ MCP設定作成
- ✅ 完了報告

**詳細**: [QUICK_START.md](QUICK_START.md)

---

### 方法2: セットアップスクリプト（CLI操作に慣れている場合）

```bash
# 1. Fork & Clone
gh auth login
gh repo fork Driedsandwich/aidd-integration-system --clone=true
cd aidd-integration-system

# 2. セットアップ実行
python scripts/setup.py

# 3. APIキー設定
# .cursor/mcp.json を編集

# 4. Cursorで開く
cursor .
```

**詳細**: [QUICK_START.md](QUICK_START.md)

---

## 🤝 コミュニティ貢献

### ブラッシュアップ案の提案

**Cursorで実行**:

```
「GitHubにIssueを作成してください：
タイトル: [提案] xxx
内容: （提案内容）」
```

**詳細**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🆕 最新更新

### 2025-10-21: AI協調実践の知見を体系化

**AI協調実践の知見を体系化**：大規模プロジェクトでの実証を基に、AI協調開発のベストプラクティスを体系化しました。

#### 主要成果
- ✅ **知見ドキュメント追加**: AI協調実践の知見を体系化（4ドキュメント、PR #58）
- ✅ **ハルシネーション対策**: 17カテゴリの原因体系と具体的対策を確立
- ✅ **AI協調パターン**: 複数AIでの役割分担と協調作業の実践パターンを記録
- ✅ **GitHub記録の完全性**: 詳細記録の標準フローとチェックリストを確立
- ✅ **AI駆動開発の5原則**: 実証済みの基本原則と厳守チェックリストを提供

#### 参照ドキュメント
- 📄 [ハルシネーション回避手法](docs/hallucination-prevention-practices.md)
- 📄 [AI協調ベストプラクティス](docs/ai-collaboration-best-practices.md)
- 📄 [GitHub記録の完全性](docs/github-record-completeness.md)
- 📄 [AI駆動開発の5原則](docs/ai-collaboration-principles.md)

---

### 2025-10-12: PDCAサイクル強制適用ルールの確立

**PDCAサイクル強制適用ルールの確立**：すべてのタスクをIssue化し、自己進化する開発体制を構築しました。

#### 主要成果
- ✅ **PDCAサイクル確立**: すべてのタスクにPDCAを強制適用（Issue #48, #49）
- ✅ **Notion組織化完了**: AIDD Workspace、Knowledge Hub、Task Management、Archive
- ✅ **@Docs拡張**: ACE論文、Notion API、GitHub API、MCP（4ドキュメント）
- ✅ **Issue整理完了**: 8件クローズ（Open: 9件 → 2件）
- ✅ **知見追加**: PDCAサイクル、Issue管理ベストプラクティス、自己検証プロセス

#### 確立された基盤
- ✅ **最小構成原則**: 「最小限で開始 → 必要に応じて拡張」
- ✅ **コンテキスト崩壊の回避**: 差分更新・3段階プロセス（ACE理論）
- ✅ **自己進化システム**: メタレベルでのPDCA適用
- ✅ **自己検証機能**: ハルシネーション回避手法

#### 参照ドキュメント
- 📄 [PDCA確立報告](docs/2025-10-12-pdca-system-establishment-report.md)
- 📄 [Issue整理報告](docs/2025-10-12-issue-cleanup-report.md)
- 📄 [セッション学習記録](docs/2025-10-12-session-learnings.md)
- 📄 [最小構成原則](docs/2025-10-12-minimal-configuration-establishment.md)
- 📄 [ACE分析](docs/2025-10-12-ace-new-video-analysis.md)

---

## 🎯 中核思想

### 1. ルール改善サイクル（RuleOps）

```
実行 → エラー → 振り返り → ルール反映 → 改善
```

`.cursor/rules/`配下のルールが使用を通じて自動的に改善されます。

### 2. 最小構成原則 + コンテキスト崩壊の回避

```
最小限で開始 → 動作確認 → 必要性評価 → 差分更新で拡張
```

**重要な原則**:
- 「将来のため」は実装しない
- ファイル全体の書き換えを避ける（差分更新）
- 「管理のための管理」を避ける

### 3. Issue管理でPDCA

```
Plan（Issue作成）→ Do（実装）→ Check（検証）→ Act（改善）
```

大きな作業はGitHub Issueで可視化・管理します。

---

## 📁 ディレクトリ構成

### ルール（.cursor/rules/）

```
.cursor/rules/（10ファイル、1,597行）
├─ cursor_rules.mdc           (46行) - ルール作成のルール
├─ general.mdc                (99行) - 基本方針、RuleOps、最小構成原則
├─ implementation.mdc        (457行) - 実装方針、ACE的アプローチ、最小構成実践
├─ knowledge.mdc             (186行) - 失敗例、再発防止、コンテキスト崩壊の認識
├─ git.mdc                   (161行) - Git/GitHub運用
├─ mcp-configuration.mdc      (42行) - MCP最小構成原則
├─ self_improve.mdc           (63行) - 自己改善サイクル
├─ environment.mdc            (12行) - 開発環境
├─ workspace-organization.mdc (22行) - ワークスペース整理
└─ auto-feedback.mdc         (611行) - AI自動フィードバック提案機能

.cursor/rules/.disabled/（参照用）
└─ taskmaster/              - 高度なタスク管理（複雑性の観点から見送り）
```

### ドキュメント（docs/）

```
docs/
├─ hallucination-prevention-practices.md - ハルシネーション回避手法（完全版）
├─ ai-collaboration-best-practices.md    - AI協調ベストプラクティス
├─ github-record-completeness.md         - GitHub記録の完全性
├─ ai-collaboration-principles.md        - AI駆動開発の5原則
├─ issue-management-best-practices.md    - Issue管理ベストプラクティス
├─ parallel-pr-review-strategy.md        - 並行PR戦略
├─ failure-case-recovery-best-practices.md - 失敗事例と再発防止
├─ pr-issue-template-best-practices.md   - PRテンプレート・Issueテンプレート
├─ ace-context-management-practices.md   - ACE実践
├─ hierarchical-readme-structure.md      - README階層体系
├─ large-document-quality-assurance.md   - 大規模文書品質保証
├─ tool-migration-guide.md               - ツール移行ガイド
├─ mcp-allowlist-guide.md                - MCP Allowlist設定ガイド
├─ SIMPLIFICATION_SUMMARY.md             - 簡素化プロジェクト完了サマリー
├─ simplification-final-report.md        - 詳細報告書
├─ video-philosophy-alignment-check.md   - 動画思想との整合性確認
├─ over-engineering-audit-report.md      - オーバーエンジニアリング監査
├─ youtube-video-analysis-integrated-report.md - YouTube動画分析
├─ notion-mcp-simple-guide.md            - Notion MCPシンプル活用ガイド
├─ git-github-beginner-guide.md          - Git/GitHub初心者ガイド
├─ PDCA_ISSUE_USAGE_GUIDE.md             - PDCA×Issue運用ガイド
├─ templates/                            - YouTube動画統合テンプレート
└─ archive/                              - アーカイブ
```

---

## 🚀 使い方（非エンジニア向け）

### 基本的なワークフロー

```
1. Cursorに自然言語で指示
   「ユーザー認証機能を追加してください」
   ↓
2. Cursorがコードを生成
   ↓
3. GitHub Desktopで差分を確認
   ↓
4. コミット（Conventional Commits形式）
   ↓
5. 大きな作業はGitHub Issueで管理
   ↓
6. 問題があればルールに自動記録（RuleOps）
```

### GitHub Issue管理

**小さな作業**: チャット内で完結  
**大きな作業**: Issueで管理

詳細: [PDCA×Issue運用ガイド](PDCA_ISSUE_USAGE_GUIDE.md)

---

## 📚 参考資料

### YouTube動画（[数理の弾丸⚡️京大博士のAI解説](https://www.youtube.com/@mathbullet)）

1. **【実践】AI駆動開発を10倍快適にする【AIDD】**（2024-06-27公開）
   - URL: https://www.youtube.com/watch?v=Uk1qB_-RAps
   - 分析: [動画分析統合レポート](docs/youtube-video-analysis-integrated-report.md)

2. **コンテキストエンジニアリングの基礎と最新【Agentic Context Engineering】**（2025-10-13閲覧）
   - URL: https://www.youtube.com/watch?v=PWOJ0QANGsA
   - 分析: [ACE新動画分析レポート](docs/2025-10-12-ace-new-video-analysis.md)

### 学術論文

- **Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models**
  - 著者: Stanford University, SambaNova Systems, UC Berkeley
  - arXiv: https://arxiv.org/html/2510.04618v1

### 実践ガイド

#### 導入・セットアップ
- [クイックスタート](QUICK_START.md) - **まずここから！**
- [環境セットアップガイド](docs/environment-setup-guide.md)
- [MCP Allowlist設定ガイド](docs/mcp-allowlist-guide.md)

#### コミュニティ・運用
- [コミュニティ貢献ガイド](CONTRIBUTING.md)
- [PDCA×Issue運用ガイド](PDCA_ISSUE_USAGE_GUIDE.md)
- [Git/GitHub初心者ガイド](docs/git-github-beginner-guide.md)

#### ツール・移行
- [ツール移行ガイド](docs/tool-migration-guide.md)

---

## 🔄 定期監査

**次回監査予定**: 2026年1月12日（3ヶ月後）

### 監査項目
- [ ] ルール総行数（目標: 1000行以下）
- [ ] 動画思想との照合
- [ ] 非エンジニア視点でのレビュー
- [ ] 新たな過剰実装の検出

---

## 📝 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

---

**最終更新**: 2025-10-21  
**開発環境**: Cursor 1.7 + Claude Sonnet 4.5
