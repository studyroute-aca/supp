import os

NEWS_DATE = os.environ.get("NEWS_DATE", "")
NEWS_TAG = os.environ.get("NEWS_TAG", "material")
NEWS_TITLE = os.environ.get("NEWS_TITLE", "")
NEWS_URL = os.environ.get("NEWS_URL", "")
NEWS_DESC = os.environ.get("NEWS_DESC", "")

tag_class = "news-tag-material" if NEWS_TAG == "material" else "news-tag-site"
tag_label = "教材" if NEWS_TAG == "material" else "サイト"

if NEWS_URL:
    title_html = (
        f'<a href="{NEWS_URL}" target="_blank" rel="noopener" '
        f'style="color:inherit; text-decoration:underline; text-underline-offset:3px;">'
        f'{NEWS_TITLE}</a>'
    )
else:
    title_html = NEWS_TITLE

block = f'''      <div class="news-item">
        <div class="news-meta">
          <span class="news-date">{NEWS_DATE}</span>
          <span class="news-tag {tag_class}">{tag_label}</span>
        </div>
        <div class="news-body">
          <h3>{title_html}</h3>
          <p>{NEWS_DESC}</p>
        </div>
      </div>
'''

marker = "<!-- NEWS_INSERT_POINT -->"

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

if marker not in content:
    raise SystemExit("marker not found in index.html. Step 1 done?")

content = content.replace(marker, marker + "\n" + block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("News item inserted successfully.")
