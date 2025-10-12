# トークン運用ポリシー（GitHub / Notion / MCP）

この文書は、本ワークスペースで使用する各種APIトークンの取り扱い方針を定義します。

## 基本原則
- 権限最小（Least Privilege）を徹底する
- 秘匿情報をリポジトリに含めない（`.cursor/mcp.json` は `.gitignore` 済み）
- ローテーションを定期実施（目安: 90日）
- 破壊的権限は恒常付与しない（必要時のみ一時的に付与）

## GitHub Personal Access Token（PAT）
- 必須スコープ: `repo`, `issues`, `read:org`（必要に応じて）
- 禁止/分離: `delete_repo` は常時付与しない（削除はブラウザから手動）
- 保存場所:
  - MCP 実行環境: `.cursor/mcp.json`（ローカルのみ。コミット禁止）
  - CI/Actions: GitHub Secrets（例: `GH_PAT`）
- ローテーション手順:
  1. 新PATを発行（既存と同等スコープ）
  2. ローカル `.cursor/mcp.json` と GitHub Secrets を更新
  3. 旧PATを失効

## Notion Integration Token
- 必須スコープ: 使用DBへの読み書き権限のみ
- 保存場所:
  - MCP 実行環境: `.cursor/mcp.json`（ローカルのみ。コミット禁止）
  - CI/Actions: GitHub Secrets（例: `NOTION_TOKEN`）
- 前提: 対象データベースにIntegrationを共有しておく

## MCP設定（.cursor/mcp.json）
- 秘匿: リポジトリに含めない
- テンプレート: `.cursor/mcp.template.json` を配布し、バージョンやトークンは手元で設定
- バージョン固定: `@modelcontextprotocol/server-github@<PINNED>` / `@notionhq/notion-mcp-server@<PINNED>` を使用（テンプレ内プレースホルダを置換）

## 事故対応
- 流出の疑いがある場合:
  1. 該当トークンを直ちに失効
  2. 影響範囲を確認（監査ログ・直近操作履歴）
  3. 新トークン発行と差し替え
  4. 再発防止（ルール更新・周知）

## 監査
- CI/同期処理は、Notionコメント等に「誰が/何を/どこへ」を記録
- 月次でランダム突合（目安50件）を実施し差異をレポート

## 運用チェックリスト（Notion同期）
- Integrationの招待先: 親ページ + 対象DB（編集可）
- GitHub Secrets: `NOTION_TOKEN`, `NOTION_TASKS_DB`/`NOTION_DB_TASKS_ID`
- ワークフロー手動起動（workflow_dispatch）を有効化し切り分け容易に
- デバッグ: HTTPコード/本文をログ出力（エラー時の一次切り分け）
