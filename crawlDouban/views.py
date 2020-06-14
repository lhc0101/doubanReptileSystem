from bs4 import BeautifulSoup
from django.contrib.sites import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from crawlDouban.claw import Claw
from crawlDouban.models import *
from crawlDouban.wordCloud import *
import numpy as np
from crawlDouban.class_model import *
import json
import requests
from doubanMovie.settings import headers

headers = headers

def randompageItems():
    ll = []
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=热门&page_limit=20"
    page = requests.get(url=url, headers=headers).json()
    page_list = []
    print(page)
    claw_obj = Claw()

    for r in range(20):  # 每次加载20条
        list = page['subjects']
        dict = list[r]
        url_split = dict['url'].split("/")
        MovieInfo = claw_obj.getMovieInfo(str(dict['url']))
        # print(MovieInfo.intro)
        homePageRecommendation = HomePageRecommendation()
        homePageRecommendation.id = int(url_split[-2])
        homePageRecommendation.name = str(dict['title'])
        homePageRecommendation.img_src = str(dict['cover'])
        homePageRecommendation.url = str(dict['url'])
        homePageRecommendation.movieSynopsis = str(MovieInfo.intro)
        homePageRecommendation.save()
        item = popularMovieInformation(
            name=dict['title'],
            img_src=dict['cover'],
            url=dict['url'],
            movieSynopsis=MovieInfo,
        )
        page_list.append(item)
    # print(page_list)
    return page_list

# Create your views here.
def index(request):
    homePageRecommendation = HomePageRecommendation.objects
    if len(homePageRecommendation) == 0:
        randompageItems()
        homePageRecommendation = HomePageRecommendation.objects
    return render(
        request, 'hotRecommendation.html',
        {
            "title": "豆瓣电影爬虫首页",
            "top250": homePageRecommendation
        }
    )

def getrecommendpageItems(html,movie_name_about):
    html = html.replace("<br>", "")
    soup = BeautifulSoup(html, "html.parser")
    all_move_id = soup.find_all('dt')
    cur_top = []
    claw_obj = Claw()
    for i, movie in enumerate(all_move_id):
        if movie.find("a").get("href") != None:
            movie_url = movie.find("a").get("href")
            # print(movie_id.split("/"))
            movie_id = movie_url.split("/")[-2]
            # movie_id = claw_obj.getMovieInfo(movie_url).id
            # print(movie_id ,movie_url , claw_obj.getMovieInfo(movie_url).intro)
            # if claw_obj.getMovieInfo(movie_url).intro == None:
            #     movie_info = None
            # else:
            try:
                movie_info = claw_obj.getMovieInfo(movie_url).intro
            except Exception as e:
                movie_info = None
                print("movie_info：电影信息出错忽略")
            # print("movie_info" , movie_info)
            img_url = movie.find("img").get("src")
            movie_name = movie.find("img").get("alt")
            # print(movie_url)
            # print(img_url)
            # print(movie_name)

            recommendedMovieInformation = RecommendedMovieInformation()
            recommendedMovieInformation.id = int(movie_id)
            recommendedMovieInformation.name = movie_name
            recommendedMovieInformation.img_src = img_url
            recommendedMovieInformation.url = movie_url
            recommendedMovieInformation.movieSynopsis = movie_info
            recommendedMovieInformation.aboutmovie = movie_name_about
            recommendedMovieInformation.save()

            item = popularMovieInformation(
                name=movie_name,
                img_src=img_url,
                url=movie_url,
                movieSynopsis =movie_info


            )
        else:
            item = popularMovieInformation(
                name=None,
                img_src=None,
                url=None,
                movieSynopsis = None
            )
        cur_top.append(item)
    print(cur_top)
    return cur_top

def recommend(request):
    movie_name = request.GET["movieName"]
    # ex1 = "https://movie.douban.com/subject/33420285/"
    claw_obj = Claw()
    recommendedMovieInformation = RecommendedMovieInformation.objects.filter(aboutmovie=str(movie_name))
    if len(recommendedMovieInformation) == 0:
        search_result_list = claw_obj.search_movie(name=str(movie_name))
        # print(search_result_list[0].id,movie_name)
        search_MovieResults = SearchMovieResults.objects.filter(id=str(search_result_list[0].id))
        # print(search_MovieResults)
        mostSimilarMovieurl = search_MovieResults[0].movieLink
        html = claw_obj.getHtmlText(mostSimilarMovieurl)
        similarMoviesRecommended = getrecommendpageItems(html,movie_name)
        # print("similarMoviesRecommended" , similarMoviesRecommended)
        # similarMoviesRecommended.insert(movieSynopsis:)
        # print(similarMoviesRecommended)
    else:
        similarMoviesRecommended = recommendedMovieInformation
    return render(
        request, 'recommend.html',
        {
            "title": "豆瓣电影爬虫同类电影推荐",
            "top250": similarMoviesRecommended
        }
    )

def search(request):
    movie_name = request.GET['movieName']
    claw_obj = Claw()
    # print("movie_name: {}".format(movie_name))
    search_result_list = claw_obj.search_movie(name=str(movie_name))
    resultNum = len(search_result_list) if search_result_list != None else 0
    print("search_result_list" , search_result_list)
    # print(type(search_result_list))
    print("resultNum" , resultNum)
    return render(request, 'searchResult.html',
                  {
                      'title': "搜索结果",
                      "searchResultList": search_result_list,
                      "resultNum": resultNum
                  })


