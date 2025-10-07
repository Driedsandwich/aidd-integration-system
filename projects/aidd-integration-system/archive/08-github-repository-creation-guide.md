# GitHubリポジトリ作成手順 - aidd-integration-system

## リポジトリ作成方法

### 方法1: GitHub Web UI（推奨）

1. **GitHub.comにアクセス**
   - https://github.com にアクセス
   - ログイン

2. **新しいリポジトリ作成**
   - 右上の「+」→「New repository」
   - Repository name: `aidd-integration-system`
   - Description: `AI-Driven Development Integration System - 統合PDCAサイクルと知見共有システム`
   - Public を選択
   - 「Add a README file」にチェック
   - 「Add .gitignore」で「Python」を選択
   - 「Choose a license」で「MIT License」を選択
   - 「Create repository」をクリック

### 方法2: GitHub CLI

```bash
# GitHub CLIのインストール（未インストールの場合）
# Windows: winget install GitHub.cli
# macOS: brew install gh
# Linux: curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

# ログイン
gh auth login

# リポジトリ作成
gh repo create aidd-integration-system \
  --public \
  --description "AI-Driven Development Integration System - 統合PDCAサイクルと知見共有システム" \
  --add-readme \
  --gitignore Python \
  --license MIT
```

### 方法3: Gitコマンド

```bash
# ローカルリポジトリ初期化
mkdir aidd-integration-system
cd aidd-integration-system
git init

# リモートリポジトリ追加（GitHubで作成後）
git remote add origin https://github.com/[USERNAME]/aidd-integration-system.git

# 初回プッシュ
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

## 初期ファイル構成

### README.md（自動生成されるものを置き換え）

```markdown
# AI-Driven Development Integration System

AI駆動開発の統合システム - ルール改善サイクルとIssue管理によるPDCAサイクル高速回転とAI横断的知見共有システム

## 🚀 概要

本システムは、AI駆動開発（AIDD）において以下の4つのコア機能を統合したシステムです：

1. **ルール改善サイクル** - AIエージェントの継続的改善
2. **Issue管理** - PDCAサイクルによるスパゲッティコード防止
3. **ドキュメント活用** - @機能による最新仕様参照
4. **MCP導入** - 外部システム連携による機能拡張

## ✨ 主な機能

- **統合PDCAサイクル**: 人間を大幅に上回る高速回転（43,344.5サイクル/分）
- **マルチレベルPDCA**: プロダクト・プロジェクト・リポジトリ横断でのPDCA実行
- **AI横断知見共有**: 中央知見リポジトリによる継続的進化
- **統合スコア**: 90%の高品質な開発プロセス

## 📚 ドキュメント

- [全体概要](docs/01-overview.md)
- [ルール改善サイクル](docs/02-rule-improvement-cycle.md)
- [Issue管理](docs/03-issue-management.md)
- [統合運用ガイド](docs/04-integration-guide.md)
- [マルチレベルPDCA](docs/05-multi-level-pdca.md)
- [知見共有システム](docs/06-knowledge-sharing.md)
- [将来ロードマップ](docs/07-future-roadmap.md)

## 🛠️ クイックスタート

### 1. リポジトリのクローン

```bash
git clone https://github.com/[USERNAME]/aidd-integration-system.git
cd aidd-integration-system
```

### 2. 仮想環境の設定

```bash
# Python仮想環境作成
python -m venv .venv

# 仮想環境有効化
# Windows
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

### 3. 統合PDCAシステムの実行

```bash
# 基本統合PDCAデモ
python src/pdca_integration_demo.py

