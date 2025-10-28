# ツール移行ガイド

このガイドは、Cursor/GitHub以外のツールへ移行する場合の手順を記載しています。

> **設計思想**: ツール非依存の設計により、将来的なツール移行を容易にする

---

## 🎯 ツール非依存の設計

### 現在の構成

```
【ツール依存層】
├─ .cursor/
│   ├─ rules/*.mdc      ← Cursor固有（但しMarkdown互換）
│   └─ mcp.json         ← Cursor固有（但しJSON標準）

【ツール非依存層】
├─ docs/               ← 完全な標準Markdown
├─ scripts/            ← 標準Python
├─ README.md           ← 標準Markdown
└─ CONTRIBUTING.md     ← 標準Markdown
```

**可搬性**: ✅ **高い**（標準フォーマット使用）

---

## 📋 移行シナリオ

---

## シナリオ1: Cursor → 別のAIエディタ

### 想定状況

- Cursorのサポート終了
- より優れたAIエディタの登場
- 組織のツール方針変更

---

### 移行手順

#### Step 1: ルールファイルの移行

**現状**: `.cursor/rules/*.mdc`（Markdown形式）

**移行方法**:

```bash
# 例: 新ツールが .newtool/rules/*.md を使用する場合

# 1. ディレクトリコピー
cp -r .cursor/rules/ .newtool/rules/

# 2. ファイル拡張子変更（必要な場合）
cd .newtool/rules/
for file in *.mdc; do
  mv "$file" "${file%.mdc}.md"
done

# 3. 内容の調整（新ツール固有の構文がある場合）
# 必要に応じて編集
```

**所要時間**: 10-20分

**自動化**: 可能（`scripts/migrate-rules.py`を作成）

---

#### Step 2: MCP設定の移行

**現状**: `.cursor/mcp.json`（JSON形式）

**移行方法**:

```bash
# 例: 新ツールが .newtool/mcp-config.json を使用する場合

# 1. 設定ファイルをコピー
cp .cursor/mcp.json .newtool/mcp-config.json

# 2. 新ツールの形式に変換（必要な場合）
# 手動編集 または 変換スクリプト使用
```

**注意**:
- MCP（Model Context Protocol）はAnthropic提唱のオープン標準
- 複数のツールで対応済み（Cursor, Claude Desktop等）
- 互換性が高い

---

#### Step 3: ドキュメント・スクリプトの利用

**現状**: `docs/`, `scripts/`（標準フォーマット）

**移行方法**: ✅ **そのまま使用可能**

**理由**:
- Markdownは標準フォーマット
- Pythonスクリプトは環境非依存
- ツール固有の要素なし

---

### 移行後の構成例

```
新ツールのディレクトリ/
├─ .newtool/
│   ├─ rules/*.md       ← .cursor/rules/*.mdc から移行
│   └─ mcp-config.json  ← .cursor/mcp.json から変換
├─ docs/               ← そのまま使用
├─ scripts/            ← そのまま使用
├─ README.md           ← そのまま使用
└─ CONTRIBUTING.md     ← そのまま使用
```

---

## シナリオ2: GitHub → 別のGitホスティング

### 想定状況

- GitHubのサービス終了
- GitLab/Gitea/BitBucket等への移行
- 完全ローカル化（プライベートGitサーバー）

---

### 移行手順

#### Step 1: リポジトリのミラーリング

```bash
# 1. 現在のリポジトリを完全バックアップ
git clone --mirror https://github.com/Driedsandwich/aidd-integration-system.git
cd aidd-integration-system.git

# 2. 新サービスへプッシュ
# 例: GitLabへ移行
git push --mirror https://gitlab.com/Driedsandwich/aidd-integration-system.git

# 例: 自前Giteaサーバーへ移行
git push --mirror https://git.yourserver.com/Driedsandwich/aidd-integration-system.git
```

**所要時間**: 数分（Gitの標準機能）

---

#### Step 2: Issue/PRの移行

**課題**: Issue/PRはGitHub固有の機能

**対応策**:

1. **エクスポート**:
   ```bash
   # GitHub CLIでIssue/PRをエクスポート
   gh issue list --repo Driedsandwich/aidd-integration-system --json number,title,body,state --limit 1000 > issues.json
   gh pr list --repo Driedsandwich/aidd-integration-system --json number,title,body,state --limit 1000 > prs.json
   ```

2. **インポート**:
   - GitLab: GitLab API使用
   - Gitea: Gitea API使用
   - 各サービスのインポート機能を利用

**所要時間**: 1-2時間（手動）、または自動化スクリプト作成

---

#### Step 3: ドキュメント内のリンク更新

**現状**: GitHub固有のURL（Issue/PR）

**更新方法**:

```bash
# 一括置換（例: GitLabへ移行）
find docs/ -name "*.md" -type f -exec sed -i 's|github.com/Driedsandwich/aidd-integration-system|gitlab.com/Driedsandwich/aidd-integration-system|g' {} \;

# または、Cursorに依頼
「docs/配下の全Markdownファイルで、
 github.com を gitlab.com に置換してください」
```

