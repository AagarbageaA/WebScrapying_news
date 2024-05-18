import jieba.analyse
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
import re

def preprocess_text(text):
    text = text.replace('，', ' ')
    text = text.replace('。', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('！', ' ')
    text = text.replace('？', ' ')
    text = text.replace('：', ' ')
    text = text.replace('；', ' ')
    text = text.replace('、', ' ')
    text = text.replace('（', ' ')
    text = text.replace('）', ' ')
    text = text.replace('“', ' ')
    text = text.replace('”', ' ')
    text = text.replace('‘', ' ')
    text = text.replace('’', ' ')
    text = text.replace('《', ' ')
    text = text.replace('》', ' ')
    #text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.replace('!', ' ')
    text = text.replace('?', ' ')
    text = text.replace(':', ' ')
    text = text.replace(';', ' ')
    text = text.replace('-', ' ')
    text = text.replace('_', ' ')
    text = text.replace('~', ' ')
    text = text.replace('"', ' ')
    text = text.replace("'", ' ')
    return text

jieba.load_userdict({   
    "地層下陷": 3000,
    "地下水":1500,
    "復工": 1500,
    "天坑": 1500,
    "勒令停工": 1500,
    "強震": 1500,
    "地震": 1500,
    "北市": 1500,
    "蹋陷": 1500,
    "透地雷達": 1500,
    "路坍": 1200,
    "基市府": 1600,
    "海水倒灌": 1500,
    "面臨":1500,
    "混凝土車":1000,
    "抽水機":1000,
    "爭取": 1000,
    "巨坑": 1000,
    "水庫": 1000,
    "蘆竹": 1500,
    "大直": 1500,
    "新北": 3000,
    "桃園": 3000,
    "台中": 3000,
    "台南": 3000,
    "高雄": 3000,
    "基隆": 3000,
    "新竹": 3000,
    "嘉義": 3000,
    "新竹": 3000,
    "苗栗": 3000,
    "彰化": 3000,
    "南投": 3000,
    "雲林": 3000,
    "嘉義": 3000,
    "屏東": 3000,
    "宜蘭": 3000,
    "花蓮": 3000,
    "台東": 3000,
    "澎湖": 3000,
    "金門": 3000,
    "連江": 3000
})

existing_data = pd.read_excel("news_data.xlsx", engine='openpyxl', sheet_name='Sheet1')

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

# 將 DataFrame 寫入 Excel 檔案
similarity_df.to_excel("similarity_matrix.xlsx", index=False)

# Optional: save the words for debugging purposes
words_df = pd.DataFrame(words)
words_df.to_excel("word_fragments.xlsx", index=False)
