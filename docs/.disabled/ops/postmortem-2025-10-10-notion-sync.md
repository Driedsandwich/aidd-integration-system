# Postmortem: Notion同期ワークフローの失敗（2025-10-10）

## 事象
- GitHub → Notion 同期ワークフローが `issue_comment` トリガで失敗。
- Actionsログに `syntax error near unexpected token '('` が出力。
- Notion側への反映が発生しなかった。

## 影響
- 同期が一時停止（少数イベント）。
- 重要レコードは無く、バックフィル不要。

## 根本原因（Root Cause）
- curl に渡す JSON を Bash 内でインライン `-d '{...}'` 指定しており、括弧/クォートの解釈が崩れてシェル構文エラーになった。

## 恒久対策（Fix / Prevention）
- JSON をファイル（`payload.json`/`update.json`）に書き出し、`--data-binary @file` で送信へ変更。
- デバッグ強化: HTTP コードと応答本文を必ずログ出力。
- `workflow_dispatch` を有効化し、迅速に再現/切り分け可能化。
- デフォルトブランチ（main）へ早期反映を徹底。

## 検知・可視化
- `PIMS Sync Logs` データベースを新設し、以下を自動記録：
  - when, result(success/failure), httpCode, ghEvent
  - runUrl, ghUrl, ghRepo, ghIssueNumber

## 残タスク / フォローアップ
- Notion側のビューで期間別成功率、HTTPコード別集計を作成（手順は `docs/ops/sync-logs-dashboards.md`）。
- 双方向同期の範囲拡張は段階導入（安全を優先）。

## タイムライン
- 14:11 失敗検知
- 14:20 原因特定（Bash構文エラー）
- 14:30 修正→PR→main反映
- 15:00 ログDB追加・拡張ログ導入

## 教訓
- シェル経由の JSON はファイル経由に統一する。
- 監査ログを最初から設置し、可観測性を確保する。
