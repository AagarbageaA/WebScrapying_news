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
                time = news.find('time').text[:10]
                time=time[0:4]+'/'+time[5:7]+'/'+time[8:10]
                category = news.find('a', class_='story-list__cate').text.strip()
                news_links.append((title, link, category,time))
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
        if news_link.find("ubrand")!=-1:
            article_content = soup.find('div', class_='story_body_content').find_all('p',class_='', recursive=False)
            content=''
            for article in article_content:
                content += article.get_text(strip=True) + '\n'
            keywords = [tag.text.strip() for tag in soup.find('div', {'id': 'tags'}).find_all('a')]
            return content, keywords
        else:
            article_content = soup.find('article', class_='article-content')
            section_content = article_content.find('section', class_='article-content__editor')
            content = section_content.text.strip()
            keywords = [tag.text.strip() for tag in soup.find('section', class_='keywords').find_all('a', class_='tag')]
            return content, keywords
    else:
        print(f"Failed to retrieve the content from {news_link}.")
    return "", []

def get_news():
    url = "https://udn.com/search/tagging/2/地層下陷"
    news_links = get_news_links(url)
    news_data = []
    for title, link, category, time in news_links:
        sleep(1)
        content, keywords = get_news_content(link)
        news_data.append({
            "Title": title,
            "Category": category,
            "Content": content,
            "Keywords": ", ".join(keywords),
            'Time':time,
            "Resourse":"udn"
        })
    return news_data