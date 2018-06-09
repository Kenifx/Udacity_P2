import requests
import bs4
import expanddouban
import codecs



url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,战争，美国'

#with codecs.open('html_test.txt','w','utf-8') as f:
html = expanddouban.getHtml(url)
#f.write(html)
soup = bs4.BeautifulSoup(html,"html.parser") #bs来解析拿到的html内容

movie_list = soup.find(class_='list-wp')

print(movie_list)

