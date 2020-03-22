Bluestacks backend developer challenge.

Simple discord bot that would reply hey to your hi.

Added functionality to allow a user to search on google through discord. 
If the user types !google nodejs, reply with top 5 links that you would get when you search nodejs on google.com

Implemented functionality to search through your search history. 
If a user uses !google to search for "nodejs" "apple games" "game of thrones", and after these searches, 
if user types !recent game, your bot should reply with "apple games" and "game of thrones"

Here history is persistent i.e. even when we kill our server and start again, search history is maintained in external database.

database used : External DataBase is used for string the value of search histroy provided by used in discord bot.
