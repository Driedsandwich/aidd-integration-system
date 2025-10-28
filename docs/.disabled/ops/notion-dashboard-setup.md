# Notionダッシュボード作成ガイド

## 概要
PIMSの3つのコアDB（Tasks/Logs/Metrics）に対して、運用に必要なビューをNotion UIで作成する手順です。

## 前提条件

- Notionワークスペースへのアクセス権（編集権限）
- PIMS MCP Hubページ（https://www.notion.so/26f867232af9814c91dbcc3498ccc33b）へのアクセス
- GitHub→Notion同期が既に動作中で、Tasks/Logsにデータが蠕積されていること

---

## 1. PIMS Tasks DBのビュー作成

**対象DB**: PIMS Tasks（ID: `28886723-2af9-81cd-8f68-e6fb0899f940`）

### 1.1 カンバンビュー（ステータス別）

**手順**:
1. Tasks DBを開く
2. 右上の「+ Add a view」→「Board」を選択
3. ビュー名: `Status Board`
4. 「Group by」→ `ghState` または `ステータス`
5. 「Filter」→ `ghState is not empty`（空行を除外）
6. 「Sort」→ `Last edited time` descending
7. 「Properties」で表示項目を選択:
   - ☑ Name
   - ☑ ghState
   - ☑ ghIssueNumber
   - ☑ ghUrl
   - ☑ ghAssignees
   - ☑ ghDue
   - ☐ その他（必要に応じて）

### 1.2 テーブルビュー（未完了/直近更新）

**手順**:
1. Tasks DBを開く
2. 右上の「+ Add a view」→「Table」を選択
3. ビュー名: `Open Tasks`
4. 「Filter」:
   - `ghState` equals `open`
5. 「Sort」:
   - `Last edited time` descending
6. 表示プロパティ: Name, ghIssueNumber, ghUrl, ghRepo, ghAssignees, ghDue, ghState

### 1.3 テーブルビュー（全体一覧）

**手順**:
1. Tasks DBを開く
2. 既存のDefaultビューを使用、または「+ Add a view」→「Table」
3. ビュー名: `All Tasks`
4. 「Filter」: なし（全行表示）
5. 「Sort」: `ghIssueNumber` descending
6. 表示プロパティ: 全て表示（必要に応じて非表示も可）

---

## 2. PIMS Sync Logs DBのビュー作成

**対象DB**: PIMS Sync Logs（ID: `28886723-2af9-8177-924b-ea981a2f6dfa`）

### 2.1 テーブルビュー（直近7日）

**手順**:
1. Sync Logs DBを開く
2. 「+ Add a view」→「Table」
3. ビュー名: `Last 7 Days`
4. 「Filter」:
   - `when` is within `Past week`
5. 「Sort」:
   - `when` descending
6. 表示プロパティ: when, result, httpCode, ghEvent, ghIssueNumber, ghUrl, runUrl, ghRepo

### 2.2 ボードビュー（成功/失敗別）

**手順**:
1. Sync Logs DBを開く
2. 「+ Add a view」→「Board」
3. ビュー名: `Success Rate`
4. 「Group by」→ `result`
5. 「Filter」:
   - `when` is within `Past week`
6. カード表示: Name, when, httpCode, ghEvent, runUrl

### 2.3 テーブルビュー（失敗のみ）

**手順**:
1. Sync Logs DBを開く
2. 「+ Add a view」→「Table」
3. ビュー名: `Failures Only`
4. 「Filter」:
   - `result` equals `failure`
5. 「Sort」:
   - `when` descending
6. 表示プロパティ: when, httpCode, ghEvent, ghIssueNumber, runUrl, note

---

## 3. PIMS Sync Metrics DBのビュー作成

**対象DB**: PIMS Sync Metrics（ID: `28886723-2af9-81eb-99de-fbb6e1af2dc5`）

### 3.1 テーブルビュー（週次推移）

**手順**:
1. Sync Metrics DBを開く
2. 「+ Add a view」→「Table」
3. ビュー名: `Weekly Trend`
4. 「Filter」:
   - なし（全期間表示）または `date` is within `Past month`
5. 「Sort」:
   - `date` descending
6. 表示プロパティ:
   - Name, date, successRate, total, success, failure, code2xx, code4xx, code5xx, lastUpdated
7. 追加設定（オプション）:
   - `successRate`プロパティに条件付き書式（< 99%で赤色表示）

### 3.2 ボードビュー（HTTPコード別）

