import requests
from urllib.parse import urlencode
import re
from pyquery import PyQuery
import json
import ast
from crawlDouban.class_model import *
from bs4 import BeautifulSoup
from crawlDouban.models import MovieComment,All_MovieComment,SearchMovieResults
from doubanMovie.settings import headers


class Claw:
    def __init__(self):
        self.headers = headers
        self.search_url = "https://search.douban.com/movie/subject_search?search_text="
        self.search_url_2 = "https://movie.douban.com/j/subject_suggest?q="
        self.hot_url = "https://movie.douban.com/top250?start="
        self.comment_url = "https://movie.douban.com/subject/{}/comments?"

    def search_movie(self, name):
        try:
            url = self.search_url_2 + name
            response = requests.get(url=url, headers=self.headers)
            # response = requests.get(url=url,)
            print("状态码：", response.status_code)
            # print(response.text)
            search_movie_result = []
            print(type(response.status_code))
            if response.status_code == 200:
                print(1)
                print(response)
                html = response.text
                print(html)
                html_str = html[1:-1].replace("\\", "")
                json_str = ast.literal_eval(html_str)
                print("查看json")
                # print(type(json_str),json_str)
                #

                json_str_tuple = []
                if type(json_str) == tuple:
                    json_str_tuple = json_str
                else:
                    json_str_tuple.append(json_str)
                print(type(json_str_tuple), json_str_tuple)
                for cur_movie in json_str_tuple:
                    print('==>', cur_movie)
                    db_search_result = SearchMovieResults.objects.filter(id = str(cur_movie["id"]) )
                    if len(db_search_result) == 0:
                        search_MovieResults = SearchMovieResults()
                        search_MovieResults.id = str(cur_movie["id"])
                        search_MovieResults.movieName = str(cur_movie['title'])
                        search_MovieResults.leiXing = str(cur_movie['type'])
                        search_MovieResults.shangYinRiQi = str(cur_movie['year'])
                        search_MovieResults.subtitle = str(cur_movie["sub_title"])
                        search_MovieResults.movieLink = str(cur_movie['url'])
                        search_MovieResults.aboutmovie = str(name)
                        search_MovieResults.save()
                        print("搜索信息存库了")
                    else:
                        print("库中已经存在")

                    search_result = SearchResult(
                        title=cur_movie['title'],
                        url=cur_movie['url'],
                        type=cur_movie['type'],
                        year=cur_movie['year'],
                        sub_title=cur_movie["sub_title"],
                        id=cur_movie["id"]
                    )

                    search_movie_result.append(search_result)
            elif response.status_code == 403:
                print("没有权限，拒绝连接，需要更换cookie")
            else:
                print("错误状态码：", response.status_code)
            return search_movie_result

        except Exception as e:
            print('访问页面' + url + '出错！')
            print(e)
            # return None

    def getMovieInfo(self, movieUrl):
        try:
            response = requests.get(movieUrl, headers=self.headers)
            print("状态码：", response.status_code)
            if response.status_code == 200:
                doc = PyQuery(response.text)
                movie_name = doc.find("#content > h1")
                movie_info = doc.find("#info:parent")  # 获取基本信息
                movie_rate = doc.find('.rating_num')  # 获取评分
                movie_star = doc.find('.item>.rating_per')  # 获取星数
                rating_people = doc.find('.rating_people')  # 获取评分人数
                image_url = doc.find('#mainpic > .nbgnbg > img').attr('src')
                # print(image_url)
                intro = doc.find('#link-report')
                # print(intro.text())
                # print(intro.text())
                # print(movie_name.text())
                movie_name_str = movie_name.text()
                # print(movie_info.text())

                # print(info.text().split(":"))
                info_text = movie_info.text().replace(" ", "")
                info_list = re.split("[: \n]", info_text)
                print("info_list" , info_list)
                if '导演' in info_list:
                    daoYan = info_list[info_list.index('导演') + 1]
                else:
                    daoYan = None
                print(daoYan)
                if '编剧' in info_list:
                    bianJu = info_list[info_list.index('编剧') + 1]
                else:
                    bianJu = None
                print(bianJu)
                if '主演' in info_list:
                    zhuYan = info_list[info_list.index("主演") + 1]
                else:
                    zhuYan = None
                print(zhuYan)
                if '类型' in info_list:
                    leiXing = info_list[info_list.index("类型") + 1]
                else:
                    leiXing = None
                print(leiXing)
                if '制片国家/地区' in info_list:
                    zhiPianGuoJia = info_list[info_list.index('制片国家/地区') + 1]
                else:
                    zhiPianGuoJia = None
                print("zhiPianGuoJia" , zhiPianGuoJia)
                if '语言' in info_list:
                    yuYan = info_list[info_list.index('语言') + 1]
                else:
                    yuYan = None
                print("yuYan" , yuYan)
                if '上映日期' in info_list:
                    shangYinRiQi = info_list[info_list.index('上映日期') + 1]
                else:
                    shangYinRiQi = None
                print("shangYinRiQi" , shangYinRiQi)
                if '片长' in info_list:
                    pianChang = info_list[info_list.index('片长') + 1]
                else:
                    pianChang = None
                print("pianChang" , pianChang)
                if '又名' in info_list:
                    youMing = info_list[info_list.index('又名') + 1]
                else:
                    youMing = None
                print("youMing" , youMing)
                if 'IMDb链接' in info_list:
                    ImdbLink = info_list[info_list.index('IMDb链接') + 1]
                else:
                    ImdbLink = None
                print("ImdbLink" , ImdbLink)

                movie_info = MovieInfo(movie_name_str, daoYan, bianJu, zhuYan, leiXing, zhiPianGuoJia, yuYan,
                                       shangYinRiQi,
                                       pianChang, youMing, ImdbLink, intro.text(), image_url)

                # print("movie_info" , movie_info.ImdbLink)
                # print("--",movie_rate)
                # print("== {} {}".format(movie_rate.text(),rating_people.text()))
                # print(movie_star.text())
                movie_star_split = (movie_star.text()).split(" ")
                print("movie_star_split" , movie_star_split)
                if movie_star_split == ['']:
                    movie_info.pingFeng = None
                else:
                    pingFeng = {}
                    pingFeng['评价人数'] = rating_people.text()
                    pingFeng['评分'] = movie_rate.text()
                    pingFeng['五星'] = movie_star_split[0]
                    pingFeng['四星'] = movie_star_split[1]
                    pingFeng['三星'] = movie_star_split[2]
                    pingFeng['二星'] = movie_star_split[3]
                    pingFeng['一星'] = movie_star_split[4]
                    print("pingFeng" , pingFeng)
                    movie_info.pingFeng = pingFeng
                    print("movie_info", movie_info.pingFeng)
                return movie_info
                # print("{} {} {} {} {}\n {} {} {} {} {}".format(
                #     daoYan,bianJu,zhuYan,leiXing,zhiPianGuoJia,yuYan ,shangYinRiQi,pianChang,youMing,ImdbLink
                # ))

            elif response.status_code == 403:
                print("没有权限，拒绝连接，需要更换cookie")
            else:
                print("错误状态码")

        except Exception as e:
            print("访问 {} 出错".format(movieUrl))
            print(e)

    def getHtmlText(self, url=None):
        # headers = {
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        #     'Host': 'movie.douban.com',
        #     'Cookie':'bid=mOmO90C-w6M; douban-fav-remind=1; _pk_id.100001.8cb4=312120cc8d0f6772.1587020240.12.1588582491.1588580338.; __gads=ID=5d5c22da650af0da:T=1587020246:S=ALNI_MafXP2w2kUeuCkrdMzI3-6DtOsISQ; __utma=30149280.1977143909.1587020248.1588580342.1588582478.22; __utmz=30149280.1588580342.21.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=gPAs1V5E0DlTUXc2Av0bRcpVaOdkZmIj; ll="108090"; _vwo_uuid_v2=D43D50D3FBBF9F8F37D287B2F209860AE|072367d27f51ea8d9fd3d1c93267222a; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1588582477%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DNQUSL9GtAjJXbMPGfKF04MK7i4KJp8mcRjYGkj_NLVGYV_OrKaQybZ-ck13qQthQ%26wd%3D%26eqid%3Da8b1e283007be3d1000000045eafa9ea%22%5D; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14418; __utmc=30149280; _pk_ses.100001.8cb4=*; __utmb=30149280.4.9.1588582492251; __utmt=1; dbcl2="144189809:1cHsR8veDe4"'
        # }
        headers = self.headers
        headers['Host'] = 'movie.douban.com'
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            return r.text
        except Exception as e:
            print("访问{}出错".format(url))
            print(e)
            return None

    def getCommentHtmlText(self, url, start_no):
        data = {
            'start': start_no,
            'limit': 20,
            'sort': 'new_score',
            'status': 'P',
            'percent_type': ''
        }
        url = url + urlencode(data)
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                # print(response.text)
                return response.text
        except Exception:
            print('访问页面' + url + '出错！')
            return None

    def getTopItems(self, html, page):
        '''
        获取热门250的信息
        :param html:
        :param page:
        :return:
        '''
        html = html.replace("<br>", "")
        soup = BeautifulSoup(html, "html.parser")
        alink = soup.find_all('a')
        all_movie_info = soup.find_all('div', {"class": "info"})
        all_movie_image = soup.find_all("div",{"class":"pic"})

        print(len(all_movie_info))
        cur_top = []
        for i,movie in enumerate(all_movie_info):
            # print(all_movie_image[i].find("img").get("src"))
            if all_movie_image[i].find("img").get("src") != None:
                img_rul = all_movie_image[i].find("img").get("src")
            else:
                img_rul = ""
            if movie.find("a").get("href")!= None:
                movie_id = movie.find("a").get("href")
                # print(movie_id.split("/"))
                movie_id =movie_id.split("/")[-2]
            else:
                movie_id = ""
            movie_name = movie.find('span', {"class": "title"})
            quote = movie.find("span", {"class": "inq"})
            d_info = movie.find("p", {"class": ""})
            if movie_name != None:
                if quote != None and d_info != None:
                    cur_top.append((movie_name.string, quote.string, d_info.string.strip(),img_rul,movie_id))
                else:
                    cur_top.append((movie_name.string, "","",img_rul,movie_id))
            # print("电影名称：{} 格言：{}".format(movie_name.string,quote.string))
            # print(d_info.string.strip())

            # print()

        # i = page * 25
        #
        # for index in range(len(alink)):
        #     if alink[index].find('span', {"class": "title"}) != None:
        #         # print('第' + str(i + 1) + '名' + alink[index].find('span', {"class": "title"}).string)
        #         cur_top.append(alink[index].find('span', {"class": "title"}).string)
        #         i += 1
        return cur_top


    def getHot(self):
        page = 10
        top_250 = []
        for index in range(page):
            url = self.hot_url + str(25 * index)
            html = self.getHtmlText(url)
            cur_top = self.getTopItems(html, index)
            top_250 += cur_top
            # break
        print("热门电影数量：{}".format(len(top_250)))
        return top_250

    def all_parse_comment_one_page(self, html, movieId):
        '''
        分析获得的短评页面
        :param html:
        :return:
        '''
        doc = PyQuery(html)
        title = doc.find('#content > h1:nth-child(1)').text()
        # print(title[:-2])
        items = list(doc('div.comment').items())
        print("items" , items)
        length = len(items)
        print(length)
        comment_list = []
        if length != 0:
            for item in items:
                commnet = {
                    'movie': title,
                    'comment user': item.find('span.comment-info').find('a').text(),  # PyQuery的特点，可以连续使用find
                    'comment': item.find('p').text(),
                    'vote': item.find('span.votes').text(),
                    'comment time': item.find('span.comment-time').text()
                }
                movie_comment_obj = All_MovieComment()
                movie_comment_obj.id = movieId + "_" + commnet['comment user']
                movie_comment_obj.movieId = movieId
                movie_comment_obj.comment = commnet['comment']
                movie_comment_obj.vote = commnet['vote']
                movie_comment_obj.comment_time = commnet['comment time']
                movie_comment_obj.save()
                # print(commnet)
                comment_list.append(commnet)
                # save_to_db(commnet)
            return True, comment_list
        elif items == []:
            print("评论为空")
            return False, comment_list
        else:
            print('爬取评论有问题')
            return False, comment_list

    def parse_comment_one_page(self, html, movieId):
        '''
        分析获得的短评页面
        :param html:
        :return:
        '''
        doc = PyQuery(html)
        title = doc.find('#content > h1:nth-child(1)').text()
        # print(title[:-2])
        items = list(doc('div.comment').items())
        length = len(items)
        # print(length)
        comment_list = []
        if length != 0:
            for item in items:
                commnet = {
                    'movie': title,
                    'comment user': item.find('span.comment-info').find('a').text(),  # PyQuery的特点，可以连续使用find
                    'comment': item.find('p').text(),
                    'vote': item.find('span.votes').text(),
                    'comment time': item.find('span.comment-time').text()
                }
                movie_comment_obj = MovieComment()
                movie_comment_obj.id = movieId + "_" + commnet['comment user']
                movie_comment_obj.movieId = movieId
                movie_comment_obj.comment = commnet['comment']
                movie_comment_obj.vote = commnet['vote']
                movie_comment_obj.comment_time = commnet['comment time']
                movie_comment_obj.save()
                # print(commnet)
                comment_list.append(commnet)
                # save_to_db(commnet)
            return True, comment_list
        elif items == []:
            print("评论为空")
            return False, comment_list
        else:
            print('爬取评论有问题')
            return False, comment_list


    def getComment(self, moiveID):
        '''
        获取影片所有评论
        :return:
        '''
        start_no = 0
        # print(url)
        flag = True
        all_comment_list = []
        while flag:
            url = self.comment_url.format(moiveID)
            print("url" , url)
            html = self.getCommentHtmlText(url, start_no * 20)
            if html == None:
                print("html", html)
                break
            else:
                # if self.all_parse_comment_one_page(html, moiveID) == None
                # print("self.all_parse_comment_one_page(html, moiveID)" , self.all_parse_comment_one_page(html, moiveID))
                flag, comment_list = self.all_parse_comment_one_page(html, moiveID)
                if flag == False:
                    break
                all_comment_list += comment_list
                print("len(all_comment_list)" , len(all_comment_list))
                print("start_no" , start_no)
                print("all_comment_list[start_no]" , all_comment_list[start_no])
                start_no += 1


    def gettenComment(self, moiveID):
        '''
        获取影片10个评论
        :return:
        '''
        start_no = 0
        all_comment_list = []
        url = self.comment_url.format(moiveID)
        html = self.getCommentHtmlText(url, start_no * 20)
        if html == None:
            print("html", html)
        else:
            flag, comment_list = self.parse_comment_one_page(html, moiveID)
            all_comment_list += comment_list
            # print(len(all_comment_list), start_no, all_comment_list[start_no])


if __name__ == '__main__':
    claw = Claw()
    # result = claw.search_movie(name="霸王别姬")
    # print("===========")
    # print(result)
    claw.getMovieInfo("https://movie.douban.com/subject/1292052/")
    # all_top = claw.getHot()
    # print(all_top[:3])
    # # print(all_top)
    # # claw.getComment("1291546")
