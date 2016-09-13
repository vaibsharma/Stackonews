#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from google import search
from bs4 import BeautifulSoup as BS 


# Create your views here.
API_KEY = "00ed9d0a7061428493500c5d9bfb223e"
PAGE_ACCESS_TOKEN = 'EAAIhB7QbAeEBAH0xBOZBSGX1mb0Gg0wMbiVZCEQuzAcXYgfpobDhgQ6EfK4pLwVoUn5vCfZCM6cCZCGgyOBjSGaBzNb6zDmVdZAaFx7ai2qCXmJswWw7tmxyUqnAyKCmw3Ga2dZCqTHyevArZA11dMuEI46xI3lRww3ZBHdoKOifoAZDZD'
VERIFY_TOKEN = "vaibhavsharma"


GREETINGS = {"name":1,"nice":0,"ok":0,"thank":0,"how are you":2,"fine":3,"talk":4,"hi":5,"hey":5,"hello":5,"afternoon":6,"morning":7,"night":8,"hafiz":9,"doing":10,"pokemon":11,"are smart":12,"no":13}
reply=["My Pleasure My Master","My name is Stacko ! can answer all your tech question.","I am Fine my master. How are you ?","Okkay! if you need any help you just need to drop a message my master \n Khuda Hafiz! :)","Master you will only ask me tech questions","Hi :)","Good afternoon! My master :)","Good morning! My master","Good night! My master :)","khuda hafiz :)",">Sitting>Eating\n>Staring at the laptop screen\n>Typing\n>Breathing\n>Blinking\n>Thinking\nLol\nHow about you? ;) ","This might help you ! Made by my master :) http://enigmatic-basin-68757.herokuapp.com just give it a try . ","Thank you master ! this made my day :)","okkay ! then ?"]
news_category = {'bollywood':'entertainment','film ':'entertainment','business':'buisness','market n':'buisness', 'entertainment':'entertainment', 'gam':'gaming', 'general new':'general','normal n':'general', 'science-and-nature':'science-and-nature','science':'science-and-nature','nature':'science-and-nature', 'sport':'sports','play':'sports', 'technology':'technology','gadgets':'technology','mobile':'technology'}

def post_facebook_message(fbid, received_message):
	print "fbid" , fbid
	if len(received_message) > 300 :
		received_message = received_message[:300]
	print received_message

	try:
		user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
		user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
		print "getting user details"
		user_details = requests.get(user_details_url, user_details_params).json()
		print "Using GET request"
		print "User details" , user_details
		answer = 'Best Answer for '+user_details['first_name']+' my Master! :'
		print answer
	except:
		print "Exception case for userdetails"
		answer = "Best Answer for my Master :"
		print answer

	print "makig a post url "
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    
	response_msg1 = json.dumps(
        {"recipient":{"id":fbid}, 
            "message":{
                "text": received_message
            }
     })
	try :
		print "Making A post request"
		status1 = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg1)
		pprint(status1.json())
	except:
		print "Post request Not working"	
	
	
	
		


