#coding: utf8 
'''
Copyright (c) <2012> Tarek Galal <tare2.galal@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR 
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import datetime, sys, base64
import tweepy

if sys.version_info >= (3, 0):
	raw_input = input

from Yowsup.connectionmanager import YowsupConnectionManager
from Examples.EchoClient import WhatsappEchoClient

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m' 

class WhatsappListenerClient:

	def __init__(self, keepAlive = False, sendReceipts = False):
		self.sendReceipts = sendReceipts

		connectionManager = YowsupConnectionManager()
		connectionManager.setAutoPong(keepAlive)

		self.signalsInterface = connectionManager.getSignalsInterface()
		self.methodsInterface = connectionManager.getMethodsInterface()

		self.signalsInterface.registerListener("message_received", self.onMessageReceived)
		self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
		self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
		self.signalsInterface.registerListener("disconnected", self.onDisconnected)

		self.cm = connectionManager

	def login(self, username, password):
		self.username = username
		self.methodsInterface.call("auth_login", (username, password))


		while True:
			raw_input()	

	def onAuthSuccess(self, username):
		print("Authed %s" % username)
		self.methodsInterface.call("ready")

	def onAuthFailed(self, username, err):
		print("Auth Failed!")

	def onDisconnected(self, reason):
		print("Disconnected because %s" %reason)	

	def onMessageReceived(self, messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadCast):
		formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
		#print("%s [%s]:%s"%(jid, formattedDate, messageContent))
		configs=[]
		try:
			f = open("Examples/configPesquisa.conf","r")
			for linha in f:
				configs += [linha.rstrip()]
			f.close()
		except IOError:
			print bcolors.WARNING + "\nO arquivo que voce tentou carregar nao existe ou foi digitado incorretamente!\n" + bcolors.ENDC
		# Configura??o do yowsup para envio - Aconselho usar um numero diferente do st4wa para nao travar :)
		###########################
		password = configs[1].split(";")				#Password dada ao registrar o numero pelo yowsup.
		password = str.format(password[1])
		password = base64.b64decode(bytes(password.encode('utf-8')))	#Codificacao do Password para envio aos servidores do whatsApp.
		username = configs[0].split(";")
		username = username[1]						#Numero de telefone para o inicio de secao
		keepAlive= False						#Conexao persistente com o servidor.
		#######################################################################################################
		consumer_key = configs[2].split(";")
		consumer_key = consumer_key[1]
                consumer_secret = configs[3].split(";")
		consumer_secret = consumer_secret[1]
		access_token_key = configs[4].split(";")
                access_token_key = access_token_key[1]
                access_token_secret = configs[5].split(";")
		access_token_secret = access_token_secret[1]

                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token_key, access_token_secret)
                api = tweepy.API(auth)

                try:
                        teste = messageContent.split(' ')
			i = 0
			for linha in teste:
				teste = teste[i]
				i += 1
				results = api.search(q=teste)
	                        for result in results:
					twit = result.text.encode('utf-8').strip()
					uTwit = result.user.screen_name
					mensagem = uTwit + ": " + twit
	                                whats = WhatsappEchoClient("", mensagem, keepAlive)
					whats.login(username, password)
                except IndexError, erro:
                        print '%s' % erro

		if wantsReceipt and self.sendReceipts:
			self.methodsInterface.call("message_ack", (jid, messageId))
