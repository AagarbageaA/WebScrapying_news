# Yahoo新聞
from time import sleep
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def get_news_links(url): # 從搜尋頁面抓結果
    response = requests.get(url)
    if response.status_code == 200: #響應成功
        soup = BeautifulSoup(response.text, 'html.parser') #解析text
        news_list = soup.find('div', {'id': 'mrt-node-Col1-1-StreamContainer'}).find_all('li', {'class': 'StreamMegaItem'}) #這裡放list的標頭
        news_links = []
        for news in news_list:  # 要抓幾條新聞
            title = news.find('a').text
            link = urljoin(url, news.find('a')['href'])
            news_links.append((title, link))
        return news_links
    else:
        print("Failed to retrieve the page.")
        return []

def get_news_content(news_link):
    response = requests.get(news_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content_divs = soup.find_all('div', class_='caas-body')
        content = ''
        for div in content_divs:
            paragraphs = div.find_all('p',class_='', recursive=False) #recursive=False可以不要找到其他div底下的文字
            for p in paragraphs:
                if not p.find_all(): # 判斷在指定的 <p> 標籤內是否有其他子標籤
                    content += p.text + '\n'
        return content.strip()
    else:
        print(f"Failed to retrieve the content from {news_link}.")
        return "", []

def get_news():
    url = "https://tw.news.yahoo.com/search?p=地層下陷&fr=uh3_news_web&fr2=p%3Anews%2Cm%3Asb%2Cv%3Aartcl&.tsrc=uh3_news_web&guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAHx8l7uBQ1xboD3afpSrtg6IpsxNAQ3ebXwG_iNpPjXftRWknF5tecJVy1j1jM_GiL10k_0gQmtVQ7oI5XEdYAauO2xwAkLC63RwCvRaOyQAqGR5zR2nhgPRseaywFSPrHREOGFbSV4_5gZW1w-IZLhHWir5kIt7ZCCAC1OtPqVZ"
    news_links = get_news_links(url)
    news_data = []
    for title, link in news_links:
        sleep(1)
        content= get_news_content(link)
        news_data.append({
            "Title": title,
            "Content": content,
            "Resourse":"yahoo"
        })
    return news_data
    
