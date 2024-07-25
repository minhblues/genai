import json
import os
import hashlib
import requests
from bs4 import BeautifulSoup


craw_url = "https://www.llamaindex.ai/blog"


def craw_blogs():

    if not os.path.isdir("blogs"):
        os.makedirs("blogs", exist_ok=True)

    try:
        print("Crawling data")
        response = requests.get(craw_url)
        soup = BeautifulSoup(response.content, "html.parser")
        blog_htmls = soup.find_all(class_="CardBlog_card__mm0Zw")

        blogs = []
        for index, blog in enumerate(blog_htmls):
            title = blog.find("a").get_text()
            link = blog.find("a").get("href")
            date = blog.find(class_="Text_text-size-16__PkjFu").get_text()
            blogs.append(
                {
                    "index": index + 1,
                    "title": title,
                    "link": "https://www.llamaindex.ai" + link,
                    "date": date,
                    "content": "",
                }
            )

        for blog in blogs:
            blog_id = hashlib.md5(blog["link"].encode()).hexdigest()
            blog_detail = get_blog_detail(blog)
            print(f"Blog {blog_id}: ", blog_detail)
            with open(f"blogs/{blog_id}.json", "w", encoding="utf-8") as f:
                json.dump(blog_detail, f, ensure_ascii=False, indent=4)

        return blogs

    except requests.RequestException as e:
        print(f"An error occurred: {e}")


headers = {
    "Authorization": "Bearer jina_169321559ff84ce0a4c730dce1a0bf9aqp-T3gzS9sg3MJmapNI_Z6l47v5j"
}


def get_blog_detail(blog):
    try:
        jina_url = "https://r.jina.ai/" + blog["link"]
        response = requests.get(jina_url, headers=headers, timeout=10)
        blog["content"] = response.content.decode("utf-8")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

    return blog
