# -*- coding: utf-8 -*-
import requests
import bs4
import urllib
import expanddouban
import codecs
import csv


'''首先先定义一些后面要用到的list'''
# regions list
locations = [
'中国','大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦'
]

# category list
categories = [
'剧情','喜剧','动作','爱情','科幻','悬疑','惊悚','恐怖','犯罪','同性','音乐','歌舞','传记','历史','战争','西部','奇幻','冒险','灾难','武侠','情色'
]

# my favorite
myFavCategory = ['战争','灾难','科幻']


'''TASK 1 获得每个地区，类型页面的url'''
"""
return a string corresponding to the URL of douban movie lists given category and location.
https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影
"""
def getMovieUrl(category, location):
    url = None
    base_url = "https://movie.douban.com/tag/"
    tag = "," + category + ',' +  location
    url = urllib.parse.urljoin(base_url,'#/?sort=S&range=9,10&tags=电影' + tag )
    return url

#print(getMovieUrl("剧情","美国"))

'''TASK 2

with codecs.open('html.txt','w','utf-8') as f:
    html = expanddouban.getHtml(getMovieUrl("剧情", "美国"))
    f.write(html)
'''

#html = expanddouban.getHtml(getMovieUrl("剧情","美国"))

'''TASK 3 任务3: 定义电影类'''
class Movie:
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

'''TASK 4 获取豆瓣电影的信息'''
"""
return a list of Movie objects with the given category and location.
"""
def getMovies(category, location):
    html = expanddouban.getHtml(getMovieUrl(category, location))
    soup = bs4.BeautifulSoup(html,"html.parser") #bs来解析拿到的html内容

    movies = soup.find(class_='list-wp')

    names = []
    rates = []
    info_links = []
    cover_links = []

    #开始查找
    for movie in movies.find_all('a'):
        names.append(movie.find(class_="title").string)
        rates.append(movie.find(class_="rate").string)
        info_links.append(movie.get("href"))
        cover_links.append(movie.find("img").get("src"))

    #存储查找到的电影
    movie_list = []
    for i in range(len(names)):
        movie_list.append(Movie(names[i],rates[i],location,category,info_links[i],cover_links[i]))
    return movie_list
    #电影存储完毕

#getMovies函数完成


'''TASK 5 构造电影信息数据表'''
#用getMovies函数查找输出爬到的电影数据表
movies = []
for category in myFavCategory:
    for location in locations:
        movies += getMovies(category, location)

#此前一直遇到gbk编码错误，所以在网上查找方法并询问其他人的建议，于是用codecs模组解决
with open('movies.csv','w') as f:
    line = csv.writer(f)
    for movie in movies:
        line.writerow([movie.name, movie.rate, movie.location, movie.category, movie.info_link, movie.cover_link])


'''TASK6 统计电影数据
统计你所选取的每个电影类别中，数量排名前三的地区有哪些，分别占此类别电影总数的百分比为多少？'''

#统计每个类别的电影个数
#统计每个类别每个地区的电影个数

