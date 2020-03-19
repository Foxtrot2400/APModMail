#AP Modmail Bot V3 - Admin
#Code created by Foxtrot2400

#Top-Level Initializations

###SET THESE###
GUILD_ID = 55555555 #Server ID Here
token = "YOUR_TOKEN_HERE"
DEBUG = False

#Basic declarations
user_name = ""
user_id = ""
firstMsg = True
chnn = ""
msgcreatedat = ""
botprefix = "%"
showErrors = False #Show correctable errors
#imports
if(DEBUG == True):
    print("--START--")
    print("Initializing...")
    print("Importing Libraries-")
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from urllib.parse import urlparse
import asyncio
import datetime
import os
import sys
import shutil
import time
import string
import re

dts = datetime.datetime.now() #6/13/2018 at 17:20
time.sleep(0.4)
if(DEBUG==True):
    print("Complete. Initialized libraries as follows - Discord, discord.ext.commands, discord.ext.commands.has_permissions, urllib.parse, asyncio, datetime, os, sys, shutil, time, string, re")
print("=========================================")
print("Welcome to AP ModMail Discord Bot V3.15.5")
print("=========================================")
time.sleep(0.2)
print("Connecting to Discord...")

#Bot Initialization for Discord
Client = discord.Client() #Initialise Client 
client = commands.Bot(command_prefix = botprefix) #Initialise client bot


async def logEntry(message, loginstance, chnn, msgcreatedat, icon, firstMsg):
    f = open('OpenModMails/'+str(loginstance)+'.MODMAIL','a', encoding='utf-8')
    if(firstMsg == True):
        user_id = loginstance.id
        user_name = await client.fetch_user(user_id)
        messageauthor = str(user_name.name)+'-'+str(user_name.discriminator)
        f.write("""
<div id="info">\n
<div class="info-left">\n
<img class="guild-icon" src="https://cdn.discordapp.com/icons/{3}/{2}.png"/>
</div>\n
<div class="info-right">\n
<div class="guild-name">{0}</div>\n
<div class="channel-name">#{1}</div>\n
<div class="channel-topic"></div>\n
</div>\n
</div>\n
<div id\n'""".format(guild.name, messageauthor, guild.icon, guild.id))


    f.write("""<div class="msg">\n <div class="msg-left">\n<img class="msg-avatar" src="{3}"/> \n</div>\n 
<div class="msg-right"> \n
<span class="msg-user" title="{0}">{0}</span> \n
<span class="msg-date">{1}</span> \n
<div class="msg-content"> \n
{2}</div> \n
</div>
</div>
""".format(str(message.author),msgcreatedat,str(message.content), icon))
    f.close()

async def logAttachment(attachurl, loginstance, chnn, msgcreatedat, icon, author):
    f = open('OpenModMails/'+str(loginstance)+'.MODMAIL','a', encoding='utf-8')
    f.write("""<div class="msg">\n <div class="msg-left">\n<img class="msg-avatar" src="{3}"/> \n</div>\n 
<div class="msg-right"> \n
<span class="msg-user" title="{0}">{0}</span> \n
<span class="msg-date">{1}</span> \n
<div class="msg-content"> \n
{2}</div> \n
</div>
</div>
""".format(str(author),msgcreatedat,str(attachurl), icon))
    f.close()

@client.event
async def on_ready():
    print("Bot is online and connected to Discord.") #Notify the user when the bot is conencted 
    print(f'''=========================================
Author: Kaleb#0847
=========================================
Logged in as: {client.user}
User ID: {client.user.id}
=========================================
        ''')
    global guild
    guild = discord.utils.get(client.guilds, id=GUILD_ID)
    
def format_name(author):
        name = author.name
        new_name = ''
        for letter in name:
            if letter in string.ascii_letters + string.digits:
                new_name += letter
        if not new_name:
            new_name = 'null'
        new_name += f'-{author.discriminator}'
        return new_name
    
