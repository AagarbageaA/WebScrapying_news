# 聯合新聞網
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def get_news_links(url,boundary): # 從搜尋頁面抓結果
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options) 
    driver.get(url)
    sleep(3)  # 等頁面載入完全

    # 模擬滾動 觸發動態載入 直到需要的年份都出現
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-4000);")
        sleep(3)  # 等待捲動後加載
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
        # 檢查最後一篇新聞的時間，並停止動態載入
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        last_news_time = soup.find('section', class_="context-box thumb-news").findAll('div', class_='story-list__news')[-1].find('time')['datetime']
        last_news_date = last_news_time.split(' ')[0]
        if int("".join(last_news_date.split("-"))) < boundary:
            break


    soup = BeautifulSoup(driver.page_source, 'html.parser')
    news_list = soup.find_all('div', class_='story-list__news') #這裡放list的標頭
    news_links = []
    for news in news_list:  # 要抓幾條新聞
        title = news.find('div', class_="story-list__text").find('h2').text.strip()
        link = news.find('a')['href']
        time = news.find('time').text[:10]
        if int("".join(time.split("-")))<boundary:
            break
        time=time[0:4]+'/'+time[5:7]+'/'+time[8:10]

        news_links.append((title, link, time))
        
    return news_links


def get_news_content(news_link): 
    response = requests.get(news_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_content = soup.find('section', class_='article-content__editor').find_all('p', class_='', recursive=False)
        content = ""
        for part in article_content:
            content += part.text.strip()
        return content
    else:
        print(f"Failed to retrieve the content from {news_link}.")
    return 0

def get_news(boundary):
    url = "https://udn.com/search/word/2/地層下陷"
    news_links = get_news_links(url,boundary)
    news_data = []
    for title, link, time in news_links:
        sleep(0.2)
        if "https://udn.com/news/story/" in link:
            print(f"fetching {link}")
            content = get_news_content(link)
            news_data.append({
                "Title": title,
                "Content": content,
                "Link": link,
                'Time': time,
                "Resourse": "udn"
            })
    return news_data

if __name__ == "__main__":
    get_news(20220101)