# S.T.4.W.A - StreamTwitter4WhatsApp
# Autor: Danilo
# Dt: 13/06/2014
 
# Import das libs que vamos utilizar
import tweepy
import json
import re
import os
import base64
######################################################
 
# Configuração da aplicação no dev.twitter.com
consumer_key = ''                                          
consumer_secret = '' 
access_token_key = ''
access_token_secret = '' 
######################################################
 
# Import das libs para usar yowsup
from Yowsup.connectionmanager import YowsupConnectionManager
from Examples.EchoClient import WhatsappEchoClient  
 
# Configuração do yowsup para envio
password = ""                                           #Password dada ao registrar o numero pelo yowsup.
password = base64.b64decode(bytes(password.encode('utf-8')))                        #Codificacao do Password para envio aos servidores do whatsApp.
username = ''                                                          #Numero de telefone para o inicio de secao
keepAlive= False                                                                    #Conexao persistente com o servidor.
######################################################
 
# Faz a autenticação com a conta no twitter através dos tokens que gerou
auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)
###################################################### 
 
# Cria a classe para fazer o stream do twitter
class StreamListener(tweepy.StreamListener):
   
    # Pega o conteúdo do twitter, já em texto "puro"   
    def on_status(self, tweet):
        print 'Ran on_status'
    # Pega os erros ocorridos
    def on_error(self, status_code):
        print 'Error: ' + repr(status_code)
        return False
    # Pega data como vem do twitter em json
    def on_data(self, data):
        # Aqui eu usei o json para parsear o conteúdo vindo do twitter.
        decoded = json.loads(data)
        
        # Abaixo ? um print do que quero ver do arquivo em json que vem.
        # -----------------------------------------------------------
        # re.findall(r"#(\w+)", s) - essa parte do c?digo que pode ser encontrada
        # quase no fim do print me faz a separa??o de todas as hastags que contem no texto
        # que vem do twitter, existe no json as hastags, mas n?o consegui separar, fiz assim.
        # a linha "s = decoded['text'].encode('ascii', 'ignore')" pega o conte?do do texto e joga na variavel s
        s = decoded['text'].encode('ascii', 'ignore')
        print decoded['user']['screen_name'],"|",decoded['user']['location'],"|",decoded['user']['verified'],"|",decoded['user']['followers_count'],"|",decoded['user']['friends_count'],"|",decoded['user']['favourites_count'],"|",decoded['user']['statuses_count'],"|",decoded['user']['created_at'],"|",decoded['created_at'].encode('ascii','ignore'),"|",decoded['user']['lang'],"|",re.findall(r"#(\w+)", s),"|",decoded['text'].encode('ascii', 'ignore')
       
####################################################################################################
        
        # Aqui ? o seguinte, eu tinha feito o envio atravez da "API" do yowsup mesmo
        # mas achei que ficou lento, para testar, basta tirar os coment?rios e ajustar
        # as configura??es l? em cima
        
        message = str('@%s: %s' % (decoded['user']['screen_name'],decoded['text'].encode('ascii', 'ignore')))
        wa = WhatsappEchoClient("", message, keepAlive)
        wa.login(username, password)
####################################################################################################
 
        # Achei mais simples e r?pido usar uma chamada na linha de comando com a mensagem.
        # os.system("python yowsup-cli -c chip3.config -s 5511922223333 '@%s: %s'" % (decoded['user']['screen_name'],decoded['text'].encode('ascii', 'ignore')))
 
l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l)
# Termos, palavras, hashtags utilizadas para a monitoração, s?o elas que estou monitorando e jogando no whatsapp.
setTerms = ['#OpMundial2014', '#OpHackingCup', 'anonymous','#naovaitercopa','Word Cup']
streamer.filter(track = setTerms)
