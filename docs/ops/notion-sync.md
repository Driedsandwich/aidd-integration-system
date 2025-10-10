# Notion連携（GitHub→Notion片方向同期・運用手順)

本書は、`.github/workflows/gh-to-notion.yml` による最小同期の運用ポイントをまとめます。

## 概要
- トリガ: `issues`, `issue_comment`, `pull_request`（opened/edited/closed/reopened）
- 条件: リポジトリSecretsに `NOTION_TOKEN`, `NOTION_TASKS_DB` が設定されている場合のみ実行
- 動作: NotionのタスクDBにページを作成（将来はidempotent更新へ拡張）

## 事前準備
1. Notionで「タスク」データベースを作成し、Database IDを取得
2. Integration（トークン）を発行し、対象DBに共有
3. GitHub Secrets を設定
   - `NOTION_TOKEN`: 上記Integrationトークン
   - `NOTION_TASKS_DB`: タスクDBのDatabase ID

## 運用
- イベント発生時、タイトル/番号/状態/URL/リポジトリがNotionに転送されます
- 現行は作成専用のベストエフォート（失敗時はジョブで検知）
- 冪等（同一Issueの更新上書き）対応は、今後「一意キー（ghIssueId等）をNotionに保存 → 事前検索して更新」に拡張予定

## トラブルシュート
- 失敗: Secrets 未設定、Notion権限不足、APIレート制限等
- 確認: ActionsログでHTTP応答、Notion側の作成有無
- 再試行: 手動再実行 or 次のイベントで再送（将来はキュー/再試行追加）

## 将来拡張
- GitHub→Notionの冪等更新
- Notion→GitHub（AutoCreateGH=true）での双方向同期
- 監査ログの強化（操作内容をNotionコメントへ付記）
