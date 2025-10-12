# Notion Organization Map

最終更新: 2025-10-13

## 🎯 整理方針

Notion APIの制約により、既存データベースの物理的移動は不可能です。そのため、**中央インデックス方式**を採用しました。

## 📊 新構造

### AIDD Workspace（新規ハブ）
- **URL**: https://www.notion.so/AIDD-Workspace-28a867232af981e38f4ee73da44f97e2
- **役割**: 全データベースへの中央アクセスポイント

### アクティブなデータベース

#### 1. AIDD Knowledge（主要知見DB）
- **URL**: https://www.notion.so/28a867232af981a1a9dec062dbe88644
- **作成日**: 2025-10-12
- **構造**: ACE理論ベース（6プロパティ）
- **カテゴリ**: 最小構成原則、ACE理論、実装、環境、Git運用
- **状態**: ✅ アクティブ

#### 2. PIMS Tasks
- **URL**: https://www.notion.so/288867232af981cd8f68e6fb0899f940
- **作成日**: 2025-10-10
- **構造**: GitHub連携対応
- **状態**: ✅ アクティブ（参照のみ）

#### 3. PIMS Projects
- **URL**: https://www.notion.so/288867232af981cca7a4fe1558074abc
- **作成日**: 2025-10-10
- **状態**: ✅ アクティブ（参照のみ）

#### 4. PIMS Knowledge
- **URL**: https://www.notion.so/288867232af981048ef6e294da63e9df
- **作成日**: 2025-10-10
- **状態**: ✅ アクティブ（参照のみ）

### レガシーデータベース（非推奨）

以下は古いPIMS Hub配下に残存。参照のみ、新規データ追加は非推奨：

- PIMS Sync Logs（ID: 28886723-2af9-8177-924b-ea981a2f6dfa）
- PIMS Sync Metrics（ID: 28886723-2af9-81eb-99de-fbb6e1af2dc5）
- PIMS Registry（ID: 28886723-2af9-81ff-8891-e62c1cdb9b26）
- Cleanup Queue（ID: 28886723-2af9-81f7-9158-e3cc7e1d850f）

## 🔄 運用ルール

### 新規データ作成
- **知見**: AIDD Knowledgeに追加
- **タスク**: GitHub Issue（最優先）または PIMS Tasks
- **プロジェクト**: 必要に応じてローカル管理

### 重要なルール
- **Legacy DB**: PIMS Sync Logs等は参照のみ、新規データ追加禁止
- **重複DB**: PIMS Tasks/Projects/Knowledgeは参照用、新規追加は慎重に
- **推奨順序**: GitHub Issue → PIMS Tasks → ローカル管理

### 既存データ参照
- AIDD Workspaceのインデックスから各DBにアクセス
- レガシーDBは参照のみ、更新は非推奨

### 今後の方針
1. AIDD Knowledgeを主要知見DBとして育成
2. レガシーDBは段階的にフェーズアウト
3. 新機能追加時は最小構成原則に従う

## 📝 整理履歴

### 2025-10-13
- AIDD Workspace作成
- 中央インデックス方式採用
- 本ドキュメント作成

### 2025-10-12
- AIDD Knowledge DB作成（ACE的構造）
- Notion MCP上階層アクセス獲得
- Token切り替え完了

