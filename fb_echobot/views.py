#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, requests, random, re
from pprint import pprint
from config import API_KEY, PAGE_ACCESS_TOKEN,VERIFY_TOKEN
from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from google import search
from bs4 import BeautifulSoup as BS 


# Create your views here.
GREETINGS = {"name":1,"nice":0,"ok":0,"thank":0,"how are you":2,"fine ":3," talk":4,"hi":1,"hey":1,"hello":1,"afternoon":6,"morning":7,"night":8,"hafiz":9,"doing":10,"pokemon":11,"are smart":12,"no":13}
reply=["My Pleasure My Master","Hi :) , My name is Stacko ! can answer all your tech question.","I am Fine my master. How are you ?","Okkay! if you need any help you just need to drop a message my master \n Khuda Hafiz! :)","Master you will only ask me tech questions","Hi :)","Good afternoon! My master :)","Good morning! My master","Good night! My master :)","khuda hafiz :)",">Sitting>Eating\n>Staring at the laptop screen\n>Typing\n>Breathing\n>Blinking\n>Thinking\nLol\nHow about you? ;) ","This might help you ! Made by my master :) http://enigmatic-basin-68757.herokuapp.com just give it a try . ","Thank you master ! this made my day :)","okkay ! then ?"]
news_category = {'bollywood':'entertainment','film ':'entertainment','business':'buisness','market n':'buisness', 'entertainment':'entertainment', 'gam':'gaming', 'general new':'general','normal n':'general', 'science-and-nature':'science-and-nature','science':'science-and-nature','nature':'science-and-nature', 'sport':'sports','play':'sports', 'technology':'technology','gadgets':'technology','mobile':'technology'}

def post_facebook_message(fbid, received_message):
	logg("@","fbid" + fbid ,"-27-")
	if len(received_message) > 300 :
		msg_length = len(received_message)/300
		start = 0
		while msg_length >=0 :
			try:
				post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
				if msg_length is not 0 :
					response_msg1 = json.dumps(
        {"recipient":{"id":fbid}, 
            "message":{
                "text": received_message[start:start+300]
            }
     })
				else :
					response_msg1 = json.dumps(
        {"recipient":{"id":fbid}, 
            "message":{
                "text": received_message[start:]
            }
     })
				status1 = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg1)
				pprint(status1.json())	


			except:
				logg("&","Post request Not working","-53-")

			start = start + 300
			msg_length = msg_length -1
			print received_message
	else:
		try:
			response_msg1 = json.dumps(
        {"recipient":{"id":fbid}, 
            "message":{
                "text": received_message
            }
     })
			post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
			
			status1 = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg1)
			pprint(status1.json())

		except:
			logg("@","RESPONSE NOT SEND","-72-")

class fb(generic.View):
	def get(self, request, *args, **kwargs):
		logg("$"," ","-71-")
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			logg("$"," ","-73-")
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			logg("$"," ","-76-")
			return HttpResponse('Error, invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		logg("$"," ","-85-")
		pprint(incoming_message)
		for entry in incoming_message['entry']:
		 	for message in entry['messaging']:
		 		if 'message' in message:
		 			pprint(message)
		 			try:
		 				logg("$","Calling from post ","-91-")
		 				chat(message['sender']['id'], message['message']['text'])
		 			except:
		 				logg("#","Message not send","-95-")
		 				pass
		 		elif 'postback' in message:
		 			pprint(message["postback"])
		 			try:
		 				logg("@","Postback","-100-")
		 				check(message['sender']['id'],message['postback']['payload'])
		 			except:
		 				logg("#","Postback was not handled","-103-")
		 				pass
		return HttpResponse()


def chat(fbid,message):
	logg("!",message,"-109-")
	flag = 1 
	for name in GREETINGS.keys():
		logg("!",name,"-112-")
		if name in message.lower() :
			flag = 0
			try:
				post_facebook_message(fbid,reply[GREETINGS[name]])
			except:
				logg("!","message not send","-118-")	
			response1 = json.dumps({
			  "recipient":{
			    "id":fbid
			},
			"message":{
			"attachment":{
			"type":"template",
			"payload":{
			"template_type":"button",
			"text":"Please select your query :-",
			"buttons":[
			{
				"type":"postback",
				"title":"Stackoverflow",
				"payload":"Stack"
				},
				{
				"type":"postback",
				"title":"News ",
				"payload":"News"
				}
				]
			}
			}
			}
			})
			logg("!","Check this line","-142-")
			
			post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
			try :
				logg("*","TRYING NEWS TEMPLATE","-142-")
				status1 = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response1)
				pprint(status1.json())
				return
			except :
				logg("!","Template failed","-146-")

		

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
				logg("#"," ","-120-")
				soverflowurl = url
			else :
				continue	

		try:
			logg("$","Trying Stackoverflow URL","-126-")
			r = requests.get(soverflowurl).text
			page = BS(r,"html.parser")
			answer = page.find_all("div",class_ = "accepted-answer")
			answer = answer[0].find_all("div",class_ = "post-text")
			logg("!","Post request made","-131")
			post_facebook_message(fbid,answer[0].text)
			logg("@",answer[0].text,"-133-")
			return
		except IndexError:
			try:
				logg("@","Index error","-137-")
				r = requests.get(soverflowurl).text
				page = BS(r,"html.parser")
				answer = page.find_all("div",id="answers")
				answer = answer[0].find_all("div",class_="answer")
				answer = answer[0].find_all("div",class_="post-text")
				logg("#","index error post request made","-143-")
				post_facebook_message(fbid,answer[0].text)
				logg("$",answer[0].text ,"-145-")
				return
			except:
				log("$","Extreme exception","-148-")
				post_facebook_message(fbid,"Try giving me the exact problem! My master!")
				return	

