import discord
import requests
import json
import pymysql.cursors
import signal
#token stored ib variable so as to change as per requirement
TOKEN="token"

#conection details and MySQL connector so as to connect the database
connection = pymysql.connect(host='HOSTNAME',
                             user='USERAME',
                             password='PASWORD',
                             db='DATABASE',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

#MyClient inherits the discord.Client class so as to reuse the functionality for the same
class MyClient(discord.Client):

    storage_list=[]
    '''list used here for store the histroy, 
    in "!recent" command it is utilised for cheking recent same searches,
    if we restart the server then this list will get initializes with previous histroy
    '''
    '''
    On start of server below function initializes the prerequisites like history once discord client is run
    '''
    async def on_ready(self, c=storage_list):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        with connection.cursor() as cursor:
            # Read records one by one and assign into list.
            sql = "SELECT * FROM histroy"
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                #print(i["keyword"])
                self.storage_list.append(i["keyword"])
    '''
    on message what all functions our bot perform is handle via below function
    '''
    async def on_message(self, message, c=storage_list):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        
        # if person sends hi then bot should reply hey
        if message.content in ('hi', 'Hi', 'HI', 'hI', 'hey'):
            await message.channel.send('hey'.format(message))
        '''    
        if message is sent as hi then bot should reply hey
        if message is sent as !google word then it searches for the word reply back provide top 5 links
        if message is sent as !recent keyword then bot replies back the recent search consisting of that word
        '''
        if message.content.startswith('!') :
            a = message.content.split(' ',1);
            if a[0].lower() == '!recent':
                finding=str(a[1])
                #print(finding)
                for i in self.storage_list:
                    if finding in i:
                        await message.channel.send(str(i).format(message))
            if a[0].lower() == '!list':
                #self.storage_list=(self.storage_list)
                #print(self.storage_list)
                await message.channel.send(str(self.storage_list).format(message))
            if a[0].lower() == '!google':
                #print(message.content)
                a=keyword=str(a[1])
                self.storage_list.append(keyword)
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO histroy (`keyword`) VALUES (%s)"
                    cursor.execute(sql, (keyword))
                    connection.commit()
                #print(a)
                a='https://www.googleapis.com/customsearch/v1?key=APICODE&cx=017576662512468239146:omuauf_lfve&q='+a
                a=requests.get(a)
                c=a.text
                b=json.loads(c)
                try:
                  #based on the no of link the in search result the output is generated.
                    l=len(b['items'])
                    if(l<5):
                        for i in range(len(b['items'])):
                            #print(b['items'][i]['link'])
                            await message.channel.send(str(b['items'][i]['link']).format(message))
                        if l==0:
                            await message.channel.send('No links found!'.format(message))
                        if l==1:
                            await message.channel.send(f'Only {l} link found!'.format(message))
                        if l>1:
                            await message.channel.send(f'Only {l} links found!'.format(message))
                            
                    if(l>4):
                        for i in range(5):
                            #print(b['items'][i]['link'])
                            await message.channel.send(str(b['items'][i]['link']).format(message))
                except KeyError:
                        await message.channel.send(f"No URLs found for the keyword : {keyword}.".format(message))

client = MyClient()

#to handle the keyboard interrupt exception a decorator is taken into application(if we terminate the server).

def decorator1(fun):
    def keyboardInterruptHandler(signal, frame):
        print("Exited the system due to Key board Intrrupt!!!")
        exit(0)

    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    client.run(TOKEN)

    while True:
        pass

    return keyboardInterruptHandler

decorator1(client.run)
