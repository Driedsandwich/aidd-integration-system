# PIMS運用Runbook

## 概要
このRunbookは、PIMS（Notion中心のタスク管理＋GitHub連携）の日常運用手順、障害対応、手動復旧を記載します。

## ダッシュボードの見方

### 1. Notion Tasks DB
- **URL**: https://www.notion.so/28886723-2af9-81cd-8f68-e6fb0899f940
- **ビュー例**:
  - カンバン: `ghState`または`ステータス`でグループ化（open/closed）
  - 未完了テーブル: フィルタ `ghState = open`、並び替え `last_edited_time desc`
- **キー項目**: `ghIssueNumber`、`ghUrl`、`ghState`、`ghAssignees`、`ghDue`、`ghRepo`

### 2. Notion Sync Logs DB
- **URL**: https://www.notion.so/28886723-2af9-8177-924b-ea981a2f6dfa
- **ビュー例**:
  - 直近7日: フィルタ `when within past week`、並び替え `when desc`
  - 失敗のみ: フィルタ `result = failure`
- **キー項目**: `when`、`result`（success/failure）、`httpCode`、`ghEvent`、`runUrl`、`ghIssueNumber`

### 3. Notion Sync Metrics DB
- **URL**: https://www.notion.so/28886723-2af9-81eb-99de-fbb6e1af2dc5
- **ビュー例**:
  - 週次推移: テーブル、並び替え `date desc`、表示 `successRate`、`code2xx/4xx/5xx`
- **キー項目**: `date`、`successRate`、`total`、`success`、`failure`、`code2xx/4xx/5xx`、`lastUpdated`

## 正常運用の確認項目（日次/週次）

### 日次チェック
1. Logs DBの直近24時間で `result=failure` が増加していないか
2. Metrics DBの当日分で `successRate < 99%` なら調査
3. HTTP 4xx（認可/権限）、5xx（Notion障害）の頻度

### 週次チェック
1. Metrics DBの週次レポート（`Weekly Report YYYY-WXX`）を確認
2. `successRate`が閾値（99%）を下回る週が連続していないか
3. クリーンアップ提案（後述）のレビュー

## 障害対応手順

### 1. 同期失敗が発生した場合

**症状**: Logs DBに `result=failure` が記録される、またはTasksへの反映が遅延

**確認手順**:
1. Logs DBの該当行を開き、`runUrl`からGitHub Actionsのログを確認
2. `httpCode`を確認:
   - `401/403`: Secrets（NOTION_TOKEN）の権限不足/有効期限切れ
   - `400`: Notionのプロパティ名変更やスキーマ不整合
   - `429`: レート制限超過（Notion API）
   - `500-5xx`: Notion側の一時障害
3. `ghEvent`を確認して、特定イベント（例: `issue_comment`）のみ失敗しているかを判定

**対処**:
- `401/403`: `.cursor/mcp.json`と`GitHub Secrets`の`NOTION_TOKEN`を再取得・更新
- `400`: Notion側でプロパティ名を確認。変更されていればworkflowを修正
- `429`: 一時的。数分後に自動リトライで正常化する想定
- `500-5xx`: Notion Statusページ（https://status.notion.so/）で障害確認。復旧待ち

**手動復旧**:
- 特定Issue/PRの再同期が必要な場合:
  1. GitHub上で該当IssueをEdit（タイトルやDescriptionを微変更）→Save
  2. `issues/edited`イベントでworkflow再発火
  3. Notion Tasks/Logsで反映を再確認

### 2. SLO未達アラート（GitHub Issue起票）

**症状**: `SLO-breach daily YYYY-MM-DD` または `SLO-breach weekly YYYY-WXX` のIssueが自動作成

**確認手順**:
1. Issueの本文でJSON（rate/total/success/failure）を確認
2. Logs DBで該当期間の `result=failure` 行を抽出し、原因特定（上記の障害対応へ）
3. 単発失敗か、継続的な低下かを判定

**対処**:
- 単発: 原因修正後にIssueをClose
- 継続: Secrets/権限/Notion側の変更を疑い、根本対策を実施

