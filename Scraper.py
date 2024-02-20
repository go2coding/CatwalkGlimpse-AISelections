# coding:utf-8

from datetime import datetime
import codecs
import requests
import os
from pyquery import PyQuery as pq
import urllib.parse

dir_path = "./data/trending/"

# 获取今天的日期
today = datetime.now().strftime("%Y-%m-%d")
year = today.split("-")[0]
month = today.split("-")[1]


today_path = dir_path + year + '/' + month


def createMarkdown(date, filename):

    if not os.path.isdir(today_path):
        os.makedirs(today_path)

    with open(today_path + '/' + filename, 'w') as f:
        f.write("## " + date + "\n")


def scrape(language, filename):
    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'zh-CN,zh;q=0.8'
    }
    url = 'https://github.com/trending/{language}'.format(language=urllib.parse.quote(language))
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return
    
    d = pq(r.content)
    items = d('div.Box article.Box-row')

    # codecs to solve the problem utf-8 codec like chinese
    with codecs.open(today_path + '/' + filename, "a", "utf-8") as f:
        f.write('\n#### {language}\n'.format(language=language))

        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text()
            owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url
            # ownerImg = i("p.repo-list-meta a img").attr("src")
            # print(ownerImg)
            f.write(u"* [{title}]({url}):{description}\n".format(title=title, url=url, description=description))



def main():
    strdate = datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    # create markdown file
    createMarkdown(strdate, filename)

    languages = ['c','c#','c++','java','Kotlin','Objective-C','php','rust','python','swift','javascript','go','TypeScript']

    # write markdown
    for language in languages:
        scrape(language, filename)

    # git add commit push
    # git_add_commit_push(strdate, filename)


if __name__ == '__main__':
    main()