def hot(request):
    craw_obj = Claw()
    top_250 = craw_obj.getHot()
    for i in range(len(top_250)):
        cur_rank = Top250()
        cur_rank.movieName,cur_rank.quota,cur_rank.direct_actor,cur_rank.imgUrl,cur_rank.id = top_250[i]
        cur_rank.save()
    top_250_set = Top250.objects
    for fuck in top_250_set:
        print(fuck.id, fuck.movieName)

    return render(
        request, 'hotResult.html',
        {
            "title": "热门电影",
            "top250": top_250_set
        }
    )


# def recommd(request):
#     return HttpResponse(str("显示推荐"))


# 在这里爬影片信息
# 在这里爬影片信息
def craw(request):
    movie_url = request.GET["movieUrl"]
    # image_file = os.path.join(static_path,'test.jpg')
    # print("fuck you ")
    # if os.path.exists(image_file):
    #     print("fuck you too")
    #     os.remove(image_file)
    # print(movie_url.split("/"))
    url_split = movie_url.split("/")
    movie_id = url_split[-2]
    # print(movie_id)
    # print(movie_url)
    db_result = MoiveInfo.objects.filter(id=movie_id)
    # print("db_result", db_result)
    if len(db_result) == 0:
        claw_obj = Claw()
        result = claw_obj.getMovieInfo(movie_url)
        print("result" , result)
        # print("result.id", movie_id)
        try:
            result.id = movie_id
            # print("result.id" , movie_id)
            movie_info = MoiveInfo()
            movie_info.id = movie_id
            movie_info.movieName = str(result.movieName)
            movie_info.daoYan = result.daoYan
            movie_info.bianJu = result.bianJu
            movie_info.zhuYan = result.zhuYan
            movie_info.leiXing = result.leiXing
            movie_info.zhiPianGuoJia = result.zhiPianGuoJia
            movie_info.yuYan = result.yuYan
            movie_info.shangYinRiQi = result.shangYinRiQi
            movie_info.pianChang = result.pianChang
            movie_info.youMing = result.youMing
            movie_info.ImdbLink = result.ImdbLink
            movie_info.pingFeng = str(result.pingFeng)
            movie_info.intro= result.intro
            movie_info.imageUrl = result.imgurl
            # print(movie_info.pingFeng)
            movie_info.save()
        except Exception as e:
            print("不入库")
    else:
        result = db_result[0]
    print(result)
    all_comment = getcomment(movie_id)
    print("all_comment" , all_comment)
    return render(request, 'movieInfo.html', {
        'title': "影片信息",
        'movieInfo': result,
        'invitation': all_comment
    })

# 爬取评论生成词云
def wordCould(request):
    movieId = request.GET['movieId']
    db_result = All_MovieComment.objects.filter(movieId=movieId)
    db_movieInfo = MoiveInfo.objects.filter(id=movieId)
    print(db_movieInfo)
    word_fre_list = []
    all_comment = ""
    if len(db_result) == 0:
        claw_obj = Claw()
        claw_obj.getComment(movieId)
        db_result = All_MovieComment.objects.filter(movieId=movieId) # 重新查询
        if len(db_result) == 0:
            return JsonResponse(dict())
        for movie in db_result:
            all_comment += movie.comment

        word_fre_list = jiebaClearText(all_comment)
    else:
        for movie in db_result:
            all_comment += movie.comment

        word_fre_list = jiebaClearText(all_comment)

    # 计算情感分数,五元组[Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]
    score = sentiment_score(sentiment_score_list(all_comment))
    # 垂直合并，第一行为所有元素的正向情感，第二行为所有元素的负向情感
    score = np.array(score)
    c = np.vstack((score[:,0],score[:,1]))
    # draw(c,db_movieInfo[0].movieName,movieId=movieId)   # 绘制散点图
    all_pos_neg_score=getAllDatasetScore(c)
    sentimentSit = {}
    sentimentSit['pos'] = all_pos_neg_score[0]
    sentimentSit['neg'] = all_pos_neg_score[1]
    sentimentSit['whole'] = 1 if all_pos_neg_score[0] > all_pos_neg_score[1] else 0
    sentimentSit = json.dumps(sentimentSit)

    # image_Path = os.path.join(static_path,"{}.jpg".format(movieId))

    # print("db_result..." , db_result[0:10])
    print(static_path)
    # print(image_Path)
    print(word_fre_list)
    res_dict = dict(
        movieId=movieId,
        wordFreqData=word_fre_list,
        sentiment = sentimentSit,
        # comment = comment[0],
        imageF='<img src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp" alt="">'
    )

    # return comment

    return JsonResponse(res_dict)

def getImage(request):
    moiveId = request.GET['movieId']
    result_db = MoiveInfo.objects.get(id=moiveId)
    print(result_db.imageUrl)
    img_html = '<img src="{}" width="100"  alt="">'.format(result_db.imageUrl)
    res_dict = dict(
        imageF=img_html
    )
    return JsonResponse(res_dict)

def getcomment(movieId):
    # movieId = request.GET['movieId']
    db_result = MovieComment.objects.filter(movieId=movieId)
    print(db_result)
    if len(db_result) == 0:
        claw_obj = Claw()
        claw_obj.gettenComment(movieId)
        db_result = MovieComment.objects.filter(movieId=movieId) # 重新查询
        comment = db_result[0:10]
    else:
        comment = db_result[0:10]
    print(1)
    print("db_result..", comment)
    all_comment = {
        'invitation': comment
    }
    return comment
    # return render(request, "all_comment.html", all_comment)
    # return JsonResponse(all_comment)

def admin(request):
    # cookie = request.GET["cookie"]
    # setting = Setting()
    # setting.key = str("Cookie")
    # setting.save()
    invi = Setting.objects.filter(key=str("Cookie"))
    # setting.objects.filter(key=str("Cookie")).update(value=str(cookie))
    grade1 = {
        'invitation':invi
    }
    print(invi[0].key)
    return render(request,"admin.html",grade1)