**所要時間**: 10分

---

### 移行後の動作確認

**確認項目**:
- [ ] リポジトリCloneが正常動作
- [ ] Issue/PR機能が正常動作
- [ ] ドキュメントリンクが有効
- [ ] CI/CDが動作（使用している場合）

---

## シナリオ3: 完全ローカル化

### 想定状況

- クラウドサービスに依存したくない
- オフライン環境での使用
- 完全なプライバシー確保

---

### 移行手順

#### Step 1: ローカルGitサーバー構築

**推奨ツール**: Gitea（軽量、セットアップ簡単）

```bash
# Dockerで実行（最も簡単）
docker run -d \
  --name gitea \
  -p 3000:3000 \
  -p 222:22 \
  -v /var/lib/gitea:/data \
  gitea/gitea:latest

# アクセス: http://localhost:3000
```

**所要時間**: 30分

---

#### Step 2: リポジトリをローカルサーバーへ

```bash
# 1. リポジトリをミラー
git clone --mirror <GitHubリポジトリ>
cd <リポジトリ>.git
git push --mirror <ローカルGitサーバー>
```

---

#### Step 3: 通常のGit操作へ切り替え

```bash
# ローカルサーバーからClone
git clone http://localhost:3000/Driedsandwich/aidd-integration-system.git
cd aidd-integration-system

# 以降、通常のGit操作
git add .
git commit -m "xxx"
git push
```

**効果**: ✅ **完全オフライン動作**

---

## 📊 移行の影響分析

### 影響が少ないもの

| 項目 | 理由 | 移行コスト |
|------|------|--------|
| ルールファイル | Markdown標準 | ほぼゼロ |
| ドキュメント | Markdown標準 | ゼロ |
| スクリプト | Python標準 | ゼロ |
| Git操作 | Git標準 | ゼロ |

---

### 影響があるもの

| 項目 | 理由 | 移行コスト | 対応策 |
|------|------|-----------|--------|
| Issue/PR | GitHub固有 | 中 | エクスポート→インポート |
| GitHub CLI (`gh`) | GitHub専用 | 低 | 新サービスのCLI使用 |
| ドキュメント内リンク | GitHub URL | 低 | 一括置換 |
| MCP設定 | ツール依存 | 低 | JSON変換 |

---

## 🔧 移行支援ツール（将来実装）

### ツール1: ルール移行スクリプト

**ファイル**: `scripts/migrate-rules.py`

```python
#!/usr/bin/env python3
"""
ルールファイルを新ツール形式へ移行

使い方:
  python scripts/migrate-rules.py --from cursor --to newtool
"""

import shutil
import argparse
from pathlib import Path

def migrate_rules(from_tool, to_tool):
    """ルールファイルを移行"""
    source_dir = Path(f".{from_tool}/rules")
    target_dir = Path(f".{to_tool}/rules")
    
    # ディレクトリ作成
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # ファイルコピー
    for file in source_dir.glob("*.mdc"):
        # 拡張子変更（.mdc → .md）
        target_file = target_dir / f"{file.stem}.md"
        shutil.copy(file, target_file)
        print(f"✅ {file.name} → {target_file.name}")
    
    print(f"\n✅ 移行完了: {source_dir} → {target_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="from_tool", required=True)
    parser.add_argument("--to", dest="to_tool", required=True)
    args = parser.parse_args()
    
    migrate_rules(args.from_tool, args.to_tool)
```

**優先度**: ⏸️ **低**（移行時に実装）

---

### ツール2: リンク更新スクリプト

**ファイル**: `scripts/update-links.py`

```python
#!/usr/bin/env python3
"""
ドキュメント内のGitHubリンクを更新

使い方:
  python scripts/update-links.py --from github.com --to gitlab.com
"""

import argparse
import re
from pathlib import Path

def update_links(from_host, to_host, directory="docs"):
    """Ｍarkdownファイル内のリンクを更新"""
    updated = 0
    
    for md_file in Path(directory).rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # リンク置換
        new_content = content.replace(from_host, to_host)
        
        if content != new_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 更新: {md_file}")
            updated += 1
    
    print(f"\n✅ {updated}ファイルを更新しました")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--dir", default="docs")
    args = parser.parse_args()
    
    update_links(args.from_arg, args.to, args.dir)
```

**優先度**: ⏸️ **低**（移行時に実装）

---

## 📋 移行チェックリスト

### Cursor → 別のAIエディタ

- [ ] ルールファイル移行（`.cursor/rules/*.mdc` → `.newtool/rules/*.md`）
- [ ] MCP設定変換（`.cursor/mcp.json` → 新ツール形式）
- [ ] ドキュメント確認（そのまま使用）
- [ ] スクリプト確認（そのまま使用）
- [ ] 動作テスト

