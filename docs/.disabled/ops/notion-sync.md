# Notion連携（GitHub→Notion片方向同期・運用手順)

本書は、`.github/workflows/gh-to-notion.yml` による最小同期の運用ポイントをまとめます。

## 概要
- トリガ: `issues`, `issue_comment`, `pull_request`（opened/edited/closed/reopened）
- 条件: リポジトリSecretsに `NOTION_TOKEN`, `NOTION_TASKS_DB` が設定されている場合のみ実行
- 動作: NotionのタスクDBにページを作成/更新（既存は `ghIssueNumber` で検索し、存在時はPATCHで更新）

## 事前準備
1. Notionで「タスク」データベースを作成し、Database IDを取得
2. Integration（トークン）を発行し、対象DBに共有
3. GitHub Secrets を設定
   - `NOTION_TOKEN`: 上記Integrationトークン
   - `NOTION_TASKS_DB`: タスクDBのDatabase ID

## 運用
- イベント発生時、タイトル/番号/状態/URL/リポジトリ/ラベルがNotionに転送されます
- Notion側のIntegration（例: PIMS MCP）が親ページおよび対象DBに「編集可」で招待されている必要があります
- 失敗時はログ末尾の HTTP コードと本文で一次切り分け（401/403=権限、404=DB ID、400=プロパティ不整合、429=レート）

## トラブルシュート
- 失敗: Secrets 未設定、Notion権限不足、APIレート制限、Bashクォート崩れ
- 確認: ActionsログでHTTP応答、Notion側の作成有無
- 再試行: 手動再実行 or 次のイベントで再送

### 今回の障害と恒久対策
- 症状: Bash内でJSONをインライン`-d '{...}'`で渡したため、括弧/クォート解釈が壊れ、`syntax error near unexpected token '('` で失敗
- 恒久対策: JSONは一度ファイル（`payload.json`/`update.json`）へ保存し、`--data-binary @file` で送信する方式へ変更
- 追加対策:
  - デバッグ: HTTPコードと本文を必ずログ出力
  - 手動実行: `workflow_dispatch` を有効化し、迅速に再現/切り分け可能
  - main優先: デフォルトブランチへ早期反映し、イベント実行との不整合を防止

## 将来拡張
- GitHub→Notionの冪等更新（完了）/ 主キーを `ghIssueNumber` or `ghIssueId` に統一
- Notion→GitHub（タイトル・ステータス限定の双方向）段階導入
- 監査ログ/メトリクス: 成功/失敗、HTTPコード、所要秒を集計し、SLOを可視化