def format_info(message, fileURL, fileSent):
        '''Get information about a member of a server
        supports users from the guild or not.'''
        global guild
        user = message.author
        server = guild
        member = guild.get_member(user.id)
        avi = user.avatar_url
        time = datetime.datetime.utcnow()
        desc = 'Modmail thread started.'
        color = 0
        if member:
            roles = sorted(member.roles, key=lambda c: c.position)
            rolenames = ', '.join([r.name for r in roles if r.name != "@everyone"]) or 'None'
            member_number = sorted(server.members, key=lambda m: m.joined_at).index(member) + 1
            for role in roles:
                if str(role.color) != "#000000":
                    color = role.color
        em = discord.Embed(colour=color, description=desc, timestamp=time)

        em.add_field(name='Account Created', value=str((time - user.created_at).days)+' days ago.')
        em.set_footer(text='User ID: '+str(user.id))
        em.set_thumbnail(url=avi)
        em.set_author(name=user, icon_url=server.icon_url)
      

        if member:
            em.add_field(name='Joined', value=str((time - member.joined_at).days)+' days ago.')
            em.add_field(name='Member No.',value=str(member_number),inline = True)
            em.add_field(name='Nick', value=member.nick, inline=True)
            em.add_field(name='Roles', value=rolenames, inline=True)
        formattedMessage = message.content
        if(fileSent == True):
            formattedMessage = str(fileURL)
            em.add_field(name='Message', value=fileURL, inline=False)
        else:
            em.add_field(name='Message', value=formattedMessage, inline=False)
        
        return em
def help_embed(prefix):
        em = discord.Embed(color=0x00FFFF)
        em.set_author(name='mod mail - Help', icon_url=client.user.avatar_url)
        em.description = 'AP Modmail V2.0.0 - By Foxtrot2400. ' \
                         'This is specifically desgined for the AP Discord server administration.'
                 

        cmds =  f'`{prefix}setup` - Command that sets up the bot.\n' \
                f'`{prefix}reply <message...>` - Sends a message to the current thread\'s recipient.\n' \
                f'`{prefix}close` - Closes the current thread and deletes the channel.\n' \
                f'`{prefix}block` - Blocks a user from using modmail!\n' \
                f'`{prefix}unblock` - Unblocks a user from using modmail!\n' \
                f'`{prefix}open` - Creates a new modmail session using a user ID.\n' \
                f'`{prefix}move` - Moves the channel to a new category, or creates it if it doesnt exist.\n' \

        warn = 'Refrain from manually deleting the category or channels as it will break the system. ' \
               'Modifying the channel topic will also break the system.'
        em.add_field(name='Commands', value=cmds)
        em.add_field(name='Warning', value=warn)
        return em
    
