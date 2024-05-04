# 自由時報

from time import sleep
import requests
from bs4 import BeautifulSoup

def get_news_links(url): # 從搜尋頁面抓結果
    response = requests.get(url)
    if response.status_code == 200: #響應成功
        soup = BeautifulSoup(response.text, 'html.parser') #解析text
        news_list = soup.find('ul', class_='searchlist').find_all('li')#這裡放list的標頭
        news_links = []
        for news in news_list:  
            title = news.find('h3').text.strip()
            link = news.find('a',class_='tit')['href']
            category = news.find('a', class_='immtag').text.strip()
            news_links.append((title, link, category))
        return news_links
    else:
        print("Failed to retrieve the page.")
        return []

def get_news_content(news_link):
    response = requests.get(news_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content_divs = soup.find_all('div', class_='text boxTitle boxText')
        content = ''
        for div in content_divs:
            paragraphs = div.find_all('p',class_='', recursive=False) #recursive=False�i�H���n����Ldiv���U����r
            for p in paragraphs:
                content += p.get_text(strip=True) + '\n'
        return content.strip()
    else:
        print(f"Failed to retrieve the content from {news_link}.")
        return "", []




def get_news():
    url = "https://news.ltn.com.tw/topic/%E5%9C%B0%E5%B1%A4%E4%B8%8B%E9%99%B7"
    news_links = get_news_links(url)
    news_data = []
    for title, link, category in news_links:
        sleep(1)
        content= get_news_content(link)
        news_data.append({
            "Title":title,
            "Category":category,
            "Content":content,
            "Resourse":"ltn"
        })
    return news_data

