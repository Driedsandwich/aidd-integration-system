# AI駆動開発（AIDD）ワークスペース

**AI駆動開発を10倍快適にする**実践ワークスペースです。YouTubeの動画思想に基づき、シンプルで強力な開発環境を提供します。

> 「最強のルールを探す」のではなく、「使えば使うほど改善する仕組み」を作る

## 🆕 最新更新（2025-10-12）

**PDCAサイクル強制適用ルールの確立**：すべてのタスクをIssue化し、自己進化する開発体制を構築しました。

### **本日の主要成果**
- ✅ **PDCAサイクル確立**: すべてのタスクにPDCAを強制適用（Issue #48, #49）
- ✅ **Notion組織化完了**: AIDD Workspace、Knowledge Hub、Task Management、Archive
- ✅ **@Docs拡張**: ACE論文、Notion API、GitHub API、MCP（4ドキュメント）
- ✅ **Issue整理完了**: 8件クローズ（Open: 9件 → 2件）
- ✅ **知見追加**: PDCAサイクル、Issue管理ベストプラクティス、自己検証プロセス

### **確立された基盤**
- ✅ **最小構成原則**: 「最小限で開始 → 必要に応じて拡張」
- ✅ **コンテキスト崩壊の回避**: 差分更新・3段階プロセス（ACE理論）
- ✅ **自己進化システム**: メタレベルでのPDCA適用
- ✅ **自己検証機能**: ハルシネーション回避手法

### **参照ドキュメント**
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
.cursor/rules/（9ファイル、986行）
├─ cursor_rules.mdc           (46行) - ルール作成のルール
├─ general.mdc                (99行) - 基本方針、RuleOps、最小構成原則
├─ implementation.mdc        (457行) - 実装方針、ACE的アプローチ、最小構成実践
├─ knowledge.mdc             (186行) - 失敗例、再発防止、コンテキスト崩壊の認識
├─ git.mdc                   (161行) - Git/GitHub運用
├─ mcp-configuration.mdc      (42行) - MCP最小構成原則
├─ self_improve.mdc           (63行) - 自己改善サイクル
├─ environment.mdc            (12行) - 開発環境
└─ workspace-organization.mdc (22行) - ワークスペース整理

.cursor/rules/.disabled/（参照用）
└─ taskmaster/              - 高度なタスク管理（複雑性の観点から見送り）
```

### ドキュメント（docs/）

```
docs/
├─ SIMPLIFICATION_SUMMARY.md        - 簡素化プロジェクト完了サマリー
├─ simplification-final-report.md   - 詳細報告書
├─ video-philosophy-alignment-check.md - 動画思想との整合性確認
├─ over-engineering-audit-report.md - オーバーエンジニアリング監査
├─ youtube-video-analysis-integrated-report.md - YouTube動画分析
├─ notion-mcp-simple-guide.md       - Notion MCPシンプル活用ガイド
├─ git-github-beginner-guide.md     - Git/GitHub初心者ガイド
├─ PDCA_ISSUE_USAGE_GUIDE.md        - PDCA×Issue運用ガイド
├─ templates/                       - YouTube動画統合テンプレート
└─ .disabled/ops/                   - 旧Notion PIMS運用体制（参照用）
```

### プロジェクト（projects/）

```
projects/
├─ hackathon-2025/          - Steppyハッカソンアプリ（凍結中）
│   └─ docs/learnings.md    - ハッカソン固有の知見
├─ aidd-integration-system/ - 統合システム（アーカイブ）
└─ pims-template/           - PIMSテンプレート
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

```bash
# Issue作成
gh issue create --title "新機能の実装" --body "詳細..."

# 進捗報告
gh issue comment 15 --body "実装完了"

# 完了時
gh issue close 15
```

詳細: `PDCA_ISSUE_USAGE_GUIDE.md`

---

## 🔧 環境セットアップ

### 必須ツール

- **Cursor**: AI駆動コードエディタ
- **GitHub Desktop**: Git GUI（コマンド不要）
- **gh CLI**: GitHub操作（任意、自然言語で指示可能）

### 推奨ツール

- **Notion**: データ保存・可視化（MCP経由）
- **Claude Code**: 補助的なAIツール

### 環境変数（.env）

```env
# AI Provider API Keys
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
PERPLEXITY_API_KEY=

# Notion（MCP使用時）
NOTION_API_KEY=
```

詳細: `docs/environment-setup-guide.md`

---

## 🔄 今後の拡張（必要に応じて）

- 📋 Notion MCP設定（Week 1計画）
- 📋 @Docs試験導入（3-5件）
- 📋 定期監査の継続（3ヶ月ごと）

詳細: [Week 1実行計画](docs/WEEK1_EXECUTION_PLAN.md)

---

## 📊 開発状況

### 最近の主要プロジェクト

- ✅ **オーバーエンジニアリング監査と簡素化**（Issue #47、2025-10-12完了）
  - ルール体系を800行→505行に簡素化（-37%）
  - 過剰な管理システムを削除、中核機能に集中
  - 詳細: [SIMPLIFICATION_SUMMARY.md](docs/SIMPLIFICATION_SUMMARY.md)

- ✅ **最小構成原則の確立**（2025-10-12）
  - 「最小限で開始→必要に応じて拡張」を体系化
  - 開発全般に適用可能な判断基準を確立

- ✅ **ACE理論の統合**（2025-10-12〜13）
  - Stanford発表の最新研究を統合
  - コンテキスト崩壊の回避、差分更新の原則化

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

- [PDCA×Issue運用ガイド](PDCA_ISSUE_USAGE_GUIDE.md)
- [Git/GitHub初心者ガイド](docs/git-github-beginner-guide.md)
- [環境セットアップガイド](docs/environment-setup-guide.md)

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

**最終更新**: 2025-10-13  
**開発環境**: Cursor 1.7 + Claude Sonnet 4.5
