import pandas as pd
import os
from hdbscan import HDBSCAN
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import KeyBERTInspired
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
from sklearn.metrics import adjusted_rand_score

def categorize(words,seedTopicList,random1,random2,random3): #利用模型進行主題分類

    # https://hackmd.io/jn1ggwrfRoak4b1uCfgUDw 自訂model簡介&參數
    # 向量化模型參數設定
    vectorizer_model = CountVectorizer(
        encoding="UTF-8",
        min_df=0.05, # 用於過濾掉在少於此閾值(%)的文檔中出現的詞彙 0~0.05
        max_df=0.8, # 0.7~1
        tokenizer=lambda text: text.split(),
        max_features=10, #取排序的前多少個詞
        #stop_words=list(stopwords)
    ) 
    
    representation_model = KeyBERTInspired()
    ctfidf_model = ClassTfidfTransformer(
        bm25_weighting = False, #default: False
        reduce_frequent_words = True, #default: False
        seed_multiplier=10 #default: 2
    ) # https://maartengr.github.io/BERTopic/getting_started/ctfidf/ctfidf.html
    
    umap_model = UMAP(
        n_neighbors=12,
        n_components=9,
        min_dist=0.05,
        metric='minkowski',
        low_memory=True,
        random_state=42
    )

    # clustering_model = HDBSCAN(
    #     min_cluster_size=2, 
    #     metric='euclidean', 
    #     cluster_selection_epsilon= 0.2,
    #     cluster_selection_method='eom', 
    #     prediction_data=True
    # )

    # BERTopic參數設定
    topic_model = BERTopic(
        language="chinese (traditional)",
        embedding_model="paraphrase-multilingual-MiniLM-L12-v2",
        # vectorizer_model=vectorizer_model, #不影響grade
        # representation_model=representation_model, #不影響grade
        umap_model=umap_model,
        #seed_topic_list=seedTopicList,
        # ctfidf_model=ctfidf_model, #不影響grade
        # # nr_topics=15,
        # hdbscan_model=clustering_model,
        min_topic_size=2, # 主題最小文檔數
        #zeroshot_min_similarity=0.05, # 最小相似度
    )

    topics, probs = topic_model.fit_transform(words)
    # topic_model.visualize_topics().show()
    topic_list = pd.DataFrame(topic_model.get_topic_info())
    topic_list.to_excel("production/topic_list.xlsx", index=False)
    #print(f'topic{topics}')
    df = pd.DataFrame({"topic": topics, "docs": words})
    df.to_excel("production/article_topic.xlsx", index=False)
    return df,topic_list["Topic"].max()

def grade(news):
    predicted=[0]*3+[1]*2+[2]*19+[3]*2+[4]*5+[5]*2+[6]*2+[7]*3+[8]*7+[9]*8+[10]*5+[11]*2+[12]*2+[13]*5+[14]*11+[15]*2+[16]*9+[17]*2+[18]*2+[19]*6+[20]*2+[21]*4+[22]*5+[23]*2+[24]*2+[25]*3+[26]*4
    grade=0
    numlist=[]
    for j in range(121):
        numlist.append(news["topic"][j])
    grade = adjusted_rand_score(numlist, predicted)
    print(grade)
    return grade

if __name__ == "__main__":
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    seedTopicList=[["drug", "cancer", "drugs", "doctor"],
                   ["windows", "drive", "dos", "file"],
                   ["space", "launch", "orbit", "lunar"]]
    # with open("repo/seedlist.txt","r",encoding="utf-8") as file: #讀取預設好的主題清單
    #     for line in file:
    #         sublist = line.strip().split(',')
    #         seedTopicList.append(sublist)

    words = pd.read_excel("production/artificial_word_fragments.xlsx", engine='openpyxl', sheet_name='Sheet1')[0].tolist()
    #words = pd.read_excel("repo/word_fragments.xlsx", engine='openpyxl', sheet_name='Sheet1')[0].tolist()
    # UmapRam=[2,65,103,121,127]
    # neighbor=[11,11,10,9,8,8,8,8,6,6]
    # component=[12,3,12,14,9,11,13,14,11,5]
    dist=[0, 0.005, 0.01, 0.015, 0.02, 0.25, 0.03, 0.035, 0.04, 0.045, 0.05]
    gradeList = pd.DataFrame(columns=["neighbor", "component", "Min_dist", "Grade","Metric"])
    for k in dist:
        for i in range(12, 16):
            for j in range(3, 11):
                print(f"neighbor={i}, component={j}, Min_dist={k}:")
                try:
                    news, topic_num = categorize(words, seedTopicList, i, j, k)
                    score = grade(news)
                    new_row = pd.DataFrame({"neighbor": [i], "component": [j], "Min_dist": [k], "Grade": [score]})
                    gradeList = pd.concat([gradeList, new_row], ignore_index=True)
                    # print(gradeList)
                except Exception as e:
                    print("錯誤:", e)
    gradeList.to_excel("production/test_grade.xlsx", index=False)

