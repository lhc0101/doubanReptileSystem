import pandas as pd
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]

def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))
    # Delete the _id
    if no_id:
        del df['_id']

    return df

def get_recommendation(title,movies=None,consine_sim=None):
    idx=indices[title]
    sim_scores=list(enumerate(cosine_sim[idx]))
    sim_scores=sorted(sim_scores,key=lambda x:x[1],reverse=True)
    sim_scores=sim_scores[1:11]
    movie_indices=[i[0]for i in sim_scores]
    return movies['movieName'].iloc[movie_indices]

if __name__ == '__main__':
    movies_meata = read_mongo(db='doubanDB', collection='moive_info')
    print(movies_meata.columns)
    # print(movies_meata.head(1))

    movies_meata['leiXing'] = movies_meata['leiXing'].fillna('')
    print(movies_meata['leiXing'].head(1))

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(movies_meata['leiXing'])  # 传入句子组成的list，这里以后可以自己分词

    # 只保留中文名字
    movies_meata['movieName']  = movies_meata['movieName'].apply(lambda row: str(row.split(' ')[0]))


    # print(movies_meata['movieName'])
    # for name in movies_meata['movieName'].items():
    #     _,name = name
    #     print(name)
    #     # print(name.split(" "))
    #     break
    print(tfidf.vocabulary_)

    indices = pd.Series(movies_meata.index, index=movies_meata['movieName']).drop_duplicates()
    # print(indices.head(10))

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    print(cosine_sim.shape)

    print(get_recommendation("肖申克的救赎",movies=movies_meata,consine_sim=cosine_sim))