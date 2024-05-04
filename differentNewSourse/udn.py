# 聯合新聞網
from time import sleep
import requests
from bs4 import BeautifulSoup

def get_news_links(url): # 從搜尋頁面抓結果
    response = requests.get(url)
    if response.status_code == 200: #響應成功
        soup = BeautifulSoup(response.text, 'html.parser') #解析text
        news_list = soup.find_all('div', class_='story-list__text') #這裡放list的標頭
        news_links = []
        for news in news_list:  # 要抓幾條新聞
            if news.find('h2')!=None:
                title = news.find('h2').text.strip()
                link = news.find('a')['href']
                category = news.find('a', class_='story-list__cate').text.strip()
                news_links.append((title, link, category))
            else:
                break
        return news_links
    else:
        print("Failed to retrieve the page.")
        return []

def get_news_content(news_link): # 抓一篇新聞的內容跟hashtag
    response = requests.get(news_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_content = soup.find('article', class_='article-content')
        if article_content:
            section_content = article_content.find('section', class_='article-content__editor')
            if section_content:
                content = section_content.text.strip()
                keywords = [tag.text.strip() for tag in soup.find('section', class_='keywords').find_all('a', class_='tag')]
                return content, keywords
            else:
                print("Failed to find section content.")
        else:
            print("Failed to find article content.")
    else:
        print(f"Failed to retrieve the content from {news_link}.")
    return "", []

def get_news():
    url = "https://udn.com/search/tagging/2/地層下陷"
    news_links = get_news_links(url)
    news_data = []
    for title, link, category in news_links:
        sleep(1)
        content, keywords = get_news_content(link)
        news_data.append({
            "Title": title,
            "Category": category,
            "Content": content,
            "Keywords": ", ".join(keywords),
            "Resourse":"udn"
        })
    return news_data