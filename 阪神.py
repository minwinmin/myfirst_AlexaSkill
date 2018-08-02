# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 22:20:17 2018

@author: spase
"""

import urllib.request
from bs4 import BeautifulSoup
import random

def build_speechlet_response(output):
    return{
            'outputSpeech':{
                    'type':'PlainText',
                    'text': output
                    },
            'card':{
                    'type': 'Simple',
                    'title':'虎速報',
                    'content': output
                    },
            'reprompt':{
                    'outputSpeech':{
                         'type':'PlainText',
                         'text': None
                            }
                    },
            'shouldEndSession': True
            }

def build_response(speechlet_response):
     return{
             'version':'1.0',
             'sessionAttributes':{},
             'response': speechlet_response
             }

def get_hanshin_result():
    html = urllib.request.urlopen('https://baseball.yahoo.co.jp/npb/schedule/').read()
    soup = BeautifulSoup(html, 'html.parser')
    
    if soup.find(class_= "yjMS", text = '阪神') == None:
        speech_output = "今日は試合ないですよ"
        return build_response(build_speechlet_response(speech_output))
    else:
        table = soup.find(class_="yjMS", text="阪神").parent.parent

#リスト型として、yjMSが抜き出されている
#.select はcssセレクタを指定して抜き出せる
#.a.string
#a tagの文字を取り出す意味
#cssの指定の仕方、前に.を付ける意味を考えればおのずとわかる
# https://torina.top/detail/266/
    team_a = table.select('.yjMS')[0].a.string
    team_b = table.select('.yjMS')[1].a.string
    
    team_a_score = table.select('.score_r')[0].string
    team_b_score = table.select('.score_r')[1].string
    
    game_status = table.select('.yjMSt')[0].string
    
    if game_status == '結果':
        lead_text = '試合終了'
    elif game_status == '中止':
        lead_text = '試合は' + game_status + 'になりました'
    else:
        lead_text = '現在' + game_status + 'です'
    
    if game_status == '試合前' or game_status == '中止':
        speech_output = lead_text
    elif team_a == '阪神' and int(team_a_score) > int(team_b_score):
        speech_output = lead_text + "阪神は" + team_a_score + "対" + team_b_score + "で勝っています"
    elif team_b == "阪神" and int(team_b_score) > int(team_a_score):
        speech_output = lead_text + "阪神は" + team_b_score + "対" + team_a_score + "で勝っています" 
        #先攻後攻でも判断できるようになているはず
        
    return build_response(build_speechlet_response(speech_output))

def handle_session_end_request():
    speech_output = 'Bye'
    return build_response(build_speechlet_response(speech_output))

def on_launch(launch_request):
    return get_hanshin_result()

def on_intent(intent_request):
    intent_name = intent_request['intent']['name']
    
    if intent_name == 'ResultIntent':
        return get_hanshin_result()
    elif intent_name == 'AMAZON.HelpIntent':
        return get_hanshin_result()
    elif intent_name == 'AMAZON,CancelIntent' or intent_name == 'AMAZON.StopIntent':
        return handle_session_end_request()
    else:
        raise ValueError('Invalid intent')
    
def lambda_handler(event,context):
    if event['request']['type'] == 'LaunchRequest':
        return on_launch(event['request'])
    elif event['request']['type'] == 'IntentRequest':
        return on_intent(event['request'])
    elif event['request']['type'] == 'SessionEndedRequest':
        return on_session_ended(event['request'])
    
    
    
    
    
    
    
    
    
    
    
    
    
    


     
     
     
     