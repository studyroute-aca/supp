import os
import html
import sys

NEWS_DATE = os.environ.get("NEWS_DATE", "")
NEWS_TAG = os.environ.get("NEWS_TAG", "material")
NEWS_TITLE = os.environ.get("NEWS_TITLE", "")
NEWS_URL = os.environ.get("NEWS_URL", "")
NEWS_DESC = os.environ.get("NEWS_DESC", "")

# 必須項目チェック（空のまま突っ込んで壊れたHTMLが生成されるのを防ぐ）
if not NEWS_DATE.strip():
    raise SystemExit("NEWS_DATE is empty. Aborting.")
if not NEWS_TITLE.strip():
    raise SystemExit("NEWS_TITLE is empty. Aborting.")
if not NEWS_DESC.strip():
    raise SystemExit("NEWS_DESC is empty. Aborting.")

tag_class = "news-tag-material" if NEWS_TAG == "material" else "news-tag-site"
tag_label = "教材" if NEWS_TAG == "material" else "サイト"

# --- ここが今回の修正の核心 ---
# タイトル・説明文はテキストとして表示される部分なので html.escape() でエスケープ。
# URLは属性値(href="...")に入るため quote=True で " も確実にエスケープする。
safe_date = html.escape(NEWS_DATE, quote=True)
safe_title = html.escape(NEWS_TITLE, quote=False)
safe_desc = html.escape(NEWS_DESC, quote=False)
safe_url = html.escape(NEWS_URL, quote=True) if NEWS_URL else ""

if safe_url:
    title_html = (
        f'<a href="{safe_url}" target="_blank" rel="noopener" '
        f'style="color:inherit; text-decoration:underline; text-underline-offset:3px;">'
        f'{safe_title}</a>'
    )
else:
    title_html = safe_title

block = f'''      <div class="news-item">
        <div class="news-meta">
          <span class="news-date">{safe_date}</span>
          <span class="news-tag {tag_class}">{tag_label}</span>
        </div>
        <div class="news-body">
          <h3>{title_html}</h3>
          <p>{safe_desc}</p>
        </div>
      </div>
'''

marker = "<!-- NEWS_INSERT_POINT -->"
index_path = "index.html"

if not os.path.exists(index_path):
    raise SystemExit(f"{index_path} not found.")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

if marker not in content:
    raise SystemExit("marker not found in index.html. Step 1 done?")

# マーカーが複数存在する場合の事故防止（1箇所だけに絶対に挿入する）
if content.count(marker) > 1:
    raise SystemExit(
        f"marker appears {content.count(marker)} times in index.html. "
        "Expected exactly 1. Aborting to avoid inserting into the wrong place."
    )

content = content.replace(marker, marker + "\n" + block)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("News item inserted successfully.")
print(f"  date={NEWS_DATE!r} tag={NEWS_TAG!r} title={NEWS_TITLE!r}")
