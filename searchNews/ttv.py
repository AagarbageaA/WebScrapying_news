#ttv台視
import string

import urllib.request as request
import urllib.parse as parse

from bs4 import BeautifulSoup
from time import sleep
from fake_useragent import UserAgent

def later_than(current, boundary):
    current = int("".join(current.split("/")))
    if current > int(boundary): return True
    return False

def fetch_links(url, boundary):
    fake_header_can = UserAgent().random
    fake_header = {'user-agent': fake_header_can}
    try:
        link_list = []
        while(True):
            requests = request.Request(url, headers=fake_header)
            with request.urlopen(requests) as response:
                data = response.read().decode("utf-8")

            soup = BeautifulSoup(data, "html.parser")

            data_list = soup.findAll("a", class_="clearfix")

            for d in data_list:
                date = d.find("div", class_="time").text.strip()[0:10]
                if later_than(date, boundary) == False: break
                link_list.append("https://news.ttv.com.tw" + d['href'])
            else:
                # click to next page
                next_page = soup.find("ul", class_="pagination").find_all("li")[-1]
                if next_page["class"] == "page-item disabled": break
                url = "https://news.ttv.com.tw" + soup.find("ul", class_="pagination").find_all("li")[-1].find("a")["href"]
                url = parse.quote(url, safe=string.printable)
                continue
            break
        return link_list
    except Exception as e:
        print(f"{e} while fetching links")
        return link_list

def fetch_content(url):
    fake_header_can = UserAgent().random
    fake_header = {'user-agent': fake_header_can}

    try:
        requests = request.Request(url, headers=fake_header)
        with request.urlopen(requests) as response:
            data = response.read().decode("utf-8")

        soup = BeautifulSoup(data, "html.parser")
        # Title
        title = soup.find("h1", class_="mb-ht-hf").text.strip()
        # content
        contents = soup.find("div", id="newscontent").findAll("p")
        content = ""
        for i, c in enumerate(contents): 
            if i!=len(contents)-1: content += c.text.strip()
        # tags
        tags = soup.find("div", class_="news-article fitVids").find("ul", class_="tag").findAll("a")
        tags = list(map(lambda x: x.text.strip(), tags))
        # Time
        date = soup.find("li", class_="date time").text.strip()
        date_temp = date.split(" ")[0].split(".")
        date = f"{date_temp[0]}/{date_temp[1]}/{date_temp[2]}"

        return {"Title": title, 
                "Content": content, 
                "Link": url, 
                "Time": date, 
                "Resourse":"ttv"}
    
    except Exception as e:
        print(f"{e} while fetching content of {url}")
        return


def get_news(boundary):
    # fetch all the article link in the serach page
    url = "https://news.ttv.com.tw/search/" + parse.quote("地層下陷")
    link_list = fetch_links(url, boundary)

    news_data = []
    for link in link_list:
        print(f"fetching {url}")
        data = fetch_content(link)
        if data == None: continue
        news_data.append(data)
        sleep(1)
    return news_data

if __name__ == "__main__":
    get_news("20220101")
