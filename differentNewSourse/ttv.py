#��P�Z
import time

import urllib.request as request
import urllib.parse as parse

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def fetch_links(url):
    fake_header_can = UserAgent().random
    fake_header = {'user-agent': fake_header_can}
    try:
        requests = request.Request(url, headers=fake_header)
        with request.urlopen(requests) as response:
            data = response.read().decode("utf-8")

        soup = BeautifulSoup(data, "html.parser")

        data_list = soup.findAll("a", class_="clearfix")

        link_list = list(map(lambda x: "https://news.ttv.com.tw" + x['href'], data_list))

        return link_list
    except:
        return

def fetch_content(url):
    fake_header_can = UserAgent().random
    fake_header = {'user-agent': fake_header_can}

    try:
        requests = request.Request(url, headers=fake_header)
        with request.urlopen(requests) as response:
            data = response.read().decode("utf-8")

        soup = BeautifulSoup(data, "html.parser")

        title = soup.find("h1", class_="mb-ht-hf").text.strip()

        date = soup.find("li", class_="date time").text.strip()
        date_temp = date.split(" ")[0].split(".")
        date = f"{date_temp[0]}/{date_temp[1]}/{date_temp[2]}"

        tags = soup.find("div", class_="news-article fitVids").find("ul", class_="tag").findAll("a")
        tags = list(map(lambda x: x.text.strip(), tags))

        contents = soup.find("div", id="newscontent").findAll("p")
        content = ""
        for i, c in enumerate(contents): 
            if i!=len(contents)-1: content += c.text.strip()
        return {"Title": title, "Content": content, "Keywords": tags, "Time": date, "Resourse":"ttv"}
    
    except:
        return


def get_news():
    # fetch all the article link in the serach page
    url = "https://news.ttv.com.tw/search/" + parse.quote("地層下陷")
    link_list = fetch_links(url)

    news_data = []
    for link in link_list:
        data = fetch_content(link)
        if data == None: continue
        news_data.append(data)
        time.sleep(1)
    return news_data

if __name__ == "__main__":
    get_news()
