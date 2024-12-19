import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ui import View, Select, button,Button,view
import asyncio
import discord.utils
import platform
import asyncio
import sys
import os
import json as jsond #api fix
from Config.config import *

def clear():
    if platform.system() == 'Windows':
        os.system('cls & title © Unirevsals Bot')  # clear console, change title
    elif platform.system() == 'Linux':
        os.system('clear')  # clear console
        sys.stdout.write("\x1b]0;© Unirevsals Bot\x07")  # change title
    elif platform.system() == 'Darwin':
        os.system("clear && printf '\e[3J'")  # clear console
        os.system('''echo - n - e "\033]0;© Unirevsals Bot\007"''')  # change title

class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        pass



bot = PersistentViewBot()





@bot.event
async def on_ready(): 
        clear()   
        print(nexus_logo)
        await asyncio.sleep(0.6)
        print("----------------------------------------------------------------------")
        await asyncio.sleep(0.6)
        print(f'|▪ Base: Logged in as: {bot.user} | {bot.user.id} ')
        await asyncio.sleep(0.6)
        print("----------------------------------------------------------------------") 
        await asyncio.sleep(0.6)
        print(f'|▪ Base: ⏳ Ping => [{round(bot.latency*1000)}] ms                                 ')
        await asyncio.sleep(0.6)
        print("----------------------------------------------------------------------")
        await bot.change_presence(status=discord.Status.dnd ,activity=discord.Activity(type=discord.ActivityType.watching, name=bot_activity_text,))






@bot.event
async def on_message_delete(message):

    channel = discord.utils.get(message.guild.channels, id=ghost_ping_channel)

    if message.author.bot: return

    elif message.mentions:

        for m in message.mentions:

            if m.bot or m.id == message.author.id: return
            
            embed = discord.Embed(title = f'>>> __**Ghost ping detected!**__', description = f"{message.author.mention} __**ghost pinged**__ {m.mention}\n \n>>> __**Original message:**__ __{message.content}__", timestamp = message.created_at)
            embed.set_author(name=copyright_text, icon_url=logo_url)
            embed.set_thumbnail(url=logo_url)
            
            await channel.send(message.author.mention,embed = embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, args):
#   embed = discord.Embed(description=f'{args}',color=0x23c0da)
#   embed.set_author(name=copyright_text, icon_url=logo_url)
#   embed.set_thumbnail(url=logo_url)
#   await ctx.send(embed=embed)
  await ctx.message.delete()
  await ctx.send(f"{args}")
  




    
#! Start of autorole    
@bot.event
async def on_member_join(member):
  if is_autorole_enabled == True:
    role = discord.utils.get(member.guild.roles, id=autoroleid)
    await member.add_roles(role)
  else:
    pass
#! End of autorole














   


    
    
    
    
    
    
    
    
    
#! UNIREVSALS BOT START
    









