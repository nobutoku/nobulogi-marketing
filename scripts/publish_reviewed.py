#!/usr/bin/env python3
"""Explicitly publish a human-reviewed SEO draft as static HTML.
Never processes note-paid content or publishes automatically.
"""
import argparse
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
def convert(md: str) -> str:
    lines=[]
    for line in md.splitlines():
        if line.startswith("<!--") or line.startswith("## AIレビュー"): break
        if not line.strip():
            lines.append("")
        elif re.match(r"^#{1,3} ",line):
            n=len(line)-len(line.lstrip("#"))
            lines.append(f"<h{n}>{html.escape(line[n+1:])}</h{n}>")
        elif line.startswith("- "):
            lines.append(f"<p>• {html.escape(line[2:])}</p>")
        else:
            lines.append(f"<p>{html.escape(line)}</p>")
    return "\n".join(lines)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("draft",help="drafts/seo/*.md only")
    p.add_argument("--slug",required=True)
    args=p.parse_args()
    path=(ROOT/args.draft).resolve()
    allowed=(ROOT/"drafts"/"seo").resolve()
    if allowed not in path.parents or path.suffix!=".md":
        raise SystemExit("Only SEO drafts may be published")
    if not re.fullmatch(r"[a-z0-9-]+",args.slug):
        raise SystemExit("Invalid slug")
    content=path.read_text(encoding="utf-8")
    if "## AIレビュー" not in content:
        raise SystemExit("Missing AI review section")
    public=content.split("---\n\n## AIレビュー",1)[0]
    public=re.sub(r"<!--.*?-->","",public,flags=re.S).strip()
    if "<!-- PAID_BOUNDARY -->" in public:
        raise SystemExit("Paid content must not be published")
    title=next((x.lstrip("# ").strip() for x in public.splitlines() if x.startswith("# ")),args.slug)
    body=convert(public)
    page=f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | NOBULOGI</title><style>body{{font-family:system-ui,sans-serif;max-width:780px;margin:50px auto;padding:0 20px;line-height:1.9;color:#193341}}a{{color:#087d83}}h1{{line-height:1.4}}</style></head><body><p><a href="../">← 記事一覧</a></p>{body}<p><a href="https://nobulogi.stores.jp/">物流・SCM相談はこちら</a></p></body></html>"""
    target=ROOT/"articles"/args.slug/"index.html"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(page,encoding="utf-8")
    print(target.relative_to(ROOT))
if __name__=="__main__":main()
