# 爬取豆瓣top250影评并生成实时词云并完成推荐

## [Li-rr](https://github.com/Li-rr)

前半部分是大佬打的基础，后半部分大佬有点忙，我接过来修修bug、完善完善一点小功能，再后来客户太穷了，坑了我们一把，甩手就不干了。基本完工，吐血~，就差整理代码了，所以代码有点乱。

## 用到的技术主要有：
django, ajax, wordCloud2.js, bootstrap, jquery, django模板语法
## 功能实现：
- 先获取top250电影 
- 再去获取top250电影的影评
- 将数据存储到mongodb中
- 实时生成词云（伪实时）
- 支持搜索功能

## 环境要求：
主要的包如下：
- django 3.0
- monogoDb
- jieba
- requests
- pyquery
- wordCloud2.js（生成词云）

## 注意事项：
- 由于推荐按钮和搜索按钮的功能是一样的，所以点击推荐按钮或者搜索按钮时，搜索框中需要有电影名称
- 点击按钮可能会出现莫名奇妙的东西，这个可能是爬虫没有爬到数据以前引起的，可以结合控制台输出的log看

## 文件目录结构
```cmd
D:.
│  .gitignore
│  manage.py        管理文件
│  readme.md        说明文件
│  requirements.txt 依赖的包
│  test.html        测试，可不用
│
├─.idea
│  │  .gitignore
│  │  doubanMovie.iml
│  │  misc.xml
│  │  modules.xml
│  │  vcs.xml
│  │  workspace.xml
│  │
│  └─inspectionProfiles
│          profiles_settings.xml
│          Project_Default.xml
│
├─crawlDouban
│  │  admin.py
│  │  apps.py
│  │  class_model.py   定义数据结构，爬取数据时用
│  │  claw.py          爬虫代码
│  │  models.py        定义django数据模型
│  │  tests.py      
│  │  urls.py          路由
│  │  views.py         视图
│  │  wordCloud.py     分词与情感分析
│  │  __init__.py
│  │
│  ├─migrations
│  │  │  __init__.py
│  │  │
│  │  └─__pycache__
│  │          __init__.cpython-37.pyc
│  │
│  ├─templates
│  │      hotResult.html    热门页面
│  │      index.html        基础页面
│  │      movieInfo.html     电影信息
│  │      searchResult.html   搜索电影后的结果
│  │
│  ├─templatetags   没有用到
│  │  │  movie_exart.py
│  │  │  __init__.py
│  │  │
│  │  └─__pycache__
│  │          movie_exart.cpython-37.pyc
│  │          __init__.cpython-37.pyc
│  │
│  ├─__pycache__
│  │      admin.cpython-37.pyc
│  │      class_model.cpython-37.pyc
│  │      claw.cpython-37.pyc
│  │      models.cpython-37.pyc
│  │      urls.cpython-37.pyc
│  │      views.cpython-37.pyc
│  │      wordCloud.cpython-37.pyc
│  │      __init__.cpython-37.pyc
│  │
│  └─词典
│      │  negative+positive文档txt文件.rar
│      │  negative.txt
│      │  positive.txt
│      │  停用词.txt
│      │  否定词.txt
│      │  正.txt
│      │  正负各一万.txt
│      │  测试验证.txt
│      │  程度副词.txt
│      │  程度级别词语+否定词.rar
│      │  程度级别词语+否定词_1_.rar
│      │  程度级别词语.txt
│      │  程度级别词语0.txt
│      │  负.txt
│      │  面板.jpg
│      │
│      └─程度级别词语+否定词_1_
│              negative.txt
│              positive.txt
│              否定词.txt
│              程度副词-有问题.txt
│              程度副词1.txt
│
├─doubanMovie
│  │  asgi.py
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
│  │
│  └─__pycache__
│          settings.cpython-37.pyc
│          urls.cpython-37.pyc
│          wsgi.cpython-37.pyc
│          __init__.cpython-37.pyc
│
├─static  没有用到
│  └─js
│          wordcloud2.js
│
├─templates
└─__pycache__
        manage.cpython-37.pyc


```
