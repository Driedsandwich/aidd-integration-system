# 動画統合パターン別テンプレート

> パターン別に最適化されたYouTube動画統合テンプレート集

## 🚀 超簡易版（コピペ即実行）

```markdown
@[動画URL] この動画の内容をプロジェクトに統合してください。

以下の手順で進めてください：
1. トランスクリプトを取得して内容を分析
2. プロジェクト構造を把握（docs/, .cursor/rules/, README.md）
3. TODOリストを作成して段階的に実装
4. 以下を作成/更新:
   - 初心者向けガイド（docs/配下）
   - Cursorルール（.cursor/rules/配下）
   - 設定ファイル（.gitignore等）
   - README（新規ドキュメントへのリンク）
5. 完了報告

注意事項：
- 既存の命名規則・スタイルに従う
- 機密情報を含めない
- 既存ドキュメントとの整合性を保つ
```

---

## 📝 パターン別テンプレート

### パターン1: Git/GitHub系

```markdown
@[動画URL] このGit/GitHub動画の内容を統合してください。

## 目的
安全なバージョン管理とAI駆動開発の統合

## 成果物
- [ ] 初心者向けガイド（GitHub Desktop使用推奨）
- [ ] Git運用ルール（.cursor/rules/git-workflow.mdc）
- [ ] .gitignoreの改善（機密情報除外）
- [ ] PRテンプレート改善

## 重点事項
- APIキー漏洩防止を最重視
- 小さく頻繁なコミットを推奨
- ブランチ戦略を明確化
```

### パターン2: Docker/環境構築系

```markdown
@[動画URL] このDocker動画の内容を統合してください。

## 目的
開発環境の統一とセットアップの簡素化

## 成果物
- [ ] Docker初心者ガイド
- [ ] Dockerfile作成
- [ ] docker-compose.yml作成
- [ ] .dockerignore作成
- [ ] セットアップ手順の更新（README）

## 重点事項
- ローカル開発とCI/CD環境の統一
- 環境変数の適切な管理
- ボリュームマウントの設計
```

### パターン3: テスト/CI/CD系

```markdown
@[動画URL] このテスト/CI/CD動画の内容を統合してください。

## 目的
自動テスト・デプロイの確立

## 成果物
- [ ] テスト戦略ガイド
- [ ] CI/CD設定（.github/workflows/）
- [ ] テストルール（.cursor/rules/testing.mdc）
- [ ] カバレッジ設定

## 重点事項
- ユニット/統合/E2Eテストの分類
- GitHub Actionsワークフロー設計
- テスト自動化の段階的導入
```

### パターン4: セキュリティ系

```markdown
@[動画URL] このセキュリティ動画の内容を統合してください。

## 目的
セキュアなコーディング・運用の確立

## 成果物
- [ ] セキュリティガイド
- [ ] セキュリティルール（.cursor/rules/security.mdc）
- [ ] 機密情報管理ガイド
- [ ] チェックリスト（PRテンプレート）

## 重点事項
- APIキー・トークン管理
- 入力検証・サニタイゼーション
- 依存関係の脆弱性スキャン
```

### パターン5: フレームワーク/ライブラリ入門系

```markdown
@[動画URL] この[フレームワーク名]動画の内容を統合してください。

## 目的
[フレームワーク名]のベストプラクティス確立

## 成果物
- [ ] [フレームワーク名]ガイド
- [ ] 実装ルール（.cursor/rules/[framework].mdc）
- [ ] プロジェクト構成例
- [ ] サンプルコード

## 重点事項
- 公式推奨パターンに準拠
- AI駆動開発での活用方法
- よくあるアンチパターンの明示
```

---

## 🎯 目的別カスタマイズポイント

### 非エンジニア向け
```markdown
## 追加要件
- コマンド不要の方法を優先（GitHub Desktop等）
- 図解・スクリーンショット多用
- 用語集セクションを追加
- トラブルシューティングを充実
```

### 上級者向け
```markdown
## 追加要件
- 詳細な技術仕様を含める
- エッジケース・最適化手法を記載
- 内部実装の説明を追加
- パフォーマンスチューニング
```

