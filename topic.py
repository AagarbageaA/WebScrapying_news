import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 讀切好的文章
existing_data = pd.read_excel("repo/word_fragments.xlsx", engine='openpyxl', sheet_name='Sheet1')
docs = existing_data[0].tolist()

# 向量化
vectorizer_model = TfidfVectorizer(
    input=docs,
    encoding="UTF-8",
    min_df=0.1,
    tokenizer=lambda text: text.split(), max_features=3000
    )

topic_model = BERTopic(language="chinese (traditional)",
                       embedding_model="paraphrase-multilingual-MiniLM-L12-v2",
                       vectorizer_model=vectorizer_model,
                       #nr_topics=20,
                       min_topic_size=2,
                       zeroshot_min_similarity=0.25
                       )
topics, probs = topic_model.fit_transform(docs)
topic_list = pd.DataFrame(topic_model.get_topic_info())
topic_list.to_excel("repo/topic_list.xlsx", index=False)
