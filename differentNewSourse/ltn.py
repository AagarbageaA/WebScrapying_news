from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
def get_news_links(url,boundary): 
    driver = webdriver.Chrome() 
    driver.get(url)
    sleep(5)  # 等頁面載入完全

    # 模擬滾動 觸發動態載入 直到需要的年份都出現
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)  # 等待
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        # 檢查最後一篇新聞的時間，並停止動態載入
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        last_news_date = soup.find('ul', class_='searchlist').find_all('li')[-1].find('span', class_='time').text[:10]
        
        if int("".join(last_news_date.split("/")))<boundary:
            break

    # 抓每則新聞
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    news_list = soup.find('ul', class_='searchlist').find_all('li')
    news_links = []
    for news in news_list:
        title = news.find('h3').text.strip()
        link = news.find('a', class_='tit')['href']
        if "https:" not in link:
            link = "https://news.ltn.com.tw/" + link
        category = news.find('a', class_='immtag').text.strip()
        time = news.find('span', class_='time').text[:10]
        if int("".join(time.split("/"))) < boundary:
            break
        news_links.append((title, link, category, time))

    driver.quit()
    return news_links

def get_news_content(news_link):
    response = requests.get(news_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if "business" in news_link:  # 找專刊
            content_divs = soup.find_all('div', class_='text')
        else:
            content_divs = soup.find_all('div', class_='text boxTitle boxText')
        content = ''
        for div in content_divs:
            paragraphs = div.find_all('p', class_='', recursive=False)
            for p in paragraphs:
                content += p.get_text(strip=True) + '\n'
        return content.strip()

def get_news(boundary):
    url = "https://news.ltn.com.tw/topic/地層下陷"
    news_links = get_news_links(url,boundary)
    news_data = []
    for title, link, category, time in news_links:
        sleep(0.2)
        content = get_news_content(link)
        news_data.append({
            "Title": title,
            "Category": category,
            "Content": content,
            "Time": time,
            "Resourse": "ltn"
        })
    #print(news_data)
    return news_data
