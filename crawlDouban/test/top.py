import requests
from urllib.parse import urlencode
import re
from pyquery import PyQuery
import json
import ast
from crawlDouban.class_model import *
from bs4 import BeautifulSoup
from crawlDouban.models import MovieComment

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    # 'Cookie': 'bid=mOmO90C-w6M; douban-fav-remind=1; _pk_id.100001.8cb4=312120cc8d0f6772.1587020240.8.1588525708.1588519229.; __gads=ID=5d5c22da650af0da:T=1587020246:S=ALNI_MafXP2w2kUeuCkrdMzI3-6DtOsISQ; __utma=30149280.1977143909.1587020248.1588517876.1588525712.17; __utmz=30149280.1588437820.10.3.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/1291546/; __yadk_uid=gPAs1V5E0DlTUXc2Av0bRcpVaOdkZmIj; ll="108090"; _vwo_uuid_v2=D43D50D3FBBF9F8F37D287B2F209860AE|072367d27f51ea8d9fd3d1c93267222a; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1588525708%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%22%5D; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14418; dbcl2="144189809:x8MCGTDWfsA"; ck=6aOj; __utmc=30149280; ap_v=0,6.0; _pk_ses.100001.8cb4=*; __utmb=30149280.2.9.1588525712; __utmt=1'
    'Cookie': 'bid=rqDgBMKyH_g; douban-fav-remind=1; ll="118183"; _vwo_uuid_v2=DD7E8A4518B1A4CA771C26A9EA09E336D|bce91a9c5e8e067e47f83f5dc35508f5; ps=y; push_noty_num=0; push_doumail_num=0; douban-profile-remind=1; __utmc=30149280; __utmc=223695111; dbcl2="216281573:UrtEzTJAbk8"; ck=LFss; __utmv=30149280.21628; __utmz=223695111.1588620474.14.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=30149280.1588622313.18.7.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1588644202%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.1764587075.1585115693.1588622313.1588644202.19; __utmb=30149280.0.10.1588644202; __utma=223695111.213308978.1585916608.1588620474.1588644202.15; __utmb=223695111.0.10.1588644202; ap_v=0,6.0; _pk_id.100001.4cf6=8e798f80dd54ca91.1585916608.15.1588644213.1588620894.'
}
search_url = "https://search.douban.com/movie/subject_search?search_text="
search_url_2 = "https://movie.douban.com/j/subject_suggest?q="
hot_url = "https://movie.douban.com/top250?start="
ex1 = "https://movie.douban.com/subject/33420285/"
comment_url = "https://movie.douban.com/subject/{}/comments?"

def getTopItems( html, page):
    '''
    获取热门250的信息
    :param html:
    :param page:
    :return:
    '''
    html = html.replace("<br>", "")
    soup = BeautifulSoup(html, "html.parser")
    # alink = soup.find_all('a')
    all_movie_info = soup.find_all('div', {"class": "info"})
    all_movie_image = soup.find_all("div", {"class": "pic"})

    print(len(all_movie_info))
    cur_top = []
    for i, movie in enumerate(all_movie_info):
        # print(all_movie_image[i].find("img").get("src"))
        if all_movie_image[i].find("img").get("src") != None:
            img_rul = all_movie_image[i].find("img").get("src")
        else:
            img_rul = ""
        if movie.find("a").get("href") != None:
            movie_id = movie.find("a").get("href")
            # print(movie_id.split("/"))
            movie_id = movie_id.split("/")[-2]
        else:
            movie_id = ""
        movie_name = movie.find('span', {"class": "title"})
        quote = movie.find("span", {"class": "inq"})
        d_info = movie.find("p", {"class": ""})
        if movie_name != None:
            if quote != None and d_info != None:
                cur_top.append((movie_name.string, quote.string, d_info.string.strip(), img_rul, movie_id))
            else:
                cur_top.append((movie_name.string, "", "", img_rul, movie_id))
    return cur_top

def getCommentHtmlText( url, start_no):
    data = {
        'start': start_no,
        'limit': 20,
        'sort': 'new_score',
        'status': 'P',
        'percent_type': ''
    }
    url = url + urlencode(data)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print(response.text)
            return response.text
    except Exception:
        print('访问页面' + url + '出错！')
        return None

def getHtmlText(url=None):
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    #     'Host': 'movie.douban.com',
    #     'Cookie':'bid=mOmO90C-w6M; douban-fav-remind=1; _pk_id.100001.8cb4=312120cc8d0f6772.1587020240.12.1588582491.1588580338.; __gads=ID=5d5c22da650af0da:T=1587020246:S=ALNI_MafXP2w2kUeuCkrdMzI3-6DtOsISQ; __utma=30149280.1977143909.1587020248.1588580342.1588582478.22; __utmz=30149280.1588580342.21.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=gPAs1V5E0DlTUXc2Av0bRcpVaOdkZmIj; ll="108090"; _vwo_uuid_v2=D43D50D3FBBF9F8F37D287B2F209860AE|072367d27f51ea8d9fd3d1c93267222a; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1588582477%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DNQUSL9GtAjJXbMPGfKF04MK7i4KJp8mcRjYGkj_NLVGYV_OrKaQybZ-ck13qQthQ%26wd%3D%26eqid%3Da8b1e283007be3d1000000045eafa9ea%22%5D; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14418; __utmc=30149280; _pk_ses.100001.8cb4=*; __utmb=30149280.4.9.1588582492251; __utmt=1; dbcl2="144189809:1cHsR8veDe4"'
    # }
    headers['Host'] = 'movie.douban.com'
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print("访问{}出错".format(url))
        print(e)
        return None

