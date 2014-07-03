# S.T.4.W.A - StreamTwitter4WhatsApp
# Autor: Danilo Vaz
# Email: danilovazb@gmail.com
# Dt: 13/06/2014

#############################################################################
# Atualizacao:                                                              #
# Data: 01/07/2014                                                          #
# - Add menu para facilitar                                                 #
# - Add funcao de importar tags de pesquisa via arquivo (Ideia do @l0ganbr) #
#                                                                           #
# Data: 03/07/2014                                                          #
# - Add server de pesquisa, onde enviada as tags de pesquisa via whatsapp   #
# ele retorna a pesquisa do conteudo tanto via whatsapp ou por e-mail       #
#############################################################################
 
# Import das libs que vamos utilizar
import tweepy
import json
import re
import os
import base64
import sys
######################################################
 
# Configura??o da aplica??o no dev.twitter.com
consumer_key = ''                                          
consumer_secret = '' 
access_token_key = ''
access_token_secret = '' 
######################################################

# Import das libs para usar yowsup
from Yowsup.connectionmanager import YowsupConnectionManager
from Examples.EchoClient import WhatsappEchoClient
from Examples.ListenerClient import WhatsappListenerClient
from Examples.ListenerClientEmail import WhatsappListenerClientEmail

# Configura??o do yowsup para envio
password = ""                                           #Password dada ao registrar o numero pelo yowsup.
password = base64.b64decode(bytes(password.encode('utf-8')))                        #Codificacao do Password para envio aos servidores do whatsApp.
username = ''                                                          #Numero de telefone para o inicio de secao
keepAlive= False                                                                    #Conexao persistente com o servidor.
######################################################

# Faz a autentica??o com a conta no twitter atrav?s dos tokens que gerou
auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)
###################################################### 

# Classe de viadagens :) 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m' 
 
# Cria a classe para fazer o stream do twitter
class StreamListener(tweepy.StreamListener):
   
    # Pega o conte?do do twitter, j? em texto "puro"   
    def on_status(self, tweet):
        print 'Ran on_status'
    # Pega os erros ocorridos
    def on_error(self, status_code):
        print 'Error: ' + repr(status_code)
        return False
    # Pega data como vem do twitter em json
    def on_data(self, data):
        # Aqui eu usei o json para parsear o conte?do vindo do twitter.
        decoded = json.loads(data)
        
        # Abaixo ? um print do que quero ver do arquivo em json que vem.
        # -----------------------------------------------------------
        # re.findall(r"#(\w+)", s) - essa parte do c?digo que pode ser encontrada
        # quase no fim do print me faz a separa??o de todas as hastags que contem no texto
        # que vem do twitter, existe no json as hastags, mas n?o consegui separar, fiz assim.
        # a linha "s = decoded['text'].encode('ascii', 'ignore')" pega o conte?do do texto e joga na variavel s
        s = decoded['text'].encode('ascii', 'ignore')
        print decoded['user']['screen_name'],"|",decoded['user']['location'],"|",decoded['user']['verified'],"|",decoded['user']['followers_count'],"|",decoded['user']['friends_count'],"|",decoded['user']['favourites_count'],"|",decoded['user']['statuses_count'],"|",decoded['user']['created_at'],"|",decoded['created_at'].encode('ascii','ignore'),"|",decoded['user']['lang'],"|",re.findall(r"#(\w+)", s),"|",decoded['text'].encode('ascii', 'ignore')
        # Aqui ? o seguinte, eu tinha feito o envio atravez da "API" do yowsup mesmo
        # mas achei que ficou lento, para testar, basta tirar os coment?rios e ajustar
        # as configura??es l? em cima
        
        message = str('@%s: %s' % (decoded['user']['screen_name'],decoded['text'].encode('ascii', 'ignore')))
        wa = WhatsappEchoClient(telefone, message, keepAlive)
        wa.login(username, password)

