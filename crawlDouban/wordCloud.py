import jieba
from collections import Counter
import numpy as np
from os import path  # 用来获取文档的路径
import os
from matplotlib import pyplot as plt
import matplotlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cidan_path = os.path.join(BASE_DIR, "crawlDouban")
static_path = os.path.join(BASE_DIR, "static")


# 分词
def jiebaClearText(text):
    '''
    返回二维数组
    :param text:
    :return:
    '''
    mywordList = []

    # 读取停用词表
    stopwords_path = os.path.join(cidan_path, '词典/停用词.txt')

    seg_list = jieba.cut(text, cut_all=False)

    listStr = '/'.join(seg_list)
    # 打开停用词表
    f_stop = open(stopwords_path, encoding="utf8")
    # 读取
    try:
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()  # 关闭资源

    f_stop_seg_list = f_stop_text.split("\n")
    for myword in listStr.split('/'):
        # 去除停用词
        if not (myword.split()) in f_stop_seg_list and len(myword.strip()) > 1:
            mywordList.append(myword)
    # 统计词频
    c = Counter()
    for x in mywordList:
        if len(x) > 1:
            c[x] += 1
    all_word_freq = []
    for k, v in c.items():
        all_word_freq.append([k, v])
    return all_word_freq


# 打开词典文件，返回列表
def open_dict(Dict, path):
    path = path + '%s.txt' % Dict
    dictionary = open(path, 'r', encoding='utf-8')
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        dict.append(word)
    return dict


def judgeodd(num):
    if (num % 2) == 0:
        return 'even'
    else:
        return 'odd'


# 注意，这里你要修改path路径。
deny_word = open_dict(Dict=os.path.join(cidan_path, '词典/否定词'), path=r'')
posdict = open_dict(Dict=os.path.join(cidan_path, '词典/positive'), path=r'')
negdict = open_dict(Dict=os.path.join(cidan_path, '词典/negative'), path=r'')
degree_word = open_dict(Dict=os.path.join(cidan_path, '词典/程度副词'), path=r'')

mostdict = degree_word[degree_word.index('extreme') + 1: degree_word.index('very')]  # 权重4，即在情感词前乘以4
verydict = degree_word[degree_word.index('very') + 1: degree_word.index('more')]  # 权重3
moredict = degree_word[degree_word.index('more') + 1: degree_word.index('ish')]  # 权重2
ishdict = degree_word[degree_word.index('ish') + 1: degree_word.index('last')]  # 权重0.5


def sentiment_score(senti_score_list):
    score = []
    for review in senti_score_list:
        score_array = np.array(review)
        Pos = np.sum(score_array[:, 0])
        Neg = np.sum(score_array[:, 1])
        AvgPos = np.mean(score_array[:, 0])
        AvgPos = float('%.1f' % AvgPos)
        AvgNeg = np.mean(score_array[:, 1])
        AvgNeg = float('%.1f' % AvgNeg)
        StdPos = np.std(score_array[:, 0])
        StdPos = float('%.1f' % StdPos)
        StdNeg = np.std(score_array[:, 1])
        StdNeg = float('%.1f' % StdNeg)
        score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])  # 积极、消极情感值总和(最重要)，积极、消极情感均值，积极、消极情感方差。
    return score


def EmotionByScore(data):
    result_list = sentiment_score(sentiment_score_list(data))
    return result_list[0][0], result_list[0][1]


def JudgingEmotionByScore(Pos, Neg):
    if Pos.all() > Neg.all():
        str = '1'
    elif Pos < Neg:
        str = '-1'
    elif Pos == Neg:
        str = '0'
    return str


def sentiment_score_list(dataset):
    # seg_sentence = dataset.split('。')

    count1 = []
    count2 = []
    for sen in dataset:  # 循环遍历每一个评论
        segtmp = jieba.lcut(sen, cut_all=False)  # 把句子进行分词，以列表的形式返回
        i = 0  # 记录扫描到的词的位置
        a = 0  # 记录情感词的位置
        poscount = 0  # 积极词的第一次分值
        poscount2 = 0  # 积极词反转后的分值
        poscount3 = 0  # 积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            if word in posdict:  # 判断词语是否是情感词
                poscount += 1
                c = 0
                for w in segtmp[a:i]:  # 扫描情感词前的程度词
                    if w in mostdict:
                        poscount *= 4.0
                    elif w in verydict:
                        poscount *= 3.0
                    elif w in moredict:
                        poscount *= 2.0
                    elif w in ishdict:
                        poscount *= 0.5
                    elif w in deny_word:
                        c += 1
                if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1  # 情感词的位置变化

            elif word in negdict:  # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in mostdict:
                        negcount *= 4.0
                    elif w in verydict:
                        negcount *= 3.0
                    elif w in moredict:
                        negcount *= 2.0
                    elif w in ishdict:
                        negcount *= 0.5
                    elif w in degree_word:
                        d += 1
                if judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif word == '！' or word == '!':  ##判断句子是否有感叹号
                for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in posdict or negdict:
                        poscount3 += 2
                        negcount3 += 2
                        break
            i += 1  # 扫描词位置前移

            # 以下是防止出现负数的情况
            pos_count = 0
            neg_count = 0
            if poscount3 < 0 and negcount3 > 0:
                neg_count += negcount3 - poscount3
                pos_count = 0
            elif negcount3 < 0 and poscount3 > 0:
                pos_count = poscount3 - negcount3
                neg_count = 0
            elif poscount3 < 0 and negcount3 < 0:
                neg_count = -poscount3
                pos_count = -negcount3
            else:
                pos_count = poscount3
                neg_count = negcount3

            count1.append([pos_count, neg_count])
        count2.append(count1)
        count1 = []

    return count2


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def getAllDatasetScore(data):
    normal_data = normalization(data)  # 归一化
    # print(normal_data)
    # print(normal_data.sum(axis=1))  # 求和
    sum_normal_data = normal_data.sum(axis=1)
    # all_pos_score = sum_normal_data[0]
    # all_neg_score = sum_normal_data[1]
    # print(all_pos_score,all_neg_score)
    return sum_normal_data


