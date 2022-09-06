import discord
import requests
from discord.ext import commands
from discord import app_commands
import random
import numpy as np
import pandas as pd
import datetime as dt
from IPython.display import display

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id=963595842252582942))
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)



@tree.command(name="fox", description = "Gets pic of fox", guild = discord.Object(id=963595842252582942))
async def self(interaction: discord.Interaction):
    r = requests.get("https://randomfox.ca/floof").json()
    em = discord.Embed()
    em.set_image(url=r['image'])
    await interaction.response.send_message(embed=em)

def get_item_details(itemName):
    total_plat = 0
    total_orders = 0
    itemOrders = requests.get(f"https://api.warframe.market/v1/items/{itemName}/orders").json()
    df = pd.DataFrame(columns=["prices", "dates"])    

    for orders in itemOrders['payload']['orders']:
        if orders['order_type']== 'sell':
            selling_price = orders['platinum']
            total_plat = total_plat + selling_price
            total_orders = total_orders+1

            date = orders['last_update'].split("T")[0]    
            df.loc[len(df.index)] = [selling_price, date]
    
    df['dates'] = pd.to_datetime(df['dates'])
    df.sort_values(by='dates', inplace=True)
    
    avg_price = round(total_plat/total_orders, 2)

    return total_orders, avg_price, df
       


@tree.command(name="warframe", description = "get thingy", guild = discord.Object(id=963595842252582942))
async def self(interaction: discord.Interaction, message: str):
    newString = message.replace(' ', '_').lower()
    frameItem = requests.get(f"https://api.warframe.market/v1/items/{newString}").json()
    df = pd.DataFrame()

    total_orders, avg_price, df = get_item_details(newString)
    display(df)
    
    em = discord.Embed(
        title=message,
        color = discord.Color.purple())
    em.set_thumbnail(url=f"https://warframe.market/static/assets/{frameItem['payload']['item']['items_in_set'][0]['icon']}")
    em.add_field(name="Total Sell Orders", value=total_orders, inline=False)
    em.add_field(name="Average Item Price", value=avg_price, inline=False)

    await interaction.response.send_message(embed=em)    

client.run("MTAxNjEzMDEyMDYwNTUxOTkwMw.GbQxjT.9holyp5EklAEqBFP1K5NdV8dNSPEzpfiqhWeng")