import discord, asyncio
import scraper
import os, sys, json
import urllib.parse
import datetime
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await get_new_roles_postings_task()

@bot.event
async def on_message(message):
    def add_to_blacklist(companies):
        config = get_config()
        blacklist = set(config["blacklist"])

        for company in companies:
            blacklist.add(company)

        s = ""
        for company in blacklist.difference(set(config["blacklist"])):
            s += company + ", "
        if len(s) == 0:
            s = "No companies were added to the blacklist."
        else:
            s = "Added " + s[:-2] + " to the blacklist!"

        config["blacklist"] = list(blacklist)
        save_config(config)
        get_companies_channel().send(s)

    def remove_from_blacklist(companies):
        config = get_config()
        blacklist = set(config["blacklist"])

        for company in companies:
            blacklist.discard(company)

        s = ""
        for company in blacklist.difference(set(config["blacklist"])):
            s += company + ", "
        if len(s) == 0:
            s = "No companies were removed from the blacklist."
        else:
            s = "Removed " + s[:-2] + " from the blacklist!"

        config["blacklist"] = list(blacklist)
        save_config(config)
        get_companies_channel().send(s)

    if message.author.bot:
        return

    if message.content.splitlines[0] == "!blacklist":
        add_to_blacklist(message.content.splitlines[1:])

    elif message.content.splitlines[0] == "!unblacklist":
        remove_from_blacklist(message.content.splitlines[1:])


async def get_new_roles_postings_task():
    async def send_new_roles():
        async def send_companies(companies):
            s = ""
            for company in companies:
                s += company + "\n"
            await get_companies_channel().send(s)

        def levels_url(company):
            base = "https://www.levels.fyi/internships/?track=Software%20Engineer&timeframe=2023%20%2F%202022&search="
            return base + urllib.parse.quote_plus(company)

        def google_url(company):
            base = "https://www.google.com/search?q="
            return base + urllib.parse.quote_plus(company)

        config = get_config()
        posted = set(config["posted"])
        blacklist = set(config["blacklist"])
        roles = scraper.get_recent_roles()
        companies = set()
        for role in roles:
            company, title, link, picture = role
            company_and_title = company + " - " + title
            if company_and_title in posted or company in blacklist:
                continue
            companies.add(company)
            config["posted"].append(company_and_title)
            posted.add(company_and_title)
            embed = discord.Embed(title=title, url=link, color=discord.Color.from_str("#378CCF"), timestamp=datetime.datetime.now())
            embed.set_author(name=company, url=google_url(company))
            embed.add_field(name="Levels.fyi Link", value=f"[{company} at Levels.fyi]({levels_url(company)})")
            embed.set_footer(text="Made by hotsno#0001")
            embed.set_thumbnail(url=picture)
            await get_new_postings_channel().send(embed=embed)
        save_config(config)
        await send_companies(companies)

    while True:
        try:
            await get_testing_channel().send('Trying to get new roles...')
            await send_new_roles()
            await get_testing_channel().send('Succeeded. Waiting 20 minutes.')
            await asyncio.sleep(1200)
        except Exception as e:
            await get_testing_channel().send('Failed. Waiting 20 minutes.')
            print(e)
            await asyncio.sleep(1200)

def get_config():
    with open(os.path.join(sys.path[0], 'config.json')) as f:
        config = json.load(f)
        return config

def save_config(config):
    with open(os.path.join(sys.path[0], 'config.json'), 'w') as f:
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

# Currently hardcoded...
async def get_new_postings_channel():
    return bot.get_channel(1020861126751289374)

async def get_testing_channel():
    return bot.get_channel(1020848013163380786)

async def get_companies_channel():
    return bot.get_channel(1020861103896547389)

with open('config.json', 'r') as f:
    bot.run(json.load(f)['token'])
