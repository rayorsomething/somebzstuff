import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

import urllib.request, json 
import time

TOKEN = "MTA1MzU3NDI0MjYxODMyMzAxNA.GJkvZM.gBmh0RaF3eAv95pvknljujRYgFmjQo3RFK2uME"

def is_me(m):
    return m.author == bot.user


class client(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(intents=intents, help_command=None)

        
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        # Register the persistent view for listening here.
        # Note that this does not send the view to any message.
        # In order to do this you need to first send a message with the View, which is shown below.
        # If you have the message_id you can also pass it as a keyword argument, but for this example
        # we don't have one.
        await self.tree.sync()

bot = client()




@bot.event
async def on_ready():
    servercount = len(bot.guilds)
    latency = bot.latency * 1000

    print(' ______     ______     __  __     __         ______     ______     _____     ______     ______    ')
    print('/\  == \   /\  __ \   /\ \_\ \   /\ \       /\  __ \   /\  __ \   /\  __-.  /\  ___\   /\  == \   ')
    print('\ \  __<   \ \  __ \  \ \____ \  \ \ \____  \ \ \/\ \  \ \  __ \  \ \ \/\ \ \ \  __\   \ \  __<   ')
    print(' \ \_\ \_\  \ \_\ \_\  \/\_____\  \ \_____\  \ \_____\  \ \_\ \_\  \ \____-  \ \_____\  \ \_\ \_\ ')
    print('  \/_/ /_/   \/_/\/_/   \/_____/   \/_____/   \/_____/   \/_/\/_/   \/____/   \/_____/   \/_/ /_/ ')
    print('                                                                                                  ')
    time.sleep(2)
    print("Starting boot process...")
    time.sleep(1)
    print("Bot has logged in as {0.user}.".format(bot))
    time.sleep(0.5)
    print("{0.user} is in {1} server(s).".format(bot, servercount))
    time.sleep(0.5)
    print("Starting latency process...")
    chan = bot.get_channel(1053576647770656802)
    b4 = time.monotonic()
    msg = await chan.send("Pong!")
    ping = (time.monotonic() - b4) * 1000
    await msg.delete()
    time.sleep(0.5)
    print("The message latency is {0}ms.".format(int(ping)))
    time.sleep(0.5)
    print("The API latency is {0}ms.".format(latency))
    time.sleep(0.5)
    print("Latency process ended!")
    time.sleep(0.5)
    print("The token is "+TOKEN)
    time.sleep(0.5)
    print("Boot process ended!")







# ------------ START LATENCY ------------
@bot.tree.command()
async def defaultping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")


@bot.tree.command()
async def apiping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Took: {round(bot.latency * 1000)}ms to ping the api!")


@bot.tree.command()
async def ping(interaction: discord.Interaction):
    b4 = time.monotonic()
    await interaction.response.send_message("Starting editing process...")
    message: discord.Message
    async for message in interaction.channel.history():
        if message.content == "Starting editing process...":
            msg = message
            break
    else:
        await interaction.channel.send('Something broke while trying to perform this command. Please DM me (Azazel#1949)')
        return
    ping = (time.monotonic() - b4) * 1000
    await msg.edit(content="Pong! Took: {}ms to edit!".format(int(ping)))
# ------------ END LATENCY ------------



bzNames = []
bzRbuyPrices = []
bzRsellPrices = []
bzVolumes = []

npcRprices = []
npcNames = []
itemNames = []

fullinfo = {}

topNPC = {}
topBZ = {}



def sortNPCprofit(item):
    return item[1]["npcProfit"]
def sortBZprofit(item):
    return item[1]["bzProfit"]
def sortNPCvolume(item):
    return item[1]["bzVolume"]
def sortBZvolume(item):
    return item[1]["bzVolume"]
def sortNPCabc(item):
    return item[1]["item"]
def sortBZabc(item):
    return item[1]["item"]

def updateBZ():
    bzRbuyPrices.clear()
    bzNames.clear()
    with urllib.request.urlopen("https://api.hypixel.net/skyblock/bazaar") as url:
        data = json.loads(url.read().decode('utf-8'))
        data = data["products"]
        for key in data:
            bzRbuyPrice = round(data[key]["quick_status"]["buyPrice"])
            bzRsellPrice = round(data[key]["quick_status"]["sellPrice"])
            bzName = str(data[key]["product_id"])
            bzVolume = data[key]["quick_status"]["buyVolume"]
        
            bzNames.append(bzName)  
            bzRbuyPrices.append(bzRsellPrice)
            bzRsellPrices.append(bzRbuyPrice)
            bzVolumes.append(bzVolume)


def updateNPC():
    npcRprices.clear()
    npcNames.clear()
    itemNames.clear()
    with urllib.request.urlopen("https://api.hypixel.net/resources/skyblock/items") as url:
        data = json.loads(url.read().decode('utf-8'))
        data = data["items"]
        for key in data:
            if "npc_sell_price" in key:
                npcRprice = round(key["npc_sell_price"])
                npcName = str(key["id"])
                itemName = str(key["name"])

                npcRprices.append(npcRprice)
                npcNames.append(npcName)
                itemNames.append(itemName)



def calcProfit():
    if not len(bzRbuyPrices) == 0 and not len(npcRprices) == 0:
        index = 0
        for key in bzNames:
            if bzNames[index] in npcNames:
                npcIndex = npcNames.index(bzNames[index])
                bzBuyPriceFinal = bzRbuyPrices[index]
                bzSellPriceFinal = bzRsellPrices[index]
                npcPriceFinal = npcRprices[npcIndex]
                bzVolmueFinal = bzVolumes[index]

                itemNameFinal = itemNames[npcIndex]

                npcFlipProfit = npcPriceFinal - bzBuyPriceFinal 
                bzFlipProfit =  bzSellPriceFinal - bzBuyPriceFinal

                fullinfo.update({str(index): {"item": itemNameFinal, "bzProfit": bzFlipProfit, "bzVolume": bzVolmueFinal, "npcProfit": npcFlipProfit, "cost": bzBuyPriceFinal}})

                index += 1
            else:
                bzBuyPriceFinal = bzRbuyPrices[index]
                bzSellPriceFinal = bzRsellPrices[index]
                bzVolmueFinal = bzVolumes[index]
                itemNameFinal = bzNames[index]

                bzFlipProfit =  bzSellPriceFinal - bzBuyPriceFinal

                if not itemNameFinal.startswith("ENCHANTMENT_"):
                    fullinfo.update({str(index): {"item": itemNameFinal, "bzProfit": bzFlipProfit, "bzVolume": bzVolmueFinal, "npcProfit": -999999999999999999999999, "cost": bzBuyPriceFinal}})

                index += 1



@bot.tree.command()
@app_commands.choices(
  sortbzby=[ # param name
    Choice(name="Highest Buy Order Volume", value="hvolume"),
    Choice(name="Highest Profit", value="hprofit"),
    Choice(name="Alphabetical Order", value="alphabet"),
    Choice(name="Lowest Buy Order Volume", value="lvolume"),
    Choice(name="Lowest Profit", value="lprofit"),
    Choice(name="Reverse Alphabetical Order", value="ralphabet")
  ],
  sortnpcby=[ # param name
    Choice(name="Highest Buy Order Volume", value="hvolume"),
    Choice(name="Highest Profit", value="hprofit"),
    Choice(name="Alphabetical Order", value="alphabet"),
    Choice(name="Lowest Buy Order Volume", value="lvolume"),
    Choice(name="Reverse Alphabetical Order", value="ralphabet")
  ]
)
@app_commands.describe( 
    items="How many items to list",
    sortbzby="How to sort Bazaar Flips",
    sortnpcby="How to sort NPC Flips"
)
async def sendflips(interaction: discord.Interaction, items: int, sortbzby: Choice[str], sortnpcby: Choice[str]):
    await interaction.response.send_message("One pile of money comin' right up!")
    updateBZ()
    updateNPC()
    calcProfit()
    for key in fullinfo:
        key = fullinfo.get(key)
        name = key["item"]
        bzFlipProfit = key["bzProfit"]
        npcFlipProfit = key["npcProfit"]
        price = key["cost"]

        #print(name, bzFlipProfit, npcFlipProfit, price)

        print(key["npcProfit"])
        if sortnpcby.value == "hvolume":
            sorted_npc = dict(sorted(fullinfo.items(), key=sortNPCvolume, reverse=True))
        elif sortnpcby.value == "hprofit":
            sorted_npc = dict(sorted(fullinfo.items(), key=sortNPCprofit, reverse=True))
        elif sortnpcby.value == "alphabet":
            sorted_npc = dict(sorted(fullinfo.items(), key=sortNPCabc, reverse=False))
        elif sortnpcby.value == "lvolume":
            sorted_npc = dict(sorted(fullinfo.items(), key=sortNPCvolume, reverse=False))
        elif sortnpcby.value == "ralphabet":
            sorted_npc = dict(sorted(fullinfo.items(), key=sortNPCabc, reverse=True))
        else:
            await interaction.channel.send("Please select a valid NPC Sorting Method")
            break

        if sortbzby.value == "hvolume":
            sorted_bz = dict(sorted(fullinfo.items(), key=sortBZvolume, reverse=True))
        elif sortbzby.value == "hprofit":
            sorted_bz = dict(sorted(fullinfo.items(), key=sortBZprofit, reverse=True))
        elif sortbzby.value == "alphabet":
            sorted_bz = dict(sorted(fullinfo.items(), key=sortBZabc, reverse=False))
        elif sortbzby.value == "lvolume":
            sorted_bz = dict(sorted(fullinfo.items(), key=sortBZvolume, reverse=False))
        elif sortbzby.value == "lprofit":
            sorted_bz = dict(sorted(fullinfo.items(), key=sortBZprofit, reverse=False))
        elif sortbzby.value == "ralphabet":
            sorted_bz = dict(sorted(fullinfo.items(), key=sortBZabc, reverse=True))
        else:
            await interaction.channel.send("Please select a valid BZ Sorting Method")
            break

        npciter = iter(sorted_npc.items())
        bziter = iter(sorted_bz.items())

        for i in range(items):
            topNPC[next(npciter)[0]] = next(npciter)[1]
            topBZ[next(bziter)[0]] = next(bziter)[1]


    npcEmbed=discord.Embed(
        title="NPC Flip Update", 
        description="Buy at `Bazaar` and sell to `NPC` listed by `"+sortnpcby.name+"`"
    )
    npcEmbed.add_field(name="------------------------------------------------------", value="** **", inline=False)
    for i in range(items):
        npcEmbed.add_field(name="*Item "+str(i+1)+"*: "+str(dict(list(topNPC.values())[i]).get("item")), value="**Price**: "+str("{:,}".format(int(str(dict(list(topNPC.values())[i]).get("cost")))).replace(',', '.'))+"\n**Profit**: "+str("{:,}".format(int(str(dict(list(topNPC.values())[i]).get("npcProfit")))).replace(',', '.')), inline=True)

    npcEmbed.add_field(name="------------------------------------------------------", value="** **", inline=False)
    
    await interaction.channel.send(embed=npcEmbed)



    bzEmbed=discord.Embed(
        title="BZ Flip Update", 
        description="Buy at `Bazaar` and sell to `Bazaar` listed by `"+sortbzby.name+"`"
    )
    #bzEmbed.add_field(name="------------------------------------------------------", value="** **", inline=False)
    for i in range(items):
        bzEmbed.add_field(name="*Item "+str(i+1)+"*: "+str(dict(list(topBZ.values())[i]).get("item")), value="**Price**: "+str("{:,}".format(int(str(dict(list(topBZ.values())[i]).get("cost")))).replace(',', '.'))+"\n**Volume**: "+str("{:,}".format(int(str(dict(list(topBZ.values())[i]).get("bzVolume")))).replace(',', '.'))+"\n**Profit**: "+str("{:,}".format(int(str(dict(list(topBZ.values())[i]).get("bzProfit")))).replace(',', '.')), inline=True)

    #bzEmbed.add_field(name="------------------------------------------------------", value="** **", inline=False)
    
    await interaction.channel.send(embed=bzEmbed)
       


bot.run(TOKEN)