def news(fbid,message):
	print "ENTER in THE NEWS FUNCTION\n"
	for category in news_category.keys():
		if category in message :
			flag = 0
			try :
				logg("$","News Funtion","-158-")
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

						logg("%","Checking all the Inputs:","-174-")	
						logg("%",xa['description'] +"\t" + xa['country'] +"\t"+ xa['urlsToLogos']['medium'] +"\t" +xa['category'] +"\t" +xa['url'] ,"-175")
						post_facebook_template_message(fbid,xa['description'],xa['country'],xa['urlsToLogos']['medium'],xa['category'],xa['url'])
						return
			except :
				logg("&","Template not send:","-179-")
				try:
					post_facebook_message(fbid,"Sorry! which news category you want (please mention it with the suffix news) Thank you!")
				except :
					logg("^","Could not connect with the news API:","-183-")
			return 

	if flag == 1:
		try :
			post_facebook_message(fbid,"Please try giving me the news category")
		except:
			logg("#","API is not working ! might be server's Problem:","-190-")

def post_facebook_template_message(fbid,description,country,logo,category,urls):
	logg("*","POST FACEBOOK TEMPLATE MESSAGE","-194-")
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
            "url":urls,
            "title":"Show Website"
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
		logg("*","TRYING NEWS TEMPLATE","-234-")
		status1 = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg1)
		pprint(status1.json())
	except :
		logg("!","Template failed","-228-")
		try :
			print "POSTING DESCRIPTION NOT TEMPLATE"
			post_facebook_message(fbid,description)
		except :
			logg("%","Template was not send","-23-")

def videos(fbid,url="https://www.youtube.com/v/ej3ebj3F"):
	logg("*","Video Section :"," -237-")
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
		logg("%","Trying video message :"," -256-")
		status1 = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg1)
		pprint(status1.json())
	except :
		try :
			logg("^","Video was not send :"," -261-")
			post_facebook_message(fbid,"Please brief your choice!")
		except :
			logg("@","Message was not send :," , "-265-")

def logg(symbol,text,lineno):
	print symbol*10 + "\n" + "\t" + text + "\n" + symbol*10 +"\n"+ "\t" + lineno*3 +"\n"

def index():
	chat("121836821328213","hi")

def check(fbid,payload):
	logg("@","Checking news function","-313-")
	if payload == "Stack":
		logg("!","Checking Stack Payload","-315-")
		try:
			logg("!","check this line","-317-")
			message = "Please ask question ?"
		except:
			logg("^","Message failed","-317-")	
	if payload == "News":
		logg("@","Checking news payload","-322-")
		try:
			logg("#","^^chhecing line ","-324-")
			message = "Please type ' country-name and category' ?"
		except:
			print "NO changes done"
	if payload == "Go_Back" :
		try:
			chat(fbid,"hi")
		except:
			logg("@","Please check the line ","-327-")
		return
	response1 = json.dumps({
		"recipient":{
		"id":fbid
		},
		"message":{
		"attachment":{
		"type":"template",
			"payload":{
			"template_type":"button",
			"text": "Please choose your option : " ,
			"buttons":[
			{
				"type":"postback",
				"title":"Wanna go back ?",
				"payload": "Go_Back"
				},
				{
				"type":"postback",
				"title":message,
				"payload": message
				}

			]
			}
		}
	}
})
	logg("!","response is ready ","-361-")
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	try :
		logg("%","Trying function :"," -352-")
		status1 = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response1)
		pprint(status1.json())
	except :
		try :
			logg("^","Check this line :"," -357-")
			post_facebook_message(fbid,"Please brief your choice!")
		except :
			logg("@","Message was not send :," , "-360-")



def blog(request):
	print "requested accepted"
	if request.method == "POST":
		print "posting"
		name = request.POST.get("name") or " "
		print name
		mail_id = request.POST.get("mail_id") or " "
		print mail_id
		phone_number = request.POST.get("phone_number") or " "
		print phone_number
		message = request.POST.get("message") or " "
		print message
		send_message ="Name : "+name+"\nMail-id :"+mail_id+"\nphone-number :"+phone_number+"\nmessage : "+message+"\n."
		print send_message
		try:
			chat("1446850468665078",message)
			print "Successful"
			return HttpResponse()
		except:
			print "failed"
			return HttpResponse()

	print "failed"		
	return HttpResponse()

def main(request):
	return render(request,"fb_echobot/account.html",{"data":None})

def index(request):
	if request.method =='POST':
		return render(request,"fb_echobot/base.html",{"data":[None]})
	return render(request,"fb_echobot/base.html",{"data":[None]})
