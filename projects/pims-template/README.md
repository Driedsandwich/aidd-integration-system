# PIMS (PDCA-Issue Muramasa System) Template

[![PIMS Template](https://img.shields.io/badge/PIMS-Template-blue.svg)](https://github.com/Driedsandwich/pims-template)
[![PDCA Cycle](https://img.shields.io/badge/PDCA-Cycle-green.svg)](https://github.com/Driedsandwich/pims-template)
[![GitHub Template](https://img.shields.io/badge/GitHub-Template-lightgrey.svg)](https://github.com/Driedsandwich/pims-template)

**PIMS (PDCA-Issue Muramasa System)** は、GitHub IssuesとPDCAサイクルを組み合わせた継続的改善システムです。このテンプレートリポジトリを使用することで、どのプロジェクトでも迅速にPIMSを導入できます。

## 🚀 クイックスタート

### 方法1: テンプレートから新規作成（推奨）

```bash
# GitHub CLIを使用
gh repo create <owner>/<repo-name> --public --template Driedsandwich/pims-template --description "PIMS運用導入リポジトリ"

# または GitHub Web UI で「Use this template」ボタンを使用
```

### 方法2: 既存リポジトリに導入

```bash
# テンプレートをクローン
gh repo clone Driedsandwich/pims-template
cd pims-template

# 必要なファイルを既存リポジトリにコピー
cp -r .github <your-repo>/
cp PDCA_ISSUE_USAGE_GUIDE.md <your-repo>/

# 既存リポジトリでコミット
cd <your-repo>
git add .
git commit -m "feat: PIMS導入（Issue/PRテンプレート＋運用ガイド）"
git push
```

## 📋 含まれる要素

### 🎯 Issueテンプレート
- **PDCA開発サイクル**: 標準的なPDCA運用用
- **緊急修復**: 障害対応用

### 🔄 Pull Requestテンプレート
- PIMS気づき記録
- Evidence（証跡）記録
- 担当者情報

### 🏷️ ラベルセット
- `pdca-phase:*`: Plan/Do/Check/Act フェーズ
- `pims-type:*`: 開発/バグ修正/リファクタリング等
- `priority:*`: 優先度
- `status:*`: 進捗状況
- `knowledge:*`: 知識蓄積状況

### ⚙️ GitHub Actions
- **pims-setup.yml**: 初期セットアップ（ラベル作成等）
- **pims-ci.yml**: PIMS構造検証
- **pims-knowledge.yml**: 知識自動抽出

## 🛠️ 初期セットアップ

### 1. ラベルセットアップ
```bash
# GitHub CLIでワークフロー実行
gh workflow run pims-setup.yml -f setup_labels=true
```

### 2. 手動ラベル作成（代替）
```bash
# ラベルファイルを確認
cat .github/labels.yml

# GitHub CLIで個別作成
gh api repos/<owner>/<repo>/labels -f name="pdca-phase:plan" -f color="0052CC" -f description="PDCA Phase: Plan"
# ... 他のラベルも同様に
```

## 📖 使用方法

### Issue作成時の流れ

1. **New Issue** → **PDCA開発サイクル**を選択
2. 目的・成功基準を記入
3. 担当者情報（AIサービス/モデル/端末）を記入
4. PDCA各フェーズを順次実行
5. PIMS気づきを記録

### Pull Request作成時

1. 変更内容を記述
2. **Decision**（判断理由）を明記
3. **Evidence**（証跡）を添付
4. **PIMS気づき**を記録
5. 担当者情報を記入

## 🎯 PIMS運用のベストプラクティス

### ✅ 良い例
- **明確な目的**: 「ユーザー認証機能を追加」ではなく「ユーザーが安全にログインできる認証システムを構築」
- **測定可能な成功基準**: 「build成功」「type-check 0件」「既存機能に回帰なし」
- **証跡の記録**: スクリーンショット、ログ、URL等を具体的に記録
- **知識の蓄積**: 失敗や成功パターンをPIMS気づきとして記録

### ❌ 避けるべき例
- **曖昧な記述**: 「改善する」「最適化する」
- **証跡なし**: 根拠のない主張
- **知識の放置**: 気づきを記録せずに終了

## 🔧 カスタマイズ

### ラベルの追加
`.github/labels.yml`を編集してワークフローを再実行：

```yaml
- name: "custom-label"
  color: "FF6B6B"
  description: "Custom label description"
```

### Issueテンプレートの修正
`.github/ISSUE_TEMPLATE/`内のファイルを編集

### Actionsの拡張
`.github/workflows/`内のワークフローをカスタマイズ

## 📚 参考資料

- [PDCA_ISSUE_USAGE_GUIDE.md](./PDCA_ISSUE_USAGE_GUIDE.md) - 詳細な運用ガイド
- [GitHub Issues ドキュメント](https://docs.github.com/en/issues)
- [GitHub Actions ドキュメント](https://docs.github.com/en/actions)

## 🤝 貢献

PIMSの改善提案やバグ報告は、このテンプレートリポジトリでIssueを作成してください。

## 📄 ライセンス

MIT License - 詳細は[LICENSE](./LICENSE)を参照

---

**PIMS** - PDCA-Issue Muramasa System  
継続的改善を通じて、プロジェクトを進化させ続けるシステム
