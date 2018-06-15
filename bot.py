'''
MIT License

Copyright (c) 2017 Kyb3r

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

GUILD_ID = 0 # Your Guild Id Here
svMsg = "FF" 
curdel = False
rplstat = False
clsstat = False
user_name = ""
user_id = 0
print('Initializing....')
print('Importing libraries...')
import discord
from discord.ext import commands
from urllib.parse import urlparse
import asyncio
import shutil
import textwrap
import datetime
import time
import json
import sys
import os
import re
import string
import traceback
import io
import inspect
import os.path
from contextlib import redirect_stdout
time.sleep(0.4)
client = discord.Client()
print('Complete.')
print('------------------------------------------')
time.sleep(0.1)
print('Welcome to AP_ModMail v1.4.7') 
print('------------------------------------------')
print('Connecting...')


class Modmail(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_pre)
        self.uptime = datetime.datetime.utcnow()
        self._add_commands()

    def _add_commands(self):
        '''Adds commands automatically'''
        for attr in dir(self):
            cmd = getattr(self, attr)
            if isinstance(cmd, commands.Command):
                self.add_command(cmd)

    @property
    def token(self):
        '''Returns your token wherever it is'''
        try:
            with open('config.json') as f:
                config = json.load(f)
                if config.get('TOKEN') == "your_token_here":
                    if not os.environ.get('TOKEN'):
                        self.run_wizard()
                else:
                    token = config.get('TOKEN').strip('\"')
        except FileNotFoundError:
            token = None
        return os.environ.get('TOKEN') or token
    
    @staticmethod
    async def get_pre(bot, message):
        '''Returns the prefix.'''
        with open('config.json') as f:
            prefix = json.load(f).get('PREFIX')
        return os.environ.get('PREFIX') or prefix or 'm.'

    @staticmethod
    def run_wizard():
        '''Wizard for first start'''
        print('------------------------------------------')
        token = input('Enter your token:\n> ')
        print('------------------------------------------')
        data = {
                "TOKEN" : token,
            }
        with open('config.json','w') as f:
            f.write(json.dumps(data, indent=4))
        print('------------------------------------------')
        print('Restarting...')
        print('------------------------------------------')
        os.execv(sys.executable, ['python'] + sys.argv)

    @classmethod
    def init(cls, token=None):
        '''Starts the actual bot'''
        bot = cls()
        if token:
            to_use = token.strip('"')
        else:
            to_use = bot.token.strip('"')
        try:
            bot.run(to_use, activity=discord.Game(os.getenv('STATUS')), reconnect=True)
        except Exception as e:
            raise e

    async def on_connect(self):
        print('---------------')
        print('Modmail connected!')
        status = os.getenv('STATUS')
        if status:
            print(f'Setting Status to {status}')
        else:
            print('No status set.')

    @property
    def guild_id(self):
        from_heroku = os.environ.get('GUILD_ID')
        return int(from_heroku) if from_heroku else GUILD_ID

    async def on_ready(self):
        '''Bot startup, sets uptime.'''
        self.guild = discord.utils.get(self.guilds, id=self.guild_id)
        print(textwrap.dedent(f'''
        ---------------
        Client is ready!
        ---------------
        Authors: Kyb3r#7220, Foxtrot2400#7933, TylerS1066#7019
        ---------------
        Logged in as: {self.user}
        User ID: {self.user.id}
        ---------------
        '''))

    def overwrites(self, ctx, modrole=None):
        '''Permision overwrites for the guild.'''
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

        if modrole:
            overwrites[modrole] = discord.PermissionOverwrite(read_messages=True)
        else:
            for role in self.guess_modroles(ctx):
                overwrites[role] = discord.PermissionOverwrite(read_messages=True)

        return overwrites

    def help_embed(self, prefix):
        em = discord.Embed(color=0x00FFFF)
        em.set_author(name='Mod Mail - Help', icon_url=self.user.avatar_url)
        em.description = 'This bot is a python implementation of a stateless "Mod Mail" bot. ' \
                         'Made by Kyb3r and improved by the suggestions of others. ' \
                         'Additional edits made by Foxtrot2400 and TylerS0166. This bot ' \
                         'saves no data and utilises channel topics for storage and syncing.' 
                 

        cmds = f'`{prefix}setup [modrole] <- (optional)` - Command that sets up the bot.\n' \
               f'`{prefix}reply <message...>` - Sends a message to the current thread\'s recipient.\n' \
               f'`{prefix}close` - Closes the current thread and deletes the channel.\n' \
               f'`{prefix}disable` - Closes all threads and disables modmail for the server.\n' \
               f'`{prefix}customstatus` - Sets the Bot status to whatever you want.\n' \
               f'`{prefix}block` - Blocks a user from using modmail!\n' \
               f'`{prefix}unblock` - Unblocks a user from using modmail!\n' \
               f'`{prefix}reset` - Resets modmail. Only use this if something is broken.' \

        warn = 'Refrain from manually deleting the category or channels as it will break the system. ' \
               'Modifying the channel topic will also break the system.'
        em.add_field(name='Commands', value=cmds)
        em.add_field(name='Warning', value=warn)
        em.add_field(name='Github', value='https://github.com/verixx/modmail')
        em.set_footer(text='Star the repository to unlock hidden features!')

        return em

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx, *, modrole: discord.Role=None):
        '''Sets up a server for modmail'''
        if discord.utils.get(ctx.guild.categories, name='Mod Mail'):
            return await ctx.send('This server is already set up.')

        categ = await ctx.guild.create_category(
            name='Mod Mail', 
            overwrites=self.overwrites(ctx, modrole=modrole)
            )
        await categ.edit(position=0)
        c = await ctx.guild.create_text_channel(name='bot-info', category=categ)
        await c.edit(topic='Manually add user id\'s to block users.\n\n'
                           'Blocked\n-------\n\n')
        await c.send(embed=self.help_embed(ctx.prefix))
        await ctx.guild.create_text_channel(name='archive', category=categ)
        await ctx.send('Successfully set up server.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        '''Close all threads and disable modmail.'''
        categ = discord.utils.get(ctx.guild.categories, name='Mod Mail')
        if not categ:
            return await ctx.send('This server is not set up.')
        for category, channels in ctx.guild.by_category():
            if category == categ:
                for chan in channels:
                    if 'User ID:' in str(chan.topic):
                        user_id = int(chan.topic.split(': ')[1])
                        user = self.get_user(user_id)
                        await user.send(f'**{ctx.author}** has closed this modmail session.')
                    await chan.delete()
        await categ.delete()
        await ctx.send('Disabled modmail.')
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, *, modrole: discord.Role=None):
        '''Resets the bot and sets up the server again.
        Only use this command if a category or channel 
        is missing, or the bot is not working properly.'''
        await ctx.send('Resetting modmail.')
        categ = discord.utils.get(ctx.guild.categories, name='Mod Mail')
        if not categ:
            return await ctx.send('This server is not set up.')
        for category, channels in ctx.guild.by_category():
            if category == categ:
                for chan in channels:
                    if 'User ID:' in str(chan.topic):
                        user_id = int(chan.topic.split(': ')[1])
                        user = self.get_user(user_id)
                        await user.send(f'**{ctx.author}** has closed this modmail session.')
                    await chan.delete()
        await categ.delete()
        await ctx.send('Server is now clean. Setting up...')
        categ = await ctx.guild.create_category(
            name='Mod Mail', 
            overwrites=self.overwrites(ctx, modrole=modrole)
            )
        await categ.edit(position=0)
        c = await ctx.guild.create_text_channel(name='bot-info', category=categ)
        await c.edit(topic='Manually add user id\'s to block users.\n\n'
                           'Blocked\n-------\n\n')
        await c.send(embed=self.help_embed(ctx.prefix))
        await ctx.guild.create_text_channel(name='archive', category=categ)
        await ctx.send('Successfully reset the server.')
        
        

    @commands.command(name='close')
    @client.event
    async def _close(self, ctx):
        '''Close the current thread.'''
        global clsstat
        global curdel
        clsstat = True
        if not os.path.exists('ClosedChatLogsCache'):
            os.makedirs('ClosedChatLogsCache') 
        
        
        dts = datetime.datetime.now() #6/13/2018 at 17:20
        msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(dts.minute)

        if "Direct Message with" in str(ctx.channel):
            user_id = ctx.author.id
            user_name = await self.get_user_info(user_id)     
            ct = datetime.datetime.now()
            tmfmt = str(ct.year)+'-'+str(ct.month)+'-'+str(ct.day)
            filename = 'OpenModMails/'+str(user_name.name)+"#"+str(user_name.discriminator)+'.MODMAIL'
            newname = str(user_name.name)+"#"+str(user_name.discriminator)+' '+str(tmfmt)+'.html'
            flcount = 2
            fltrip = False
            line = '\n <!DOCTYPE html>\n <html lang="en"> \n <head> \n <title>{0}</title> \n'.format(self.guild)
            message = ctx.message
            author = message.author
            geticon = await self.get_user_info(user_id)
            
            curdel = True
            #If we have to go here, this was called from a DM.
            chnn = str(user_name.name)+'-'+str(user_name.discriminator)
            nmfmt = str(user_name.name)+'#'+str(user_name.discriminator)
            botname = str(self.user)
            chnn = chnn.lower()
            channeltodel = discord.utils.get(self.guild.text_channels, name=str(chnn))
            with open(filename, 'r+') as f:
                file_data = f.read()
                f.seek(0, 0)
                f.write(line.rstrip('\r\n') + '\n' + file_data)
                f.close
            cls = open(filename, 'a')
            cls.write("""<div class="msg">\n <div class="msg-left">\n<img class="msg-avatar" src="{2}"/> \n</div>\n 
<div class="msg-right"> \n
<span class="msg-user" title="{0}">{0}</span> \n
<span class="msg-date">{1}</span> \n
<div class="msg-content"> \n
/close </div> \n
</div>
</div>
""".format(str(author),msgcreatedat, geticon.avatar_url))
            cls.write('</div> \n</body> \n </html>')
            cls.close()
            if os.path.isfile('ClosedChatLogsCache/'+newname):
                 while fltrip == False:
                      newname = str(user_name.name)+"#"+str(user_name.discriminator)+' '+str(tmfmt)+"("+str(flcount)+")"+'.html'
                      if os.path.isfile('ClosedChatLogsCache/'+newname):
                           flcount = flcount + 1
                      else:
                           shutil.move(filename, 'ClosedChatLogsCache/'+newname)
                           fltrip = True
            else:
                 shutil.move(filename, 'ClosedChatLogsCache/'+newname)
            if os.path.isfile(filename):
                 os.rename(filename, newname)
            user = self.get_user(user_id)
            em = discord.Embed(title='Thread Closed')
            em.description = f'**{ctx.author}** has closed this modmail session.'
            em.color = discord.Color.red()
            try:
                await user.send(embed=em)
            except:
                pass
            chnn = "archive"
            archivechannel = discord.utils.get(self.guild.text_channels, name=str(chnn))
            await archivechannel.send(content=None, tts=False, embed=None, file=discord.File('ClosedChatLogsCache/'+newname))
            await channeltodel.delete()
            os.system('rm "ClosedChatLogsCache/'+newname+'"')
            return 
        user_id = int(ctx.channel.topic.split(': ')[1])
        user_name = await self.get_user_info(user_id)
        author = str(user_name.name)+"#"+str(user_name.discriminator)
        ct = datetime.datetime.now()
        tmfmt = str(ct.year)+'-'+str(ct.month)+'-'+str(ct.day)
        filename = 'OpenModMails/'+str(user_name.name)+"#"+str(user_name.discriminator)+'.MODMAIL'
        newname = str(user_name.name)+"#"+str(user_name.discriminator)+' '+str(tmfmt)+'.html'
        flcount = 2
        fltrip = False
        line = '\n <!DOCTYPE html>\n <html lang="en"> \n <head> \n <title>{0}</title> \n'.format(self.guild)
        message = ctx.message
        geticon = await self.get_user_info(user_id)
        closerid = ctx.author.id
        closericon = await self.get_user_info(closerid)
        closername = str(closericon.name)+"#"+str(closericon.discriminator)
        
        curdel = True
        if 'User ID:' not in str(ctx.channel.topic):
            return await ctx.send('This is not a modmail thread.')

        
        with open(filename, 'r+') as f:
             file_data = f.read()
             f.seek(0, 0)
             f.write(line.rstrip('\r\n') + '\n' + file_data)
             f.close
 
        cls = open(filename, 'a')
        cls.write("""<div class="msg">\n <div class="msg-left">\n<img class="msg-avatar" src="{2}"/> \n</div>\n 
<div class="msg-right"> \n
<span class="msg-user" title="{0}">{0}</span> \n
<span class="msg-date">{1}</span> \n
<div class="msg-content"> \n
/close </div> \n
</div>
</div>
""".format(closername,msgcreatedat, closericon.avatar_url))
        cls.write('</div> \n</body> \n </html>')
        cls.close()
        if os.path.isfile('ClosedChatLogsCache/'+newname):
            while fltrip == False:
                 newname = str(user_name.name)+"#"+str(user_name.discriminator)+' '+str(tmfmt)+"("+str(flcount)+")"+'.html'
                 if os.path.isfile('ClosedChatLogsCache/'+newname):
                      flcount = flcount + 1
                 else:
                      shutil.move(filename, 'ClosedChatLogsCache/'+newname)
                      fltrip = True
        else:
            shutil.move(filename, 'ClosedChatLogsCache/'+newname)
        if os.path.isfile(filename):
            os.rename(filename, newname)
        user = self.get_user(user_id)
        em = discord.Embed(title='Thread Closed')
        em.description = f'**{ctx.author}** has closed this modmail session.'
        em.color = discord.Color.red()
        chnn = "archive"
        archivechannel = discord.utils.get(self.guild.text_channels, name=str(chnn))
        await archivechannel.send(content=None, tts=False, embed=None, file=discord.File('ClosedChatLogsCache/'+newname))
        try:
            await user.send(embed=em)
        except:
            pass
        os.system('rm "ClosedChatLogsCache/'+newname+'"')
        await ctx.channel.delete()

    @commands.command()
    async def ping(self, ctx):
        """Pong! Returns your websocket latency."""
        em = discord.Embed()
        em.title ='Pong! Websocket Latency:'
        em.description = f'{self.ws.latency * 1000:.4f} ms'
        em.color = 0x00FF00
        await ctx.send(embed=em)

    def guess_modroles(self, ctx):
        '''Finds roles if it has the manage_guild perm'''
        for role in ctx.guild.roles:
            if role.permissions.manage_guild:
                yield role

    def format_info(self, message):
        '''Get information about a member of a server
        supports users from the guild or not.'''
        user = message.author
        server = self.guild
        member = self.guild.get_member(user.id)
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
        
        em.add_field(name='Message', value=message.content, inline=False)

        return em

    async def send_mail(self, message, channel, mod):
        author = message.author
        fmt = discord.Embed()
        fmt.description = message.content
        fmt.timestamp = message.created_at
        if os.path.isfile('OpenModMails/'+str(author)+'.MODMAIL'):
             f = open('OpenModMails/'+str(author)+'.MODMAIL', 'a')
        else:
             shutil.copyfile("htmltemplate.txt", 'OpenModMails/'+str(author)+'.MODMAIL')
             f = open('OpenModMails/'+str(author)+'.MODMAIL', 'a')
             user_id = author.id
             geticon = await self.get_user_info(user_id) 
             f.write("""
<div id="info">\n
<div class="info-left">\n
<img class="guild-icon" src="{2}"/>
</div>\n
<div class="info-right">\n
<div class="guild-name">{0}</div>\n
<div class="channel-name">#{1}</div>\n
<div class="channel-topic"></div>\n
</div>\n
</div>\n
<div id\n
<did id="log">\n'""".format(message.guild.name, message.channel.name, self.guild.icon))
             
        
        if rplstat == False:
             user_id = author.id
             geticon = await self.get_user_info(user_id)
             dts = datetime.datetime.now() #6/13/2018 at 17:20
             msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(dts.minute)
#             user_id = int(message.channel.topic.split(': ')[1])
#             user_name = await self.get_user_info(user_id)
#             author = str(user_name.name)+"#"+str(user_name.discriminator)
             f.write("""<div class="msg">\n <div class="msg-left">\n<img class="msg-avatar" src="{3}" />
\n</div>\n 
<div class="msg-right"> \n
<span class="msg-user" title="{0}">{0}</span> \n
<span class="msg-date">{1}</span> \n
<div class="msg-content"> \n
{2}</div> \n
</div>
</div>
""".format(str(author),msgcreatedat,message.content, geticon.avatar_url))
        f.close()
        urls = re.findall(r'(https?://[^\s]+)', message.content)

        types = ['.png', '.jpg', '.gif', '.jpeg', '.webp']

        for u in urls:
            if any(urlparse(u).path.endswith(x) for x in types):
                fmt.set_image(url=u)
                break

        if mod:
            fmt.color=discord.Color.green()
            fmt.set_author(name=str(author), icon_url=author.avatar_url)
            fmt.set_footer(text='Moderator')
        else:
            fmt.color=discord.Color.gold()
            fmt.set_author(name=str(author), icon_url=author.avatar_url)
            fmt.set_footer(text='User')

        embed = None

        if message.attachments:
            fmt.set_image(url=message.attachments[0].url)

        await channel.send(embed=fmt)

    async def process_reply(self, message):
        try:
            await message.delete()
        except discord.errors.NotFound:
            pass
        await self.send_mail(message, message.channel, mod=True)
        user_id = int(message.channel.topic.split(': ')[1])
        user = self.get_user(user_id)
        await self.send_mail(message, user, mod=True)

    def format_name(self, author):
        name = author.name
        new_name = ''
        for letter in name:
            if letter in string.ascii_letters + string.digits:
                new_name += letter
        if not new_name:
            new_name = 'null'
        new_name += f'-{author.discriminator}'
        return new_name

    @property
    def blocked_em(self):
        em = discord.Embed(title='Message not sent!', color=discord.Color.red())
        em.description = 'You have been blocked from using modmail.'
        return em

    async def process_modmail(self, message, svMsg):
        '''Processes messages sent to the bot.'''
        global curdel
        if curdel == True:
            curdel = False
            return
        try:
            await message.add_reaction('✅')
        except:
            pass

        guild = self.guild
        author = message.author
        topic = f'User ID: {author.id}'
        channel = discord.utils.get(guild.text_channels, topic=topic)
        categ = discord.utils.get(guild.categories, name='Mod Mail')
        top_chan = categ.channels[0] #bot-info
        blocked = top_chan.topic.split('Blocked\n-------')[1].strip().split('\n')
        blocked = [x.strip() for x in blocked]

        if str(message.author.id) in blocked:
            return await message.author.send(embed=self.blocked_em)
        
        em = discord.Embed(title='Thanks for the message!')
        em.description = 'Our moderation team will get back to you as soon as possible!'
        em.color = discord.Color.green()

        if channel is not None:
            await self.send_mail(message, channel, mod=False)
        else:
            await message.author.send(embed=em)
            channel = await guild.create_text_channel(
                name=self.format_name(author),
                category=categ
                )
            await channel.edit(topic=topic)
            await channel.send("""```css
--BEGINNING OF HELP REQUEST--```""", embed=self.format_info(message))
        author = message.author
        if categ.name == 'Mod Mail' and 'User ID:' in channel.topic and os.path.isfile('OpenModMails/'+str(author)+'.MODMAIL'):
             return
        user_id = author.id
        geticon = await self.get_user_info(user_id) 
        shutil.copyfile("htmltemplate.txt", 'OpenModMails/'+str(author)+'.MODMAIL')
        f = open('OpenModMails/'+str(author)+'.MODMAIL','a')
        user_name = await self.get_user_info(user_id)
        chnn = str(user_name.name)+'-'+str(user_name.discriminator)
        dts = datetime.datetime.now() #6/13/2018 at 17:20
        msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(dts.minute)
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
<div id\n'""".format(self.guild.name, chnn, self.guild.icon, self.guild.id))
#        user_id = int(message.channel.topic.split(': ')[1])
#        user_name = await self.get_user_info(user_id)
#        author = str(user_name.name)+"#"+str(user_name.discriminator)
        f.write("""<div class="msg">\n <div class="msg-left">\n<img class="msg-avatar" src="{3}"/> \n</div>\n 
<div class="msg-right"> \n
<span class="msg-user" title="{0}">{0}</span> \n
<span class="msg-date">{1}</span> \n
<div class="msg-content"> \n
{2}</div> \n
</div>
</div>
""".format(str(author),msgcreatedat,str(svMsg), geticon.avatar_url))
        f.close()
        

    async def on_message(self, message):
        global rplstat
        global clsstat
        global svMsg
        author = message.author
        user_id = author.id
        geticon = await self.get_user_info(user_id)
        svMsg = str(message.content)
        if not os.path.exists('OpenModMails'):
            os.makedirs('OpenModMails')
        if message.author.bot:
            return
        await self.process_commands(message)
        if isinstance(message.channel, discord.DMChannel):
            await self.process_modmail(message, svMsg)
        else:
            if rplstat == True:
               rplstat = False
               return
            if clsstat == True:
               clsstat = False
               return
            catego = discord.utils.get(message.guild.categories, id=message.channel.category_id)
            if catego.name == 'Mod Mail' and 'User ID:' in message.channel.topic:  
                 user_id = int(message.channel.topic.split(': ')[1])
                 user_name = await self.get_user_info(user_id)
                 author = str(user_name.name)+"#"+str(user_name.discriminator)
                 dts = datetime.datetime.now() #6/13/2018 at 17:20
                 msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(dts.minute)
                 f = open('OpenModMails/'+str(author)+'.MODMAIL', 'a')
                 
                 f.write("""<div class="msg">\n <div class="msg-left">\n<img class="msg-avatar" src="{3}"/> \n</div>\n 
<div class="msg-right"> \n
<span class="msg-user" title="{0}">{0}</span> \n
<span class="msg-date">{1}</span> \n
<div class="msg-content"> \n
{2}</div> \n
</div>
</div>
""".format(str(author),msgcreatedat,svMsg, geticon.avatar_url))
                 f.close()
            else:
                 #print('[DEBUG] Not in modmail.')
                 return

    @commands.command()
    async def reply(self, ctx, *, msg):
        '''Reply to users using this command.'''
       
        global rplstat
        global svMsg
        author = ctx.message.author
        user_id = author.id
        geticon = await self.get_user_info(user_id)
        rplstat = True
        categ = discord.utils.get(ctx.guild.categories, id=ctx.channel.category_id)
        if categ is not None:
            if categ.name == 'Mod Mail':
                if 'User ID:' in ctx.channel.topic:
                    ctx.message.content = msg
                    await self.process_reply(ctx.message)
                user_id = int(ctx.channel.topic.split(': ')[1])
                user_name = await self.get_user_info(user_id)
                author = str(user_name.name)+"#"+str(user_name.discriminator)
                f = open('OpenModMails/'+str(user_name.name)+"#"+str(user_name.discriminator)+'.MODMAIL','a')
                dts = datetime.datetime.now() #6/13/2018 at 17:20
                msgcreatedat = str(dts.month)+"/"+str(dts.day)+"/"+str(dts.year)+" at "+str(dts.hour)+":"+str(dts.minute)
                f.write("""<div class="msg">\n <div class="msg-left">\n<img class="msg-avatar" src="{3}"/> \n</div>\n 
<div class="msg-right"> \n
<span class="msg-user" title="{0}">{0}</span> \n
<span class="msg-date">{1}</span> \n
<div class="msg-content"> \n
/reply {2}</div> \n
</div>
</div>
""".format(str(author),msgcreatedat,msg, geticon.avatar_url))
                f.close()
                
                

    @commands.command(name="customstatus", aliases=['status', 'presence'])
    @commands.has_permissions(administrator=True)
    async def _status(self, ctx, *, message):
        '''Set a custom playing status for the bot.'''
        if message == 'clear':
            return await self.change_presence(activity=None)
        await self.change_presence(activity=discord.Game(message))
        await ctx.send(f"Changed status to **{message}**")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def block(self, ctx, id=None):
        '''Block a user from using modmail. You must use their ID, not a mention.'''
        if id is None:
            if 'User ID:' in str(ctx.channel.topic):
                id = ctx.channel.topic.split('User ID: ')[1].strip()
            else:
                return await ctx.send('No User ID provided.')

        categ = discord.utils.get(ctx.guild.categories, name='Mod Mail')
        top_chan = categ.channels[0] #bot-info
        topic = str(top_chan.topic)
        topic += id + '\n'

        if id not in top_chan.topic:  
            await top_chan.edit(topic=topic)
            await ctx.send('User successfully blocked!')
        else:
            await ctx.send('User is already blocked.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unblock(self, ctx, id=None):
        '''Unblocks a user from using modmail. You must use their ID, not a mention.'''
        if id is None:
            if 'User ID:' in str(ctx.channel.topic):
                id = ctx.channel.topic.split('User ID: ')[1].strip()
            else:
                return await ctx.send('No User ID provided.')

        categ = discord.utils.get(ctx.guild.categories, name='Mod Mail')
        top_chan = categ.channels[0] #bot-info
        topic = str(top_chan.topic)
        topic = topic.replace(id+'\n', '')

        if id in top_chan.topic:
            await top_chan.edit(topic=topic)
            await ctx.send('User successfully unblocked!')
        else:
            await ctx.send('User is not already blocked.')

    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates python code"""
        allowed = [int(x) for x in os.getenv('OWNERS', '').split(',')]
        if ctx.author.id not in allowed: 
            return
        
        env = {
            'bot': self,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await err.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        await ctx.send('```Result is too long to send.```')
            else:
                self._last_result = ret
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    await ctx.send('```Result is too long to send.```')
        if out:
            await ctx.message.add_reaction('\u2705') #tick
        if err:
            await ctx.message.add_reaction('\u2049') #x
        else:
            await ctx.message.add_reaction('\u2705')

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')
        
if __name__ == '__main__':
    Modmail.init()

