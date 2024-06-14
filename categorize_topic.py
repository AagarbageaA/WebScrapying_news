import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import TfidfVectorizer
from bertopic.representation import KeyBERTInspired
from umap import UMAP

def categorize(words,stopwords): #利用模型進行主題分類

    # 向量化模型參數設定
    vectorizer_model = TfidfVectorizer(
        encoding="UTF-8",
        min_df=0.3, # 用於過濾掉在少於此閾值的文檔中出現的詞彙
        tokenizer=lambda text: text.split(),
        max_features=5000,
        stop_words=list(stopwords)
        ) 
    representation_model = KeyBERTInspired(
        random_state=0
    )
    umap = UMAP(n_neighbors=15,
            n_components=5,
            min_dist=0.0,
            metric='cosine',
            low_memory=False,
            random_state=1337) 
    # BERTopic參數設定
    topic_model = BERTopic(language="chinese (traditional)",
                        embedding_model="paraphrase-multilingual-MiniLM-L12-v2",
                        vectorizer_model=vectorizer_model,
                        representation_model=representation_model,
                        umap_model=umap,
                        #nr_topics=20,
                        min_topic_size=2, # 主題最小文檔數
                        zeroshot_min_similarity=0.35, # 最小相似度
                        )
    
    topic_model.fit_transform(words)
    topics, probs = topic_model.fit_transform(words)
    topic_list = pd.DataFrame(topic_model.get_topic_info())
    topic_list.to_excel("repo/topic_list.xlsx", index=False)
    df = pd.DataFrame({"topic": topics, "docs": words})
    df.to_excel("repo/article_topic.xlsx", index=False)
if __name__ == "__main__":
    #生成的結果看 topic_list.xlsx
    with open("repo/stop_words.txt","r",encoding="utf-8") as record: #讀取上次更新的日期
        stopwords=record.read()
    words = pd.read_excel("repo/artificial_word_fragments.xlsx", engine='openpyxl', sheet_name='Sheet1')[0].tolist()
    categorize(words,stopwords)