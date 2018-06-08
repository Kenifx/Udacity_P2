#coding=utf-8
import requests
import bs4
import urllib
import expanddouban


#create regions list
region = [
'中国','大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦'
]

#create category list
category = [
'剧情','喜剧','动作','爱情','科幻','悬疑','惊悚','恐怖','犯罪','同性','音乐','歌舞','传记','历史','战争','西部','奇幻','冒险','灾难','武侠','情色'
]


'''TASK 1'''
"""
return a string corresponding to the URL of douban movie lists given category and location.
#https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影
"""
def getMovieUrl(category, location):
    url = None
    base_url = "https://movie.douban.com/tag/"
    tag = "," + category + ',' +  location
    url = urllib.parse.urljoin(base_url,'#/?sort=S&range=9,10&tags=电影' + tag )
    return url

#print(getMovieUrl("剧情","美国"))

html = expanddouban.getHtml(getMovieUrl("剧情","美国"))

