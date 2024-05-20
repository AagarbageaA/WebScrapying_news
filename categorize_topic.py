import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
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

def cut_content(articles): #把文章用空格切割並分隔

    #讀取userdict
    jieba.load_userdict('repo/jieba_userdict.txt')

    words = []

    # 針對Content作文本切割
    for content in articles['Content']:
        processed_content = preprocess_text(content)
        tokens = [word for word in jieba.lcut(processed_content, cut_all=False) if word not in stopwords]
        words.append(" ".join(tokens))
    
    return words

def categorize(words,stopwords): #利用模型進行主題分類

    # 向量化模型參數設定
    vectorizer_model = TfidfVectorizer(
        encoding="UTF-8",
        min_df=5, # 用於過濾掉在少於此閾值的文檔中出現的詞彙
        tokenizer=lambda text: text.split(),
        max_features=5000,
        stop_words=list(stopwords)
    ) 
    
    # BERTopic參數設定
    topic_model = BERTopic(language="chinese (traditional)",
                        embedding_model="paraphrase-multilingual-MiniLM-L12-v2",
                        vectorizer_model=vectorizer_model,
                        #nr_topics=20,
                        min_topic_size=2, # 主題最小文檔數
                        zeroshot_min_similarity=0.5 # 最小相似度
    )

    topics, probs = topic_model.fit_transform(words)
    topic_list = pd.DataFrame(topic_model.get_topic_info())
    topic_list.to_excel("repo/topic_list.xlsx", index=False)

    df = pd.DataFrame({"topic": topics, "docs": words})
    df.to_excel("repo/article_topic.xlsx", index=False)
 
if __name__ == "__main__":
    #讀取新聞內容
    contents = pd.read_excel("repo/news_data.xlsx", engine='openpyxl', sheet_name='Sheet1')
    with open("repo/stop_words.txt", "r", encoding="utf-8") as record: #讀取上次更新的日期
        stopwords = record.read()
    words = cut_content(contents)
    for i in range(1):
        categorize(words, stopwords)