async def processDM(message):
    global user_id
    user_id = message.author.id
    if(str(user_id) in open('blockedusers.json').read()):
        await message.add_reaction('❌')
        em = discord.Embed(title='Blocked from IPE Modmail')
        em.description = ("You have been blocked from using IPE Modmail.")
        em.color = discord.Color.red()
        await message.author.send(embed=em)
        return
    try:
        await message.add_reaction('✅')
    except:
        pass
    global guild
    global user_name
    global chnn
    global dts
    global geticon
    author = message.author
    topic = f'User ID: {author.id}'
    channel = discord.utils.get(guild.text_channels, topic=topic)
    categ = discord.utils.get(guild.categories, name='mod mail')
    em = discord.Embed(title='Thank you for your message!')
    em.description = ("The AP Admin team will get back to you as soon as possible!")
    em.color = discord.Color.green()
    if(channel is not None):
        fmt = discord.Embed()
        fmt.description = message.content
        fmt.timestamp = message.created_at
    else:
        await message.author.send(embed=em)
        channel = await guild.create_text_channel(
            name=format_name(author),
            category=categ
        )
        await channel.edit(topic=topic)
        if message.attachments:
            if message.content == None:
                formattedMessage = ""
            else:
                formattedMessage = message.content
            await channel.send("""```css
--BEGINNING OF HELP REQUEST--```""", embed=format_info(message, message.attachments[0].url, True))
        else:
            await channel.send("""```css
--BEGINNING OF HELP REQUEST--```""", embed=format_info(message, "", False))
            
    if("User ID:" in channel.topic and os.path.isfile("OpenModMails/"+str(message.author)+".MODMAIL")):
        if(dts.minute < 10):
            cminute = "0"+str(dts.minute)
        else:
            cminute = str(dts.minute)
        msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(cminute)
        fmt.color=discord.Color.gold()
        fmt.set_author(name=str(author), icon_url=author.avatar_url)
        fmt.set_footer(text='User')
        urls = re.findall(r'(https://[^\s]+)', message.content)
        types = ['.png', '.jpg', '.gif', '.jpeg', '.webp']
        for u in urls:
            if any(urlparse(u).path.endswith(x) for x in types):
                fmt.set_image(url=u)
                break
        if message.attachments:
            attach = message.attachments[0].url
            await logAttachment(attach, message.author, chnn, msgcreatedat, author.avatar_url, message.author)
            if(".png" in message.attachments[0].url or ".jpg" in message.attachments[0].url or ".gif" in message.attachments[0].url or ".jpeg" in message.attachments[0].url or ".webp" in message.attachments[0].url):
                fmt.set_image(url=message.attachments[0].url)
            else:
                fmt.description = message.attachments[0].url
        else:
            await logEntry(message, message.author, chnn, msgcreatedat, author.avatar_url, False)
        await channel.send(embed=fmt)
    else:
        shutil.copyfile("htmltemplate.txt", 'OpenModMails/'+str(message.author)+'.MODMAIL')
        user_name = await client.fetch_user(user_id)
        chnn = str(user_name.name)+'-'+str(user_name.discriminator)
        dts = datetime.datetime.now() #6/13/2018 at 17:20
        if(dts.minute < 10):
            cminute = "0"+str(dts.minute)
        else:
            cminute = str(dts.minute)
        msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(cminute)
        if message.attachments:
            attach = message.attachments[0].url
            await logEntry(message, message.author, chnn, msgcreatedat, author.avatar_url, True)
            await logAttachment(attach, message.author, chnn, msgcreatedat, author.avatar_url, message.author)
        else:
            await logEntry(message, message.author, chnn, msgcreatedat, author.avatar_url, True)


async def reply(message):
    if not("User ID:" in message.channel.topic):
        return
    global guild
    global user_id
    global user_name
    global chnn
    global dts
    global geticon
    fmt = discord.Embed()
    fmt.description = message.content[6:]
    fmt.timestamp = message.created_at
    author = message.author
    topic = f'User ID: {author.id}'
    channel = message.channel
    fmt.set_author(name=str(author), icon_url=author.avatar_url)
    fmt.color=discord.Color.green()
    fmt.set_footer(text='Staff')
    user_id = int(message.channel.topic.split(': ')[1])
    user = client.get_user(user_id)
    await message.channel.send(embed=fmt)
    try:
        await user.send(embed=fmt)
    except discord.errors.Forbidden:
        errorfmt = discord.Embed()
        errorfmt.description = "Could not send a message to this user. (Are their DM's turned off?)"
        errorfmt.timestamp = message.created_at
        errorfmt.set_author(name="ModMail", icon_url=client.user.avatar_url)
        errorfmt.color=discord.Color.red()
        errorfmt.set_footer(text='Error')
        await message.channel.send(embed=errorfmt)
    user_name = await client.fetch_user(user_id)
    chnn = str(user_name.name)+'-'+str(user_name.discriminator)
    dts = datetime.datetime.now() #6/13/2018 at 17:20
    if(dts.minute < 10):
        cminute = "0"+str(dts.minute)
    else:
        cminute = str(dts.minute)
    msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(cminute)
    await logEntry(message, user, chnn, str(msgcreatedat), author.avatar_url, False)
    try:
        await message.delete()
    except discord.errors.notFound:
        pass
    