### チーム開発向け
```markdown
## 追加要件
- コミュニケーションルールを明確化
- レビュープロセスを定義
- Issue/PRテンプレート改善
- ブランチ戦略の詳細化
```

---

## ⚡ AI Agent向け実行指示

### 標準フロー

```markdown
以下の手順で動画内容を統合してください：

## Phase 1: 分析
1. `mcp_fetch_fetch_youtube_transcript` で動画トランスクリプト取得
2. 主要テーマ・実践的知見を抽出
3. プロジェクト構造を確認（list_dir, read_file）

## Phase 2: 計画
1. `todo_write` でTODOリスト作成（merge=false）
2. 以下のタスクを含める:
   - ガイド作成
   - ルール追加
   - 設定更新
   - 統合・リンク
3. 各タスクをin_progressに変更しながら実行

## Phase 3: 実装
1. 各TODOを順次実行
2. 完了したらステータスをcompletedに更新
3. 以下を作成/更新:
   - `docs/[テーマ]-guide.md`
   - `.cursor/rules/[テーマ].mdc`
   - `.gitignore`, `.env.example`（必要に応じて）
   - 統合運用ガイド等（セクション追加）

## Phase 4: 統合
1. `README.md` に新規ドキュメントへのリンク追加
2. 相互リンクを設定
3. 整合性確認

## Phase 5: 完了報告
1. 作成/更新ファイル一覧
2. メリット
3. 次のステップ提案

## 注意事項
- 既存の命名規則を維持
- 日本語で記述
- 機密情報を含めない
- 全てのTODOをcompletedにしてから完了報告
```

---

## 🔧 トラブルシューティング

### トランスクリプトが取得できない

**症状**: YouTube動画のトランスクリプトが取得できない

**対処**:
```markdown
動画に字幕がない可能性があります。以下を試してください：
1. 動画の概要欄・コメントから要点を抽出
2. 動画タイトルと概要から推測
3. 類似の動画を検索
4. ユーザーに手動要約を依頼
```

### 既存構造との衝突

**症状**: 既存ファイル・ルールと命名が衝突

**対処**:
```markdown
1. 既存ファイルを確認: `grep -r "キーワード"`
2. 命名を調整: 
   - `git-workflow.mdc` → `git-workflow-ai.mdc`
   - `setup-guide.md` → `environment-setup-guide.md`
3. ユーザーに確認を求める
```

### 大量のファイル更新

**症状**: 統合範囲が広すぎて作業が膨大

**対処**:
```markdown
段階的に実装:
1. **Phase 1**: 最小限のガイド作成
2. **Phase 2**: ルール追加
3. **Phase 3**: 設定ファイル
4. 各Phaseでユーザー確認
```

---

## 📊 成功指標

### 必須達成項目
- [ ] トランスクリプト分析完了
- [ ] 最低1つのガイドドキュメント作成
- [ ] READMEにリンク追加
- [ ] 内部リンクが機能

### 推奨達成項目
- [ ] Cursorルール追加
- [ ] 設定ファイル更新
- [ ] 既存ドキュメント拡張
- [ ] テンプレート改善

### 理想的な達成項目
- [ ] 図解・スクリーンショット追加
- [ ] サンプルコード実装
- [ ] トラブルシューティング充実
- [ ] チェックリスト作成

---

## 🎁 出力フォーマット例

### 最小限の報告

```markdown
## 完了報告

### 作成ファイル
- `docs/docker-guide.md` - Docker初心者ガイド

### 更新ファイル
- `README.md` - Dockerガイドへのリンク追加

### 次のステップ
1. Dockerfileを作成
2. docker-compose.ymlを設定
```

### 標準的な報告

```markdown
## 🎉 統合完了

### 📋 作成ファイル
1. `docs/docker-beginner-guide.md` - Docker入門
2. `.cursor/rules/docker-workflow.mdc` - Docker運用ルール
3. `Dockerfile` - 開発環境用
4. `docker-compose.yml` - サービス構成

### 📝 更新ファイル
1. `README.md` - Dockerセクション追加
2. `.gitignore` - Docker関連除外追加
3. `docs/04-integration-guide.md` - Docker統合セクション

### 🎯 メリット
1. 環境統一 - チーム全体で同じ環境
2. セットアップ簡素化 - `docker-compose up` で完了
3. CI/CD統合 - ローカルと本番環境が一致

### 🚀 次のステップ
1. 実際にDockerを起動して動作確認
2. CI/CDパイプラインにDocker統合
3. チームメンバーに展開
```