### 3. Metrics/Logsが更新されない

**症状**: Daily Metrics/週次レポートが空、または古い

**確認手順**:
1. GitHub Actionsの該当workflow（`Weekly Notion sync report`、`Evaluate SLO`）の実行履歴を確認
2. cron未発火の場合、GitHub Actionsが無効化されていないか確認
3. Secretsが未設定または誤っている可能性

**対処**:
- workflowを`workflow_dispatch`で手動再実行
- Secretsを再確認（`NOTION_TOKEN`、`NOTION_TASKS_DB`または`NOTION_DB_TASKS_ID`）

## 手動操作が必要な運用

### 1. バックフィル（ghAssignees/ghDue補完）
- **トリガー**: Notion Tasksで過去分のassignees/dueが空の場合
- **手順**:
  1. GitHub Actions → `Backfill ghAssignees/ghDue (Notion Tasks)` → `Run workflow`
  2. `limit=20`（少量でテスト）→ 実行
  3. Notion Tasksで数件の更新を確認→問題なければ`limit=100`等で再実行

### 2. クリーンアップ提案の承認
- **トリガー**: 週次で`cleanup-propose`が実行され、Cleanup Queueに`status=proposed`の行が追加
- **手順**:
  1. Cleanup Queue DBを開く（URL: 未作成の場合は初回実行後に追加）
  2. `status=proposed`をフィルタ
  3. 各行の`targetUrl`を確認し、削除/アーカイブの妥当性を判断
  4. 承認する場合: `status=approved`に変更（14日後に自動アーカイブ）
  5. 却下する場合: `status=rejected`に変更または行を削除

### 3. Notion→GitHubの同期（制限運用）
- **現状**: `notion-to-gh-assign.yml`は`workflow_dispatch`のみ、`preview_only=true`でデフォルト動作なし
- **手順**:
  1. Notion Tasksで担当者/期日を設定
  2. GitHub Actions → `Notion → GitHub (assignees/due sync)` → `Run workflow`
  3. Inputs: `issue_number=<番号>`, `notion_page_id=<NotionのページID>`, `preview_only=true`
  4. 実行ログでPreview内容を確認
  5. 問題なければ`preview_only=false`で再実行

## トラブルシューティング（よくある失敗）

### Q1. Notion Tasksに行が作られない
- **原因**: Secretsの未設定、DB IDの誤り
- **確認**: `.cursor/mcp.json`の`NOTION_TOKEN`、GitHub Secretsの`NOTION_TASKS_DB`または`NOTION_DB_TASKS_ID`
- **対処**: Secretsを再設定→テストIssueで再試行

### Q2. ghStateが更新されない（常にopen）
- **原因**: GitHub Issueの`closed`イベントでworkflowが発火していない
- **確認**: `.github/workflows/gh-to-notion.yml`の`on.issues.types`に`closed`が含まれているか
- **対処**: 既にmainに反映済み。手動でIssueをEdit→closeで再同期

### Q3. 週次レポートが空（total=0）
- **原因**: Logs DBに過去7日のレコードが無い（同期が全く走っていない）
- **確認**: Logs DBを開いて直近の`when`を確認
- **対処**: テストIssueを作成/編集して同期を発火→Logsに記録→翌週のレポートで反映

## エスカレーション

- **Notion API障害**: https://status.notion.so/ で確認、復旧待ち
- **GitHub Actions障害**: https://www.githubstatus.com/ で確認、復旧待ち
- **権限問題**: Notion Integration（https://www.notion.so/my-integrations）でDB共有を再確認
- **設計変更が必要**: 新規PRを作成し、小さく分割して検証

## 関連ドキュメント
- [Token Policy](token-policy.md): Secrets管理と権限最小化
- [Notion Sync](notion-sync.md): 片方向同期の運用ポイント
- [Governance](governance.md): Notion最上層の命名/配置/クリーンアップ
- [Postmortem 2025-10-10](postmortem-2025-10-10-notion-sync.md): 過去の障害事例
- [Sync Logs Dashboards](sync-logs-dashboards.md): ビュー作成手順
