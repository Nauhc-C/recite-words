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
import search
import recite

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




#main
#init()
#链接数据库
conn = sqlite3.connect('./wordbank.sqlite3')
cur = conn.cursor()
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
                str, need = search.search(paste_str)  # 联网搜索 str为翻译,need为是否是考纲需要的s
                # 录入
                print(str, end='')
                if(need):
                    search.search_insert(paste_str, str,cur,conn)
            except Exception as e:
                print("出错了")
                print(e)
                continue
            last_paste_str = pyperclip.paste()
elif(mode == '2'):
    recite.recite(cur,conn)
elif(mode == '0'):
    print("测试用")

