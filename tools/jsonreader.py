import json

news_articles = []
with open("data.json") as json_file:
    data = json.load(json_file)
    news = data['articles']
    for x, y in enumerate(news):
    	news_articles.append([x, [y['title'], y['url'], y['urlToImage'], y['source']['name']]])
    print(news_articles[0][1][3])
    	#for z in range(0, 1):
        	#for key, value in news[z].items():

'''
news_articles = []
for articles in news:
	news_articles.append(articles['title'])
	news_articles.append(articles['url'])

print(news_articles)
'''