# bot_A2

### Cloning the repo

```sh
git clone git@github.com:clovislfbv/bot_A2.git
```
Now, you're good to go!

### Requirements
To run the bot you need to install this module: https://github.com/mccoderpy/discord.py-message-components

This module allows you to have all the functionalities of discord.py (slash commands, buttons...) in a single module. Please follow the steps indicated in the README of the module to install it

### Add commands
To add commands to the bot, you must go to the bottom of the main.py file. Then write your command under this format:
```py
@bot.command()
async def yourfunction(ctx): #ctx needs to be in the arguments for the command to work on Discord 
         '''your code'''
```

Careful! If you add a command to the bot. It must be before the lines :
```py
with open('token_bot.txt', 'r') as token:
    bot.run(token.read())
```
Otherwise, the bot will not take into account your new command in its list of commands
