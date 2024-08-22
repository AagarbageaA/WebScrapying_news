#公視
import ftfy
import urllib.request as request
import urllib.parse as parse

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
    if current >= boundary: return True
    return False # don't want

def get_news_link(url, boundary):
    fake_header_can = UserAgent().random
    fake_header = {'user-agent': fake_header_can}
    # try:
    news_link_list = []
    while(True):
        requests = request.Request(url, headers=fake_header) # 用 fake header 去 request 網頁 html
        with request.urlopen(requests) as response:
            data = response.read().decode("utf-8")

        soup = BeautifulSoup(data, "html.parser")

        news_search = soup.find("ul", class_="list-unstyled search-list relative-news-list-content").findAll("li", class_="row")

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
            url = "https://news.pts.org.tw/search/" + parse.quote("地層下陷") + url[12:]
            continue
        break

    return news_link_list
    # except Exception as e:
    #     print(f"{e} while fetching links")
    #     return

def get_news_content(url):
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
        article_contents = soup.find("div", class_="post-article text-align-left").findAll("p", dir="")
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

        return {"Title": ftfy.fix_text(title),
                "Content": ftfy.fix_text(overview),
                "Link": url,
                "Time": date,
                "Resourse":"pts"}

    except:
        with open(r"production\failed.txt", "a") as f:
            f.write(url + "\n")
        return

def get_news(boundary):
    # fetch all the article link in the serach page
    url = "https://news.pts.org.tw/search/" + parse.quote("地層下陷")
    link_list = get_news_link(url, boundary)
    news_data = []
    for link in link_list:
        print(f"fetching {link}")
        content = get_news_content(link)
        if content == None: continue
        news_data.append(content)
        sleep(2)
    return news_data
    
if __name__ == "__main__":
    get_news(20240101)
