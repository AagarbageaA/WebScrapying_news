import pandas as pd
from scipy import stats #用來計算眾數

if __name__ == "__main__":
    news=pd.read_excel("repo/article_topic.xlsx", engine='openpyxl', sheet_name='Sheet1')
    index=[0,2,5,8,10,29,31,36,40,42,44,48,54,62,67,69]
    grade=0
    for i in range(0,15):
        numlist=[]
        for j in range(index[i],index[i+1]):
            numlist.append(news["topic"][j])
        mode = stats.mode(numlist)
        print(mode)
        if mode.mode!=-1:
            grade+=mode.count
    print("grade",grade)