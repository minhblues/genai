import json
import requests
from bs4 import BeautifulSoup


# Step 1: Get blog content
def get_blog_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    blogs = soup.find_all(class_="CardBlog_card__mm0Zw")

    blog_content = []
    for index, blog in enumerate(blogs):
        title = blog.find("a").get_text()
        link = blog.find("a").get("href")
        date = blog.find(class_="Text_text-size-16__PkjFu").get_text()
        blog_content.append(
            {
                "index": index + 1,
                "title": title,
                "link": "https://www.llamaindex.ai" + link,
                "date": date,
            }
        )

    return blog_content


blog_url = "https://www.llamaindex.ai/blog"
blogs = get_blog_content(blog_url)

with open("blogs.json", "w", encoding="utf-8") as f:
    json.dump(blogs, f, ensure_ascii=False, indent=4)

with open("blogs.json", "r", encoding="utf-8") as f:
    blogs = json.load(f)