class UnirevsalsCommonInfoSelect(discord.ui.Select):
    def __init__(self):


        options=[
        discord.SelectOption(value="01",label="BackBoard", emoji="⚙", description="Displays info about the Backbored"),
        discord.SelectOption(value="02",label="Field Pictures", emoji="📷", description="Displays Pictures of the Field"),
        discord.SelectOption(value="03",label="Point List", emoji="📜", description="Displays the list of points"),
        discord.SelectOption(value="04",label="Todo List", emoji="🙍‍♂️", description="Displays the task that have to be done for our next meeting"),
        discord.SelectOption(value="05",label="Local LeaderBored", emoji="⏱", description="Displays our best times during practise")
        ]

        super().__init__(placeholder="Choose the type of data you want to view", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "01":
          backembed = discord.Embed(title = f'BackBoard', description = f"",color=0x03b1fc)
          backembed.add_field(name="First Set Line" , value="`12 3/8in` | `31.43cm`", inline= False)
          backembed.add_field(name="Seccond Set Line" , value="`19in` | `48.26cm`", inline=False)
          backembed.add_field(name="Third Set Line" , value="`25 3/4in` | `65.405cm`",inline=False)
          await interaction.response.send_message(embed=backembed,ephemeral=True)
          
        if self.values[0] == "02":
          pic1bed = discord.Embed(title = f'Picture 1', description = f"",color=0x03b1fc)
          pic1bed.set_image(url="https://i.imgur.com/SCQFc2w.png")
          pic2bed = discord.Embed(title = f'Picture 2', description = f"",color=0x03b1fc)
          pic2bed.set_image(url="https://i.imgur.com/Sjo9fsJ.jpg")
          pic3bed = discord.Embed(title = f'Picture 3', description = f"",color=0x03b1fc)
          pic3bed.set_image(url="https://i.imgur.com/TGxmZIR.jpg")
          await interaction.response.send_message(embed=pic1bed,ephemeral=True)
          await interaction.followup.send(embed=pic2bed,ephemeral=True)
          await interaction.followup.send(embed=pic3bed,ephemeral=True)
        if self.values[0] == "03":
          point = discord.Embed(title = f'Points', description = f"",color=0x03b1fc)
          point.set_image(url="https://i.imgur.com/qX2oce5.png")
          await interaction.response.send_message(embed=point,ephemeral=True)  
        if self.values[0] == "04":
          
          
          
          
          
          
          
          server = interaction.guild
          giannhs = discord.utils.get(server.members, id = Giannhs_id)
          GiorgosL = discord.utils.get(server.members, id = GiorgosL_id)
          GiorgosA = discord.utils.get(server.members, id = GiorgosA_id)
          Alex = discord.utils.get(server.members, id = Alex_id)
          Aris = discord.utils.get(server.members, id = Aris_id)
          Hlias = discord.utils.get(server.members, id = Hlias_id)
          Melissa = discord.utils.get(server.members, id = Melissa_id)
          Markos = discord.utils.get(server.members, id = Markos_id)
          Despina = discord.utils.get(server.members, id = Despina_id)


          def set_task(user, task):
              try:
                  with open('tasks.json', 'r') as json_file:
                      user_tasks = jsond.load(json_file)
              except FileNotFoundError:
                  user_tasks = {
                      "Giannhs": "",
                      "GiorgosL": "",
                      "GiorgosA": "",
                      "Alex": "",
                      "Aris": "",
                      "Hlias": "",
                      "Melissa": "",
                      "Markos": "",
                      "Despina": ""
                  }
              if user in user_tasks:
                  if user_tasks[user]:
                      print(f"Task exists for {user}. Overwriting...")
                  user_tasks[user] = task
                  print(f"Task overwritten for {user}")
                  with open('tasks.json', 'w') as json_file:
                      jsond.dump(user_tasks, json_file)

          # Function to get tasks for a specific user ID
          def get_task(user):
              try:
                  with open('tasks.json', 'r') as json_file:
                      user_tasks = jsond.load(json_file)
              except FileNotFoundError:
                  user_tasks = {
                      "Giannhs": "",
                      "GiorgosL": "",
                      "GiorgosA": "",
                      "Alex": "",
                      "Aris": "",
                      "Hlias": "",
                      "Melissa": "",
                      "Markos": "",
                      "Despina": ""
                  }
              if user in user_tasks:
                  return user_tasks[user]
              else:
                  return f"No task found for {user}"
          Giannhs_task = get_task("Giannhs")
          GiorgosL_task = get_task("GiorgosL")
          GiorgosA_task = get_task("GiorgosA")
          Alex_task = get_task("Alex")
          Aris_task = get_task("Aris")
          Hlias_task = get_task("Hlias")
          Melissa_task = get_task("Melissa")
          Markos_task = get_task("Markos")
          Despina_task = get_task("Despina")



          
          
          
          
          
          tasks = discord.Embed(title = f'Tasks', description = f"",color=0x03b1fc)
          tasks.add_field(name=f"{giannhs.display_name} Task",value=f"{Giannhs_task}",inline=False)
          tasks.add_field(name=f"{GiorgosL.display_name} Task",value=f"{GiorgosA_task}",inline=False)
          tasks.add_field(name=f"{GiorgosA.display_name} Task",value=f"{GiorgosL_task}",inline=False)
          tasks.add_field(name=f"{Alex.display_name} Task",value=f"{Alex_task}",inline=False)
          tasks.add_field(name=f"{Aris.display_name} Task",value=f"{Aris_task}",inline=False)
          tasks.add_field(name=f"{Hlias.display_name} Task",value=f"{Hlias_task}",inline=False)
          tasks.add_field(name=f"{Melissa.display_name} Task",value=f"{Melissa_task}",inline=False)
          tasks.add_field(name=f"{Markos.display_name} Task",value=f"{Markos_task}",inline=False)
          tasks.add_field(name=f"{Despina.display_name} Task",value=f"{Despina_task}",inline=False)
          await interaction.response.send_message(embed=tasks,ephemeral=True)
        if self.values[0] == "05":
            pass
          
          
                  
          
          
          
          
          
        await interaction.message.edit(view=UnirevsalsCommonInfoViewFix())


class UnirevsalsCommonInfoView(discord.ui.View):
    def __init__(self):
        super().__init__()


        self.add_item(UnirevsalsCommonInfoSelect())
class UnirevsalsCommonInfoViewFix(discord.ui.View):
    def __init__(self):
        super().__init__()


        self.add_item(UnirevsalsCommonInfoSelect())

@bot.command()
async def udata(ctx):

    view = UnirevsalsCommonInfoView()
    await ctx.send(view=view)
      




















#! Unirevsals Set Task With Modal
class SetTodo_Modal(discord.ui.Modal, title='Set Todo 1/2'):
    def __init__(self):
        super().__init__(timeout=None)
    Giannhs_tasks = discord.ui.TextInput(label='Tasks For Giannhs', style=discord.TextStyle.long, required=True, max_length=2000)
    GeorgeL_tasks = discord.ui.TextInput(label='Tasks For George L', style=discord.TextStyle.long, required=True, max_length=2000)
    GerogeA_tasks = discord.ui.TextInput(label='Tasks For George A', style=discord.TextStyle.long, required=True, max_length=2000)
    Alex_tasks = discord.ui.TextInput(label='Tasks For Alex', style=discord.TextStyle.long, required=True, max_length=2000)
    Aris_tasks = discord.ui.TextInput(label='Tasks For Aris', style=discord.TextStyle.long, required=True, max_length=2000)



    async def on_submit(self, interaction: discord.Interaction):
        def set_task(user, task):
            try:
                with open('tasks.json', 'r') as json_file:
                    user_tasks = jsond.load(json_file)
            except FileNotFoundError:
                user_tasks = {
                    "Giannhs": "",
                    "GiorgosL": "",
                    "GiorgosA": "",
                    "Alex": "",
                    "Aris": "",
                    "Hlias": "",
                    "Melissa": "",
                    "Markos": "",
                    "Despina": ""
                }
            if user in user_tasks:
                user_tasks[user] = task
                with open('tasks.json', 'w') as json_file:
                    jsond.dump(user_tasks, json_file)
        
    
        

        await interaction.response.send_modal(SetTodo_Modal2())
 

        




class SetTodo_Modal2(discord.ui.Modal, title='Set Todo part 2/2'):
    def __init__(self):
        super().__init__(timeout=None)
    Hlias_tasks = discord.ui.TextInput(label='Tasks For Hlias', style=discord.TextStyle.long, required=True, max_length=2000)
    Melissa_tasks = discord.ui.TextInput(label='Tasks For Melissa', style=discord.TextStyle.long, required=True, max_length=2000)
    Despina_tasks = discord.ui.TextInput(label='Tasks For Despina', style=discord.TextStyle.long, required=True, max_length=2000)


    async def on_submit(self, interaction: discord.Interaction):


        embed = discord.Embed(description=f">>> You setted the todo list successfully")

        await interaction.response.send_message(interaction.user.mention, embed=embed, ephemeral=True)
 

        



        






class SetTodo(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(emoji=f'📃', custom_id='SetTodo',style=discord.ButtonStyle.grey)
    async def receive(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetTodo_Modal())








@bot.command()
@commands.has_permissions(administrator=True)
async def settodo(ctx):
    embed = discord.Embed(description=f'>>> **Παρακάτω μπορείτε να πατησετε το ✅ για να επιλέξετε να κάνετε αίτηση για whitelist**')
    embed.set_author(name=copyright_text
, icon_url=logo_url)
    embed.set_thumbnail(url=logo_url)
    view=SetTodo()

    await ctx.send(view=view, embed=embed)
    await ctx.message.delete()












 
    
    

    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[: -3]}')
            extension = filename[:-3]

            try:
              extension = f"'{extension}'.py"
              print(f"Loaded extension {extension}")
              print('---- ✔ -----------------------------')
            except Exception as e:
              exception = f"{type(e).__name__}: {e}"

              print('---- ❌ -----------------------------')
              print(
                f"Failed to load extension {extension}\n{exception}")
              print('----------------------------------')






async def main():
   await load_cogs()
   await bot.start(token)


clear()
print("Ititializing please wait...")
if async_mode == True:

        asyncio.run(main())

else:
        bot.run(token=token)