def draw(all_score=None, dymz="test", movieId="test"):
    print(all_score)
    score_pos = all_score[0]
    score_neg = all_score[1]
    print(score_pos)
    print(score_neg)
    matplotlib.rc("font", family='KaiTi', weight="bold")

    x_label = range(0, len(score_neg))
    print(x_label)

    # 设置图形大小
    plt.figure()
    plt.xlim((0, len(score_neg)))

    plt.scatter(x_label, score_pos, label="正面得分")
    plt.scatter(x_label, score_neg, label="负面得分")
    # plt.plot(x_label,score_pos,label="正面得分")
    # plt.plot(x_label, score_neg, label="负面得分")

    # 添加图例
    plt.legend(loc="best")
    plt.xlabel("序号")
    plt.ylabel("得分")
    plt.title(dymz + "影评情感分数散点图")
    plt.savefig(os.path.join(static_path, 'test.jpg'))
    plt.show()


if __name__ == '__main__':
    str1 = '''
    当年的奥斯卡颁奖礼上，被如日中天的《阿甘正传》掩盖了它的光彩，而随着时间的推移，这部电影在越来越多的人们心中的地位已超越了《阿甘》。每当现实令我疲惫得产生无力感，翻出这张碟，就重获力量。毫无疑问，本片位列男人必看的电影前三名！回顾那一段经典台词：“有的人的羽翼是如此光辉，即使世界上最黑暗的牢狱，也无法长久地将他围困！”
不需要女主角的好电影
恐惧让你沦为囚犯，希望让你重获自由。——《肖申克的救赎》
“这是一部男人必看的电影。”人人都这么说。但单纯从性别区分，就会让这电影变狭隘。《肖申克的救赎》突破了男人电影的局限，通篇几乎充满令人难以置信的温馨基调，而电影里最伟大的主题是“希望”。 当我们无奈地遇到了如同肖申克一般囚禁了心灵自由的那种囹圄，我们是无奈的老布鲁克，灰心的瑞德，还是智慧的安迪？运用智慧，信任希望，并且勇敢面对恐惧心理，去打败它？ 经典的电影之所以经典，因为他们都在做同一件事——让你从不同的角度来欣赏希望的美好。
策划了19年的私奔……
关于希望最强有力的注释。
有种鸟是关不住的.
超级喜欢超级喜欢,不看的话人生不圆满.
忒经典的东西,我要带去我的坟墓
    '''
    # print(jiebaClearText(str1))
    data1 = '今天上海的天气真好！我的心情非常高兴！如果去旅游的话我会非常兴奋！和你一起去旅游我会更加幸福！'
    data2 = '每次看这些神作的时候想到这是动画片这是一群牛人一笔一笔画出来的,就觉得漏看掉一帧都实在是对不起他们啊'
    data3 = '美国华裔科学家,祖籍江苏扬州市高邮县,生于上海,斯坦福大学物理系,电子工程系和应用物理系终身教授!'
    data4 = ' 但还是就回家'
    data = []
    data.append(data1)
    data.append(data2)
    data.append(data3)
    data.append(data4)
    score = sentiment_score(sentiment_score_list(data))  # 得到情感分数
    print(score)
    score = np.array(score)
    # print(score)
    # print(score[:,0])
    # print(score[:,1])
    emotion = JudgingEmotionByScore(score[:, 0], score[:, 1])
    print(emotion)
    # 垂直合并，第一行为所有元素的正向情感，第二行为所有元素的负向情感
    c = np.vstack((score[:, 0], score[:, 1]))
    print("--")
    print(c)
    # print(score[:,0]>score[:,1])
    # print(score[:, 0] == score[:, 1])
    # print(score[:, 0] < score[:, 1])
    all_sum_socre = getAllDatasetScore(c)
    print('正面情感的数量：', sum(score[:, 0] > score[:, 1]))
    print('中性情感的数量：', sum(score[:, 0] == score[:, 1]))
    print('负面情感的数量：', sum(score[:, 0] < score[:, 1]))