async def close(message):
    if not("User ID:" in message.channel.topic):
        return
    global guild
    if not os.path.exists('ClosedChatLogsCache'):
        os.makedirs('ClosedChatLogsCache') 
    dts = datetime.datetime.now()
    if(dts.minute < 10):
        cminute = "0"+str(dts.minute)
    else:
        cminute = str(dts.minute)
    msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(cminute)
    if "Direct Message with" in str(message.channel):
        user_id = message.author.id
        user_name = await client.fetch_user(user_id)
        user = client.get_user(user_id)
        chnn = str(user_name.name)+'-'+str(user_name.discriminator)
        chnn = chnn.lower()
        await logEntry(message, user, chnn, str(msgcreatedat), message.author.avatar_url, False)
        ct = datetime.datetime.now()
        tmfmt = str(ct.year)+'-'+str(ct.month)+'-'+str(ct.day)
        filename = 'OpenModMails/'+str(user_name.name)+"#"+str(user_name.discriminator)+'.MODMAIL'
        newname = str(user_name.name)+"#"+str(user_name.discriminator)+' '+str(tmfmt)+'.html'
        shutil.move(filename, 'ClosedChatLogsCache/'+newname)
        em = discord.Embed(title='Thread Closed')
        em.description = f'**{message.author}** has closed this modmail session.'
        channeltodel = discord.utils.get(guild.text_channels, name=str(chnn))
        em.color = discord.Color.red()
        try:
            await user.send(embed=em)
        except:
            pass
        chnn = "archive"
        archivechannel = discord.utils.get(guild.text_channels, name=str(chnn))
        await archivechannel.send(content=None, tts=False, embed=None, file=discord.File('ClosedChatLogsCache/'+newname))
        cacheName = "ClosedChatLogsCache/" + newname
        os.remove(cacheName)
        await channeltodel.delete()
        return
    user_id = int(message.channel.topic.split(': ')[1])
    user_name = await client.fetch_user(user_id)
    ct = datetime.datetime.now()
    tmfmt = str(ct.year)+'-'+str(ct.month)+'-'+str(ct.day)
    user = client.get_user(user_id)
    chnn = str(user_name.name)+'-'+str(user_name.discriminator)
    await logEntry(message, user, chnn, str(msgcreatedat), message.author.avatar_url, False)
    filename = 'OpenModMails/'+str(user_name.name)+"#"+str(user_name.discriminator)+'.MODMAIL'
    newname = str(user_name.name)+"#"+str(user_name.discriminator)+' '+str(tmfmt)+'.html'
    shutil.move(filename, 'ClosedChatLogsCache/'+newname)
    em = discord.Embed(title='Thread Closed')
    em.description = str(message.content[6:]) 
    em.set_footer(text=f'{message.author} has closed this modmail session.')
    em.timestamp = message.created_at
    em.color = discord.Color.red()
    try:
        await user.send(embed=em)
    except:
        pass
    chnn = "archive"
    archivechannel = discord.utils.get(guild.text_channels, name=str(chnn))
    await archivechannel.send(content=None, tts=False, embed=None, file=discord.File('ClosedChatLogsCache/'+newname))
    cacheName = "ClosedChatLogsCache/" + newname
    os.remove(cacheName)
    await message.channel.delete()
    
def guess_modroles(message):
    for role in message.guild.roles:
        if role.permissions.manage_guild:
            yield role
    
