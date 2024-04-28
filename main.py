import discord
from discord.ext import commands
import sqlite3
import traceback
from discord import Embed
import asyncio

conn = sqlite3.connect('esports.db')
c = conn.cursor()
Token = "MTE5ODI0MTM3MDk2MDMxNDQ3MA.GufKxH.3hZvDNzAcje29Nw4DST_LIaXR6lxIZwKABDa3c"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
channels={
    "free-agenti" : 1197925809504141343,
    "novinky": 1199338907154788373,
    "oznámenia":1198205457207148604,
    "content": 1198204526256214107,
    "subs" : 1205162111257546822,
    "wows" : 1198202103160643585,
    "tours_teams" : 1202569026975432724,
    "interviews" : 1199338928931602473,
    "leaderboards" : 1200018081876033576,
    "monthly_leaderboards" : 1212994670162878497,
    "logs": 1221793236285395034,
    "staff":1197919004820504586,
    "používanie-bota":1210250726689996830,
    "ranking-system":1197925625156096050,
    "team-statistics":1198202244328337499,
    "rosters":1198202432145072191,
    "chat":1197930935862177964,
    "návrhy":1197987512451334164,
    "botspam":1198202023301091358,
    "team-vs-team":1198202103160643585,
    "wow-codes":1201213666406703197,
    "coach-team":1198220201083289610,
    "tips":1202542704706461696,
    "registrácia-turnajov":1198237670384619590,
    "registrácia-scrimov":1221102416586477691,
    "zoznam-turnajov":1198201375385980928,
    "treningove-wowka":1198203660862242917,
    "teamy-mesiaca":1198203723957141595,
    "hall-of-fame":1198204035627491478,
    "qualified":1198204367510188174,
    "info":1202545973985943593,
    "uc-rooms-info":1221062484920766536,
    "teams":1219676454162530385,


}

@bot.event
async def on_member_join(member):
    role = member.guild.get_role(1199985402770100284)
    guild = bot.get_guild(1197918865242472479)
    channel = bot.get_channel(channels.get("logs"))
    member_count = guild.member_count
    if role is not None:
        await member.add_roles(role)
        print(f"Added autorole to {member.display_name}")
    else:
        print("Role not found. ")
    await channel.send(f'{member.display_name} joined! Members: {member_count}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(activity=discord.Game(name='Pubg Mobile'))
    asyncio.create_task(periodic_update())


@bot.event
async def on_member_remove(member):
    guild = bot.get_guild(1197918865242472479)
    channel_id = 1221793236285395034
    channel = bot.get_channel(channel_id)
    member_count = guild.member_count
    if channel:
        await channel.send(f"{member} has left the server. Members: {member_count}")
    else:
        print("Error: Channel not found.")


@commands.command()
@commands.has_role("CZSK | Staff")
async def embed(ctx, *, args):
    # Parse the input string
    args_list = args.split()
    channel_name = args_list[0]
    title = args_list[1]
    text = ' '.join(args_list[2:])  # Join the remaining parts of the text
    image_url = None
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        image_url = attachment.url

    # Get the channel ID from the channels dictionary
    channel_id = channels.get(channel_name)
    if channel_id:
        channel = bot.get_channel(channel_id)
        embed = discord.Embed(title=title, description=text, color=0x00ff00)
        if image_url:
            embed.set_image(url=image_url)
        await channel.send(embed=embed)
    else:
        await ctx.send("Error: Channel not found.")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1222102723013644301:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        if str(payload.emoji) == '✅':
            role = guild.get_role(1221062278003298386)
            await member.add_roles(role)
            
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 1222102723013644301:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if str(payload.emoji) == '✅':
            role = guild.get_role(1221062278003298386)
            await member.remove_roles(role)

@commands.command()
async def fa(ctx, *, info):
    channel_id = channels.get("free-agenti")
    if channel_id:
        channel = bot.get_channel(channel_id)
        lines = info.split('\n')
        embed = discord.Embed(title=f"Free Agent: {ctx.author.display_name}", color=0x00ff00)
        for i, line in enumerate(lines, start=1):
            embed.add_field(name=f"{line.strip()}", value="", inline=False)
        await channel.send(embed=embed)
    else:
        await ctx.send("Error: Channel ID for 'free-agenti' not found.")

@commands.command()
async def recruiting(ctx, *, info):
    channel_id = channels.get("free-agenti")
    if channel_id:
        channel = bot.get_channel(channel_id)
        lines = info.split('\n')
        embed = discord.Embed(title=f"{ctx.author.display_name} robí nábor do teamu.", color=0x00ff00)
        for i, line in enumerate(lines, start=1):
            embed.add_field(name=f"{line.strip()}", value="", inline=False)
        await channel.send(embed=embed)
    else:
        await ctx.send("Error: Channel ID for 'free-agenti' not found.")

@commands.command()
async def sub(ctx, *, info):
    channel_id = channels.get("subs")
    if channel_id:
        channel = bot.get_channel(channel_id)
        lines = info.split('\n')
        embed = discord.Embed(title=f"Sub: {ctx.author.display_name}", color=0x00ff00)
        for i, line in enumerate(lines, start=1):
            embed.add_field(name=f"{line.strip()}", value="", inline=False)
        
        await channel.send(embed=embed)

@commands.command()
async def needsub(ctx, *, info):
    channel_id = channels.get("subs")
    if channel_id:
        channel = bot.get_channel(channel_id)
        lines = info.split('\n')
        embed = discord.Embed(title=f"Suba potrebuje: {ctx.author.display_name}", color=0x00ff00)
        for i, line in enumerate(lines, start=1):
            embed.add_field(name=f"{line.strip()}", value="", inline=False)
        
        await channel.send(embed=embed)

@commands.command()
async def wow(ctx, *, info):
    channel_id = channels.get("wows")
    if channel_id:
        channel = bot.get_channel(channel_id)
        lines = info.split('\n')
        embed = discord.Embed(title=f"WOW rooms: {ctx.author.display_name}", color=0x00ff00)
        for i, line in enumerate(lines, start=1):
            embed.add_field(name=f"{line.strip()}", value="", inline=False)
        
        await channel.send(embed=embed)


@commands.command()
async def content(ctx, *, info):
    channel_id = channels.get("content")
    if channel_id:
        channel = bot.get_channel(channel_id)
        lines = info.split('\n')
        embed = discord.Embed(title=f"{ctx.author.display_name}", color=0x00ff00)
        for i, line in enumerate(lines, start=1):
            embed.add_field(name=f"{line.strip()}", value="", inline=False)
        
        await channel.send(embed=embed)

@commands.command()
async def tournament(ctx, *, info):
    channel_id = channels.get("tours_teams")
    if channel_id:
        channel = bot.get_channel(channel_id)
        lines = info.split('\n')
        embed = discord.Embed(title=f"{ctx.author.display_name}", color=0x00ff00)
        for i, line in enumerate(lines, start=1):
            embed.add_field(name=f"{line.strip()}", value="", inline=False)
        
        await channel.send(embed=embed)

async def handle_error(ctx, command, error):
    print(f"Error in {command}: {error}")
    traceback.print_exc()
    channel = bot.get_channel(1198202023301091358)
    await channel.send(f"An error occurred in {command}: {error}")

@commands.command()
async def results(ctx):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="Results")
    if not category:
        category = await guild.create_category("Results")
    
    existing_channels = [int(channel.name.split("results")[1]) for channel in category.channels if channel.name.startswith("results")]
    ticket_number = max(existing_channels) + 1 if existing_channels else 1
    
    channel_name = f"results{ticket_number}"
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True)
    }

    new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)
    await ctx.send(f"Results channel {new_channel.mention} created.")