class fb(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:

			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		for entry in incoming_message['entry']:
		 	for message in entry['messaging']:
		 		if 'message' in message:
		 			pprint(message)
		 			try:
		 				chat(message['sender']['id'], message['message']['text'])
		 			except:
		 				print "Message not send"
		 				pass
		return HttpResponse()


def chat(fbid,message):
	flag = 1 
	for name in GREETINGS.keys():
		if name in message.lower() :
			flag = 0
			post_facebook_message(fbid,reply[GREETINGS[name]])
			return

	if 'news' in message :
		news(fbid,message)
		return 

	if flag == 1 :
		soverflowurl = "http://stackoverflow.com"
		for url in search(message.encode('utf8')):
			flag = flag + 1
			if flag > 10 :
				break
			print url
			if "http://stackoverflow.com/" in url:
				print "entered"
				soverflowurl = url
			else :
				continue	

		try:
			print "Trying Stackoverflow URL"
			r = requests.get(soverflowurl).text
			page = BS(r,"html.parser")
			answer = page.find_all("div",class_ = "accepted-answer")
			answer = answer[0].find_all("div",class_ = "post-text")
			print "Post request made"
			post_facebook_message(fbid,answer[0].text)
			print answer[0].text
		except IndexError:
			try:
				print "Index error"
				r = requests.get(soverflowurl).text
				page = BS(r,"html.parser")
				answer = page.find_all("div",id="answers")
				answer = answer[0].find_all("div",class_="answer")
				answer = answer[0].find_all("div",class_="post-text")
				print "index error post request made"
				post_facebook_message(fbid,answer[0].text)
				print answer[0].text
			except:
				print "Extreme exception"
				post_facebook_message(fbid,"Try giving me the exact problem! My master!")	

def news(fbid,message):
	print "ENTER in THE NEWS FUNCTION\n"
	for category in news_category.keys():
		if category in message :
			flag = 0
			try :
				print "Getting inside the try of news"
				result = requests.get("https://newsapi.org/v1/sources?source=techcrunch&language=en&apikey="+API_KEY).json()
				categ = news_category[category]
				print categ
				news_result = result['sources']
				for xa in news_result:
					if xa['category'] == categ :
						print xa['description']
						if len(xa['description']) == 0:
							try :
								post_facebook_message(fbid,"Sorry!   which news category you want (please mention it with the suffix news) Thank you!")

							except:
								print "No response"	
							return

						print "Checking all the inputs"	
						print xa['description'],xa['country'],xa['urlsToLogos']['medium'],xa['category'],xa['url']	
						post_facebook_template_message(fbid,xa['description'],xa['country'],xa['urlsToLogos']['medium'],xa['category'],xa['url'])
						return
			except :
				print "template not send"
				try:
					post_facebook_message(fbid,"Sorry! which news category you want (please mention it with the suffix news) Thank you!")
				except :
					print "%s%s%s" %('*'*10+'\n',"Could not connect with the news API\n","'*'*10+'\n'")
			return 

	if flag == 1:
		try :
			post_facebook_message(fbid,"Please try giving me the news category")
		except:
			print "%s%s%s" %('*'*10+'\n',"Could not connect with the news API\n","'*'*10+'\n'")

def post_facebook_template_message(fbid,description,country,logo,category,urls):

	print "*************** post_facebbok_template_message() ***********"

	response_msg1 = json.dumps(
        {"recipient":{"id":fbid}, 
            "message":{
            "attachment":{
            "type":"template",
            "payload":{
            "template_type":"generic",
            "elements":[
            	{
            		"title":category.decode('utf-8'),
           			"item_url":urls.decode('utf-8'),
            		"image_url":logo.decode('utf-8'),
            		"subtitle":description.decode('utf-8')[:250],
            		"buttons":[
                 	{
                    	"type":"web_url",
                    	"url":urls.decode('utf-8'),
           	 			"title":"View Website"
                 	}             
       				]
          		}
        	]
      	}
    }
  }
})
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	try :
		print "**********\n TRYING NEWS TEMPLATE ***********\n"
		status1 = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg1)
		pprint(status1.json())
	except :
		print "NEWS TEMPLATE FAILED"
		try :
			print "POSTING DESCRIPTION NOT TEMPLATE"
			post_facebook_message(fbid,description)
		except :
			print "NOTHING HAS WORKED OUT"
			print "%s%s%s" %('*'*10+'\n',"Message was not send!",'*'*10+'\n')

def videos(fbid,url="https://www.youtube.com/v/ej3ebj3F"):
	print "************\nEntered inside the videos\n************"
	url = url +"\n"
	url = url.decode('utf-8')
	p = re.compile(ur'^https:\/\/www.youtube.com\/watch\?(?P<digit>\w+)=(?P<first_name>[0-9a-zA-Z]+)$')
	result = re.search(p, url)
	newURL = "https://www.youtube.com/"+str(result.group('digit').decode('utf-8'))+"/"+str(result.group('first_name').decode('utf-8'))
	print newURL
	response_msg1 = json.dumps(
        {"recipient":{"id":fbid}, 
            "message":{
    "attachment":{
      "type":"video",
      "payload":{
        "url":newURL}
    }
  }
})
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	try :
		print "trying video message"
		status1 = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg1)
		pprint(status1.json())
	except :
		try :
			print "************ VIDEO WAS NOT SEND ************"
			post_facebook_message(fbid,"Please brief your choice!")
		except :
			print "EVERYTHING HAS FAILED MESSAGE WAS NOT SEND"
			print "%s%s%s" %('*'*10+'\n',"Message was not send!",'*'*10+'\n')

