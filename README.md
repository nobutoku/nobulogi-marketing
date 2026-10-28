# NOBULOGI Marketing

NOBULOGI の公式集客サイト・SEO記事・note原稿を管理するリポジトリ。

- `index.html`: 公式サイト
- `articles/`: レビュー済み公開記事
- `drafts/seo/`: SEO記事の下書き
- `drafts/note-free/`: note無料記事の下書き
- `drafts/note-paid/`: note有料記事の下書き（無料部分・有料部分の境界を明示）
- `scripts/generate.py`: AIによる原稿作成とレビュー
- `.github/workflows/content-drafts.yml`: GitHub Actionsで下書きPRを作成

## 公開ルール
AI生成原稿は必ず人間が事実・権利・機密・商品案内を確認する。自動でnote投稿はしない。note有料記事の無料/有料境界は手動設定する。クライアントの実データや秘密情報は入力しない。

## 設定
GitHub Actions Secrets に `OPENAI_API_KEY` と `ANTHROPIC_API_KEY` を登録。GitHub Actions の `workflow_dispatch` から手動試験する。予算上限はGitHub Actionsだけで保証できないためAPI側でも制限する。

GitHub Pages: Settings → Pages → Deploy from a branch → main / (root)。
