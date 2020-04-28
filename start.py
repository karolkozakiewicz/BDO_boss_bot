from discord.ext import commands, tasks
import bot_functions
import connection
import datetime


client = commands.Bot(command_prefix='.')
bot = client
client.remove_command("help")
functions = bot_functions.BotFunctions()


# @client.event
# async def on_command_error(self, exception):
#     if isinstance(exception, commands.errors.CommandNotFound):
#         pass

@client.command(pass_context=False)
async def rozsypanka(ctx, *args):
    try:
        if not args:
            await ctx.send(functions.rozsypanka())
        else:
            await ctx.send(functions.rozsypanka(args))
    except TypeError:
        pass



@client.command(pass_context=False)
async def msg(ctx, *args):
    try:
        if not args:
            await ctx.send("```.msg add | del | send | list ```")
        elif args[0] == "add":
            await ctx.send(functions.message_add(args))
        elif args[0] == "del":
            await ctx.send(functions.message_del(args))
        elif args[0] == "list":
            await ctx.send(functions.message_list(args))
        elif args[0] == "send":
            await ctx.send(functions.message_send(args))
        elif args[0] == "show":
            await ctx.send(functions.message_show(args))
        else:
            await ctx.send("```Niepoprawna nazwa komendy```")
    except TypeError:
        pass

@client.command()
async def klik(ctx, *args):
    try:
        if not args:
            await ctx.send("Podaj poprawną liczbę failstacków")
        elif int(args[0]) > 100:
            await ctx.send("```Maksymalnie możesz wpisać 100, byczku ;)```")
        else:
            if len(args) > 1:
                ile_razy = args[1]
                if int(ile_razy)>= 20:
                    ile_razy = 20
                odp = ""
                for _ in range(int(ile_razy)):
                    dane = functions.klik(args)
                    if dane[0] == True:
                        odp += f"Enhancement SUCCEED. Szansa: {dane[1]}\n"
                    else:
                        odp += f"Enhancement FAILED. Szansa: {dane[1]}\n"
                await ctx.send(f"```{odp}```")

            else:
                dane = functions.klik(args)
                if dane[0] == True:
                    await ctx.send(f"```Enhancement SUCCEED. Szansa: {dane[1]}```")
                else:
                    await ctx.send(f"```Enhancement FAILED. Szansa: {dane[1]}```")
    except TypeError:
        pass

@client.command()
@commands.has_any_role(*functions.roles())
async def clear(ctx, amount=5):
    if (amount >= 0):
        await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.send("Invalid argument")

@client.command()
async def help(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(functions.help())

@client.command()
async def reset(ctx):
    await ctx.channel.purge(limit=1)
    nick = ctx.author.display_name
    await ctx.author.edit(nick=functions.reset_nick(nick))

@client.command()
async def pt1(ctx):
    await ctx.channel.purge(limit=1)
    nick = ctx.author.display_name
    await ctx.author.edit(nick=functions.reset_nick(nick))
    await ctx.author.edit(nick=functions.add_party(nick, party=1))

@client.command()
async def pt2(ctx):
    await ctx.channel.purge(limit=1)
    nick = ctx.author.display_name
    await ctx.author.edit(nick=functions.reset_nick(nick))
    await ctx.author.edit(nick=functions.add_party(nick, party=2))

@client.command()
async def pt3(ctx):
    await ctx.channel.purge(limit=1)
    nick = ctx.author.display_name
    await ctx.author.edit(nick=functions.reset_nick(nick))
    await ctx.author.edit(nick=functions.add_party(nick, party=3))

@client.command()
async def u(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(f"Liczba userów na serwerze (wraz z botami): {id.member_count}")

@client.command()
async def b(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(functions.all_todays_bosses())

@client.command()
async def jutro(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(functions.all_tomorrows_bosses())

@client.command()
async def next(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(functions.todays_next_boss()[0])

@client.command()
async def discord(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("Link do discorda: https://discord.gg/zdZYt6V")

@client.command()
async def minecraft(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("```IP SERWERA: mc.spiritapps.net\nWersja: 1.15.2``` \
Pobrać minecrafta można ze strony: https://tlauncher.org/installer")



@client.event
async def on_ready():
    auto_message.start()
    print(f'{client.user.name} has connected to Discord. {datetime.datetime.now()}')


@tasks.loop(seconds=60)
async def auto_message():
    """
    time_to_send_message = czas do następnego bossa podany w MINUTACH
    :return:
    """
    channel = client.get_channel(700075948447367182)
    time_to_send_message = int(functions.compare_time(functions.next_boss()[1]))
    if time_to_send_message == 30:
        await channel.purge(limit=3)
        await channel.send(f" <@&700076061945233409> {functions.next_boss()[0]}")



client.run(connection.key)