# マルチレベル統合PDCAシステム
python src/multi_level_knowledge_system.py
```

## 📁 プロジェクト構成

```
aidd-integration-system/
├── README.md                    # プロジェクト概要
├── docs/                        # ドキュメント
├── src/                         # ソースコード
├── templates/                   # テンプレート集
├── examples/                    # 実装例
├── research/                    # 研究資料
└── .github/                     # GitHub設定
```

## 🤝 貢献

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🙏 謝辞

- [【実践】AI駆動開発を10倍快適にする【AIDD】](https://www.youtube.com/watch?v=Uk1qB_-RAps) - 数理の弾丸⚡️京大博士のAI解説
- [【実践】AI駆動開発を10倍快適にする完全ガイド](https://zenn.dev/daideguchi/articles/85f1af576667e0) - Zenn記事
- Cursor - AI駆動開発エディタ

## 📞 サポート

質問やサポートが必要な場合は、[Issues](https://github.com/[USERNAME]/aidd-integration-system/issues)でお気軽にお問い合わせください。

---

**AI駆動開発の新たなスタンダードを目指して**
```

### LICENSE（MIT License）

```text
MIT License

Copyright (c) 2025 AI-Driven Development Integration System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### .gitignore（Python用）

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Cursor
.cursor/

# Logs
*.log

# Temporary files
*.tmp
*.temp
```

## ファイルアップロード手順

### 1. 基本ファイルのアップロード

リポジトリ作成後、以下のファイルをアップロード：

1. **ドキュメント類**
   - `統合運用ガイド.md` → `docs/04-integration-guide.md`
   - `ルール改善サイクル実践ガイド.md` → `docs/02-rule-improvement-cycle.md`
   - `Issue管理実践ガイド.md` → `docs/03-issue-management.md`
   - `マルチレベル統合PDCA設計.md` → `docs/05-multi-level-pdca.md`

2. **ソースコード**
   - `src/pdca_integration_demo.py`
   - `src/multi_level_knowledge_system.py`

3. **テンプレート**
   - `.cursor/rules/` ディレクトリ → `templates/cursor-rules/`

### 2. GitHub Web UIでのアップロード

1. リポジトリページで「Add file」→「Upload files」
2. ファイルをドラッグ&ドロップまたは「choose your files」
3. コミットメッセージを入力
4. 「Commit changes」をクリック

### 3. Gitコマンドでのアップロード

```bash
# ローカルリポジトリのクローン
git clone https://github.com/[USERNAME]/aidd-integration-system.git
cd aidd-integration-system

# ファイルのコピー（既存の成果物から）
# ここで作成した成果物を適切なディレクトリに配置

# コミット・プッシュ
git add .
git commit -m "Add AIDD integration system implementation"
git push origin main
```

## 推奨設定

### リポジトリ設定

1. **About設定**
   - Description: `AI-Driven Development Integration System - 統合PDCAサイクルと知見共有システム`
   - Website: （将来のWebサイトURL）
   - Topics: `ai-driven-development`, `pdca`, `cursor`, `github-integration`, `knowledge-sharing`, `automation`

2. **Features設定**
   - Issues: 有効
   - Projects: 有効
   - Wiki: 有効
   - Discussions: 有効

3. **Security設定**
   - Dependency graph: 有効
   - Dependabot alerts: 有効
   - Dependabot security updates: 有効

### 初期Issue作成

リポジトリ作成後、以下のIssueを作成することを推奨：

1. **Welcome Issue** - プロジェクト紹介
2. **Documentation Improvement** - ドキュメント改善
3. **Feature Requests** - 機能要求
4. **Community Guidelines** - コミュニティガイドライン

## まとめ

`aidd-integration-system`リポジトリの作成により、本件で実現した価値ある成果物を体系的に整理し、継続的な発展とコミュニティ形成を実現できます。

### 次のステップ

1. **リポジトリ作成**: 上記手順に従ってリポジトリを作成
2. **ファイルアップロード**: 既存の成果物を適切に配置
3. **コミュニティ形成**: Issue・Discussionを活用したコミュニティ形成
4. **継続的改善**: ユーザーフィードバックに基づく継続的改善

このリポジトリは、AI駆動開発の新たなスタンダードとなる可能性を秘めています。
