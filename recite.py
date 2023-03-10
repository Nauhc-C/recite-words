

import datetime
import random
import time
import pyttsx3
import sound
#计算日期和时间的部分
def calDay(day1,day2):
    day1 = day1.replace("\n",'')
    time_array1 = time.strptime(day1, "%Y-%m-%d")
    timestamp_day1 = int(time.mktime(time_array1))
    time_array2 = time.strptime(day2, "%Y-%m-%d")
    timestamp_day2 = int(time.mktime(time_array2))
    result = (timestamp_day2 - timestamp_day1) // 60 // 60 // 24
    return result
#背单词的程序部分
def recite(cur,conn):
    lines = open("test.txt",'r+',encoding='utf-8')
    line = lines.readline()
    print("相差",end='')
    result = calDay(str(line),(str)(datetime.date.today()))
    print(result)
    lines.close()
    a = open("test.txt", 'w+', encoding='utf-8')
    a.write((str)(datetime.date.today())+"\n")#写入今天时间
    a.close()

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
    print("开始背单词,输入0~3回答问题,输入-1退出")
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
            answer = -1
        if(answer == loc):  #选择正确
            print("-----回答正确")
            cur.execute(f"""update lexicon set TFNR = 3+count, count = count+1 where wordE = '{i[0]}'""")
            conn.commit()
            sound.correct()
        elif(answer == -1):
            print("退出")
            break
        else:
            print("-----回答错误")
            print("-----正确答案是"+str(i[1]))
            cur.execute(f"""update lexicon set TFNR = 1 where wordE = '{i[0]}'""")
            conn.commit()
            sound.worse()
    print("本次要背的单词都背完辣")