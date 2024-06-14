import pandas as pd
import os
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import KeyBERTInspired
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP

def categorize(words,stopwords): #利用模型進行主題分類

    county = ['新竹', '台北', '高雄']
    # https://hackmd.io/jn1ggwrfRoak4b1uCfgUDw 自訂model簡介&參數
    # 向量化模型參數設定
    vectorizer_model = CountVectorizer(
    vectorizer_model = CountVectorizer(
        encoding="UTF-8",
        min_df=0.05, # 用於過濾掉在少於此閾值(%)的文檔中出現的詞彙
        max_df=0.8,
        min_df=0.05, # 用於過濾掉在少於此閾值(%)的文檔中出現的詞彙
        max_df=0.8,
        tokenizer=lambda text: text.split(),
        max_features=5000, #取排序的前多少個詞
        max_features=5000, #取排序的前多少個詞
        stop_words=list(stopwords)
    ) 
    
    representation_model = KeyBERTInspired(
        random_state=0
    )

    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric='cosine',
        low_memory=False,
        random_state=1337
    )

    ctfidf_model = ClassTfidfTransformer(
        bm25_weighting = False, #default: False
        reduce_frequent_words = False, #default: False
        seed_words=county, #default: None
        seed_multiplier=10 #default: 2
    ) # https://maartengr.github.io/BERTopic/getting_started/ctfidf/ctfidf.html


    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric='cosine',
        low_memory=False,
        random_state=1337
    )

    ctfidf_model = ClassTfidfTransformer(
        bm25_weighting = False, #default: False
        reduce_frequent_words = False, #default: False
        seed_words=county, #default: None
        seed_multiplier=10 #default: 2
    ) # https://maartengr.github.io/BERTopic/getting_started/ctfidf/ctfidf.html

    # BERTopic參數設定
    topic_model = BERTopic(
        language="chinese (traditional)",
        embedding_model="paraphrase-multilingual-MiniLM-L12-v2",
        vectorizer_model=vectorizer_model,
        representation_model=representation_model,
        umap_model=umap_model,
        ctfidf_model=ctfidf_model,
        #nr_topics=20,
        min_topic_size=2, # 主題最小文檔數
        zeroshot_min_similarity=0.35, # 最小相似度
    )

    topics, probs = topic_model.fit_transform(words)
    # topic_model.visualize_topics().show()
    topic_list = pd.DataFrame(topic_model.get_topic_info())
    topic_list.to_excel("repo/topic_list.xlsx", index=False)
    
    df = pd.DataFrame({"topic": topics, "docs": words})
    df.to_excel("repo/article_topic.xlsx", index=False)

 
if __name__ == "__main__":
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    with open("repo/stop_words.txt","r",encoding="utf-8") as record: #讀取上次更新的日期
        stopwords=record.read()
    words = pd.read_excel("repo/word_fragments.xlsx", engine='openpyxl', sheet_name='Sheet1')[0].tolist()
    categorize(words,stopwords)