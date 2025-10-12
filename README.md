# PIMS - Product Integration Management System

**PIMS**（Product Integration Management System）は、AI駆動開発（AIDD）における知見蓄積とタスク管理を統合したシステムです。Notion中心のタスク管理とGitHub連携により、開発の全プロセスを可視化・自動化します。

---

## 🎯 主要機能

### 1. GitHub ⇄ Notion 統合
- **片方向同期（自動）**: GitHub Issues/PR → Notion Tasks DB
- **双方向同期（限定）**: Notion Tasks ⇄ GitHub（assignees/due、preview運用中）
- **監査ログ**: 全同期イベントをNotion Sync Logs DBに記録
- **SLO自動評価**: 日次/週次でsuccessRate算出、99%未達時に自動Issue起票

### 2. 自動化ワークフロー（12種類）
- **同期**: `gh-to-notion.yml`（GitHub→Notion）、`notion-to-gh-assign.yml`（Notion→GitHub、preview）
- **監査**: `slo-evaluate.yml`（SLO評価＋未達時アラート）
- **メトリクス**: `weekly-report.yml`（週次集計）、`sync-metrics.yml`（日次集計）
- **運用**: `registry-update.yml`（Notionページ棚卸し）、`cleanup-propose.yml`（削除候補提案）
- **整備**: `backfill-assignees-due.yml`（欠損データ補完）、`seed-dummy-data.yml`（テストデータ）

### 3. Notion構成
- **PIMS MCP Hub**（中央管理ページ）
  - PIMS Tasks（GitHub Issue/PR同期先）
  - PIMS Sync Logs（同期実行履歴・障害追跡）
  - PIMS Sync Metrics（週次/日次集計・SLO可視化）
  - PIMS Projects（プロジェクト管理）
  - PIMS Knowledge（知見蓄積）
  - PIMS Registry（週次構築、Hub配下のページ/DB一覧）
  - PIMS Cleanup Queue（削除候補の提案→承認→実施）

---

## 📁 リポジトリ構成

### コアシステム
- `.github/workflows/` - GitHub Actions（12 workflows）
- `docs/ops/` - 運用ドキュメント（9ファイル）
- `.cursor/` - Cursor/MCP設定

### アーカイブ/サブプロジェクト
- `aidd-integration-system/` - 統合システム本体（埋め込みリポジトリ、.gitignoreで除外）
- `hackathon-2025/` - Steppyハッカソンアプリ（埋め込みリポジトリ、.gitignoreで除外）
- `development-docs/` - AI駆動開発実践ガイド・PDCA設計
- `docs/` - 要件・引継ぎ・アーカイブ
- `src/` - Pythonスクリプト（マルチデバイス同期、知見蓄積等）

---

## 🚀 クイックスタート

### 前提条件
- GitHubアカウント（`Driedsandwich`）
- Notionワークスペース＋Integration Token
- Cursor/MCP設定済み（`.cursor/mcp.json`）

### 初期セットアップ

#### 1. GitHub Secrets設定
Repository Settings → Secrets and variables → Actions → New repository secret

| Secret名 | 値 | 説明 |
|---------|-----|------|
| `NOTION_TOKEN` | `ntn_xxxxx...` | Notion Integration Token |
| `NOTION_TASKS_DB` | `28886723-2af9-81cd-...` | PIMS Tasks DB ID |

#### 2. Notion Integration共有
1. https://www.notion.so/my-integrations で該当Integrationを選択
2. 以下のDB/ページに「Connections」で追加:
   - PIMS MCP Hub
   - PIMS Tasks
   - PIMS Sync Logs
   - PIMS Sync Metrics
   - （他、必要に応じてProjects/Knowledge/Registry/Cleanup Queue）

#### 3. ダッシュボード作成（オプション）
`docs/ops/notion-dashboard-setup.md`の手順に従い、Notion UIでビューを作成:
- Tasks: Status Board（カンバン）、Open Tasks（テーブル）
- Logs: Last 7 Days（テーブル）、Failures Only（テーブル）
- Metrics: Weekly Trend（テーブル）

---

## 📚 ドキュメント

### 運用ガイド
- [Runbook](docs/ops/runbook.md) - 日常運用・障害対応・手動復旧
- [Notion同期](docs/ops/notion-sync.md) - 片方向同期の運用ポイント
- [ダッシュボード作成](docs/ops/notion-dashboard-setup.md) - NotionビューのUI作成手順

