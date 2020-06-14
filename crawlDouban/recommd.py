import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
from pymongo import MongoClient

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


def readFile():
    # ['ImdbLink', 'bianJu', 'daoYan', 'imageUrl', 'intro', 'leiXing',
    #        'movieName', 'pianChang', 'pingFeng', 'shangYinRiQi', 'youMing',
    #        'yuYan', 'zhiPianGuoJia', 'zhuYan']
    movie_meta = read_mongo(db='doubanDB', collection='moive_info', no_id=False)
    # 只保留中文名字
    movie_meta['movieName'] = movie_meta['movieName'].apply(lambda row: str(row.split(' ')[0]))

    # ['movieId', 'comment', 'vote', 'comment_time', 'comment_user', 'rating']
    movie_comment_info = read_mongo(db='doubanDB', collection='movieComment_3')
    print(movie_meta.columns)
    print(movie_comment_info.columns)
    return movie_meta, movie_comment_info


def get_movie(df_movie, moive_list,movie_total):
    df_movieId = pd.DataFrame(moive_list, index=np.arange(len(moive_list)), columns=['movieId'])
    corr_movies = pd.merge(df_movieId, movie_total, on='movieId')
    return corr_movies



def pearson_method(df_movie, pivot, movie, num):
    '''
    皮尔森系数
    :param df_movie:
    :param pivot:
    :param movie:
    :param num:
    :return:
    '''
    print("开始计算")
    bones_ratings = pivot[movie]
    print(bones_ratings)
    similar_to_bones = pivot.corrwith(bones_ratings)
    print("fuck you")
    corr_bones = pd.DataFrame(similar_to_bones, columns=['pearson'])
    corr_bones.dropna(inplace=True)
    corr_summary = corr_bones.join(df_movie[['movieId', 'ratingCount']].set_index('movieId'))

    movie_list = corr_summary[corr_summary['ratingCount'] >= 100].sort_values('pearson', ascending=False).index[
                 :num].tolist()
    print(movie_list)
    return movie_list

def knn_method(movie_pivot, movie, num):
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(movie_pivot)
    distances, indices = model_knn.kneighbors(movie_pivot.loc[[movie], :].values, n_neighbors=num)
    movie_list = movie_pivot.iloc[indices[0], :].index.tolist()


    return movie_list

def SVD_method(movie_pivot, movie, num):
    SVD = TruncatedSVD(n_components=12, random_state=17)
    matrix = SVD.fit_transform(movie_pivot.values)
    movie_SVD = pd.DataFrame(matrix, index=movie_pivot.index).T


    corr = movie_SVD.corr()
    search_movie = movie_pivot.loc[[movie], :].index[0]
    print('search_movie',search_movie)
    movie_list = corr.sort_values(search_movie, ascending=False).index[0:num].tolist()
    return movie_list