**手順**:
1. Sync Metrics DBを開く
2. 「+ Add a view」→「Board」
3. ビュー名: `HTTP Code Breakdown`
4. 「Group by」→ 新規Formulaプロパティを作成：
   - 名前: `Dominant Code`
   - 式: `if(prop("code2xx") > prop("code4xx") and prop("code2xx") > prop("code5xx"), "2xx", if(prop("code4xx") > prop("code5xx"), "4xx", "5xx"))`
5. カード表示: Name, date, successRate, code2xx, code4xx, code5xx

**簡略版（Formula省略）**:
- Group byを使わず、Tableビューで `code2xx/4xx/5xx` を並べて表示するのみでもOK

---

## 4. ダッシュボードページの作成（オプション）

### 4.1 新規ページ作成

**手順**:
1. PIMS MCP Hubページを開く
2. 「+」ボタン→「Page」
3. タイトル: `PIMS Dashboard`
4. アイコン: 📊（棒グラフ）

### 4.2 Linked Databaseの埋め込み

**Tasksカンバン**:
1. Dashboardページで「/linked」と入力→「Create linked database」
2. 「PIMS Tasks」を選択
3. Viewを「Status Board」に切り替え

**Logs直近7日**:
1. Dashboardページで「/linked」
2. 「PIMS Sync Logs」を選択
3. Viewを「Last 7 Days」に切り替え

**Metrics週次推移**:
1. Dashboardページで「/linked」
2. 「PIMS Sync Metrics」を選択
3. Viewを「Weekly Trend」に切り替え

### 4.3 レイアウト例

```
[PIMS Dashboard 📊]

## タスク状況
[Linked: PIMS Tasks - Status Board]

## 同期ログ（直近7日）
[Linked: PIMS Sync Logs - Last 7 Days]

## 週次メトリクス
[Linked: PIMS Sync Metrics - Weekly Trend]
```

---

## 5. 高度な設定（オプション）

### 5.1 条件付き書式（Conditional Formatting）

**Metrics DBのsuccessRate**:
1. Metrics DBを開く
2. `successRate`プロパティのヘッダーをクリック→「Customize property」
3. 「Show as」→「Number with bar」または「Ring」
4. 条件追加（Notion UIの制約で完全自動化は不可、手動で色分け）

### 5.2 リレーション（Tasks ↔ Projects）

**現在の設定確認**:
1. Tasks DBで「Projects」プロパティ（Relation）があれば有効化
2. Projects DBで逆参照（Related to Tasks）を表示

---

## 6. ダッシュボード運用の確認項目

### 日次確認
- [ ] Tasksの「Open Tasks」ビューで新規GitHub Issue/PRが反映されている
- [ ] Logsの「Last 7 Days」で`result=failure`が増えていないか
- [ ] Metricsの最新行で`successRate >= 99%`

### 週次確認
- [ ] Metricsの「Weekly Trend」で直近4週の`successRate`推移を確認
- [ ] Logsの「Failures Only」で異常パターンを検知（同じhttpCodeが連続等）
- [ ] Tasksで`ghState=open`かつ`ghDue`が過去のものがあればエスカレーション

---

## 7. トラブルシューティング

### Q1. Linked Databaseが空
- **原因**: Filterが厳しすぎる、またはDB自体にデータがない
- **対処**: Filterを一時的に全解除して確認、またはGitHubでテストIssue作成で同期発火

### Q2. ビューが表示されない
- **原因**: ビュー作成時に「Show in」を限定した
- **対処**: ビュー名の右の「...」→「Show in」→「All pages」に変更

### Q3. プロパティが空（GitHub起因）
- **原因**: GitHub→Notion同期が未実行、またはSecrets未設定
- **対処**: `docs/ops/runbook.md`の障害対応手順を参照

---

## 8. 関連ドキュメント

- [Runbook](runbook.md): 日常運用と障害対応
- [Sync Logs Dashboards](sync-logs-dashboards.md): Logs DBのビュー作成詳細
- [Governance](governance.md): Notion最上層の命名/配置/クリーンアップ

---

## 9. 完了チェックリスト

以下が全て作成されていれば完了です：

- [ ] PIMS Tasks: Status Board（カンバン）
- [ ] PIMS Tasks: Open Tasks（テーブル）
- [ ] PIMS Sync Logs: Last 7 Days（テーブル）
- [ ] PIMS Sync Logs: Success Rate（ボード）
- [ ] PIMS Sync Logs: Failures Only（テーブル）
- [ ] PIMS Sync Metrics: Weekly Trend（テーブル）
- [ ] オプション: PIMS DashboardページでLinked Databaseを統合

**注意**: これらのUI操作はNotionのブラウザで手動実施します。MCP/APIからのビュー作成は現時点でNotion APIが対応していません。

---

## 10. 変更履歴

- 2025-10-11: 初版作成（ダッシュボード作成ガイド）
