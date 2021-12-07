# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 00:45:24 2021

@author: Administrator
"""

# import 爬蟲所需要的東西
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import os,sys,time
from PIL import Image
from urllib import request
import requests
import json

# 實作　Node 單位
import unittest
class Node:
    #建構子，初始化節點
    #初始authority跟 hub,值皆為1
    def __init__(self, ID): #一定會有self這個值，並用self代稱上面的class_name(Node)
        self.ID = ID
        self.children = []  #初始的children 跟 parents串列裡面都是空的。(因為都沒有建立任何連結)
        self.parents = []
        self.auth = 1.0
        self.hub = 1.0
        
    def show(self): #所有的function裡面都要有self，代指使用自己方法的本身。
        print(f"This's {self.ID}")
        
    #link_child 跟 link_parent，為網站間的有向連結，但其並沒有考慮到各child節點或各parent節點之間加入到"children"或"parent"串列的先後順序。
    #只能計算此節點所有連出的節點個數計算。
        
    def link_child(self,new_child): #這Method中有兩個參數，self如上述，"new child" 為其他的Node類物件，近來這個城市的代稱為"new_child"
        for child in self.children: #在呼叫Method link_child的 Node 中，依序搜尋children 串列。
            if(new_child.ID == child.ID): #若已經有了，回傳None
                print("duplicate") #若有重複印出"duplicate"
                return None
        self.children.append(new_child)
        
    def link_parent(self,new_parent): #同上
        for parent in self.parents:
            if (new_parent.ID == self.ID):
                print("duplicate")
                return None
        self.parents.append(new_parent)
        
    def show_children(self): #印出一個節點的所有孩子(印出這個node所有連出的連結)
        if len(self.children) == 0:
            print("this node :",self.ID,", children_list is empty.")
        else:
            for i in range(len(self.children)):
                print(self.children[i].ID)
        
    def show_parents(self): #印出一個節點的所有parent(印出這個node所有連入的連結)
        for i in range(len(self.parents)):
            print(self.parents[i].ID)
            
    def update_hub(self):  #更新此點的hub分數
        hub_score = 1
        for i in self.children:
            hub_score += i.hub
        return hub_score
    
    def update_auth(self):   #更新此點的authority分數
        authority_score = 0
        for i in self.parents:
            authority_score += i.auth
        return authority_score
    
    def show_indegree(self):  #算出所有此點的 in_degree
        pass
    
    def show_outdegree(self):  #算出所有此點的 out_degree
        pass
    
    def normalize_hub_score(self):   #將此點的hub分數除以全部的hub分數總合
        pass
    
    def normalize_authority_socre(self):   #將此點的authority分數除已全部的authority分數總合。
        pass
    
#實作 Graph

class Graph:   #在這個網絡上(圖)的所有網站(點)集合
    def _init_(self, G_name):
        self.name = G_name  #圖的名字
        self.nodes = [] #一開始的nodes集合為空
        self.edges = [] #所有的邊集合我也設一個串列存起來，但這邊我目前還沒有想到怎麼加入可以加入有向邊。
    
    def insert_node(self, node):  #將外來的點加入這個圖的點集合中
        pass
    
    def display_hub_authority_score(self):
        pass
    

# 將所有 ID 一樣的都刪除。
def set_node_list(list_a):
    # 比較所有的ID名稱，先用for迴圈將所有的ID名稱存起來。
    all_name = [] #所有名字的列表
    for i in list_a:
        all_name.append(i.ID)
    all_name_count = [] #計算每個網站重複的數量
    for index,i in enumerate(list_a):  #對每個list_a 的元素做檢查
        count = 0
        for k in all_name: # 在所有的名字中搜尋，如果有一樣的名字，count就加一。
            if i.ID == k:
                count +=1
        all_name_count.append(count)
    for index,i in enumerate(all_name_count):  #超過一次以上的就刪除
        if i > 1:
            del list_a[index]
            del all_name[index]
            del all_name_count[index]
    return list_a                   #回傳一list 其為不重複的 node版本


def search_all_link(query_link):
    a = []  # 這個網站所有的 outlink
    html = requests.get(query_link, timeout = 10)
    # 為防止爬蟲卡死情況(request 不會自行斷開)，故上面設置 timeout 參數，設定固定時間若未完成則 斷開連結。
    html.encoding = 'UTF-8' #使用html編碼。
    sp = BeautifulSoup(html.text, 'html5lib') #指定'html5lib'作為解析器
    #若只使用sp.link 則只會找出第一筆
    #故這邊要使用"find.all"語法
    link_search = sp.find_all("a") #找出所有的 <a> (超連結)
    for i in range(len(link_search)):
        k = str(link_search[i].get("href"))  #這行一定要記得要轉type！！！轉成str不然有時候會無法切片取值。
        if k[0:5] == "https": #只留下"https"
            a.append(k)
    return a  #回傳一列網址(type list)

#先將所有node_list中的資料轉換成type str存入到list再寫入檔案
def node_to_text(all_node_list):
    node_list_txt = [] # node_list 的所有內容
    for i in all_node_list:
        tmp_list = [] # 初始化
        # 依序記錄結構化的node的每個資料
        tmp_list.append(i.ID)
        # 這邊嘗試寫遞迴函式，不停往下找
        # 加入parents
        tmp_parents = []
        for k in i.parents:
            tmp_parents.append(k.ID)
        tmp_list.append(tmp_parents)
        # 加入cildren
        tmp_children = []
        for j in i.children:
            tmp_children.append(j.ID)
        tmp_list.append(tmp_children)
        
        # 先加入parents
        # 再加入children
        
        tmp_list.append(i.auth)
        tmp_list.append(i.hub)
        # 再加入list
        node_list_txt.append(tmp_list)
    return node_list_txt  # 回傳一個 list

path = "url_list.txt"
f = open(path, "r")
level_0 = f.readlines()
for i in range(len(level_0)):
    level_0[i] = level_0[i][:-1]
level_0

# 建立一所有網站之list。
all_https_url = [] #list型態。
node_list = [] #所有網站列表(Node版)

# 這邊應該要在所有網站中做搜尋，若outlink中新的網站才需要加入。若重複則不需要加入 all_https_url。 另外需要建立每一層增加的 link 的紀錄。
# 也就是說，一開始都是加入node的outlink(children)。
import time

level_1 = []  # 第一層中新增的 link 

for i in range(len(level_0)): #此迴圈為對每個url_list中的網址找尋其out_link 使用range方法   # len(url_list)
    try:
        if level_0[i] in all_https_url:  # 如果重複就不加
            continue
        else:
            all_https_url.append(level_0[i]) # 如果沒有重複，就加入其之 url
            tmp_1 = Node(level_0[i]) #原生網址轉成node
            #node_list.append(tmp_1)
            time.sleep(1)
            k = search_all_link(level_0[i]) # 搜尋這個網址所有的out_link (type(list))
            for url in k: #對每個out_link
                # 先找尋此網址是不是在所有網址內出現過。若有出現相同的就不加入搜尋。
                if url in all_https_url:
                    print("url 重複")
                    continue  # 一樣的就不需加入。
                else:
                    tmp_2 = Node(url) #找到的不重複的網址。
                    # node_list.append(tmp_2) # 加入nodelist中
                    # tmp_1.link_child(tmp_2)
                    level_1.append(tmp_2.ID) # level_1為第一層所有的不重複的url
                    all_https_url.append(tmp_2.ID)
            # 再將所有的 level_1 加入 all_https_url
            # 整理出新的 all_https_url
    except Exception as e:
        print(i)
        print(f"error = {e}")
        continue


# 檢查第一層
print(len(level_1))
print(level_1)

# 這邊應該要在所有網站中做搜尋，若outlink中新的網站才需要加入。若重複則不需要加入 all_https_url。 另外需要建立每一層增加的 link 的紀錄。
# 也就是說，一開始都是加入node的outlink(children)。
import time

level_2 = []  # 第一層中新增的 link 

for i in range(len(level_1)): #此迴圈為對每個url_list中的網址找尋其out_link 使用range方法   # len(url_list)
    try:
        #if level_1[i] in all_https_url:  # 如果重複就不加
            #continue
        #else:
        #all_https_url.append(level_1[i]) # 如果沒有重複，就加入其之 url
        #tmp_1 = Node(level_1[i]) #原生網址轉成node
        #node_list.append(tmp_1) # 上面加過了
        time.sleep(1)
        k = search_all_link(level_1[i]) # 搜尋這個網址所有的out_link (type(list))
        for url in k: #對每個out_link
            # 先找尋此網址是不是在所有網址內出現過。若有出現相同的就不加入搜尋。
            if url in all_https_url:
                print("url 重複")
                continue  # 一樣的就不需加入。
            else:
                tmp_2 = Node(url) #找到的不重複的網址。
                # node_list.append(tmp_2) # 加入nodelist中
                # tmp_1.link_child(tmp_2) # 所有outlink
                level_2.append(tmp_2.ID) # level_2為第2層所有的不重複的url
                all_https_url.append(tmp_2.ID)
        # 再將所有的 level_1 加入 all_https_url
        # 整理出新的 all_https_url
    except Exception as e:
        print(i)
        print(f"error = {e}")
        continue

# 檢查第二層

print(len(level_2))
print(level_2)


#所有網站列表長度。
print(len(all_https_url))
for i in all_https_url:
    print(i)
    
# 第三層之後用迴圈找
# 迴圈停止條件，只要當數量增加到達一定程度(目前暫定小於10%)，就確定網路已經收斂，停止演算法。

level_tmp = level_2 # 初始化要先給定上一層level_2的值
counter = 2   # 記錄目前在做了幾層(因為第三層之後才用迴圈，所以目前記錄為第2層)

while True:
    upper_level = level_tmp # 給定值
    level_tmp = [] # 重置 level_tmp   # 暫存這一次迴圈所儲存的link (也就是這一層level所增加的所有link)
    for i in range(len(upper_level)): #對上一層找out_link
        try:
            #if level_1[i] in all_https_url:  # 如果重複就不加
                #continue
            #else:
            #all_https_url.append(level_1[i]) # 如果沒有重複，就加入其之 url
            #tmp_1 = Node(level_1[i]) #原生網址轉成node
            #node_list.append(tmp_1) # 上面加過了
            time.sleep(0.5)
            k = search_all_link(upper_level[i]) # 搜尋這個網址所有的out_link (type(list))
            for url in k: #對每個out_link
                # 先找尋此網址是不是在所有網址內出現過。若有出現相同的就不加入搜尋。
                if url in all_https_url:
                    print("url 重複")
                    continue  # 一樣的就不需加入。
                else:
                    tmp_2 = Node(url) #找到的不重複的網址。
                    # node_list.append(tmp_2) # 加入nodelist中
                    # tmp_1.link_child(tmp_2) # 所有outlink
                    level_tmp.append(tmp_2.ID) # level_tmp為第 n 層所有的不重複的url
                    all_https_url.append(tmp_2.ID)
            # 再將所有的 level_1 加入 all_https_url
            # 整理出新的 all_https_url
        except Exception as e:
            print(i)
            print(f"error = {e}")
            continue
    counter += 1 # 每次做完上述流程 LEVEL加一層
    # 檢查式所在地，如果每層增加數目小於之所增加數目之10% 那麼就停止演算法。
    if len(level_tmp) < len(upper_level)/10:
        print("第",counter,"層，網址長度收斂，增加數目為:",len(level_tmp),"上一層為:",len(upper_level))
        break

for i in all_https_url:
    node_list.append(Node(i)) #node化
    

# 問題：目前我的node_list(所有網站的node版)中可能會有重複的名稱，所以我要做處理，將名字變為唯一

# 利用上面已經宣告過的set_node_list()函式整理出唯一集合
# 這邊我先不做，因為我覺得 目前我 node_list 還不知道該如何刪除缺失值，鑒於一次演算法可能會跑非常久，所以先全部紀錄
# no_duplicate_node_list= set_node_list(node_list)

# 將所有的node記錄下來

node_list_txt = node_to_text(node_list) #所有的node 
node_list_txt


len(node_list)

import pandas as pd

df = pd.DataFrame(node_list_txt)
df.to_csv('node_list_txt.csv')