# YouTube動画統合プロンプト（シンプル版）

> コピペして使える、再利用可能なプロンプト

---

## 🚀 基本プロンプト

```markdown
@[YouTube動画URL] この動画の内容をプロジェクトに統合してください。

## 統合方針
1. 動画のトランスクリプトを取得・分析
2. プロジェクト構造を把握（docs/, .cursor/rules/, README.md）
3. TODOリストを作成
4. 以下を段階的に作成/更新:
   - 初心者向けガイド（docs/配下）
   - Cursorルール（.cursor/rules/配下）
   - 設定ファイル（.gitignore, .env.example等、必要に応じて）
   - 統合運用ガイドへのセクション追加（必要に応じて）
   - PRテンプレート改善（必要に応じて）
   - README（新規ドキュメントへのリンク）
5. 完了報告（作成ファイル、メリット、次のステップ）

## 制約
- 既存の命名規則・スタイルに従う
- 機密情報（APIキー等）を絶対に含めない
- 日本語で記述
- 既存ドキュメントとの整合性を保つ
```

---

## 📝 使い方

1. 上記プロンプトをコピー
2. `[YouTube動画URL]` を実際のURLに置き換え
3. Cursor Agent / Composer に貼り付けて実行

**それだけです。**

---

## 🎯 パターン特化版（オプション）

### Git/GitHub系
```markdown
@[動画URL] Git/GitHub動画の内容を統合してください。

成果物:
- [ ] Git初心者ガイド（GitHub Desktop推奨）
- [ ] Git運用ルール（.cursor/rules/git-workflow.mdc）
- [ ] .gitignore改善（APIキー除外）
```

### Docker系
```markdown
@[動画URL] Docker動画の内容を統合してください。

成果物:
- [ ] Docker初心者ガイド
- [ ] Dockerfile、docker-compose.yml作成
```

### セキュリティ系
```markdown
@[動画URL] セキュリティ動画の内容を統合してください。

成果物:
- [ ] セキュリティガイド
- [ ] セキュリティルール（.cursor/rules/security.mdc）
```

---

## 📊 実績

**事例**: Git/GitHub統合（[元動画](https://youtu.be/Uml3jEPWIKo)）
- 所要時間: 約45分
- 作成物: 5ファイル（約14,500語）
- 効果: 非エンジニアのGit習得時間が80%削減

---

## 📚 詳細版テンプレート

より詳細な設定が必要な場合は、[完全版テンプレート集](README.md)を参照してください。

---

**シンプルに、再利用可能に。**

