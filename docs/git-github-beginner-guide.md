# Git/GitHub 初心者ガイド（AI駆動開発対応）

> 非エンジニアのためのGit+GitHub入門 - コマンド暗記不要、GitHub Desktop使用

## 📚 目次

1. [なぜAI時代にGitが重要なのか](#なぜai時代にgitが重要なのか)
2. [GitとGitHubの基礎概念](#gitとgithubの基礎概念)
3. [セットアップ手順](#セットアップ手順)
4. [基本操作（GitHub Desktop）](#基本操作github-desktop)
5. [ブランチ戦略](#ブランチ戦略)
6. [よく使う操作](#よく使う操作)
7. [重要な注意事項](#重要な注意事項)

---

## なぜAI時代にGitが重要なのか

### 🤖 AIという「共同作業者」の登場

従来、Gitは主にチーム開発のツールでしたが、AI時代では**個人作業でも必須**になりました。その理由は：

1. **AIがファイルを勝手に編集・削除する可能性がある**
   - Cursorなどのエージェント型AIは、ファイルを自動的に変更します
   - 予期しない変更が起きても、Gitで簡単に元に戻せます

2. **クラウドでAIに作業を依頼できる**
   - GitHubと連携することで、スマホからでもAIに仕事を依頼可能
   - GitHub ActionsやCodespaces等を活用できます

3. **変更履歴が「学習記録」になる**
   - どんな試行錯誤をしたか、AIとどう対話したかが記録されます
   - チーム全体の知見として共有できます

### ✅ このガイドで学べること

- ✨ **コマンド不要** - GitHub Desktopで全て操作
- 🔰 **初心者向け** - 必要最小限の概念だけ解説
- 🤝 **AI連携** - Cursor/Windsurf等との統合運用方法

---

## GitとGitHubの基礎概念

### 📖 重要用語（最小限）

#### 1. リポジトリ（Repository）
- Gitで管理されるプロジェクト全体のこと
- ファイル + 変更履歴がまとまったもの
- 「レポジトリー」とも呼ばれます（どちらでもOK）

#### 2. コミット（Commit）
- 変更内容を確定して履歴に記録する操作
- Googleドキュメントの「変更履歴」の1つ1つに相当
- コミットメッセージで「何を変更したか」を説明します

#### 3. ローカル vs リモート
- **ローカル**: あなたのPCにあるリポジトリ
- **リモート**: GitHub（クラウド）にあるリポジトリ
- ExcelファイルをGoogleドライブにアップロードするイメージ

#### 4. プッシュ（Push） / プル（Pull）
- **プッシュ**: ローカルの変更をGitHubにアップロード
- **プル**: GitHubの最新状態をローカルに取得

#### 5. ブランチ（Branch）
- 変更履歴を分岐させる機能
- 実験的な変更や、複数人での並行作業に使用
- メインブランチを壊さずに安全に作業できます

#### 6. マージ（Merge）
- ブランチの変更を統合する操作
- 例: 実験ブランチの成果をメインブランチに取り込む

#### 7. プルリクエスト（Pull Request / PR）
- 「この変更をマージしてください」というリクエスト
- レビューやディスカッションができます
- **AI活用**: AIにプルリクを作成してもらうことも可能

---

## セットアップ手順

### 前提条件

- **エディター**: Cursor または VS Code をインストール済み
- **ブラウザ**: 最新のChrome/Edge/Firefox等

### 1️⃣ Gitのインストール

#### 🪟 Windows
1. [Git公式サイト](https://git-scm.com/)からダウンロード
2. インストーラーを実行（基本的にデフォルト設定でOK）

#### 🍎 Mac
- 最近のmacOSには最初から入っています
- ターミナルで確認:
  ```bash
  git --version
  ```
- 入っていない場合はHomebrewでインストール:
  ```bash
  brew install git
  ```

### 2️⃣ GitHubアカウント作成

1. [GitHub](https://github.com/)を開く
2. 右上の「Sign up」をクリック
3. **Googleログインが簡単**: アカウントを選択
4. **ユーザー名を入力**: URLにも使われるので慎重に
5. 「Create account」をクリック

### 3️⃣ GitHub Desktopのインストール

1. [GitHub Desktop公式サイト](https://desktop.github.com/)からダウンロード
2. インストーラーの指示に従う
3. GitHubアカウントでサインイン
4. デフォルト設定のまま進める

> **💡 なぜGitHub Desktop？**
> - コマンドを覚える必要がない
> - SSH鍵の設定など、初心者にハードルが高い部分をスキップできる
> - 視覚的に変更を確認できる

---

## 基本操作（GitHub Desktop）

### 📦 最初のリポジトリを作成

#### GitHubで新規リポジトリ作成

1. GitHubにログインし、左の「Create repository」をクリック
2. **Repository name**: `my-first-repo` など入力
3. **⚠️ Visibility**: 「Private」を選択（重要！）
   - Publicにすると誰でも見れてしまいます
4. 「Create repository」をクリック

#### GitHub Desktopでクローン

1. GitHub Desktopで先ほど作成したリポジトリを選択
2. 「Clone」ボタンをクリック
3. PCのどのフォルダーに保存するか指定
4. 完了！ローカルにリポジトリがダウンロードされました

### 📝 ファイルを追加してコミット

1. **エディター（Cursor/VS Code）でリポジトリフォルダを開く**
2. **新しいファイルを作成**: 例 `test.md`
3. **内容を書いて保存**:
   ```markdown
   # テストファイル
   
   これは最初のコミットです。
   ```

4. **GitHub Desktopに戻る**
   - 変更が自動的に検出されています
   - チェックが付いているファイルが「ステージング」状態

5. **コミットメッセージを入力**
   - AIに自動生成させる場合: 左下のCopilotマークをクリック
   - 手動で書く場合: 「Add test.md」など簡潔に

6. **「Commit to main」ボタンをクリック**

7. **「Push origin」ボタンをクリック**
   - GitHubにアップロードされます

8. **GitHubで確認**
   - ブラウザでリポジトリを開き、ファイルが反映されているか確認

### 🎉 おめでとうございます！

これでGitの基礎である「コミット作成」と「リモートと同期」ができました。

---

## ブランチ戦略

### 🌿 ブランチとは

- コミット履歴を分岐させる機能
- メインブランチを壊さずに実験できる
- AI活用時の重要なパターン:
  - AIに作業させる専用ブランチを作る
  - 結果を確認してからメインにマージ

### ブランチの作成

1. GitHub Desktop上部の現在のブランチ名をクリック
2. 「New Branch」をクリック
3. ブランチ名を入力: 例 `feature/new-experiment`
4. 「Create Branch」をクリック

### ブランチでの作業

1. **ファイルを編集・保存**
2. **コミット** （通常と同じ手順）
3. **メインブランチに切り替え**
   - ファイルが消えていることを確認
4. **ブランチを戻す**
   - ファイルが復活します

### マージ方法

#### 方法1: ローカルで直接マージ

1. **メインブランチに切り替え**
2. ブランチドロップダウン下の「Choose a branch to merge into main」をクリック
3. マージするブランチを選択
4. 完了！

#### 方法2: プルリクエスト（推奨）

1. **ブランチを選択した状態で「Publish branch」をクリック**
2. **「Preview Pull Request」→「Create Pull Request」**
3. **GitHubのページが開く**
   - コミット履歴やファイル変更を確認できます
4. **「Merge pull request」→「Confirm merge」**
5. **GitHub Desktopに戻り、メインブランチをPull**
   - 左上のメニューから「Pull」を選択
   - リモートの変更がローカルに反映されます

> **💡 プルリクエストのメリット**
> - 変更内容をレビューできる
> - ディスカッションができる
> - AIが作成したプルリクを確認してからマージできる

---

## よく使う操作

### 1. Discard Changes（変更を破棄）

**用途**: やっぱりこの変更いらないな、という時

1. GitHub Desktopで削除したい変更を右クリック
2. 「Discard Changes」をクリック
3. ファイル全体または一部の変更を取り消せます

### 2. Revert（コミットを打ち消す）

**用途**: 過去のコミットが原因で問題が起きた時

1. 「History」タブを開く
2. 取り消したいコミットを右クリック
3. 「Revert Changes in Commit」を選択
4. そのコミットの変更を打ち消す新しいコミットが作成されます

### 3. マージコンフリクトの解消

**発生条件**: 複数の人（またはAI）が同じファイルの同じ場所を編集した時

#### 解消手順

1. **GitHub Desktopに警告が表示**
   - コンフリクトしているファイルが表示されます

2. **エディターでファイルを開く**
   ```
   <<<<<<< HEAD
   あなたの変更
   =======
   他者（AI）の変更
   >>>>>>> branch-name
   ```

3. **どちらを採用するか決定**
   - Cursorなら上部にボタンが表示されるのでクリックするだけ
   - 手動の場合は記号を削除して適切に編集

4. **GitHub Desktopに戻り「Continue Merge」をクリック**

---

## 重要な注意事項

### 🚨 APIキーなどの機密情報を絶対にアップロードしない

**これは非常に重要です！**

#### 問題
- APIキーをGitHubにアップすると、悪意のある人に使われる可能性があります
- 高額な請求が来る事例が多数報告されています

#### 対策

1. **`.env` ファイルに機密情報を書く**
   ```env
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   OPENAI_API_KEY=sk-xxxxxxxxxxxxx
   ```

2. **`.gitignore` ファイルを作成**
   ```gitignore
   # 環境変数ファイル
   .env
   .env.local
   .env.*.local
   
   # APIキー関連
   **/secrets/
   **/*secret*
   
   # OS関連
   .DS_Store
   Thumbs.db
   
   # エディター関連
   .vscode/
   .idea/
   ```

3. **`.env.example` を作成（値は空）**
   ```env
   # APIキーの例（実際の値は.envに記入してください）
   ANTHROPIC_API_KEY=
   OPENAI_API_KEY=
   ```

4. **確認方法**
   - GitHub Desktopで `.env` が表示されないことを確認
   - 表示されたら即座に `.gitignore` を修正

> **⚠️ すでにアップロードしてしまった場合**
> 1. 即座にAPIキーを無効化（各サービスのダッシュボードで）
> 2. 新しいAPIキーを発行
> 3. Gitの履歴から完全に削除（高度な操作が必要）

---

## AI駆動開発との統合

### 🤖 Cursorとの統合運用

#### 推奨ワークフロー

1. **作業開始前に新しいブランチを作成**
   ```
   feature/ai-suggested-changes
   ```

2. **CursorでAIに作業を依頼**
   - AIがファイルを編集します

3. **変更を確認**
   - GitHub Desktopで差分を確認
   - 意図しない変更がないかチェック

4. **コミット**
   - AIが生成したコード: `feat: AI generated authentication logic`
   - 手動修正: `fix: Corrected AI-generated typo in auth.js`

5. **プルリクエストを作成**
   - AIの変更をレビュー
   - 問題なければマージ

#### コミットメッセージの規則

このプロジェクトでは [Conventional Commits](https://www.conventionalcommits.org/) を推奨：

- `feat:` - 新機能
- `fix:` - バグ修正
- `docs:` - ドキュメント変更
- `refactor:` - リファクタリング
- `test:` - テスト追加
- `chore:` - 雑務

例:
```
feat(auth): Add JWT authentication
fix(api): Correct endpoint validation
docs(readme): Update installation instructions
```

### 🔄 Taskmasterとの連携

このプロジェクトはTaskmasterで管理されています。Git運用との統合：

1. **タスクごとにブランチを作成**
   ```
   task-15-implement-auth
   ```

2. **コミットメッセージにタスクIDを含める**
   ```
   feat: Implement user authentication (Task #15)
   ```

3. **サブタスク完了時にコミット**
   ```bash
   task-master update-subtask --id=15.2 --prompt="GitHub認証を実装。コミットID: abc123"
   ```

---

## 参考リンク

- [GitHub Desktop公式ドキュメント](https://docs.github.com/ja/desktop)
- [Git入門（日本語）](https://git-scm.com/book/ja/v2)
- [Conventional Commits](https://www.conventionalcommits.org/ja/)
- 元動画: [非エンジニアのためのGit+GitHub入門](https://youtu.be/Uml3jEPWIKo)

---

## トラブルシューティング

### よくある問題

#### Q: プッシュできない
- **原因**: リモートが先に進んでいる可能性
- **解決**: まず `Pull` してから `Push`

#### Q: コンフリクトが怖い
- **解決**: ブランチを使えばメインを壊さない。安心して実験できます

#### Q: 間違えてコミットしてしまった
- **解決**: `Revert` で打ち消すか、まだプッシュしていなければ履歴から削除可能

#### Q: .gitignoreが効かない
- **原因**: すでにGitに追跡されているファイルは無視されません
- **解決**: 一度Gitから削除してから.gitignoreに追加
  ```bash
  git rm --cached ファイル名
  ```

---

## まとめ

✅ **覚えるべき最小限の操作**
1. コミット（変更を記録）
2. プッシュ（GitHubにアップロード）
3. プル（GitHubから取得）
4. ブランチ作成（安全に実験）
5. マージ（変更を統合）

✅ **AI時代のGit活用**
- AIの変更を安全に管理
- クラウドでAIを動かす基盤
- チーム全体の知見として蓄積

✅ **絶対に守ること**
- APIキーを `.env` に書く
- `.gitignore` で `.env` を除外
- プライベートリポジトリを使う

このガイドをマスターすれば、AI駆動開発の基盤が整います。次のステップとして、GitHub ActionsやCodespacesを活用したクラウドAI運用に進みましょう！

---

**関連ドキュメント**
- [AI駆動開発実践ガイド](./AI駆動開発実践ガイド.md)
- [統合運用ガイド](./04-integration-guide.md)
- [Issue管理実践ガイド](./03-issue-management.md)



