import datetime
import sqlite3
import urllib.request
import parsel
import requests
import pyperclip
import random
import time
import pyttsx3


#此方法用于联网搜索
def search(word):
    rootUrl = 'http://www.iciba.com/word?w='
    url = rootUrl + urllib.parse.quote(word)  # 解决url中带有中文编译失败的问题
    print(url)
    response = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0'})
    selector = parsel.Selector(response.text)
    lis = selector.css('ul.Mean_part__UI9M6 > li')
    str = ""
    for li in lis:
        str += li.css("i::text").get()
        for i in li.css("span::text").getall():
            if (i != ';'):
                str += i
        str += "\n"
    tag = selector.css(".Mean_tag__K_C8K").css("p::text").get()
    need = False
    if(tag is None):
        print("没有tag")
        need = False
    else:
        if ("考研" in tag or "CET6" in tag):
            print("这是个你需要背的词汇:"+tag)
            need = True
        else:
            print("这是个超纲词汇")
            need = False
    return str,need
#此方法用于处理查单词
def search_insert(word,str,cur,conn):
    cur.execute(f"""SELECT 1 from lexicon WHERE wordE = '{word}' LIMIT 1""")
    results = cur.fetchall()
    if (results == []):
        print("录入单词库!")
        cur.execute(f"""INSERT INTO lexicon VALUES ('{word}','{str}','{0}',{0})""")
        conn.commit()
    else:
        print("已经在单词库里了")
#此方法用于计算两个字符串之间相差几天