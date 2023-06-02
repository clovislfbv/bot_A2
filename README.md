# bot_A2

### Cloning the repo

```sh
git clone git@github.com:clovislfbv/bot_A2.git
```
Now, you're good to go!

### Requirements
You need to have the discord module installed which allows you to interact with discord directly with Python, the vobject module which help to interact easily with an ics file and finally, the pytz module which let's you edit a time with the timezone you want.

### Add commands
To add commands to the bot, you must go to the bottom of the main.py file. Then write your command under this format:
```py
@tree.command(name='NameOfYourCommand', description = "Description of your command")
async def yourfunction(interaction:discord.Interaction): #interaction needs to be in the arguments for the command to work on Discord 
         '''your code'''
```

Careful! If you add a command to the bot. It must be before the lines :
```py
with open('token_bot.txt', 'r') as token:
    client.run(token.read())
```
Otherwise, the bot will not take into account your new command in its list of commands
