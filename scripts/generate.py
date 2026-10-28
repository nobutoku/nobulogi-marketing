import os,sys,pathlib,datetime,re
from openai import OpenAI
from anthropic import Anthropic

TOPICS = [
 ("csv-comparison","Excelで2つのCSVを照合する方法","seo"),
 ("safety-stock","EC事業の安全在庫と発注点の考え方","note-free"),
 ("warehouse-migration","倉庫移管プロジェクトの進め方・実務ガイド","note-paid"),
]
def main():
    kind=os.environ.get("CONTENT_KIND","seo")
    choices=[x for x in TOPICS if x[2]==kind]
    if not choices: raise SystemExit("Unsupported CONTENT_KIND")
    slug,title,_=choices[0]
    today=datetime.date.today().isoformat()
    prompt=f"""日本のEC・物流実務者向けの原稿を日本語Markdownで作成。題名: {title}。
実際の顧客事例・具体的な導入実績・統計・出典を捏造しない。法務・規約・製品仕様は未検証なら確認事項と記す。
抽象論ではなく計算例・手順・チェックポイントを含める。NOBULOGIの相談先 https://nobulogi.stores.jp/ を最後に自然に案内。
{('note有料記事として冒頭の無料部分の後に「<!-- PAID_BOUNDARY -->」を一度だけ入れ、購入価値のある詳細な手順・テンプレートを有料部分に記載。' if kind=='note-paid' else '')}
見出しと本文のみ出力。"""
    client=OpenAI()
    draft=client.responses.create(model=os.environ.get("OPENAI_MODEL","gpt-4.1-mini"),input=prompt,max_output_tokens=2200).output_text
    reviewer=Anthropic()
    review=reviewer.messages.create(model=os.environ.get("ANTHROPIC_MODEL","claude-sonnet-4-6"),max_tokens=1100,messages=[{"role":"user","content":"以下の記事を事実性、誇大表現、機密、読者への実用性、未検証の断定について日本語でレビュー。修正箇所と理由を箇条書き。\n\n"+draft}])
    review_text="\n".join(b.text for b in review.content if getattr(b,"type",None)=="text")
    root=pathlib.Path("drafts")/kind
    root.mkdir(parents=True,exist_ok=True)
    (root/f"{today}-{slug}.md").write_text(f"<!-- DRAFT: 人間の承認前に公開しない -->\n\n"+draft+"\n\n---\n\n## AIレビュー（公開前に削除）\n\n"+review_text+"\n",encoding="utf-8")
    print("Draft generated:",root)
if __name__=="__main__":main()
