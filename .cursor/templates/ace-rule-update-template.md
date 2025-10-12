# ACE的ルール更新テンプレート

このテンプレートは、Agentic Context Engineering（ACE）理論に基づく
3段階プロセスでルールを更新するためのガイドです。

---

## Stage 1: Reflect（振り返り）

### タスク内容

**何を実装したか**:


**どのような結果になったか**:


---

### 分析

**✅ うまくいった点**:
- 
- 

**❌ 問題点**:
- 
- 

**💡 改善案**:
- 
- 

---

## Stage 2: Generate Delta（差分生成）

### 対象の特定

**対象ルールファイル**: 
```
例: .cursor/rules/implementation.mdc
```

**対象セクション**: 
```
例: ## コード品質
```

---

### 追加内容

**追加する項目**:
```markdown
（ここに追加する内容を記載）
```

**追加の根拠**:


---

## Stage 3: Apply（適用）

### 実施チェックリスト

- [ ] search_replaceで差分のみ適用（writeは使用しない）
- [ ] 他の情報が失われていないか確認
- [ ] 変更をコミット
- [ ] knowledge.mdcに記録（必要に応じて）

### コミットメッセージ例

```bash
git commit -m "feat: add [項目名] to [ファイル名]

Added based on ACE 3-stage process:
- Reflect: [振り返りサマリー]
- Delta: [変更箇所]
- Apply: Differential update only

Related: [Issue番号 or タスク説明]"
```

---

## 📚 参考

- 詳細ガイド: [implementation.mdc](mdc:.cursor/rules/implementation.mdc)
- 理論的背景: [knowledge.mdc](mdc:.cursor/rules/knowledge.mdc)
- ACE論文: https://arxiv.org/html/2510.04618v1

---

**使い方**:

1. このテンプレートをコピー
2. 各セクションを埋める
3. 3段階プロセスに従って実施
4. コンテキスト崩壊を回避

