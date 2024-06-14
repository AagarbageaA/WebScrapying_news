
from datetime import datetime
import differentNewSourse.udn as udn
import differentNewSourse.ltn as ltn
import differentNewSourse.yahoo as yahoo
import differentNewSourse.mirrormedia as mirror
import differentNewSourse.pts as pts
import differentNewSourse.ttv as ttv
import pandas as pd
import jieba

def fetch():
    with open("repo/record.txt","r") as record: #讀取上次更新的日期
        last_time=record.read()
    BOUNDARY = int(last_time)

    df = pd.DataFrame(columns=["Title", "Category", "Content", "Keywords","Time","Resourse"])
    
    # 把每個網站爬到的資料存進df
    df = pd.concat([df, pd.DataFrame(ltn.get_news(BOUNDARY), columns=["Title", "Category", "Content","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(udn.get_news(BOUNDARY), columns=["Title",  "Category", "Content", "Keywords","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(yahoo.get_news(BOUNDARY), columns=["Title",  "Content","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(mirror.get_news(BOUNDARY), columns=["Title",  "Content", "Keywords","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(pts.get_news(BOUNDARY), columns=["Title",  "Content", "Keywords","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(ttv.get_news(BOUNDARY), columns=["Title",  "Content", "Keywords","Time","Resourse"])], ignore_index=True)
    
    # 存成excel，成功的話才更新時間
    try:
        df = df.apply(lambda x: x if not isinstance(x, str) else x.encode('utf-8').decode('utf-8'))
        
        #讀現有的資料
        existing_data = pd.read_excel("repo/news_data.xlsx", engine='openpyxl', sheet_name='Sheet1')
        
        #要新增的資料
        updated_data = pd.concat([existing_data, df], ignore_index=True,axis=0)
        
        # 根據時間和來源排序
        updated_data.sort_values(by=['Time'], inplace=True)

        #寫入excel
        updated_data.to_excel("repo/news_data.xlsx", index=False)

        #更新日期
        with open("repo/record.txt", "w") as record: 
            current_date = datetime.now() # 更新成現在
            formatted_date = current_date.strftime("%Y%m%d")
            record.write(formatted_date)

    except Exception as e:
        print("錯誤:", e)

    return updated_data

def preprocess_text(text):
    text = text.replace('，', ' ').replace('。', ' ').replace('\n', ' ').replace('”', ' ')
    text = text.replace('！', ' ').replace('？', ' ').replace('：', ' ').replace('；', ' ')
    text = text.replace('、', ' ').replace('（', ' ').replace('）', ' ').replace('“', ' ')
    text = text.replace('‘', ' ').replace('’', ' ').replace('《', ' ').replace('》', ' ')
    #text = text.replace('/', ' ')
    text = text.replace(',', ' ').replace('!', ' ').replace('?', ' ').replace(':', ' ')
    text = text.replace(';', ' ').replace('-', ' ').replace('_', ' ').replace('~', ' ')
    text = text.replace('"', ' ').replace("'", ' ').replace("「", ' ').replace("」", ' ')
    text = text.replace("／ ", ' ').replace("〔 ", ' ').replace("〕 ", ' ')
    return text

def cut_and_save_content(articles,stopwords): #把文章用空格切割並分隔

    #讀取userdict
    jieba.load_userdict('repo/jieba_userdict.txt')

    words = []

    # 針對Content作文本切割
    for content in articles:
        processed_content = preprocess_text(content)
        tokens = [word for word in jieba.lcut(processed_content, cut_all=False) if word not in stopwords]
        words.append(" ".join(tokens))
    
    words_df = pd.DataFrame(words)
    #words_df.to_excel("repo/word_fragments.xlsx", index=False)
    words_df.to_excel("repo/artificial_word_fragments.xlsx", index=False)
    return words

if __name__ == "__main__":
    read_news=input("Fetch of not? Yes:1  No:0")
    print(read_news)
    if read_news==1:
        news=fetch()
    else:
        news=pd.read_excel("repo/artificial_news.xlsx", engine='openpyxl', sheet_name='Sheet1')
        #news=pd.read_excel("repo/news_data.xlsx", engine='openpyxl', sheet_name='Sheet1')
    contents=news["Content"]

    with open("repo/stop_words.txt","r",encoding="utf-8") as record: #讀取stopword
        stopwords=record.read()
    cut_and_save_content(contents,stopwords)

    

    
