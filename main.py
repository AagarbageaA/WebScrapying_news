
from datetime import datetime
import differentNewSourse.udn as udn
import differentNewSourse.ltn as ltn
import differentNewSourse.yahoo as yahoo
import differentNewSourse.mirrormedia as mirror
import differentNewSourse.pts as pts
import differentNewSourse.ttv as ttv
import pandas as pd

if __name__ == "__main__":

    with open("record.txt","r") as record: #讀取上次更新的日期
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
        existing_data = pd.read_excel("news_data.xlsx", engine='openpyxl', sheet_name='Sheet1')
        
        #要新增的資料
        updated_data = pd.concat([existing_data, df], ignore_index=True,axis=0)
        
        # 根據時間和來源排序
        updated_data.sort_values(by=['Time'], inplace=True)

        #寫入excel
        updated_data.to_excel("news_data.xlsx", index=False)

        #更新日期
        with open("record.txt", "w") as record: 
            current_date = datetime.now() # 更新成現在
            formatted_date = current_date.strftime("%Y%m%d")
            record.write(formatted_date)

    except Exception as e:
        print("錯誤:", e)
