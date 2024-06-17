import pandas as pd
from scipy import stats #用來計算眾數
from sklearn.metrics import adjusted_rand_score

if __name__ == "__main__":
    news=pd.read_excel("repo/article_topic.xlsx", engine='openpyxl', sheet_name='Sheet1')
    topic_num=pd.read_excel("repo/topic_list.xlsx", engine='openpyxl', sheet_name='Sheet1')["Topic"].max()
    index=[0,2,5,8,10,29,31,36,40,42,44,47,54,62,67,69]
    predicted=[0]*2+[1]*3+[2]*3+[3]*2+[4]*19+[5]*2+[6]*5+[7]*4+[8]*2+[9]*2+[10]*3+[11]*7+[12]*8+[13]*5+[14]*2

    grade=0
    numlist=[]
    for j in range(69):
        if (num:=news["topic"][j]) != -1:
            numlist.append(num)
        else:
            numlist.append(j-100)
    grade = adjusted_rand_score(numlist, predicted)
    print(grade)
