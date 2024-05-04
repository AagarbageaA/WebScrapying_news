
import differentNewSourse.udn as udn
import differentNewSourse.ltn as ltn
import differentNewSourse.yahoo as yahoo
import differentNewSourse.mirrormedia as mirror
import differentNewSourse.pts as pts
import differentNewSourse.ttv as ttv
import pandas as pd

if __name__ == "__main__":
    df = pd.DataFrame(columns=["Title", "Category", "Content", "Keywords","Time","Resourse"])
    
    # 把每個網站爬到的資料存進df

    df = pd.concat([df, pd.DataFrame(ltn.get_news(), columns=["Title", "Category", "Content","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(udn.get_news(), columns=["Title",  "Category", "Content", "Keywords","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(yahoo.get_news(), columns=["Title",  "Content","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(mirror.get_news(), columns=["Title",  "Content", "Keywords","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(pts.get_news(), columns=["Title",  "Content", "Keywords","Time","Resourse"])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame(ttv.get_news(), columns=["Title",  "Content", "Keywords","Time","Resourse"])], ignore_index=True)
    
    # 存成excel
    try:
        
        
        df = df.apply(lambda x: x if not isinstance(x, str) else x.encode('utf-8').decode('utf-8'))
        df.to_excel("news_data.xlsx", index=False)

    except Exception as e:
        print("Error:", e)
