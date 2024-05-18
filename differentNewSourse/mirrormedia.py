# mirrormedia鏡周刊
import urllib.request as request

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from time import sleep

def later_than(current, boundary):
    if int(current) > int(boundary): return True
    return False

def fetch_links(url, boundary):
    driver = webdriver.Chrome() 
    driver.get(url)
    sleep(2)  # 等頁面載入完全

    # 模擬滾動 觸發動態載入 直到需要的年份都出現
    last_height = driver.execute_script("return document.body.scrollHeight")
    try:
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)  # 等待
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            last_news_year = soup.find("main", class_="slug-__TagContainer-sc-140ded25-0 fwwkvD").find_all("a")[-1]["href"][7:11]
            if int(last_news_year) < 2022: break
        
        # fetch the link
        link_list = []
        links_list = soup.find("main", class_="slug-__TagContainer-sc-140ded25-0 fwwkvD").find_all("div", class_="article-list__ItemContainer-sc-75e83cda-0 eotvdK")
        
        for links in links_list: 
            links_ = links.findAll("a", recursive=True)
            for link in links_:
                if link["href"][0:4]=="http" or later_than(link["href"][7:15], boundary) == False: continue # skip advertise news
                link_list.append("https://www.mirrormedia.mg" + link['href'])

        return link_list
    
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
    except Exception as e:
        print(f"{e} while fetching content")
        return



def get_news(boundary):
    # fetch all the article link in the serach page
    url = "https://www.mirrormedia.mg/tag/597ec945e531830d00e334e9"
    link_list = fetch_links(url, boundary)
    print(link_list)

    news_data = []
    for link in link_list:
        data = fetch_content(link)
        if data == None: continue
        news_data.append(data)
        sleep(1)
    return news_data

if __name__ == "__main__":
    get_news("20220101")