### 詳細な報告

```markdown
## 🎉 動画統合完了報告

### 📹 元動画情報
- URL: [動画URL]
- タイトル: [動画タイトル]
- 投稿者: [チャンネル名]
- 対象: [初心者/中級者]

### 📋 実施内容

#### 新規作成ファイル（5件）
1. **`docs/docker-beginner-guide.md`**
   - Docker基本概念
   - インストール手順（Windows/Mac）
   - 基本コマンド解説
   - トラブルシューティング

2. **`.cursor/rules/docker-workflow.mdc`**
   - Dockerfile作成ルール
   - docker-compose.yml設計パターン
   - ボリュームマウントのベストプラクティス

3. **`Dockerfile`**
   - Python 3.11ベース
   - 依存関係インストール
   - ヘルスチェック設定

4. **`docker-compose.yml`**
   - アプリケーションサービス
   - PostgreSQL
   - Redis

5. **`.dockerignore`**
   - node_modules, .venv除外
   - .git, .env除外

#### 更新ファイル（4件）
1. **`README.md`**
   - Dockerクイックスタートセクション追加
   - セットアップ手順を更新

2. **`.gitignore`**
   - Dockerボリュームデータ除外

3. **`docs/04-integration-guide.md`**
   - Docker統合セクション追加
   - コンテナ運用との連携

4. **`.github/PULL_REQUEST_TEMPLATE.md`**
   - Docker関連チェックリスト追加

### 🎯 得られるメリット

#### 1. 開発環境の統一 🔧
- 全メンバーが同じPython/Node.jsバージョン使用
- 「私の環境では動く」問題を解消
- 新メンバーのオンボーディング時間を80%削減

#### 2. セットアップの簡素化 ⚡
```bash
# 従来: 20ステップ、30分
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# ... (多数の手順)

# 新: 1コマンド、5分
docker-compose up
```

#### 3. CI/CD統合 🚀
- ローカルと本番環境が完全一致
- デプロイエラーを事前検出
- GitHub Actionsで同じコンテナ使用

#### 4. AI駆動開発との親和性 🤖
- Cursorルールでコンテナ設計を標準化
- 環境差異によるAI誤判断を防止

### 📊 ドキュメント統計
- 新規ドキュメント: 約3,500語
- コードサンプル: 15箇所
- 図解: 3箇所
- チェックリスト: 4箇所

### 🚀 次のステップ

#### 短期（今すぐ）
1. `docker-compose up` で動作確認
2. `.env` ファイル作成（`.env.example`参考）
3. コンテナログ確認

#### 中期（今週中）
1. CI/CDパイプラインにDocker統合
2. ステージング環境でテスト
3. チームメンバーに展開・フィードバック収集

#### 長期（今月中）
1. 本番環境にデプロイ
2. モニタリング設定
3. パフォーマンスチューニング

### 🔗 関連リンク
- 元動画: [URL]
- Docker公式ドキュメント: https://docs.docker.com/
- docker-compose公式: https://docs.docker.com/compose/

---

**質問・不明点があれば、各ガイドのトラブルシューティングを参照するか、Issueを作成してください！**
```

---

## 💡 カスタマイズ例

### 自分のプロジェクト用に調整

```markdown
# プロジェクト固有設定をここに記載
PROJECT_NAME="PIMS"
DOCS_DIR="docs/"
RULES_DIR=".cursor/rules/"
STYLE="emoji使用、日本語、Markdown"

# テンプレートの[変数]を置き換え
sed "s/\[プロジェクト名\]/$PROJECT_NAME/g" template.md > my-prompt.md
```

---

## 📚 関連リソース

- [詳細版テンプレート](./video-integration-prompt-template.md)
- [Git/GitHub統合事例](../git-github-beginner-guide.md)
- [プロジェクト構造ルール](../../.cursor/rules/project-structure.mdc)

---

_このクイックリファレンスは、実践を通じて継続的に改善されます。_

