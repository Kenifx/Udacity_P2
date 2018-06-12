# -*- coding: utf-8 -*-
import bs4
import expanddouban
import codecs
import csv
import urllib

#@ kenif@163.com

'''首先先定义一些后面要用到的list
根据审阅建议，此处最好查询网页tag来获取地区。因为手动输入容易造成错误，也不方便后期维护'''
# regions list
#locations = ['中国','大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']

#这里构建函数用来获取地区
locations = []

def getLocations():
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影'
    html = expanddouban.getHtml(url, loadmore=False, waittime=2)
    soup = bs4.BeautifulSoup(html,"html.parser")

    content = soup.find(class_='tags').find(class_='category').next_sibling.next_sibling
    for sibling in content:
         location = sibling.find(class_='tag').get_text()
         if location != '全部地区':
             locations.append(location)

#使用函数获得地区
getLocations()


# my favorite
myFavCategory = ['战争','犯罪','科幻']


'''TASK 1 获得每个地区，类型页面的url'''
"""
return a string corresponding to the URL of douban movie lists given category and location.
https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影
"""
#
#def getMovieUrl(category, location):
#    url = None
#    base_url = "https://movie.douban.com/tag/"
#    tag = "," + category + ',' +  location
#    url = urllib.parse.urljoin(base_url,'#/?sort=S&range=9,10&tags=电影' + tag )
#    return url

#根据审阅建议，此处用format来简化构成url的语句
def getMovieUrl(category, location):
    url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category,location)
    return url



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
    html = expanddouban.getHtml(getMovieUrl(category, location),loadmore= True, waittime = 2)
    soup = bs4.BeautifulSoup(html,"html.parser") #bs来解析拿到的html内容

    movies = soup.find(class_='list-wp')

    names = []
    rates = []
    info_links = []
    cover_links = []

    for movie in movies.find_all('a'):
        names.append(movie.find(class_="title").string)
        rates.append(movie.find(class_="rate").string)
        info_links.append(movie.get("href"))
        cover_links.append(movie.find("img").get("src"))

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
with codecs.open('movies.csv','w', 'utf_8_sig') as f:
    line = csv.writer(f)
    for movie in movies:
        line.writerow([movie.name, movie.rate, movie.location, movie.category, movie.info_link, movie.cover_link])


'''TASK6 统计电影数据
统计你所选取的每个电影类别中，数量排名前三的地区有哪些，分别占此类别电影总数的百分比为多少？'''

#统计每个类别的电影个数
#统计每个类别每个地区的电影个数


#根据审阅建议，这里该用一个列表包含的列表来存储数据，而不是hard-code电影类型来获取
movieByCategory = [[],[],[]]
for movie in movies:
    for i in range(len(myFavCategory)):
        if movie.category == myFavCategory[i]:
            movieByCategory[i].append(movie)



def countByLocation(movies):
    movie_location_dict = {}
    for movie in movies:
        if movie.location not in movie_dict:
            movie_location_dict[movie.location] = 1
        else:
            movie_location_dict[movie.location] += 1
    return movie_location_dict

def countByCategory(movies):
    movie_category_dict = {}
    for movie in movies:
        if movie.category not in movie_category_dict:
            movie_category_dict[movie.category] = 1
        else:
            movie_category_dict[movie.category] += 1
    return movie_category_dict

movie_location = [[],[],[]]
for i in range(len(myFavCategory)):
    movie_location[i] = countByLocation(movieByCategory[i])


movie_category = [[],[],[]]
for i in range(len(myFavCategory)):
    movie_category[i] = countByCategory(movieByCategory[i])


movie_location_sorted = [[],[],[]]
for i in range(len(myFavCategory)):
    movie_location_sorted[i] = sorted(movie_location[i].items(), key=lambda x: x[1], reverse=True)[:3]



#顺序战争，犯罪，科幻
with open("output.txt", "w", encoding='utf-8') as f:
    for i in range(len(myFavCategory)):
        f.write("在{}电影中，前三的国家分别是第一：{},占比 {:.2%}, 第二：{},占比 {:.2%}，第三：{},占比 {:.2%} \n".format(
        myFavCategory[i],
        movie_location_sorted[i][0],
        round(movie_location[i][0] / movie_category[i][0]),
        movie_location_sorted[i][1],
        round(movie_location[i][1] / movie_category[i][1]),
        movie_location_sorted[i][2],
        round(movie_location[i][2] / movie_category[i][2])
        )
        )