def overwrites(message, modrole=None):
    '''Permission overwrites for the guild.'''
    overwrites = {
        message.guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    if modrole:
        overwrites[modrole] = discord.PermissionOverwrite(read_messages=True)
    else:
        for role in guess_modroles(message):
            overwrites[role] = discord.PermissionOverwrite(read_messages=True)
    return overwrites

@has_permissions(manage_guild=True)
async def setupServer(message, modrole: discord.Role=None):
    if discord.utils.get(message.guild.categories, name='mod mail'):
        return await message.send('This server is already set up.')
    categ = await message.guild.create_category(
        name='mod mail',
        overwrites=overwrites(message, modrole=modrole)
        )
    await categ.edit(position=0)
    c = await message.guild.create_text_channel(name='bot-info', category=categ)
    await c.edit(topic='Generalized Bot Info.')
    await c.send(embed=help_embed(botprefix))
    await message.guild.create_text_channel(name='archive', category=categ)
    await message.channel.send('Successfully set up server.')
    
@has_permissions(manage_guild=True)
async def forceSetup(message, modrole: discord.Role=None):
    try:
        categ = await message.guild.create_category(
            name='mod mail',
            overwrites=overwrites(message, modrole=modrole)
        )
        await categ.edit(position=0)
    except:
        pass
    c = await message.guild.create_text_channel(name='bot-info', category=categ)
    await c.edit(topic='Generalized Bot Info.')
    await c.send(embed=help_embed(botprefix))
    await message.guild.create_text_channel(name='archive', category=categ)
    await message.channel.send('Successfully set up server.')
    
@has_permissions(manage_guild=True)
async def blockUser(message, id=None):
    if not("User ID:" in message.channel.topic):
        return
    if not(os.path.isfile("blockedusers.json")):
        f = open("blockedusers.json", "w")
        f.write("--This is the file containing user IDs for blocked users--")
        f.close()
    if not(id is None):
        f = open('blockedusers.json', 'a')
        idstr = str(id)
        idstr.strip()
        idstr.replace(" ", "")
        f.write('\n'+idstr)
        f.close()
        await message.channel.send('User successfully blocked from using Modmail.')
        return
    user_id = int(message.channel.topic.split(': ')[1])
    f = open("blockedusers.json", "a")
    f.write(user_id)
    f.close()
    await message.channel.send('User successfully blocked from using Modmail.')
    
@has_permissions(manage_guild=True)
async def unblockUser(message, id=None):
    if not("User ID:" in message.channel.topic):
        return
    if not(os.path.isfile("blockedusers.json")):
        f = open("blockedusers.json", "w")
        f.write("--This is the file containing user IDs for blocked users--")
        f.close()
    if not(id is None):
        idstr = str(id)
        idstr.strip()
        idstr.replace(" ", "")
        os.system(f"sed -i '/^{idstr}/d' blockedusers.json")
        await message.channel.send('User successfully unblocked.')
    else:
        await message.channel.send('Please specify a user ID.')
@has_permissions(manage_guild=True)
async def openModMail(message):
    openMailto = message.content[6:]
    openMailto = str(openMailto)
    author = message.author
    topic = f'User ID: {openMailto}'
    channel = discord.utils.get(guild.text_channels, topic=topic)
    categ = discord.utils.get(guild.categories, name='mod mail')
    user_name = await client.fetch_user(openMailto)
    chnn = str(user_name.name)+'-'+str(user_name.discriminator)
    dts = datetime.datetime.now()
    if(dts.minute < 10):
        cminute = "0"+str(dts.minute)
    else:
        cminute = str(dts.minute)
    msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(cminute)
    if(discord.utils.get(guild.text_channels, topic=topic)):
        await message.channel.send("```WARNING -- This user already has a modmail channel in this discord. The new channel has not been created.```")
        return
    #Begin creation
    shutil.copyfile("htmltemplate.txt", 'OpenModMails/'+str(user_name)+'.MODMAIL')
    await logEntry(message, user_name, chnn, str(msgcreatedat), message.author.avatar_url, True)
    em = discord.Embed(title='Thread Opened')
    em.description = f'**{message.author}** has started a modmail session.'
    em.color = discord.Color.gold()
    await user_name.send(embed=em)
    categ = discord.utils.get(guild.categories, name='mod mail')
    channel = await guild.create_text_channel(
        name=chnn,
        category=categ
    )
    await channel.edit(topic=topic)
    await channel.send("""```css
--BEGINNING OF ADMIN REQUEST--```""", embed=format_info(message, "", False))

def convertSet(set):
    return list(set)
    
@has_permissions(manage_guild=True)
async def moveChannel(message, modrole: discord.Role=None):
    if not("User ID:" in message.channel.topic):
        return
    failureEmbed = discord.Embed(title='Error while executing command')
    failureEmbed.color = discord.Color.red()
    for categ in message.guild.categories:
        try:
            await discord.CategoryChannel.edit(categ, name=categ.name.lower())
        except:
            if(showErrors):
                print(f"[ERROR] Attempted to change category {categ.name} to lowercase but failed. Continuing.")
            pass
    author = message.author
    if(dts.minute < 10):
        cminute = "0"+str(dts.minute)
    else:
        cminute = str(dts.minute)
    msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(cminute)
    if not("User ID:" in message.channel.topic):
        await message.channel.send("This is not a modmail managed channel.")
    user_id=int(message.channel.topic.split(': ')[1])
    topic = f'User ID: {user_id}'
    newCategory = message.content[6:]
    newCategory = newCategory.lower()
    if not discord.utils.get(message.guild.categories, name=newCategory.lower()):
        try:
            categ = await message.guild.create_category(
            name=newCategory, 
            overwrites=overwrites(message, modrole=modrole)
            )
        except:
            failureEmbed.description = f'Failed while attempting to create new category. Please check if the bot has permissions to manage channels in the server.'
            await message.channel.send(embed=failureEmbed)
            return
    newCategoryID = discord.utils.get(message.guild.categories, name=newCategory)
    channel = discord.utils.get(guild.text_channels, topic=topic) #Rediscover channel in the new category
    try:
        await message.channel.edit(category=newCategoryID)
    except:
        if(showErrors):
            print(f"[ERROR] Attempted to change channel to category {newCategory} but failed. Perhaps the bot lacks manage channel permissions for this category?")
        failureEmbed.description = f'Failed while attempting to move channel to category {newCategory}. Please check if the bot has the permissions to manage channels in this category.'
        await channel.send(embed=failureEmbed)
        return
    timestamp = message.created_at
    await channel.send(f'```Channel moved to {newCategory} at {msgcreatedat} by {author}```')
    user_name = await client.fetch_user(user_id)
    chnn = str(user_name.name)+'-'+str(user_name.discriminator)
    user_id = int(message.channel.topic.split(': ')[1])
    user = client.get_user(user_id)
    f = open('OpenModMails/'+str(user)+'.MODMAIL','a') 
    f.write("""<div class="msg">\n <div class="msg-left">\n<img class="msg-avatar" src="{3}"/> \n</div>\n 
<div class="msg-right"> \n
<span class="msg-user" title="{0}">{0}</span> \n
<span class="msg-date">{1}</span> \n
<div class="msg-content"> \n
{2}</div> \n
</div>
</div>
""".format(str(client.user),msgcreatedat,str(f'---Channel moved to {newCategory} at {msgcreatedat} by {author}---'), f'https://cdn.discordapp.com/avatars/{client.user.id}/{client.user.avatar}.png?size=1024'))
    f.close()
    

@client.event
async def on_message(message):
    global guild
    global user_id
    global user_name
    global chnn
    global dts
    global geticon
    user_id = message.author.id
    user_name = await client.fetch_user(user_id)
    chnn = str(user_name.name)+'-'+str(user_name.discriminator)
    topic = f'User ID: {message.author.id}'
    channel = discord.utils.get(guild.text_channels, topic=topic)
    dts = datetime.datetime.now() #6/13/2018 at 17:20
    geticon = await client.fetch_user(user_id)
    if(dts.minute < 10):
        cminute = "0"+str(dts.minute)
    else:
        cminute = str(dts.minute)
    msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(cminute)
    if not os.path.exists('OpenModMails'):
        os.makedirs('OpenModMails')
    if message.author.bot:
        return
    elif message.content.upper().startswith(f"{botprefix}OPEN"):
        await openModMail(message)
    elif message.content.upper().startswith(f"{botprefix}REPLY"):
        await reply(message)
    elif message.content.upper().startswith(f"{botprefix}CLOSE"):
        await close(message)
    elif message.content.upper().startswith(f"{botprefix}SETUPADMIN"):
        await setupServer(message)
    elif message.content.upper().startswith(f"{botprefix}SETUPADMIN /FORCE"):
        await setupServer(message)
    elif message.content.upper().startswith(f"{botprefix}BLOCK"):
        id = message.content[6:]
        await blockUser(message, id)
    elif message.content.upper().startswith(f"{botprefix}UNBLOCK"):
        id = message.content[8:]
        await unblockUser(message, id)
    elif message.content.upper().startswith(f"{botprefix}MOVE"):
        await moveChannel(message)
    elif isinstance(message.channel, discord.DMChannel):
        await processDM(message)
    elif("User ID:" in message.channel.topic):
        user_id = int(message.channel.topic.split(': ')[1])
        user = client.get_user(user_id)
        urls = re.findall(r'(https://[^\s]+)', message.content)
        types = ['.png', '.jpg', '.gif', '.jpeg', '.webp']
        for u in urls:
            if any(urlparse(u).path.endswith(x) for x in types):
                fmt.set_image(url=u)
                break
        if message.attachments:
            attach = message.attachments[0].url
            await logAttachment(attach, user, chnn, msgcreatedat, user.avatar_url, user)
        else:
            await logEntry(message, user, chnn, msgcreatedat, geticon.avatar_url, False)
client.run(token)
