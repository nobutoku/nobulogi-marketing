# 記事公開の手順

## SEO記事
1. AIの下書きPRをレビュー。Claudeの指摘、事実、機密、引用、リンク、計算式を確認。
2. 修正したSEO原稿をmainにマージしても、まだWebには掲載されない。
3. main上で `python scripts/publish_reviewed.py drafts/seo/対象.md --slug csv-comparison` を実行。
4. 生成された `articles/csv-comparison/index.html` を確認してから別PRでマージ。これでGitHub Pagesに公開される。
5. 記事一覧へのリンク追加は別途必要。

## note記事
note-freeとnote-paidは原稿のみ。noteに自動投稿しない。
有料記事の `<!-- PAID_BOUNDARY -->` はnoteエディタで有料ラインとして手動設定する。
有料部分を公開リポジトリに置くと誰でも読めるため、**有料記事の実際の本文は公開GitHubに保存しない**運用へ移行するまで、有料記事の生成を実行しないこと。

## 定期生成
毎週月曜 01:20 UTC（日本時間10:20）にSEO下書き生成を予定。公開は自動ではない。
APIの利用上限はOpenAI/Anthropic側で別途設定すること。