def getHot():
    page = 10
    top_250 = []
    for index in range(page):
        url = hot_url + str(25 * index)
        html = getHtmlText(url)
        cur_top = getTopItems(html, index)
        top_250 += cur_top
        # break
    print("热门电影数量：{}".format(len(top_250)))
    return top_250

def getexpageItems(html):
    html = html.replace("<br>", "")
    soup = BeautifulSoup(html, "html.parser")
    all_move_id = soup.find_all('dt')
    cur_top = []
    for i, movie in enumerate(all_move_id):
        if movie.find("a").get("href") != None:
            movie_url = movie.find("a").get("href")
            # print(movie_id.split("/"))
            # movie_id = movie_url.split("/")[-2]
            img_url = movie.find("img").get("src")
            movie_name = movie.find("img").get("alt")
            # print(movie_url)
            # print(img_url)
            # print(movie_name)
        else:
            movie_id = ""
        cur_top.append((movie_name, movie_url, img_url))
    print(cur_top)
    return cur_top


def randompageItems():
    ll = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        # 'Cookie': 'bid=mOmO90C-w6M; douban-fav-remind=1; _pk_id.100001.8cb4=312120cc8d0f6772.1587020240.8.1588525708.1588519229.; __gads=ID=5d5c22da650af0da:T=1587020246:S=ALNI_MafXP2w2kUeuCkrdMzI3-6DtOsISQ; __utma=30149280.1977143909.1587020248.1588517876.1588525712.17; __utmz=30149280.1588437820.10.3.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/1291546/; __yadk_uid=gPAs1V5E0DlTUXc2Av0bRcpVaOdkZmIj; ll="108090"; _vwo_uuid_v2=D43D50D3FBBF9F8F37D287B2F209860AE|072367d27f51ea8d9fd3d1c93267222a; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1588525708%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%22%5D; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14418; dbcl2="144189809:x8MCGTDWfsA"; ck=6aOj; __utmc=30149280; ap_v=0,6.0; _pk_ses.100001.8cb4=*; __utmb=30149280.2.9.1588525712; __utmt=1'
        'Cookie': 'bid=rqDgBMKyH_g; douban-fav-remind=1; ll="118183"; _vwo_uuid_v2=DD7E8A4518B1A4CA771C26A9EA09E336D|bce91a9c5e8e067e47f83f5dc35508f5; ps=y; push_doumail_num=0; push_noty_num=0; douban-profile-remind=1; __utmv=30149280.21628; __utmz=30149280.1588734910.24.10.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ct=y; __gads=ID=af8be540a0c107f2:T=1588849015:S=ALNI_MYJ4YNDp2QTydl8NaWupHGfaSnL_g; ap_v=0,6.0; __utmc=30149280; __utmc=223695111; __utmz=223695111.1588938087.24.13.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=30149280.1764587075.1585115693.1588938083.1588943084.29; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1588943506%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.213308978.1585916608.1588938087.1588943506.25; __utmb=223695111.0.10.1588943506; dbcl2="216281573:PHp7DLkk3Oo"; ck=lc3J; _pk_id.100001.4cf6=8e798f80dd54ca91.1585916608.24.1588943519.1588939950.; __utmb=30149280.5.10.1588943084'

    }
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=热门&page_limit=20"
    page = requests.get(url=url, headers=headers).json()
    page_list = []
    print(page)
    for r in range(20):  # 每次加载20条
        list = page['subjects']
        dict = list[r]
        # item = {}
        # item['name'] = dict['title']  # 电影名称
        # item['img_src'] = dict['cover']  # 图片链接
        # item['url'] = dict['url']  # 电影链接
        # page_list.append((item['name'], item['url'], item['img_src']))
        item = popularMovieInformation(
            name=dict['title'],
            img_src=dict['cover'],
            url=dict['url']
        )
        page_list.append(item)
    # ll.extend(page_list)
    # print(ll[0])
    print(page_list)

if __name__ == '__main__':
    # result = claw.search_movie(name="霸王别姬")
    # print("===========")
    # print(result)
    # claw.getMovieInfo("https://movie.douban.com/subject/1292052/")
    # all_top = getHot()
    # print(all_top)
    # ex1 = "https://movie.douban.com/subject/33420285/"
    # html = getHtmlText(ex1)
    # ex_page = getexpageItems(html)
    # ex1 = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0"
    # html = getHtmlText(ex1)
    # ex_page = getrandompageItems(html)
    randompageItems()