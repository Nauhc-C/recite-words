# -*- coding: utf-8 -*-
"""
@author: Sulingchuan
"""
import datetime
import sqlite3
import urllib.request
import parsel
import requests
import pyperclip
import random
import time
import pyttsx3

rootUrl = 'http://www.iciba.com/word?w='

#此方法用于建立数据库
def createTable():
    conn = sqlite3.connect('./wordbank.sqlite3')
    cur = conn.cursor()
    #期中TFNR是下一次背诵时间
    sql = """CREATE TABLE lexicon (
                    id integer primary key autoincrement,
                    wordE varchar(255) not null,
                    wordC varchar(255) not null,
                    TFNR integer,
                    count integer
                );"""
    cur.execute(sql)
    print("create table success")
#此方法用于联网搜索
def search(word):
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
            print("这是个你需要背的词汇")
            need = True
        else:
            print("这是个超纲词汇")
            need = False
    return str,need
#此方法用于处理查单词
def search_insert(word,str):
    cur.execute(f"""SELECT 1 from lexicon WHERE wordE = '{word}' LIMIT 1""")
    results = cur.fetchall()
    if (results == []):
        print("录入单词库!")
        cur.execute(f"""INSERT INTO lexicon VALUES ('{word}','{str}','{0}',{0})""")
        conn.commit()
    else:
        print("已经在单词库里了")
#此方法用于计算两个字符串之间相差几天

def calDay(day1,day2):
    day1 = day1.replace("\n",'')
    time_array1 = time.strptime(day1, "%Y-%m-%d")
    timestamp_day1 = int(time.mktime(time_array1))
    time_array2 = time.strptime(day2, "%Y-%m-%d")
    timestamp_day2 = int(time.mktime(time_array2))
    result = (timestamp_day2 - timestamp_day1) // 60 // 60 // 24
    return result



#main
#init()
#链接数据库
conn = sqlite3.connect('./wordbank.sqlite3')
cur = conn.cursor()
mode = '2'
mode = input("请选择模式,1查单词,2背单词")
if(mode == '1'):
    last_paste_str = pyperclip.paste()
    print(last_paste_str)
    while True:
        time.sleep(1)
        paste_str = pyperclip.paste()
        if last_paste_str != paste_str:  #只有在有变化的时候才会改变
            last_paste_str = pyperclip.paste()
            print(paste_str + " * " + last_paste_str)
            paste_str = paste_str.strip() #消除空格
            try:
                str, need = search(paste_str)  # 联网搜索 str为翻译,need为是否是考纲需要的s
                # 录入
                print(str, end='')
                if(need):
                    search_insert(paste_str, str)
            except Exception as e:
                print("出错了")
                print(e)

                continue
            last_paste_str = pyperclip.paste()
elif(mode == '2'):
    #首先获取时间差
    lines = open("test.txt",'r+',encoding='utf-8')
    line = lines.readline()
    print("相差",end='')
    result = calDay(str(line),(str)(datetime.date.today()))
    print(result)
    lines.close()
    a = open("test.txt", 'w+', encoding='utf-8')
    a.write((str)(datetime.date.today())+"\n")#写入今天时间

    for i in range(0,result):
        cur.execute(f"""update lexicon set TFNR=TFNR-1""")  #正常使用
    #cur.execute(f"""update lexicon set TFNR = 3""")
        conn.commit()
    sql = cur.execute(f"""SELECT * from lexicon""")

    fulllist = []
    checklist = []
    #读取单词到list里
    for row in sql:
        fulllist.append(row)
    #读取单词到背单词list里
    for row in fulllist:
        if row[2] <= 0:
            checklist.append(row)
    print("本次加载了" + str(len(checklist)) + "个,单词,请好好背诵哦")
#开始背单词
    for i in checklist: #i 代表这次要考察的单词
        print(i[0])
        pyttsx3.speak(i[0])
        loc = random.randint(0,3)#确定随机位置
        for j in range(0,4):  #打印选项的部分
            print(j,end="]:")
            if(j == loc):
                print(i[1].replace("\n","  "),end='\n')
            else:
                print(random.choice(fulllist)[1].replace("\n","  "),end='\n')
        try:
            answer = int(input("请选择中文释义,输入数字"))
        except:
            answer = '-1'
        if(answer == loc):  #选择正确
            print("-----回答正确")
            cur.execute(f"""update lexicon set TFNR = 3+count, count = count+1 where wordE = '{i[0]}'""")
            conn.commit()
        else:
            print("-----回答错误")
            print("-----正确答案是"+str(i[1]))
            cur.execute(f"""update lexicon set TFNR = 1 where wordE = '{i[0]}'""")
            conn.commit()
    print("本次要背的单词都背完辣")
