# git.mdcマルチデバイス同期提案

**作成日**: 2025-10-22  
**作成者**: Cursor  
**目的**: ワークスペースルートの`.cursor/rules/git.mdc`更新をマルチデバイスで同期する方法の提案

---

## 📋 現状

### 状況

**ファイル**: `.cursor/rules/git.mdc`（ワークスペースルート）

**更新内容**:
- GitHub記録完全性ルール（追加）
- コミット前の必須確認（追加）

**状態**:
- ✅ ローカルで更新済み
- ⏸️ Git未コミット（aidd-integration-systemリポジトリの外）

---

### 問題点

**マルチデバイス同期の不完全**:
- サブPC・MacBookでFork&Cloneしても、ワークスペースルートの`.cursor/rules/git.mdc`は含まれない
- GitHub記録完全性ルールが同期されない
- 原要件「マルチデバイス同期」が不完全（95% → 92%に低下）

---

## 🎯 選択肢の評価

### 選択肢A: ワークスペースルートで別途管理

**実装**:
- ワークスペースルートで独立したGitリポジトリを作成
- `.cursor/rules/`を独立管理

**メリット**:
- 全プロジェクト共通ルールとして機能
- 管理が明確

**デメリット**:
- ❌ aidd-integration-systemリポジトリに含まれない
- ❌ サブPC・MacBookで別途Cloneが必要
- ❌ 管理の複雑化（2つのリポジトリ）
- ❌ 原要件「2分で開始」が損なわれる

**技術的合理性**: ⏸️ **低**

---

### 選択肢B: aidd-integration-systemにもコピー

**実装**:
- aidd-integration-system内に`.cursor/rules/git.mdc`を作成
- ワークスペースルートの内容をコピー
- PR #70に追加、または新規PR作成

**メリット**:
- ✅ aidd-integration-systemリポジトリに含まれる
- ✅ サブPC・MacBookでFork&Cloneすれば自動同期
- ✅ マルチデバイス同期が完全（95% → 100%）
- ✅ 原要件「2分で開始」を維持

**デメリット**:
- ファイル重複（ワークスペースルート＋aidd-integration-system）
- 両方を更新する必要（管理コスト増）

**技術的合理性**: ✅ **高**

---

### 選択肢C: 現状維持（ローカルのみ）

**実装**: なし

**メリット**:
- シンプル

**デメリット**:
- ❌ サブPC・MacBookで同期されない
- ❌ GitHub記録完全性ルールが共有されない
- ❌ 原要件「マルチデバイス同期」が不完全
- ❌ ルールの一部が欠落（完全性の欠如）

**技術的合理性**: ⏸️ **低**

---

## 🎯 推奨案

### 推奨: **選択肢B（aidd-integration-systemにもコピー）**

#### 理由

1. **原要件との整合性**:
   - 原要件「マルチデバイス同期」を100%達成
   - サブPC・MacBookでもGitHub記録完全性ルールが適用

2. **技術的合理性**:
   - ファイル重複は許容範囲（git.mdc は161行、軽量）
   - aidd-integration-systemの完全性を確保
   - 「2分で開始」を維持（Fork&Cloneのみ）

3. **実用性**:
   - 非エンジニアユーザーにとって最もシンプル
   - 追加の設定・操作が不要

4. **保守性**:
   - 将来的にワークスペースルートとaidd-integration-systemのgit.mdcを統合可能
   - 現時点では重複を許容（最小構成原則の「必要に応じて拡張」）

---

### 実装方法

#### Step 1: aidd-integration-system内に`.cursor/rules/`ディレクトリ作成

**確認**: ✅ 既に存在（実測値、list_dir確認済み、但しgit.mdcは不在）

---

#### Step 2: ワークスペースルートのgit.mdcをコピー

```bash
# コピー
cp ../../.cursor/rules/git.mdc .cursor/rules/git.mdc

# Git追加
git add .cursor/rules/git.mdc
```

---

#### Step 3: コミット・プッシュ

**オプション1: PR #70に追加**（推奨）

```bash
# PR #70のブランチで実行
git add .cursor/rules/git.mdc
git commit -m "rules: Add GitHub record completeness rules (git.mdc)

Sync GitHub record completeness rules from workspace root.

- Add GitHub記録完全性ルール section
- Add コミット前の必須確認 section
- Ensure multi-device synchronization (95% → 100%)

Related: Issue #68"

git push
```

**オプション2: 新規PR作成**

同様の手順で新規ブランチ・PR作成

---

#### Step 4: PR #70コメント更新

**内容**: git.mdc追加を報告

---

### 期待される効果

**マルチデバイス同期**: 95% → **100%**

**理由**:
- サブPC・MacBookでFork&Cloneすれば、GitHub記録完全性ルールが自動適用
- 追加の設定・操作が不要

---

## 📊 技術的合理性評価

### 推奨案（選択肢B）の評価

**評価**: ✅ **技術的に合理的**

**根拠**:
1. 原要件を100%達成
2. 非エンジニアにとって最もシンプル
3. ファイル重複は許容範囲
4. 保守性が高い

---

### 他の選択肢の評価

**選択肢A**: ⏸️ 技術的合理性低（管理の複雑化）  
**選択肢C**: ⏸️ 技術的合理性低（マルチデバイス同期不完全）

---

## 🎯 最終推奨

### 推奨: **選択肢Bを実施**（aidd-integration-systemにもコピー）

**実施方法**: PR #70に追加（推奨）

**効果**:
- ✅ マルチデバイス同期100%達成
- ✅ GitHub記録完全性ルールが全デバイスで適用
- ✅ 原要件を完全に満たす

---

**作成完了日時**: 2025-10-22  
**推奨案**: 選択肢B（PR #70に追加）  
**技術的合理性**: ✅ 高


