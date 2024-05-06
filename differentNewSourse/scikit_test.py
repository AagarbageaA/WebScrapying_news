import jieba.analyse
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba

jieba.load_userdict({"地層下陷": 3000, "松山區": 1000, "汽車": 1000, "蔣萬安": 1000, "趕到": 1000})

# 範例文本
text1 = "台北市信義區崇德街下午出現地層下陷，天坑長15公尺、寬3公尺、深度2至3公尺。台北市長蔣萬安晚上到場關心並指出，整個狀況控制住以後，會針對台北市的工地，做全面的清查，是不是有這次事件類似的情況，再積極處理。蔣萬安表示，工地的部分，市府馬上勒令停工，找出這次地面坍塌的原因，盡快排除，避免坍塌面積持續擴大。這次地層下陷的事件，整起事件會做完整的調查，並且就工地全面檢視，以及營造商的相關紀錄。台北市信義區崇德街下午出現地層下陷，天坑長15公尺、寬3公尺、深度2至3公尺。周邊拉起警戒線提醒民眾注意安全，有民眾在警方協助下，回住處拿東西。記者林伯東／攝影台北市信義區崇德街下午出現地層下陷，天坑長15公尺、寬3公尺、深度2至3公尺。周邊民眾聚集關心。記者林伯東／攝影台北市信義區崇德街下午出現地層下陷，天坑長15公尺、寬3公尺、深度2至3公尺，晚間坑洞正在持續灌漿，阻止繼續塌陷。記者林伯東／攝影台北市信義區崇德街下午出現地層下陷，天坑長15公尺、寬3公尺、深度2至3公尺。台北市議員許淑華（前右）到場關心民眾。記者林伯東／攝影台北市信義區崇德街下午出現地層下陷，天坑長15公尺、寬3公尺、深度2至3公尺。台北市長蔣萬安（左二）、台北市議員徐巧芯（右二）到場關心。記者林伯東／攝影"
text2 = "台北市信義區崇德街下午出現地層下陷，天坑長15公尺、寬3公尺、深度2至3公尺。台北市長蔣萬安（中）到場關心。記者林伯東／攝影台北市信義區崇德街今（13）日下午出現地層下陷，天坑長15公尺、寬3公尺、深度2至3公尺，且二度坍塌。台北市長蔣萬安晚上到場關心並作出四點指示。蔣萬安表示，市府已在第一時間做出相關的緊急疏散處置，並向同仁作出四點指示。第一、安全至上：相關緊急應變處置必須儘速地完成，包括疏散、安置等，已媒合旅宿業進行安置，住民入住可依規定申請補助，我們也會盡力將損害降到最低。第二、釐清坍塌原因、儘快排除：目前了解可能是連續壁滲水的問題，市府會儘速地找出造成地面坍塌的真正原因，並儘快排除，避免坍塌的面積持續擴大。第三、事件整體調查：就這次地面坍塌的事件，將針對工地的負責營造商，就過去相關建造紀錄整體調查。第四、全市工地全面清查：崇德街案緊急處置後，將針對台北市興建工程工地作全面清查，避免相關事件重演。蔣萬安強調，目前已責成相關局處，務必盡速完成相關緊急應變作為，確保住民、市民的安全，避免讓地面坍塌的損壞再持續擴大，將損害降到最低，全力捍衛市民生命財產安全。根據建管處資料顯示，該起工程工地起造人是東禧建設；承造人是華熊營造；監造人是向度聯合建築師事務所，目前則已針對承造人、監造人各開罰新台幣九萬元。"
text3 = "test"
# 分割文字成字串陣列
words1 = jieba.lcut(text1, cut_all = False)
words2 = jieba.lcut(text2, cut_all = False)
words3 = jieba.lcut(text3, cut_all = False)

# 把字串陣列轉換成用空格隔開的字串
words1_str = " ".join(words1)
words2_str = " ".join(words2)
words3_str = " ".join(words3)

# TFidf 生成的 tags，測試用
tags = jieba.analyse.extract_tags(text1, topK=20)
t1=" ".join(tags)
print(tags)
tags = jieba.analyse.extract_tags(text2, topK=20)
t2=" ".join(tags)
print(tags)
tags = jieba.analyse.extract_tags(text3, topK=20)
t3=" ".join(tags)
print(tags)

# 串建TF-IDF向量化器
vectorizer = TfidfVectorizer()

# 合併三份分割的文本成一個 list
corpus = [words1_str, words2_str, words3_str]

# 計算TFIDF陣列
tfidf_matrix = vectorizer.fit_transform(corpus)

print(tfidf_matrix)

# 計算三份文本相似度
similarity = cosine_similarity(tfidf_matrix[0:3], tfidf_matrix[0:3])

print(f"similarity:\n{similarity}")
