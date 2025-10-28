# Notion→GitHub 双方向同期のロールアウト計画

## 現状（Phase 0）

- GitHub→Notionの片方向同期は稼働中（自動）
- Notion→GitHubは**限定プレビュー運用**:
  - `notion-to-gh-assign.yml`: `workflow_dispatch`のみ、`preview_only=true`でデフォルト非破壊
  - 対象: 担当者（assignees）と期日（dueラベル）のみ

## ロールアウト戦略（段階導入）

### Phase 1: プレビュー検証（現在地）

**対象**:
- テストリポジトリ: `aidd-integration-system`
- 対象Issue: 手動選択（`workflow_dispatch`の入力で指定）
- 許可ユーザー: リポジトリOwner（`Driedsandwich`）のみ

**実行条件**:
- `preview_only=true`で常に実行→ログでPreview内容を確認
- 問題なければ個別に`preview_only=false`で実適用

**成功基準**:
- 10回のPreview実行で0件の異常（既存データ不整合、権限エラー等）
- 5回の実適用で意図通りのassignees/dueラベル反映

**ロールバック**:
- GitHub側で誤ったassignees/labelを手動削除
- workflowを無効化（PRでCloseまたはファイル削除）

### Phase 2: 限定自動化

**前提**: Phase 1が成功

**対象拡大**:
- Notion Tasksで`AutoSyncGH=true`のチェックボックスを追加（プロパティ）
- workflow側で`AutoSyncGH=true`の行のみを対象に自動実行（cron or イベント駆動）

**実行条件**:
- 初回は`AutoSyncGH=true`の行が5件以下に限定
- 週次cron（UTCで低トラフィック時間帯）
- `preview_only=false`で実適用

**成功基準**:
- 連続2週間、異常なし（GitHub側の不整合、重複ラベル等）
- Logs DBで`result=success`率 100%

**ロールバック**:
- `AutoSyncGH=false`に一括変更（Notion側で手動）
- workflowのcronを無効化

### Phase 3: 全面展開

**前提**: Phase 2が成功

**対象**:
- 全Notion Tasks（`AutoSyncGH`のデフォルトを`true`へ）
- 複数リポジトリへの拡大（`ghRepo`プロパティで判定）

**実行条件**:
- Notion側で担当者/期日を変更→数分以内にGitHub反映（webhook駆動を検討）
- `preview_only`は完全廃止、実適用のみ

**成功基準**:
- 月次で`result=success`率 99%以上
- GitHubとNotionの双方向整合性が保たれる（SoTはNotion Tasks）

**ロールバック**:
- 全体を片方向（GitHub→Notion）のみに戻す
- Notion→GitHub workflowを全て無効化

## 許可リスト（Phase 1〜2）

### リポジトリ
- `Driedsandwich/aidd-integration-system`（テスト/本番兼用）
- 追加候補: `Driedsandwich/ucomm`（承認後）

### ユーザー（Notion側で操作可能）
- Owner: `Driedsandwich`（GitHub login）
- 追加候補: コラボレーター（要承認）

### 同期対象プロパティ
- Phase 1-2: `ghAssignees`、`ghDue`のみ
- Phase 3候補: `ステータス`→`ghState`の双方向（要慎重評価）

## リスク管理

### 高リスク操作（禁止）
- GitHub Issue/PRの**削除**（Notion側から）
- タイトル/本文の**上書き**（SoTはGitHub）
- ラベルの**削除**（GitHub側の既存ラベルを保護）

### 中リスク操作（段階導入）
- assigneesの**追加/削除**（現在はPhase 1で検証中）
- 期日ラベル（`due:YYYY-MM-DD`）の**追加**（現在はPhase 1で検証中）

### 低リスク操作（実装済み）
- GitHub→Notionの**全プロパティ同期**（既存動作、問題なし）

## 運用判断基準

### Phaseを進める条件
- 前Phaseの成功基準を全て満たす
- 直近30日でSLO未達が0回
- 手動復旧が不要（自動リトライで正常化）

### Phaseを後退する条件
- 連続2回のSLO未達
- データ不整合の発生（GitHub/Notionで食い違い）
- ユーザーからの誤動作報告

## 現在のPhase判定

- **Phase**: 1（プレビュー検証）
- **次Phase移行の見込み**: 2025-11月中旬（Phase 1の成功基準達成後）
- **判定者**: システム管理者またはリポジトリOwner

## 変更履歴

- 2025-10-11: 初版作成（ロールアウト計画策定）