**所要時間**: 1-2時間

---

### GitHub → GitLab/Gitea

- [ ] リポジトリミラーリング（`git clone --mirror` → `git push --mirror`）
- [ ] Issue/PRエクスポート（`gh issue/pr list --json`）
- [ ] 新サービスへインポート
- [ ] ドキュメント内リンク更新（`github.com` → `gitlab.com`）
- [ ] 動作テスト

**所要時間**: 2-3時間

---

### 完全ローカル化

- [ ] ローカルGitサーバー構築（Gitea/GitLab CE）
- [ ] リポジトリミラーリング
- [ ] チーム内での利用設定
- [ ] バックアップ戦略確立

**所要時間**: 半日-1日

---

## 🎯 移行を容易にする設計原則

### 1. 標準フォーマットの使用

**現状**:
- ✅ Markdown（ルール、ドキュメント）
- ✅ JSON（設定ファイル）
- ✅ Python（スクリプト）
- ✅ Git（バージョン管理）

**効果**: ✅ **他のツールでも読める・使える**

---

### 2. ツール固有機能の最小化

**原則**:
- Cursor固有の機能に過度に依存しない
- 標準的なファイル・ディレクトリ構造
- 環境変数・設定ファイルで抽象化

**効果**: ✅ **移行時の書き換えが最小限**

---

### 3. 設定の外部化

**現状**:
- `.cursor/mcp.json`: MCP設定
- `.gitignore`: 除外設定
- `docs/`: ドキュメント（ツール非依存）

**効果**: ✅ **設定ファイルのみ変換すれば移行完了**

---

## 📝 移行時のドキュメント更新

### 更新が必要なファイル

1. **README.md**
   - ツール名の変更（Cursor → 新ツール）
   - インストール手順の更新

2. **QUICK_START.md**
   - セットアップ手順の更新
   - CLI名の変更（`gh` → 新サービスのCLI）

3. **docs/environment-setup-guide.md**
   - 環境変数の説明更新
   - ツール固有の設定説明

---

### 更新方法（Cursorに依頼）

```
Cursorに指示:

「docs/配下の全Markdownファイルで、
 以下の置換を行ってください：
 - Cursor → NewTool
 - github.com → gitlab.com
 - gh コマンド → glab コマンド」
```

**所要時間**: 10分

---

## 🔄 継続的な可搬性の維持

### 定期チェック

**監査項目**（3ヶ月ごと）:
- [ ] ツール固有の機能に過度に依存していないか
- [ ] 標準フォーマットを維持しているか
- [ ] 新しい依存関係が追加されていないか
- [ ] ドキュメントが最新か

---

### 新機能追加時の原則

**追加前のチェック**:
- [ ] この機能はツール非依存か？
- [ ] 標準的な方法で実装できるか？
- [ ] 他のツールでも再現できるか？

**YES → 実装**  
**NO → 代替案を検討**

---

## 💡 推奨事項

### 1. バックアップ戦略

**定期バックアップ**:
```bash
# 月次バックアップ（完全ミラー）
git clone --mirror https://github.com/Driedsandwich/aidd-integration-system.git
# ローカル/外部ストレージに保存
```

**効果**: サービス終了時でも即座に復旧可能

---

### 2. 複数サービスでのミラーリング

**戦略**:
```
GitHub（メイン）
  ↓（自動同期）
GitLab（バックアップ）
  ↓（自動同期）
ローカルGitサーバー（最終バックアップ）
```

**実装**:
```bash
# GitHub ActionsでGitLabへ自動同期
# .github/workflows/mirror.yml を作成
```

**優先度**: ⏸️ **低**（現時点では不要）

---

### 3. 移行練習

**年次移行演習**:
- テスト環境で実際に移行を試す
- 手順を検証・更新
- 所要時間を計測

**効果**: 実際の移行時に慈てない

---

## 🎯 現時点での推奨

### 即座に実施

- ✅ **このガイドをリポジトリに追加**（今回実施）
- ✅ **標準フォーマットの維持**（既に実施中）

### 将来検討

- ⏸️ 移行スクリプトの作成（移行時）
- ⏸️ 複数サービスミラーリング（必要に応じて）
- ⏸️ 定期バックアップの自動化（必要に応じて）

---

## 📊 結論

### 現在の設計の評価

**ツール可搬性**: ✅ **高い**

**理由**:
1. 標準フォーマット使用（Markdown, JSON, Python, Git）
2. ツール固有機能の最小化
3. 設定の外部化

**移行コスト**: ✅ **低い**（1-3時間で完了可能）

---

### 安心して使える

現在の設計は、将来的なツール移行を十分に考慮しています。

**Cursor/GitHubが終了しても**:
- ルールは他のエディタで使える
- スクリプトはそのまま動く
- ドキュメントは変わらず読める
- Gitの履歴は保持される

---

**最終更新**: 2025-10-21  
**対象**: ツール移行を検討する全ユーザー
