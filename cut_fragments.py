import jieba.analyse
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba

def preprocess_text(text):
    with open("repo/stop_words.txt","r",encoding="utf-8") as record: #讀取上次更新的日期
        stopwords=record.read()
        for word in stopwords:
            text = text.replace(word, '')
    text = text.replace('，', '')
    text = text.replace('。', '')
    text = text.replace('\n', '')
    text = text.replace('！', '')
    text = text.replace('？', '')
    text = text.replace('：', '')
    text = text.replace('；', '')
    text = text.replace('、', '')
    text = text.replace('（', '')
    text = text.replace('）', '')
    text = text.replace('“', '')
    text = text.replace('”', '')
    text = text.replace('‘', '')
    text = text.replace('’', '')
    text = text.replace('《', '')
    text = text.replace('》', '')
    #text = text.replace('.', ' ')
    text = text.replace(',', '')
    text = text.replace('!', '')
    text = text.replace('?', '')
    text = text.replace(':', '')
    text = text.replace(';', '')
    text = text.replace('-', '')
    text = text.replace('_', '')
    text = text.replace('~', '')
    text = text.replace('"', '')
    text = text.replace("'", '')
    text = text.replace("[ 周刊 王 CTWANT ]", '')

    flag1 = False
    lst = list(text)
    for i, item in enumerate(lst):
        if item == "〔" or item == "[":
            flag1 = True
            lst[i] = ''
            continue
        elif item == "〕" or item == "]":
            flag1 = False
            lst[i] = ''
            continue
        if flag1:
            lst[i] = ''
    else:
        text = ''.join(lst)
        
        
    return text

#讀取userdict
jieba.load_userdict('repo/jieba_userdict.txt')

#讀取新聞內容
#existing_data = pd.read_excel("repo/news_data.xlsx", engine='openpyxl', sheet_name='Sheet1')
existing_data = pd.read_excel("repo/artificial_news.xlsx", engine='openpyxl', sheet_name='Sheet1')
words = []
num_rows = existing_data.shape[0]

# 針對Content作文本切割
for content in existing_data['Content']:
    processed_content = preprocess_text(content)
    words.append(" ".join(jieba.lcut(processed_content, cut_all=False)))

# 創建TF-IDF向量化器
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(words)

# 計算所有文本相似度(n*n的矩陣)
similarity = cosine_similarity(tfidf_matrix[0:num_rows], tfidf_matrix[0:num_rows])

print(f"similarity:\n{similarity}")

# 將相似度矩陣轉換為 DataFrame
similarity_df = pd.DataFrame(similarity)

# 寫入 similarity_matrix
#similarity_df.to_excel("production/similarity_matrix.xlsx", index=False)

# 寫入 切好的片段
words_df = pd.DataFrame(words)
#words_df.to_excel("production/word_fragments.xlsx", index=False)
words_df.to_excel("production/artificial_word_fragments.xlsx", index=False)
