# PIMS Governance（命名/配置/運用）

## 目的
Notion最上層をシンプルに保ち、継続的に整理するためのルールと自動化を定義します。

## 最上層（Hub直下）の構成
- Projects（DB）/ Tasks（DB）/ Knowledge（DB）
- Logs（PIMS Sync Logs）/ Metrics（PIMS Sync Metrics）
- Registry（PIMS Registry）/ Governance（本ドキュメント）

## 命名規則（例）
- ページ: `[カテゴリ] タイトル`（例: `[Guide] Notion運用`）
- DB: `PIMS <機能名>`（例: `PIMS Sync Logs`）
- 作成日を付ける場合は ISO (`2025-10-10`) を末尾に付記

## 配置規則
- Hub直下に新規直置きは禁止。カテゴリ配下に作成する
- 動的・短期の検証は `Temp` 配下で管理、90日未更新で整理対象

## 逸脱検知
- 週次のレジストリ構築（registry-update）
- 自動タグ（registry-autotag）により `autoTag` を提案
- 未分類（`tag`空）や `Temp`/`Other` は Cleanup 提案の候補

## クリーンアップ運用
- proposal → approved（14日保留）→ archive → 30日後にdelete（参照/中身なしのみ）
- すべてNotion MCP/Actions経由で自動or半自動。手動での誤削除を避ける

## 変更管理
- ルール変更はPR経由でこのドキュメントを更新
- 自動化の閾値（未更新日数など）はワークフローの入力/定数で管理
