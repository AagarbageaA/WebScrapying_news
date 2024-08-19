from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_news_links(url, boundary): 
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options) 
    driver.get(url)
    sleep(3)  # 等頁面載入完全

    news_links = []

    # 模擬滾動 觸發動態載入 直到需要的年份都出現
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        sleep(3)
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)  # 等待
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        # 抓每則新聞
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        news_list = soup.find('ul', class_='list boxTitle').find_all('li')
        for news in news_list:
            title = news.find('a')['title']
            link = news.find('a')['href']
            if "https:" not in link:
                link = "https://news.ltn.com.tw/" + link
            # if int("".join(time.split("/"))) < boundary:
            #     break
            news_links.append((title, link))

        # 檢查最後一篇新聞的時間，並停止動態載入
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        last_news_date = soup.find('ul', class_='list boxTitle').find_all('li')[-1].find('span', class_='time').text[:10]
        
        try:
            if int("".join(last_news_date.split("/"))) < boundary:
                break
        except Exception as e:
            print(e)


        next_page_url = driver.find_element(By.CLASS_NAME, "p_next")
        next_page_url.click()

    driver.quit()

    return news_links

def get_news_content(news_link, boundary):

    response = requests.get(news_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        time = soup.find("span", class_="time").text.strip()
        if "https://news.ltn.com.tw" in news_link:  # 找專刊
            content_divs = soup.find_all('div', class_='text boxTitle boxText')
        else: 
            return 0, 0
        print(f"fetching {news_link}")
        try:
            date = int("".join((time.split(" ")[0]).split("/")))
        except Exception as e:
            print(e)
        if date < boundary:
            return 0, -1
        content = ''
        for div in content_divs:
            paragraphs = div.find_all('p', class_='', recursive=False)
            for p in paragraphs:
                content += p.get_text(strip=True) + '\n'
        return content.strip(), time

def get_news(boundary):
    url = "https://search.ltn.com.tw/list?keyword=地層下陷"
    news_links = get_news_links(url,boundary)
    news_data = []
    for title, link in news_links:
        sleep(0.2)
        content, time = get_news_content(link, boundary)
        if content:
            news_data.append({
                "Title": title,
                "Content": content,
                "Link": link,
                "Time": time,
                "Resourse": "ltn"
            })
        if time == -1: break
    #print(news_data)
    return news_data

if __name__ == "__main__":
    get_news(20220101)