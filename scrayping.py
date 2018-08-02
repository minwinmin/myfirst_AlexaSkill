# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 09:18:46 2018

@author: spase
"""

from __future__ import print_function
import urllib.request
from datetime import datetime as dt
from bs4 import BeautifulSoup


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def results_order():

    #日付を調べる
    tdatatime = dt.now()
    tstr = tdatatime.strftime('%Y%m%d')

    #URLの文字列の後ろ　%Y%m%d(日付)＋05(チームナンバー：5で阪神を示す)
    f = urllib.request.urlopen("https://baseball.yahoo.co.jp/npb/game/2018031805/text").read()
    soup = BeautifulSoup(f,"html.parser")
    #https://qiita.com/itkr/items/513318a9b5b92bd56185

    da1s = soup.div.find_all("div", class_= "item T clearfix")
    #soup.find().textで文章だけを表示
    #http://yanomekeita.com/%E3%80%90python%E5%85%A5%E9%96%80%E3%80%91beautiful-soup%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%88%E3%81%86/
    #class_でclassを抜き出す
    #da1sは配列　print(da1s[0].text)

    #textだけで表示するにはdor文で回せばよい
    #for da1 in da1s:
    #   print(da1.text)
    #   print('-------------------------')
    
    return (da1s[0].text)
    
def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = results_order()

    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def handle_session_end_request():
    card_title = "実況終了"
    speech_output = "阪神最強"
    
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
def baseball_results(intent, session):
    session_attributes = {}
    reprompt_text = None

    speech_output = results_order()
    should_end_session = True
    
    return build_response(session_attributes, build_speechlet_response(
           intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "HanshinTigers":
        return baseball_results(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
