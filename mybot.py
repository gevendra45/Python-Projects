import discord
import requests
import json
import pymysql.cursors
import signal
#token stored ib variable so as to change as per requirement
TOKEN="NjkwODIyMzUyNDY4MDQ5OTQx.XnXJZw.1Gt-WjoBaf061k6L0Y9w-f_N1w0"

connection = pymysql.connect(host='remotemysql.com',
                             user='UzkO1dL2uA',
                             password='rUIhQpUxJg',
                             db='UzkO1dL2uA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

class MyClient(discord.Client):

    storage_list=[]
    
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
        #finally:
        #    connection.close()
        #print('Input the value from file or data structure to the list here.')
        #print(self.storage_list)

    async def on_message(self, message, c=storage_list):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        
        if message.content in ('hi', 'Hi', 'HI', 'hI', 'hey'):
            await message.channel.send('hey'.format(message))
            #print(message.content, type(message.content))

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
                a='https://www.googleapis.com/customsearch/v1?key=AIzaSyC8d7W081agxdVieeHNa8vkZXI7BXa9XvQ&cx=017576662512468239146:omuauf_lfve&q='+a
                a=requests.get(a)
                c=a.text
                b=json.loads(c)
                try:
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



