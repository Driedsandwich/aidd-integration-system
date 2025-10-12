# AI駆動開発（AIDD）ワークスペース

**AI駆動開発を10倍快適にする**実践ワークスペースです。YouTubeの動画思想に基づき、シンプルで強力な開発環境を提供します。

> 「最強のルールを探す」のではなく、「使えば使うほど改善する仕組み」を作る

## 🆕 最新更新（2025-10-12）

**最小構成原則を確立**：MCP設定での試行錯誤から学んだ教訓を、開発全般に適用できる原則として体系化しました。

- ✅ **原則確立**: 「最小限で開始 → 必要に応じて拡張」
- ✅ **3つのルールに統合**: general.mdc、implementation.mdc、knowledge.mdc
- ✅ **実践ガイド**: 具体例、判断フロー、チェックリスト
- 📄 **詳細報告**: [最小構成原則確立プロジェクト完了報告](docs/2025-10-12-minimal-configuration-establishment.md)

---

## 🎯 中核思想（動画ベース）

### 1. ルール改善サイクル（RuleOps） ✅

```
指示理解 → 実行 → エラー → フィードバック 
→ 解決策整理 → ルール反映 → 次の指示
```

**実装**: `.cursor/rules/`配下のルールが自動的に改善されます

### 2. 最小構成原則 ✅

```
最小限で開始 → 動作確認 → 必要性評価 → 段階的拡張
```

**実装**: `general.mdc`と`implementation.mdc`で実践ガイド提供

**重要**: 
- 「将来のため」は実装しない
- 「管理のための管理」を避ける
- 既存の方法で不可能な場合のみ追加

### 3. Issue管理でPDCA ✅

```
Plan（Issue作成）→ Do（実装）→ Check（検証）→ Act（改善）
```

**実装**: GitHub Issueで作業を可視化・管理します

### 4. Docs活用 ⚠️

```
@docsに最新ドキュメントを登録
ライブラリの仕様を正確に参照
```

**実装**: これから拡張予定

### 5. MCP（必要に応じて） ✅

```
コアサーバーのみ（4-6個）
段階的拡張方針
シンプルで安定した構成
```

**実装**: `mcp-configuration.mdc`で最小構成原則を確立

---

## 📁 ディレクトリ構成

### ルール（.cursor/rules/）

```
.cursor/rules/（9ファイル、770行）
├─ cursor_rules.mdc           (46行) - ルール作成のルール
├─ general.mdc                (69行) - 基本方針、RuleOps、最小構成原則
├─ self_improve.mdc           (63行) - 自己改善サイクル
├─ environment.mdc            (12行) - 開発環境
├─ implementation.mdc        (241行) - 実装方針、PRD駆動、MVP原則、最小構成実践
├─ knowledge.mdc             (114行) - 失敗例と再発防止、最小構成原則の確立
├─ git.mdc                   (161行) - Git/GitHub運用
├─ mcp-configuration.mdc      (42行) - MCP最小構成原則
└─ workspace-organization.mdc (22行) - ワークスペース整理

.cursor/rules/.disabled/（無効化・参照用）
├─ taskmaster/              - Taskmaster rules（複雑性の観点から見送り）
└─ git-workflow.mdc.old     - 旧Git運用ルール
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

## 📊 プロジェクト状態

### 完了したプロジェクト

- ✅ **ルール改善サイクル構築**（Issue #6）
- ✅ **Issue管理・PDCAサイクル実装**（Issue #7）
- ✅ **統合運用システム実装**（Issue #8）
- ✅ **GitHubリポジトリ統合**（Issue #9）
- ✅ **AI駆動開発実践ガイド統合**（Issue #10）
- ✅ **Issue管理システム構築**（Issue #11）
- ✅ **オーバーエンジニアリング監査と簡素化**（Issue #47）

### 進行中のプロジェクト

- 🔄 **ClaudeCodeリファクタリング**（Issue #12）
- 🔄 **ハッカソン最終調整**（Issue #13）
- 🔄 **Vercelデプロイ修復**（Issue #14）

---

## 📈 簡素化プロジェクトの成果

**実施日**: 2025年10月12日  
**Issue**: #47（クローズ済み）

### 削減実績

| 指標 | Before | After | 削減率 |
|------|--------|-------|--------|
| ルールファイル数 | 10個 | **8個** | **-20%** |
| 総行数 | ~800行 | **505行** | **-37%** |
| knowledge.mdc | 200行 | **67行** | **-67%** |
| Git運用 | 396行 | **130行** | **-67%** |

### 撤収した過剰実装

- ❌ problem_detection_system（メタ管理システム）
- ❌ SubChat並行開発システム
- ❌ 統括役システム
- ❌ Notion PIMS運用体制（ポストモーテム/SLO）

### 保持した中核機能

- ✅ ルール改善サイクル（RuleOps）
- ✅ Issue管理PDCA
- ✅ 基本的な失敗例と再発防止
- ✅ シンプルなGit運用

詳細: `docs/SIMPLIFICATION_SUMMARY.md`

---

## 🎓 参考資料

### YouTube動画（元ネタ）

**【実践】AI駆動開発を10倍快適にする【AIDD】**  
公開日: 2024年6月27日  
URL: https://www.youtube.com/watch?v=Uk1qB_-RAps

### 分析報告書

- `docs/youtube-video-analysis-integrated-report.md` - 動画内容の体系的整理
- `docs/video-philosophy-alignment-check.md` - 動画思想との整合性確認

### AI駆動開発ガイド

- `PDCA_ISSUE_USAGE_GUIDE.md` - Issue×PDCAの実践ガイド
- `docs/git-github-beginner-guide.md` - Git/GitHub初心者ガイド
- `docs/environment-setup-guide.md` - 環境セットアップガイド

---

## 🔄 定期監査

**次回監査予定**: 2026年1月12日（3ヶ月後）

### 監査項目
- [ ] ルール総行数（目標: 500行以下）
- [ ] 動画思想との照合
- [ ] 非エンジニア視点でのレビュー
- [ ] 新たな過剰実装の検出

---

## 🚀 今後の拡張（必要に応じて）

### 短期（1-2週間）
- [ ] Notion MCP設定
- [ ] @Docs試験導入（3-5件）

### 中期（1-3ヶ月）
- [ ] Cursor 1.7 Hooks機能評価
- [ ] MCPエコシステム活用

### 長期（3ヶ月〜）
- [ ] Team Rules評価（組織展開時）
- [ ] 定期監査の継続実施

---

## 📝 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

---

## 🙏 謝辞

本ワークスペースは、以下の知見・ツールに基づいて構築されています：

- **YouTube動画**: 「AI駆動開発を10倍快適にする」（2024/06/27）
- **Cursor**: AI駆動コードエディタ
- **MCP**: Model Context Protocol
- **GitHub**: Issue管理、Git履歴管理
- **Notion**: データ保存・可視化（MCP経由）

---

**最終更新**: 2025年10月12日  
**メンテナー**: Driedsandwich  
**開発環境**: Cursor 1.7.44 + Claude Sonnet 4.5
