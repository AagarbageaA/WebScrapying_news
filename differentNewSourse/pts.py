#公視
import time

import urllib.request as request

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def fetch_links(url):
    fake_header_can = UserAgent().random
    fake_header = {'user-agent': fake_header_can}
    try:
        requests = request.Request(url, headers=fake_header) # 用 fake header 去 request 網頁 html
        with request.urlopen(requests) as response:
            data = response.read().decode("utf-8")

        soup = BeautifulSoup(data, "html.parser")

        news_search = soup.find("ul", class_="list-unstyled news-list tag-news-list").findAll("li", class_="d-flex")

        news_link_list = []
        for item in news_search:
            news_link = item.find("a")["href"]
            news_link_list.append(news_link)
        return news_link_list
    except:
        return

def fetch_content(url):
    fake_header_can = UserAgent().random
    fake_header = {'user-agent': fake_header_can}
    try:
        requests = request.Request(url, headers=fake_header) # 用 fake header 去 request 網頁 html
        with request.urlopen(requests) as response:
            data = response.read().decode("utf-8")
        
        soup = BeautifulSoup(data, "html.parser")

        # title
        title = soup.find("h1", class_="article-title").text.strip()

        # content
        overview = soup.find("div", class_="articleimg").text.strip()
        article_contents = soup.find("div", class_="post-article text-align-left").findAll("p")
        for c in article_contents:
            overview += c.text.strip()
        
        # tags
        tags = soup.find("div", class_="position-relative article-like-area").findAll("li", class_="blue-tag hashList")
        tags += soup.find("div", class_="position-relative article-like-area").findAll("li", class_="blue-tag hide-tag hashList")
        for i, tag in enumerate(tags):
            tags[i] = tag.text.strip()
        # time
        date = soup.find("span", class_="text-nowrap mr-2").find("time").text.strip()
        date_temp = date.split(" ")[0].split("-")
        date = f"{date_temp[0]}/{date_temp[1]}/{date_temp[2]}"

        # write_file(title, pos_title, article_contents, tag_list, route)

        return {"Title": title, 
                "Content": overview, 
                "Keywords": tags,
                "Time": date,
                "Resourse":"pts"}


    except:
        return

# def write_file(title, pos_title, article_contents, tag_list, route):
#     f = open(route, mode="a+", encoding="utf-8")
#     # title
#     f.write(title + "\n")
#     # overview
#     f.write(pos_title + "\n\n")
#     # article
#     for content in article_contents:
#         f.write(content.text.strip() + "\n")
#     # tags
#     f.write("tags: ")
#     for tag in tag_list:
#         f.write(tag.find("a").text.strip()+" ")
#     # seperate line
#     f.write("\n\n\n" + "-------------------" + "\n\n")


def get_news():
    # fetch all the article link in the serach page
    url = "https://news.pts.org.tw/tag/2240/"
    link_list = fetch_links(url)

    # write file
    # route = r"file\pts\content.txt"
    # f = open(route, mode="w+", encoding="utf-8")
    news_data = []
    for link in link_list:
        news_data.append(fetch_content(link))
        time.sleep(1)
    return news_data
    
if __name__ == "__main__":
    print(get_news())
