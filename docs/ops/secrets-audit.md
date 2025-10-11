# Secrets/権限監査記録

## 概要
PIMSで使用するSecrets、Notion Integration権限、GitHub権限を定期的に監査し記録します。

## 監査対象

### 1. GitHub Secrets（Repository Settings → Secrets and variables → Actions）

| Secret名 | 用途 | 最終更新 | 次回ローテーション |
|---------|------|---------|-------------------|
| `NOTION_TOKEN` | Notion API認証（Integration Token） | 2025-10-10 | 2026-01-10（90日） |
| `NOTION_TASKS_DB` | PIMS Tasks DB ID | 2025-10-10 | 不要（固定値） |
| `NOTION_DB_TASKS_ID` | PIMS Tasks DB ID（互換用） | 2025-10-10 | 不要（固定値） |

**確認方法**:
- Repository Settings → Secrets and variables → Actions → Repository secrets
- 各Secretの`Updated`日時を記録

**ローテーション手順**（NOTION_TOKEN）:
1. https://www.notion.so/my-integrations で該当Integrationを開く
2. 「Secrets」タブ → 「New secret」→ 新トークンを生成
3. `.cursor/mcp.json`の`env.NOTION_TOKEN`を更新（ローカル）
4. GitHub Repository Settings → Secrets → `NOTION_TOKEN` → 「Update」で新値を設定
5. テストIssue作成→同期成功を確認
6. 旧トークンを無効化（Notion Integration設定で「Revoke」）

### 2. Notion Integration権限

**Integration名**: PIMS MCP Integration（例）

**共有されたDB/ページ**:
- PIMS MCP Hub（親ページ）
- PIMS Tasks（DB）
- PIMS Sync Logs（DB）
- PIMS Sync Metrics（DB）
- PIMS Projects（DB）
- PIMS Knowledge（DB）
- PIMS Registry（DB・週次構築）
- PIMS Cleanup Queue（DB・クリーンアップ提案）

**確認方法**:
1. https://www.notion.so/my-integrations → 該当Integration
2. 「Associated workspaces」でワークスペースを確認
3. 各DBを開き、右上の「...」→「Connections」→Integrationが表示されていることを確認

**権限最小化チェック**:
- 読み取り専用が適切なDB: なし（現在は全て読み書き必要）
- 将来的に読み取り専用化: Projects/Knowledge（現在は未実装）

### 3. GitHub権限（Actionsのpermissions）

**各workflow**:
- `gh-to-notion.yml`: `contents: read`, `issues: read`, `pull-requests: read`
- `slo-evaluate.yml`: `contents: read`, `issues: write`（SLO未達時にIssue起票）
- `registry-update.yml`: `contents: read`
- `cleanup-propose.yml`: `contents: read`
- `backfill-assignees-due.yml`: `contents: read`
- `notion-to-gh-assign.yml`: `contents: read`, `issues: write`

**確認方法**:
- 各workflowファイルの`permissions:`セクションを確認
- 最小権限原則: 必要な操作のみに限定

**監査結果記録**:
- 不要な`write`権限が付与されていないか
- `secrets: write`や`actions: write`等の管理権限は付与禁止

## 定期監査スケジュール

- **月次**: Secrets有効性確認（NOTION_TOKEN）、GitHub Actions実行履歴の異常検知
- **四半期**: NOTION_TOKENのローテーション（推奨90日）
- **半期**: Notion Integration権限の棚卸し、不要なDB共有の削除
- **年次**: 全体設計のレビュー、ゼロトラスト原則の再確認

## チェックリスト（監査時）

- [ ] NOTION_TOKENの最終更新日が90日以内
- [ ] GitHub Secretsに不要なSecretが無い
- [ ] Notion IntegrationのDB共有が必要最小限
- [ ] GitHub Actionsのpermissionsが最小権限
- [ ] Logs DBで過去30日の`result=failure`率が1%未満
- [ ] Metrics DBで週次`successRate`が99%以上
- [ ] クリーンアップ提案が適切にレビュー済み
- [ ] Runbookが最新の運用に追従している

## 次回監査予定

- 次回月次監査: 2025-11-11
- 次回四半期監査: 2026-01-10
- 監査責任者: （運用チームまたはシステム管理者を記載）

## 変更履歴

- 2025-10-11: 初版作成（運用Runbook統合）
