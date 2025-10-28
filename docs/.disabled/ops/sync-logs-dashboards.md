# PIMS Sync Logs ダッシュボード作成手順

`PIMS Sync Logs` をもとに、運用SLOを可視化します。

## 必要プロパティ
- when(Date)
- result(Select: success/failure)
- httpCode(Number)
- ghEvent(Rich text)
- runUrl(URL), ghUrl(URL), ghRepo(Rich text), ghIssueNumber(Number)

## ビュー例
1. Today（テーブル）
   - フィルタ: when is within past week（必要に応じてToday）
   - 表示: when, result, httpCode, ghEvent, ghIssueNumber, ghUrl, runUrl
2. Success Rate（ボード）
   - グループ: result（success/failure）
   - フィルタ: when within past 7 days
3. HTTP Code Breakdown（テーブル）
   - フィルタ: when within past 7 days
   - 並び替え: httpCode desc

## 運用メモ
- レート超過(429)/認可(401/403)/スキーマ不整合(400)は要注意。増加時はSecrets・権限・DBプロパティを再点検。
- GitHubのRun画面（runUrl）から該当ログを即追跡可能。