### 監査・セキュリティ
- [Token Policy](docs/ops/token-policy.md) - 最小権限・ローテーション方針
- [Secrets監査](docs/ops/secrets-audit.md) - Secrets棚卸し・監査チェックリスト

### 拡張計画
- [双方向ロールアウト](docs/ops/notion-to-github-rollout.md) - Notion→GitHubのPhase 1-3計画
- [Governance](docs/ops/governance.md) - Notion最上層の命名/配置/クリーンアップ

### トラブルシューティング
- [Postmortem 2025-10-10](docs/ops/postmortem-2025-10-10-notion-sync.md) - 過去の障害事例
- [Sync Logs Dashboards](docs/ops/sync-logs-dashboards.md) - Logsビュー作成詳細

### AI駆動開発ガイド
- [AI駆動開発実践ガイド](development-docs/AI駆動開発実践ガイド.md)
- [Issue管理実践ガイド](development-docs/Issue管理実践ガイド.md)
- [ルール改善サイクル実践ガイド](development-docs/ルール改善サイクル実践ガイド.md)
- [Git/GitHub初心者ガイド](docs/git-github-beginner-guide.md) - 非エンジニア向けGit入門（コマンド不要）
- [環境変数設定ガイド](docs/environment-setup-guide.md) - APIキー・機密情報の安全な管理

### YouTube動画統合テンプレート
- **[GitHub: youtube-video-integration-templates](https://github.com/Driedsandwich/youtube-video-integration-templates)** 🔗
- **[すぐ使えるプロンプト](docs/templates/SIMPLE_PROMPT.md)** ⚡ - 基本版（コピペで即実行）
- [テンプレート詳細](docs/templates/) - 4段階のテンプレート（30秒版/1分版/5分版/JSON版）
- _Author: Driedsandwich / Created with Cursor (Claude Sonnet 4.5)_

---

## 🔧 運用フロー

### 日常運用
1. **GitHub Issue/PR作成** → 自動的にNotion Tasksへ同期
2. **Notion Logs DBで同期結果確認**（直近7日ビュー）
3. **Metrics DBでsuccessRate確認**（週次推移）
4. **SLO未達時**: 自動起票されたIssueで原因調査

### 週次運用（月曜日UTC 01:00-03:00）
1. **Registry更新** → Notion Hub配下をスキャン
2. **自動タグ付け** → 未分類ページにautoTag提案
3. **クリーンアップ提案** → 60日超/Temp/Otherを候補登録
4. **週次レポート** → 直近7日の集計をMetrics DBへ
5. **レビュー**: Cleanup Queue DBでproposed候補を確認→approved/rejected

### データ整備（初回のみ）
1. **バックフィル実行**: GitHub Actions → `Backfill ghAssignees/ghDue` → Run workflow
   - Input: `limit=20`（テスト）→ 確認後に`limit=50`

---

## 🛡️ 安全設計

### 非破壊原則
- **クリーンアップ**: 提案→承認→14日保留→archive→30日後削除（参照なし確認後）
- **双方向**: preview_onlyデフォルト、実適用は手動承認必須
- **冪等性**: Notion同期はghIssueNumber照合でPATCH/POST判定

### 権限最小化
- **Notion**: Integrationは必要DBのみ共有
- **GitHub Actions**: 各workflowで`contents: read`基本、書き込みは最小限（issues: write等）

### ロールバック
- **workflow無効化**: PRでファイル削除またはcron無効化
- **Notion復元**: 履歴から復元（30日以内）
- **GitHub復元**: 誤ラベル/assigneesの手動削除

---

## 📊 監視ポイント

### 日次確認
- [ ] Logs DBで`result=failure`増加がないか
- [ ] Metrics DBのsuccessRate >= 99%
- [ ] HTTP 4xx（権限）/5xx（障害）の頻度

### 週次確認
- [ ] 週次レポートの`successRate`推移
- [ ] Cleanup Queue DBの候補レビュー
- [ ] SLO未達Issueの有無（あれば原因調査）

---

## 🔗 関連リンク

- **GitHub Repository**: https://github.com/Driedsandwich/aidd-integration-system
- **Notion Hub**: https://www.notion.so/PIMS-MCP-Hub-26f867232af9814c91dbcc3498ccc33b
- **完了レポート**: [docs/completion-report-2025-10-11.md](docs/completion-report-2025-10-11.md)

---

## 📝 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

---

## 🙏 謝辞

本システムは、Cursor/MCP、GitHub Actions、Notion APIを活用し、AI駆動開発の実践知見を蓄積・活用するために構築されました。
