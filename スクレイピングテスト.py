# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 22:36:12 2018

@author: spase
"""

import urllib.request
from bs4 import BeautifulSoup
import random

lose_text_list = ["今日はいい天気ですね","横浜Fマリノスの結果をお調べですか？","他人を応援するより自分が頑張ったほうが楽しいですよ","大魔神は今、馬ぬしをやっているそうです"]

html = urllib.request.urlopen('https://baseball.yahoo.co.jp/npb/schedule/').read()
soup = BeautifulSoup(html, 'html.parser')


if soup.find(class_= "yjMS", text = '阪神') == None:
        speech_output = "今日は試合ないですよ"
        print(speech_output)
else:
        #阪神の情報部分を切り抜いている
        table = soup.find(class_="yjMS", text="阪神").parent.parent

#print(table)  

#td classの項が
team_a = table.select('.yjMS')

team_b = table.select('.yjMS')[1].a.string
    
#print(team_a)

game_status = table.select('.yjMSt')[0].string
 
print(game_status)



  