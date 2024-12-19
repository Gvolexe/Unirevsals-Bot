import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ui import View, Select, button,Button,view
import DiscordUtils
import discord.utils
import asyncio
import json


intents = discord.Intents.all()

class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tracker = DiscordUtils.InviteTracker(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        
        await self.tracker.cache_invites()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.tracker.update_guild_cache(guild)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.tracker.remove_guild_cache(guild)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        cat = await ctx.guild.create_category(name='logs')
        await cat.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
        a = await ctx.guild.create_text_channel(name='welcome-logs', category=cat)
        b = await ctx.guild.create_text_channel(name='leave-logs', category=cat)
        c = await ctx.guild.create_text_channel(name='voice-logs', category=cat)
        e = await ctx.guild.create_text_channel(name='guild-logs', category=cat)
        k = await ctx.guild.create_text_channel(name='members-logs', category=cat)
        me = await ctx.guild.create_text_channel(name='message-logs', category=cat)
        g = await ctx.guild.create_text_channel(name='ban-logs', category=cat)
        h = await ctx.guild.create_text_channel(name='unban-logs', category=cat)

        with open("./Database/logs.json") as f:
            data = json.load(f)

        data[f"welcome"] = a.id
        data[f"leave"] = b.id
        data[f"voice"] = c.id
        data[f"guild"] = e.id

        with open("./Database/logs.json", 'w') as f:
            json.dump(data, f)

        with open("./Database/logs.json") as f:
            data = json.load(f)

        data[f"ban"] = g.id
        data[f"unban"] = h.id
        data[f"members"] = k.id
        data[f"message"] = me.id

        with open("./Database/logs.json", 'w') as f:
            json.dump(data, f)



    @commands.Cog.listener()
    async def on_message_delete(self, message):
    
        if message.author.bot:
            return

        with open("./Database/logs.json", "r") as f:
            data = json.load(f)
        id = data["message"]

        channel = self.bot.get_channel(id)
        
        try:
          async for entry in message.guild.audit_logs(limit=1):
            deleter = entry.user
  
            embed = discord.Embed(description=f"Message of {message.author.mention} Deleted", color=0xe74c3c)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar)
            embed.add_field(name="__Message__", value=f"{message.content}", inline=False)
            embed.add_field(name="__Channel__", value=f"{message.channel.mention}", inline=False)
            embed.add_field(name="Deleter", value=f"{deleter.mention}", inline=False)
            await channel.send(embed=embed)

        except:
            embed = discord.Embed(description=f"Message of {message.author.mention} Deleted", color=0xe74c3c)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar)
            embed.add_field(name="__Message__", value=f"{message.content}", inline=False)
            embed.add_field(name="__Channel__", value=f"{message.channel.mention}", inline=False)
            await channel.send(embed=embed)               

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if after.author.bot:
            return

        if before.content == after.content:
            return

        with open("./Database/logs.json", "r") as f:
          data = json.load(f)
        id = data["message"]

        channel = self.bot.get_channel(id)

        embed = discord.Embed(description=f"Message of {after.author.mention} Edited", color=0x3498db)
        embed.set_author(name=after.author.name, icon_url=after.author.avatar)
        embed.add_field(name="__Before__", value=f"{before.content}", inline=False)
        embed.add_field(name="__After__", value=f"{after.content}", inline=False)
        embed.add_field(name="Channel", value=f"{after.channel.mention}", inline=False)        
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):

      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["guild"]

      try:
        async for entry in after.guild.audit_logs(limit=1):
            deleter = entry.user
      except:
         deleter = 'None'

      channel = self.bot.get_channel(id)
      if len(before.roles) > len(after.roles):
        role = next(role for role in before.roles if role not in after.roles)
        embed = discord.Embed(title = f"{before.name}(*{before.id}*)'s Role has Been Removed", description = f"{role.mention}(*{role.id}*) was removed from {before.mention}.\n\n__Responsible Moderator:__: {deleter.mention}", color=0xe74c3c)
      elif len(after.roles) > len(before.roles):
        role = next(role for role in after.roles if role not in before.roles)
        embed = discord.Embed(title = f"{before.name}(*{before.id}*) Got a New Role", description = f"{role.mention}(*{role.id}*) was added to {before.mention}.\n\n__Responsible Moderator:__: {deleter.mention}", color=0x2ecc71)
      elif before.nick != after.nick:
        embed = discord.Embed(title = f"{before.name}(*{before.id}*)'s Nickname", description = f"Before: ```{before.nick}```\nAfter: ```{after.nick}```\nResponsible Moderator::\n{deleter.mention}", color=0x3498db)
      else:
        return
      embed.set_author(name = after.name, icon_url = after.avatar)
      await channel.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_user_update(self, before, after):

      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["members"]    

      channel = self.bot.get_channel(id)
      if before.avatar != after.avatar:
        embed = discord.Embed(title = f"{before.name}(*{before.id}*)'s Avatar", description = f"Changed: ```Look the Image```", color=0x3498db)
        embed.set_image(url=after.avatar)
      elif before.name != after.name:
        embed = discord.Embed(title = f"{before.name}(*{before.id}*)'s Username", description = f"Old: ```{before.name}```\nNew: ```{after.name}```", color=0x3498db)

      else:
        return
      embed.set_author(name = after.name, icon_url = after.avatar)
      await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["ban"]    

      channel = self.bot.get_channel(id)       

      try:
        async for entry in guild.audit_logs(limit=1):
            deleter = entry.user
      except:
         deleter = 'None'

      embed = discord.Embed(title = f"{member.name}(*{member.id}*)'s Banned", description=f"__Who Banned Him?__\n{deleter.mention}", color=0xe74c3c)
      embed.set_author(name = guild.name, icon_url = guild.icon)
      await channel.send(embed=embed)    

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["unban"]    

      channel = self.bot.get_channel(id) 

      try:
        async for entry in guild.audit_logs(limit=1):
            deleter = entry.user
      except:
         deleter = 'None'

      embed = discord.Embed(title = f"{user.name}(*{user.id}*)'s Unbanned", description=f"__Who Unbanned Him?__\n{deleter.mention}", color=0x2ecc71)
      embed.set_author(name = guild.name, icon_url = guild.icon)
      await channel.send(embed=embed)    

    @commands.Cog.listener()
    async def on_member_join(self, member):

      joinRole = discord.utils.get(member.guild.roles, id=1133433296588644372)
      await member.add_roles(joinRole)

      inviter = await self.tracker.fetch_inviter(member)

      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["welcome"]    

      with open("tracker.json") as f:
            data = json.load(f)

      data[str(member.id)] = inviter.id 

      with open("tracker.json", 'w') as f:
            json.dump(data, f)

      channel = self.bot.get_channel(id) 

      embed = discord.Embed(title = f"{member.name}(*{member.id}*)'s Joined", description=f"Invited By: {inviter.mention}\n\nAccount Creation Date: ```{member.created_at.strftime('%A, %d. %B %Y %H:%M:%S')}```", color=0x2ecc71)
      embed.set_author(name = member.name, icon_url = member.avatar)
      await channel.send(embed=embed)    



    @commands.Cog.listener()
    async def on_member_remove(self, member):

      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["leave"]    

      channel = self.bot.get_channel(id) 

      try:
        with open("tracker.json", "r") as f:
          data = json.load(f)
        u = data[str(member.id)]  


        embed = discord.Embed(title = f"{member.name}(*{member.id}*)'s Left", description=f"He was Invited By: <@{u}>(*{u}*)", color=0xe74c3c)
        embed.set_author(name = member.name, icon_url = member.avatar)
        await channel.send(embed=embed)    

        with open('tracker.json', 'r') as f:
            prefixes = json.load(f)
        del prefixes[str(member.id)]
        with open('tracker.json', 'w') as f:
            json.dump(prefixes, f)           

      except:
        embed = discord.Embed(title = f"{member.name}(*{member.id}*)'s Left", description=f"```I Donk know who invited him.```", color=0xe74c3c)
        embed.set_author(name = member.name, icon_url = member.avatar)
        await channel.send(embed=embed)    


    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["guild"]
       
      c = self.bot.get_channel(id)

      if before.name != after.name:
        embed = discord.Embed(description=f"{before.mention}(*{before.id}*) Name Changed.```{before.name} -> {after.name}```", color=0x1f8b4c)
        await c.send(embed=embed)

      elif before.color != after.color:
        embed = discord.Embed(description=f"{before.mention}(*{before.id}*) Color Changed.```{before.color} -> {after.color}```", color=0x1f8b4c)
        await c.send(embed=embed)

      elif before.permissions != after.permissions:
        diff = list(set(after.permissions).difference(set(before.permissions)))
        lista = []
        for changed_perm in diff:
            a = ''.join(f"{changed_perm[0]} -> {changed_perm[1]}\n").replace("_", " ").title()
            lista.append(a)
        b = ''.join(lista)

        embed = discord.Embed(description=f"{before.mention}(*{before.id}*) Pemrs Changed.```- {b}```", color=0x1f8b4c)
        await c.send(embed=embed)

      else:
         return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):

      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["guild"]

      perm_list = [perm[0] for perm in role.permissions if perm[1]]
      if perm_list == None:
         a = 'Permissions not logsured'
      else:
         a = ', '.join(perm_list).replace("_", " ").title() 

      try:
        async for entry in role.guild.audit_logs(limit=1):
            deleter = entry.user
      except:
         deleter = 'None'


      c = self.bot.get_channel(id)

      embed = discord.Embed(title=f"Role Deleted", description=f"**NAMED**: [{role.name}] / Had the Following **Perms**:\n```- {a}```\nResponsible Moderator: {deleter.mention}", color=0xe74c3c)
      await c.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_role_create(self, role):

      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["guild"]
       
      c = self.bot.get_channel(id)


      try:
        async for entry in role.guild.audit_logs(limit=1):
            deleter = entry.user
      except:
         deleter = 'None'

      embed = discord.Embed(title=f"New Role Created", description=f"{role.mention}\n```{role.id}```\nResponsible Moderator: {deleter.mention}", color=0x2ecc71)
      await c.send(embed=embed)



    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
      
      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["guild"]
       
      c = self.bot.get_channel(id)

      try:
        async for entry in channel.guild.audit_logs(limit=1):
            deleter = entry.user
      except:
         deleter = 'None'

      if channel.category == None:
         cat = 'WASNT'
      else:
         cat = f'{channel.category.name}/({channel.category.id})'


      embed = discord.Embed(title=f"Channel Deleted", description=f"**NAMED**: [{channel.name}]\n\nCategory: ```{cat}```\nResponsible Moderator: {deleter.mention}", color=0xe74c3c)
      await c.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["guild"]
       
      c = self.bot.get_channel(id)

      try:
        async for entry in channel.guild.audit_logs(limit=1):
            deleter = entry.user
      except:
         deleter = 'None'

      if channel.category == None:
         cat = 'NOT IN'
      else:
         cat = f'**{channel.category.name}/*({channel.category.id})***'

      embed = discord.Embed(title=f"New Channel Created", description=f"{channel.mention} in [{cat}] category \n```{channel.id}```\nResponsible Moderator: {deleter.mention}", color=0x2ecc71)
      await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["guild"]

      try:
        async for entry in after.guild.audit_logs(limit=1):
            deleter = entry.user
      except:
         deleter = 'None'

      c = self.bot.get_channel(id)

      if before.name != after.name:
        embed = discord.Embed(description=f"{before.mention}(*{before.id}*) Name Changed.```{before.name} -> {after.name}```\nResponsible Moderator: {deleter.mention}", color=0x1f8b4c)
        await c.send(embed=embed)

      elif before.overwrites != after.overwrites:

        embed = discord.Embed(description=f"{before.mention}(*{before.id}*) overwrites Changed.\nResponsible Moderator: {deleter.mention}", color=0x1f8b4c)
        await c.send(embed=embed)

      elif before.category != after.category:

        embed = discord.Embed(description=f"{before.mention}(*{before.id}*) Category Changed.\n```{before.category.name}({before.category.id}) -> {after.category.name}({after.category.id})```Responsible Moderator: {deleter.mention}", color=0x1f8b4c)
        await c.send(embed=embed)

      else:
         return       



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["voice"]

      c = self.bot.get_channel(id)

      try:
        async for entry in after.guild.audit_logs(limit=1):
            deleter = entry.user
            voice = entry.user  
      except:
         voice = 'By his Self'             
         deleter = 'None'       

      if before.channel != after.channel and before.channel != None and after.channel != None:
        if after.mute:
           m = 'True'
        else:
           m = 'False'

        if after.deaf:
           d = 'True'
        else:
           d = 'False'

        if after.self_mute:
           sm = 'True'
        else:
           sm = 'False'

        if after.self_deaf:
           sd = 'True'
        else:
           sd = 'False'

        if after.self_stream:
           st = 'True'
        else:
           st = 'False'           

        embed = discord.Embed(description=f"{member.mention}(*{member.id}*) Moved.\n\n{before.channel.mention} -> {after.channel.mention}```Server Mute -> {m}\nServer Deafen -> {d}\n\nSelf Mute -> {sm}\nSelf Deafen -> {sd}\nStreaming -> {st}```", color=0x1f8b4c)
        await c.send(embed=embed)


      elif before.channel is None and after.channel is not None:

        if after.mute:
           m = 'True'
        else:
           m = 'False'

        if after.deaf:
           d = 'True'
        else:
           d = 'False'

        if after.self_mute:
           sm = 'True'
        else:
           sm = 'False'

        if after.self_deaf:
           sd = 'True'
        else:
           sd = 'False'

        if after.self_stream:
           st = 'True'
        else:
           st = 'False'           

        embed = discord.Embed(description=f"{member.mention}(*{member.id}*) Joined a Voice.\n\n{after.channel.mention}```Server Mute -> {m}\nServer Deafen -> {d}\n\nSelf Mute -> {sm}\nSelf Deafen -> {sd}\nStreaming -> {st}```", color=0x2ecc71)
        await c.send(embed=embed)

      elif before.channel is not None and after.channel is None:

        embed = discord.Embed(description=f"{member.mention}(*{member.id}*) Left a Voice.\n\n{before.channel.mention}", color=0xe74c3c)
        await c.send(embed=embed)
      
      else:
         return


    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
      with open("./Database/logs.json", "r") as f:
        data = json.load(f)
      id = data["guild"]

      try:
        async for entry in after.audit_logs(limit=1):
            deleter = entry.user
      except:
         deleter = 'None'

      c = self.bot.get_channel(id)

      if before.name != after.name:
        embed = discord.Embed(description=f"{after.name}(*{after.id}*) Name Changed.```{before.name} -> {after.name}```\nResponsible Moderator: {deleter.mention}", color=0x1f8b4c)
        await c.send(embed=embed)

      elif before.icon != after.icon:
        embed = discord.Embed(description=f"{after.name}(*{after.id}*) Icon Changed.```Look Image Down```\nResponsible Moderator: {deleter.mention}", color=0x1f8b4c)
        embed.set_image(url=after.icon)
        await c.send(embed=embed)

      else:
         return             


async def setup(bot):
    await bot.add_cog(Logs(bot))