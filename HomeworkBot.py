import os
import discord
import random
import time

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

global Username
global Password
global tasks
global homeworks
global soup

Username = '16cselmes'
Password = '*********'
soup = ''

tasks = []
homeworks = []
Dates = []

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path="D:\Program Files (x86)\chromedriver.exe")

def site_login():
    global soup
    
    driver.get("https://www.satchelone.com/login?subdomain=lintonvillage&userType=student")
    time.sleep(1.5)

    #driver.find_element_by_id("school-selector-search-box").send_keys("Linton Village Collage", Keys.RETURN)
    driver.find_element_by_id("identification").send_keys(Username)
    driver.find_element_by_id("password").send_keys(Password)

    driver.find_element_by_css_selector("button.login-form__btn").click()

    time.sleep(1.5)
    newURL = driver.current_url
    driver.get(newURL)
    time.sleep(1.5)

    page = driver.page_source
    soup = BeautifulSoup(page[page.find("ember-basic-dropdown-wormhole"): ], 'html.parser')

    print("Login Sucessful")

site_login()

def logout():
    driver.find_element_by_class_name("linearicon-power-switch").click()
    site_login()

# ================================ END OF SCRAPE ================================ #

load_dotenv()
TOKEN = os.getenv('SMHWBOT_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    
    print()
    print(
        f'{bot.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})\n'
        f' - - SHMWbot Ready - - '
    )
    print()

@bot.event
async def on_message(message):
    global soup

    homeworkNo = 0

    if message.author == bot.user:
        return 

    elif "showmyhomework" in message.content.lower():
        accountName = soup.find(attrs={"class":"satchel-content-card__title"})
        accountMessage = "- _ - logged in as: "+accountName.getText().strip()+" - _ - "

        await message.channel.send(accountMessage+"\n")
        titles = soup.findAll("h4")
        await message.channel.send("**Homeworks are: **")

        for title in range(0, len(titles)-5):
            arg=titles[title]
            homeworks.append(arg.text.strip())
            await message.channel.send(arg.text.strip())
        print("Homeworks added to homework list")

        await message.channel.send(" **= = = NO MORE HOMEWORKS TO SHOW = = =** ")
        print("Shown Homework Titles")

    elif "descriptions" in message.content.lower():
        taskDescriptions = soup.findAll(attrs={"class":"truncate-text"})

        for taskDescription in taskDescriptions:
            tasks.append(taskDescription.text.strip())
        print("Tasks added to task list")

        for i in homeworks:
            await message.channel.send('**'+homeworks[homeworkNo]+'**')
            await message.channel.send(tasks[homeworkNo+1]+"\n")
            homeworkNo+=1

        await message.channel.send(" **= = = NO MORE HOMEWORKS TO SHOW = = =** ")
        print("Shown Homeworks With Descriptions")

    elif "dates" in message.content.lower():
        
        dates = soup.findAll(attrs={"class":"col-md-3 date"})
        for date in dates:
            temp = date.text.split()
            date = " ".join(temp)
            Dates.append(date)
        print("Dates added to date list")

        homeworkNo = 0
        for i in homeworks:
            dateMessage = '**'+homeworks[homeworkNo]+'**'+" is due on "+'**'+Dates[homeworkNo]+'**'
            await message.channel.send(dateMessage)
            homeworkNo+=1
            
        await message.channel.send(" **= = = NO MORE HOMEWORKS TO SHOW = = =** ")
        print("Shown Homeworks With Dates")

    await bot.process_commands(message)

@bot.command(name='login')
async def login(ctx):
    global Password
    global Username

    print("Login Requested")

    msg = await ctx.author.send("Enter Username")
    def check(message):
        return message.author == ctx.author and message.channel == msg.channel
    reply = await bot.wait_for('message', check=check)
    if reply.content.lower() == reply.content.lower():
        Username = reply.content

    msg = await ctx.author.send("Enter Password")
    def check(message):
        return message.author == ctx.author and message.channel == msg.channel
    reply = await bot.wait_for('message', check=check)
    if reply.content.lower() == reply.content.lower():
        Password = reply.content

    logout()

bot.run(TOKEN)
