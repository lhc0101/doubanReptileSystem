from django.db import models
import mongoengine


# Create your models here.
class Top250(mongoengine.Document):
    id = mongoengine.IntField(primary_key=True)
    movieName = mongoengine.StringField(max_length=32)
    direct_actor = mongoengine.StringField()
    quota = mongoengine.StringField()
    imgUrl = mongoengine.StringField()

class HomePageRecommendation(mongoengine.Document):
    id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()
    img_src = mongoengine.StringField()
    url = mongoengine.StringField()
    movieSynopsis = mongoengine.StringField()

class MoiveInfo(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)
    movieName = mongoengine.StringField()
    daoYan = mongoengine.StringField()
    bianJu = mongoengine.StringField()
    zhuYan = mongoengine.StringField()
    leiXing = mongoengine.StringField()
    zhiPianGuoJia = mongoengine.StringField()
    yuYan = mongoengine.StringField()
    shangYinRiQi = mongoengine.StringField()
    pianChang = mongoengine.StringField()
    youMing = mongoengine.StringField()
    ImdbLink = mongoengine.StringField()
    pingFeng = mongoengine.StringField()
    intro = mongoengine.StringField()
    imageUrl = mongoengine.StringField()

class MovieComment(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)  # id为电影ID加评论用户名例如“123456_张三”
    movieId = mongoengine.StringField()
    comment = mongoengine.StringField()
    vote = mongoengine.IntField()
    comment_time = mongoengine.DateField()

class All_MovieComment(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)  # id为电影ID加评论用户名例如“123456_张三”
    movieId = mongoengine.StringField()
    comment = mongoengine.StringField()
    vote = mongoengine.IntField()
    comment_time = mongoengine.DateField()

class SearchMovieResults(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)  # id为电影ID加评论用户名例如“123456_张三”
    movieName = mongoengine.StringField()
    leiXing = mongoengine.StringField()
    shangYinRiQi = mongoengine.StringField()
    subtitle = mongoengine.StringField()
    movieLink = mongoengine.StringField()
    aboutmovie = mongoengine.StringField()

class Setting(mongoengine.Document):
    key = mongoengine.StringField(primary_key=True)
    value = mongoengine.StringField()

class RecommendedMovieInformation(mongoengine.Document):
    id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()
    img_src = mongoengine.StringField()
    url = mongoengine.StringField()
    movieSynopsis = mongoengine.StringField()
    aboutmovie = mongoengine.StringField()