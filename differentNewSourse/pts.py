#公視

import urllib.request as request

from bs4 import BeautifulSoup
from time import sleep
from fake_useragent import UserAgent

def date_format_transform(date): # 20xx.xx.xx xx:xx -> 20xx/xx/xx
    try:
        date_temp = date.split(" ")[0].split("-")
        return f"{date_temp[0]}/{date_temp[1]}/{date_temp[2]}"
    except:
        print("Unsupported date format")
        return "0000/00/00"

def later_than(current, boundary):
    current = int("".join(current.split("/")))
    if current >= int(boundary): return True
    return False # don't want

def fetch_links(url, boundary):
    fake_header_can = UserAgent().random
    fake_header = {'user-agent': fake_header_can}
    try:
        news_link_list = []
        current_page = 1
        while(True):
            requests = request.Request(url, headers=fake_header) # 用 fake header 去 request 網頁 html
            with request.urlopen(requests) as response:
                data = response.read().decode("utf-8")

            soup = BeautifulSoup(data, "html.parser")

            news_search = soup.find("ul", class_="list-unstyled news-list tag-news-list").findAll("li", class_="d-flex")

            for news in news_search:
                date = news.find("div", class_="news-info").find("time").text.strip()
                date = date_format_transform(date)
                if later_than(date, boundary) == False: break  # Earlier than boundary => break, if break, will not go into the following else
                news_link_list.append(news.find("a")['href'])
            else:
                next_page = soup.find("ul", class_="list-unstyled pages d-flex justify-content-center align-items-center").findAll("li")
                if len(next_page) == 2:
                    if next_page[1].find("a")["href"] == "": break # no following page
                    else: url = next_page[1].find("a")["href"]
                else:
                    url = next_page[2].find("a")["href"]
                continue
            break

        return news_link_list
    except Exception as e:
        print(f"{e} while fetching links")
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
        print(title)

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
        date = date_format_transform(date)

        return {"Title": title, 
                "Content": overview, 
                "Keywords": tags,
                "Time": date,
                "Resourse":"pts"}

    except Exception as e:
        print(f"{e} while fetching content of {url}")
        return

def get_news(boundary):
    # fetch all the article link in the serach page
    url = "https://news.pts.org.tw/tag/2240/"
    link_list = fetch_links(url, boundary)
    news_data = []
    for link in link_list:
        news_data.append(fetch_content(link))
        sleep(1)
    return news_data
    
if __name__ == "__main__":
    get_news("20220101")
