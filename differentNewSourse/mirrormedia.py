#��P�Z
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

        # fetch the link
        soup = BeautifulSoup(data, "html.parser")

        link_list = soup.find("div", class_="article-list__ItemContainer-sc-4a6f6218-0 dZwMjE").findAll("a")
        for i, link in enumerate(link_list): 
            link_list[i] = "https://www.mirrormedia.mg" + link['href']
        return link_list
        
    except:
        return

def fetch_content(url):
    fake_header_can = UserAgent().random
    fake_header = {'user-agent': fake_header_can}
    try:
        requests = request.Request(url, headers=fake_header) # 用 fake header 去 request 網頁 html
        with request.urlopen(requests) as response:
            data = response.read().decode("utf-8")

        # fetch the link
        soup = BeautifulSoup(data, "html.parser")

        # title
        try:
            title = soup.find("h1", class_="normal__Title-sc-feea3c7c-0 dreoUD").text.strip()
        except:
            return
        # content
        contents = soup.findAll("span", {"data-text":"true"})
        content = ""
        for c in contents:
            content += c.text.strip()
        # tags
        tags = soup.find("section", class_="tags__TagsWrapper-sc-d99abf99-0 fKrSHt article-info__StyledTags-sc-a05ad886-4 fhVRaZ").findAll("a")
        for i, tag in enumerate(tags):
            tags[i] = tag.text.strip()
        # time
        date = soup.find("div", class_="normal__Date-sc-feea3c7c-5 lCa-Da").text.strip()
        date_temp = date.split(" ")[0].split(".")
        date = f"{date_temp[0]}/{date_temp[1]}/{date_temp[2]}"


        return {"Title": title, 
                "Content": content, 
                "Keywords": tags,
                "Time": date,
                "Resourse":"mirrormedia"}
    except:

        return



def get_news():
    # fetch all the article link in the serach page
    url = "https://www.mirrormedia.mg/tag/597ec945e531830d00e334e9"
    link_list = fetch_links(url)

    news_data = []
    for link in link_list:
        data = fetch_content(link)
        if data == None: continue
        news_data.append(data)
        time.sleep(1)
    return news_data

if __name__ == "__main__":
    print(get_news())
