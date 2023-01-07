# bot_A2

### Cloning the repo

```sh
git clone git@github.com:clovislfbv/all_things-my-Discord-bot.git
```
Now, you're good to go!

### Add commands
To add commands to the bot, you must go to the bottom of the main.py file. Then write your command in this form:
```py
@bot.command()
async def yourfunction(ctx): #ctx needs to be in the arguments for the command to work on Discord 
         '''your code'''
```
