import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import requests as r
from datetime import datetime
import vobject
import pytz
from random import choice

bot = commands.Bot(command_prefix="$")
slash = SlashCommand(bot, sync_commands = True)
client = discord.Client()

lastdlday = None
lastedt = None

@bot.event
async def on_ready():
    print("ready")
    changeStatus.start()

status = ["$help", "$edt", "aider les A2 à retrouver la classe où ils ont cours"]

@bot.command()
async def start(ctx, secondes = 5):
    ''' ne fait rien '''
    changeStatus.change_interval(seconds = secondes)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Dsl la commande que t'as écrite existe peut être dans tes rêves mais moi je la connais pas")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Dsl mais t'as pas les permissions d'utiliser cette commande.")
    elif isinstance(error.original, discord.Forbidden):
        await ctx.send("Dsl je peux pas exécuter ta commande pcq les admins ne m'ont pas donner les permissions pour faire cela.")

@tasks.loop(seconds = 5)
async def changeStatus():
    game = discord.Game(choice(status))
    await bot.change_presence(activity = game)

@slash.slash(name="edt", description = "donne notre emploi du temps", options=[
    create_option(name="day", description="le jour que tu veux consulté avec le format 'dd/mm/yyyy'", option_type=3, required=False)
])
@bot.command()
async def edt(ctx:SlashContext, day=None):
    global lastdlday, lastedt

    if day is not None:
        number_slash = 0
        for char in day:
            if char == "/":
                number_slash += 1
        if number_slash == 2:
            today=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            todayStr = today.isoformat()
            todayFinal = ""
            todayStr = todayStr.split("-")
            todayStr[2] = todayStr[2][0] + todayStr[2][1]
            for i in range(len(todayStr)-1):
                todayFinal = "/" + todayStr[i] + todayFinal
            todayFinal = todayStr[2] + todayFinal

            if day != todayFinal:
                day = day.split("/")
                today = datetime(int(day[2]), int(day[1]), int(day[0]), 0, 0)
    else:
        number_slash = 2
        today=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if number_slash == 2:
        if lastdlday is not None and (datetime.now()-lastdlday).days <= 0:
            cal = lastedt
            print("ics already installed")
        else:
            with open('edt_token.txt', 'r') as token_edt:
                url = token_edt.read().rstrip('\n')
            response = r.get(url)
            response.encoding = "utf-8"
            data = response.text
            cal = vobject.readOne(data)

            lastdlday = datetime.now()
            lastedt = cal

            print("installing ics...")

        emb = discord.Embed(title=today.strftime("%A %d %B %Y"), color=0x3498db)
        dates = []
        for ev in cal.vevent_list:
            start_time = ev.dtstart.valueRepr().isoformat().split("-")
            variable = start_time[0]
            start_time[0] = start_time[2][0] + start_time[2][1]
            start_time[2] = variable
            time = datetime(int(start_time[2]), int(start_time[1]), int(start_time[0]), 0, 0)
            if time == today:
                date_start = ev.dtstart.value.astimezone(pytz.timezone("Europe/Paris")).strftime("%H:%M")
                date_end = ev.dtend.value.astimezone(pytz.timezone("Europe/Paris")).strftime("%H:%M")
                dates.append(date_end)
                dates.sort()
                for i in range(len(dates)):
                    if dates[i] == date_end:
                        index = i
                field = emb.insert_field_at(index=index, name = ev.summary.valueRepr(), value = "time start : " + date_start + "\n" + "time end : " + date_end + "\n" + "location : " + ev.location.value)

        if len(dates) == 0:
            emb.add_field(name = "PAS COURS !!", value = "Aujourd'hui, il n'y a pas cours")
        msg = await ctx.send(embed = emb)
    else:
        print("bad argument")
        await ctx.send("Je n'ai pas compris la date que tu as mise. La date que tu écris doit être sous le format `dd/mm/yyyy`. Cependant, si tu ne mets aucune date en argument, la commande montrera l'emploi du temps d'aujourd'hui.")


with open('token_bot.txt', 'r') as token:
    bot.run(token.read())