@commands.command()
@commands.has_role("CZSK | Staff")
async def news(ctx, *, args):
    title, *description_list = args.split('\n')
    description = '\n'.join(description_list)
    channel_id = channels.get("novinky")
    if channel_id:
        channel = bot.get_channel(channel_id)
        image_url = None
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            image_url = attachment.url
        embed = discord.Embed(title=title, description=description, color=0xFF5733)
        if image_url:
            embed.set_image(url=image_url)
        await channel.send(embed=embed)


@commands.command()
@commands.has_role("CZSK | Staff")
async def interview(ctx, *, args):
    title, file_path = args.split(',')
    try:
        with open(file_path.strip(), 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        await ctx.send("Error: Interview file not found.")
        return
    except Exception as e:
        await ctx.send(f"Error: {e}")
        return
    channel_id = channels.get("interviews")
    if channel_id:
        channel = bot.get_channel(channel_id)
        image_url = None
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            image_url = attachment.url

        embed = discord.Embed(title=title.strip(), color=0xFF5733)
        if image_url:
            embed.set_image(url=image_url)

        segments = text.split('\n\n')
        for segment in segments:
            if not segment.strip():
                continue

            question, *answers = segment.split('\n')
            answer = '\n'.join(answers)
            embed.add_field(name=question.strip(), value=f"\n{answer.strip()}\n", inline=False)

        await channel.send(embed=embed)



def get_monthly_leaderboard():
    c.execute("SELECT team_name, monthly_rating FROM teams ORDER BY monthly_rating DESC")
    rows = c.fetchall()
    
    leaderboard = ""
    rank = 1
    for row in rows:
        leaderboard += f"{rank}. {row[0]} - {row[1]}\n"
        rank += 1
    
    return leaderboard

def get_total_leaderboard():
    c.execute("SELECT team_name, rating FROM teams ORDER BY rating DESC")
    rows = c.fetchall()
    
    leaderboard = ""
    rank = 1
    for row in rows:
        leaderboard += f"{rank}. {row[0]} - {row[1]}\n"
        rank += 1
    
    return leaderboard

async def update_leaderboards():
    monthly_leaderboard = get_monthly_leaderboard()
    channel_id = channels.get("monthly_leaderboards")
    if channel_id:
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(1224265611954356235)
        embed = discord.Embed(title="2. Sezóna", description=monthly_leaderboard, color=0xFF5733)
        await message.edit(embed=embed)
    else:
        print("Monthly Leaderboards channel not found.")

    total_leaderboard = get_total_leaderboard()
    channel_id = channels.get("leaderboards")
    if channel_id:
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(1220336261588324472)
        embed = discord.Embed(title="Leaderboards", description=total_leaderboard, color=0xFF5733)
        await message.edit(embed=embed)
    else:
        print("Total Leaderboards channel not found.")


async def periodic_update():
    while True:
        await update_leaderboards()
        await asyncio.sleep(500)

bot.add_command(fa)
bot.add_command(sub)
bot.add_command(tournament)
bot.add_command(needsub)
bot.add_command(results)
bot.add_command(wow)
bot.add_command(news)
bot.add_command(interview)
bot.add_command(content)
bot.add_command(embed)
bot.add_command(recruiting)
bot.run(Token)