ans=True
while ans:
    sys.exc_clear
    print( bcolors.OKBLUE + '''
                                                                                          
                                                                                
                                               .,=== .                          
                                           .????????????.       .?.             
              ,?.                         I???????????????~ ~????.              
             .????.                     .???????????????????????.               
             .?????:                   .??????????????????????,. I?.            
             ~???????                  ???????????????????????????.             
             .??????????.              ?????????????????????????.               
             .????????????+.          .???????????????????????+.                
              ,???????????????+       .???????????????????????.                 
               =????????????????????II????????????????????????.                 
                +?????????????????????????????????????????????                  
             +??~.???????????????????????????????????????????I                  
              ?????? Autor: Danilo Vaz ?????????????????????~         _________________________  __      __  _____               
              ?????? Email: danilovazb[at]gmail[dot]com ????.        /   _____/\__    ___/  |  |/  \    /  \/  _  \              
              .??????????????????????????????????????????????        \_____  \   |    | /   |  |\   \/\/   /  /_\  \              
                ????????????????????????????????????????????.        /        \  |    |/    ^   /\        /    |    \             
                 :??????????????????????????????????????????        /_______  /  |____|\____   |  \__/\  /\____|__  /             
                   .???????????????????????????????????????.                \/              |__|       \/         \/              
                  ????????????????????????????????????????                                                 V 1.1 ;)
                  ???????????????????????????????????????                       
                   ?????????????????????????????????????.                       
                     ??????????????????????????????????.                        
                      .I??????????????????????????????.                         
                          . ????????????????????????+                           
                        .=?????????????????????????.                            
                     .~??????????????????????????                               
           ++~~+?I?????????????????????????????                                 
              I?????????????????????????????                                    
                . I?????????????????????,.                                      
                      . ~?II??II?= ..                                           
    
    1.Monitorar Palavras
    2.Monitorar Palavras por arquivo
    3.Server de Pesquisa
    4.Exit/Quit
                                                                           
          ''' + bcolors.ENDC)
    
    ans=raw_input("~//#")
    if ans=="1":
        palavras = raw_input(bcolors.HEADER + "Digite abaixo as palavras que vai monitorar separadas por virgula: \n" + bcolors.ENDC)
        telefone = raw_input(bcolors.HEADER + "Agora digite o celular que vai receber os twitts(EX: 5511998878234): \n" + bcolors.ENDC)
        l = StreamListener()
        streamer = tweepy.Stream(auth=auth1, listener=l)
        # Termos, palavras, hashtags utilizadas para a monitora??o, s?o elas que estou monitorando e jogando no whatsapp.
        setTerms = palavras.split(',')
        streamer.filter(track = setTerms)
    
    elif ans=="2":    
        arquivo = raw_input(bcolors.HEADER + "Digite o nome ou o caminho do seu arquivo: \n" + bcolors.ENDC)
        telefone = raw_input(bcolors.HEADER + "Agora digite o celular que vai receber os twitts(EX: 5511998878234): \n" + bcolors.ENDC)
        setTerms = []
        try:
          f = open(arquivo,"r")
          for linha in f:
            setTerms += [linha.rstrip()]
          f.close()
        except IOError:
          print bcolors.WARNING + "\nO arquivo que voce tentou carregar nao existe ou foi digitado incorretamente!\n" + bcolors.ENDC
        
        l = StreamListener()
        streamer = tweepy.Stream(auth=auth1, listener=l)
        streamer.filter(track = setTerms)  
    elif ans=="3":
        sys.exc_clear
        print('''                                                                         
  .--.--.                                                  
 /  /    '.                                                
|  :  /`. /             __  ,-.                    __  ,-. 
;  |  |--`            ,' ,'/ /|    .---.         ,' ,'/ /| 
|  :  ;_       ,---.  '  | |' |  /.  ./|  ,---.  '  | |' | 
 \  \    `.   /     \ |  |   ,'.-' . ' | /     \ |  |   ,' 
  `----.   \ /    /  |'  :  / /___/ \: |/    /  |'  :  /   
  __ \  \  |.    ' / ||  | '  .   \  ' .    ' / ||  | '    
 /  /`--'  /'   ;   /|;  : |   \   \   '   ;   /|;  : |    
'--'.     / '   |  / ||  , ;    \   \  '   |  / ||  , ;    
  `--'---'  |   :    | ---'      \   \ |   :    | ---'     
             \   \  /             '---" \   \  /           
              `----'                     `----'
-----------------------------------------------------------------------------------
- Esse modo o ''' + bcolors.OKBLUE + "ST4WA" + bcolors.ENDC + ''' ainda esta em ''' + bcolors.OKGREEN + "BETA" + bcolors.ENDC + '''!!

- Ativando o Listening, ele vira um server de pesquisa, voce pode escolher receber
receber o resultado de sua pesquisa por Whatsapp* ou por e-mail(So testei com GMAIL).

- Para pesquisar, basta enviar as palavras que deseja via Whatsapp para o numero que
registrou no Whatsapp que esta usando acima.

* Para receber por Whatsapp o resultado, eh preciso configurar mais um numero do whatsapp
para nao dar problemas de derrubar o whatsapp na hora que enviar as mensagens.

A configuracao pode ser feita no arquivo Examples/configPesquisa.conf

              ''')
        servOpt=True
        servOpt=raw_input("Deseja receber o resultado da pesquisa por qual meio?\n1.Whatsapp\n2.Email\n\n~//#")
        while servOpt:
            if servOpt=="1":
                wa = WhatsappListenerClient('keepalive', 'autoack')
                wa.login(username, password)
            elif servOpt=="2":
                wa = WhatsappListenerClientEmail('keepalive', 'autoack')
                wa.login(username, password)
            elif servOpt !="":
                print(bcolors.WARNING + "\n Not Valid Choice Try again" + bcolors.ENDC)
    elif ans=="4":
      break
    elif ans !="":
      print(bcolors.WARNING + "\n Not Valid Choice Try again" + bcolors.ENDC)
