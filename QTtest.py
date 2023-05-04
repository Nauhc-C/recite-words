from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import QTimer
import sys
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
import sound


class TabDemo(QWidget):
    def __init__(self):
        super().__init__()

        # 以下是各种属性
        self.count = 0
        self.count1 = 0
        self.recite_count = 0
        self.last_paste_str = pyperclip.paste()
        self.check_list = []
        self.current_correct_answer = ""
        self.current_word = ""

        self.setWindowTitle('八荒六谷唯我独尊背单词')
        self.setGeometry(1200, 200, 200, 200)

        # 创建一个QTabWidget对象
        tab_widget = QTabWidget()
        tab_widget.addTab(self.create_tab_search(), '查单词')
        tab_widget.addTab(self.create_tab2(), '背单词')

        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        self.setLayout(layout)

    #用于查单词的tab
    def create_tab_search(self):
        # 创建一个QWidget对象作为Tab 1的内容
        widget = QWidget()

        # 在QWidget中添加一个QLabel用于显示变化的字符串
        self.label = QLabel()
        self.label.setText('Initial Value')
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        widget.setLayout(layout)

        # 创建一个计时器
        timer = QTimer(self)
        timer.timeout.connect(self.Myupdate)  # 将计时器超时信号连接到槽函数

        # 每隔1秒触发一次计时器
        timer.start(1000)

        return widget

    def create_tab2(self):
        '''
        先完成基本信息的设置
        :return:
        '''
        # 创建一个QWidget对象作为Tab 2的内容
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        lines = open("test.txt", 'r+', encoding='utf-8')
        line = lines.readline()
        print("相差", end='')
        result = recite.calDay(str(line), (str)(datetime.date.today()))
        print(result)
        lines.close()
        a = open("test.txt", 'w+', encoding='utf-8')
        a.write((str)(datetime.date.today()) + "\n")  # 写入今天时间
        a.close()

        for i in range(0, result):
            cur.execute(f"""update lexicon set TFNR=TFNR-1""")  # 正常使用
            # cur.execute(f"""update lexicon set TFNR = 3""")
            conn.commit()
        sql = cur.execute(f"""SELECT * from lexicon""")

        self.fulllist = []
        self.checklist = []
        # 读取单词到list里
        for row in sql:
            self.fulllist.append(row)
        # 读取单词到背单词list里
        for row in self.fulllist:
            if row[2] <= 0:
                self.checklist.append(row)
        print("本次加载了" + str(len(self.checklist)) + "个,单词,请好好背诵哦")

        print("开始背单词,输入0~3回答问题,输入-1退出")
        print(self.checklist[self.recite_count][0])
        loc = random.randint(0, 3)  # 确定随机位置
        current_wordlist=[]  # 临时使用的数组
        for j in range(0, 4):  # 打印选项的部分
            if (j == loc):
                #print(checklist[0][1].replace("\n", "  "), end='\n')
                current_wordlist.append(self.checklist[self.recite_count][1].rstrip())
                self.current_correct_answer = self.checklist[self.recite_count][1].rstrip()
                self.current_word = self.checklist[self.recite_count][0]
            else:
                #print(random.choice(fulllist)[1].replace("\n", "  "), end='\n')
                current_wordlist.append(random.choice(self.fulllist)[1].rstrip())


        # 创建四个QPushButton按钮
        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label1.setText(self.checklist[0][0])
        self.button1 = QPushButton(current_wordlist[0])
        self.button2 = QPushButton(current_wordlist[1])
        self.button3 = QPushButton(current_wordlist[2])
        self.button4 = QPushButton(current_wordlist[3])
        self.button1.clicked.connect(self.on_button_clicked)
        self.button2.clicked.connect(self.on_button_clicked)
        self.button3.clicked.connect(self.on_button_clicked)
        self.button4.clicked.connect(self.on_button_clicked)

        self.label2.setText("要好好背单词哦")

        # 将四个按钮添加到layout中
        layout.addWidget(self.label1)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.label2)
        widget.setLayout(layout)
        return widget

    def on_button_clicked(self):
        button_text = self.sender().text()
        print("你的回答是:"+button_text+"正确答案是:"+self.current_correct_answer)
        if(button_text == self.current_correct_answer):
            print("回答正确")
            self.label2.setText("回答正确")
            cur.execute(f"""update lexicon set TFNR = 3+count, count = count+1 where wordE = '{self.current_word}'""")
            conn.commit()
            #sound.correct()
        else:
            print("-----回答错误")
            print("-----正确答案是"+str(button_text))
            self.label2.setText("回答错误,正确答案是"+str(self.current_word)+"\n"+str(self.current_correct_answer))
            cur.execute(f"""update lexicon set TFNR = 1 where wordE = '{self.current_word}'""")
            conn.commit()
            #sound.worse()

        # 以下为更新单词
        self.recite_count += 1

        print(self.checklist[self.recite_count][0])
        loc = random.randint(0, 3)  # 确定随机位置
        current_wordlist = []  # 临时使用的数组
        for j in range(0, 4):  # 打印选项的部分
            if (j == loc):
                # print(checklist[0][1].replace("\n", "  "), end='\n')
                current_wordlist.append(self.checklist[self.recite_count][1].rstrip())
                self.current_correct_answer = self.checklist[self.recite_count][1].rstrip()
                self.current_word = self.checklist[self.recite_count][0]
            else:
                # print(random.choice(fulllist)[1].replace("\n", "  "), end='\n')
                current_wordlist.append(random.choice(self.fulllist)[1].rstrip())

        self.label1.setText(self.checklist[self.recite_count][0])
        self.button1.setText(current_wordlist[0])
        self.button2.setText(current_wordlist[1])
        self.button3.setText(current_wordlist[2])
        self.button4.setText(current_wordlist[3])


    # 定义槽函数，用于改变字符串
    def Myupdate(self):
        paste_str = pyperclip.paste()
        if self.last_paste_str != paste_str:  # 只有在有变化的时候才会改变
            self.last_paste_str = pyperclip.paste()
            #print(paste_str + " * " + last_paste_str)
            paste_str = paste_str.strip()  # 消除空格
            try:
                str, need = search.search(paste_str)  # 联网搜索 str为翻译,need为是否是考纲需要的s
                # 录入
                self.label.setText(str)
                if (need):
                    search.search_insert(paste_str, str, cur, conn)
            except Exception as e:
                #print("出错了")
                print(e)
            self.last_paste_str = pyperclip.paste()



if __name__ == '__main__':
    conn = sqlite3.connect('./wordbank.sqlite3')
    cur = conn.cursor()
    app = QApplication(sys.argv)
    demo = TabDemo()
    demo.show()
    sys.exit(app.exec_())