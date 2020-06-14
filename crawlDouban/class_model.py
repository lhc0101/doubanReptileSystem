class SearchResult:
    def __init__(self, title=None, url=None, type=None, year=None, sub_title=None, id=None):
        self.title = title
        self.url = url
        self.type = type
        self.year = year
        self.sub_title = sub_title
        self.id = id

    def __str__(self):
        return "{} {} {}".format(self.title, self.type, self.year)

class popularMovieInformation:
    def __init__(self, name=None, img_src=None, url=None , movieSynopsis=None):
        self.name = name
        self.img_src = img_src
        self.url = url
        self.movieSynopsis = movieSynopsis

    def __str__(self):
        return "{} {} {} {}".format(self.name, self.img_src, self.url, self.movieSynopsis)

class recommendMovieInformation:
    def __init__(self, name=None, img_src=None, url=None):
        self.name = name
        self.img_src = img_src
        self.url = url

    def __str__(self):
        return "{} {} {}".format(self.name, self.img_src, self.url)


class MovieInfo:
    def __init__(self, movieName=None, daoYan=None, bianJu=None, zhuYan=None, leiXing=None,
                 zhiPianGuoJia=None, yuYan=None, shangYinRiqi=None, pianChang=None,
                 youMing=None, Imdb=None,intro=None,imgurl=None):
        self.movieName = movieName
        self.daoYan = daoYan
        self.bianJu = bianJu
        self.zhuYan = zhuYan
        self.leiXing = leiXing
        self.zhiPianGuoJia = zhiPianGuoJia
        self.yuYan = yuYan
        self.shangYinRiQi = shangYinRiqi
        self.pianChang = pianChang
        self.youMing = youMing
        self.ImdbLink = Imdb
        self.id = None
        self.pingFeng = {}
        self.intro = intro
        self.imgurl=imgurl

    def __str__(self):
        return "导演：{} 类型：{}".format(self.daoYan, self.leiXing)
