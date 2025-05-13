import discord
from discord.ext import commands
import pandas as pd
from discord import app_commands
import math
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load the Excel file
def load_products():
    try:
        df = pd.read_excel("sportland_apavi_viriesu.xlsx")
        return df
    except Exception as e:
        print(f"Kļūda ielādējot Excel failu: {str(e)}")
        return None

@bot.event
async def on_ready():
    print(f"{bot.user} ir gatavs!")
    try:
        synced = await bot.tree.sync()
        print(f"Sinhronizētas {len(synced)} komandas")
    except Exception as e:
        print(f"Kļūda sinhronizējot komandas: {str(e)}")

@bot.tree.command(name="search", description="Meklē produktu pēc SKU")
async def search(interaction: discord.Interaction, sku: str):
    # Load products
    df = load_products()
    if df is None:
        await interaction.response.send_message("Neizdevās ielādēt produktu datus!")
        return

    # Search for the product
    try:
        product = df[df["Produkta kods"] == sku].iloc[0]
        
        # Create embed
        embed = discord.Embed(
            title=product["Nosaukums"],
            url=product["Saite"],
            color=discord.Color.red()
        )
        
        embed.add_field(name="Zīmols", value=product["Zīmols"], inline=True)
        embed.add_field(name="Cena", value=f"{product['Cena']}€", inline=True)
        embed.add_field(name="Produkta kods", value=product["Produkta kods"], inline=True)
        
        if pd.notna(product["Pieejamie izmēri"]):
            embed.add_field(
                name="Pieejamie izmēri", 
                value=product["Pieejamie izmēri"], 
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
        
    except IndexError:
        await interaction.response.send_message(f"Produkts ar SKU '{sku}' netika atrasts!")
    except Exception as e:
        await interaction.response.send_message(f"Kļūda meklējot produktu: {str(e)}")

@bot.tree.command(name="list", description="Parāda produktu sarakstu ar SKU (20 produkti lapā)")
async def list_products(interaction: discord.Interaction, page: int = 1):
    # Load products
    df = load_products()
    if df is None:
        await interaction.response.send_message("Neizdevās ielādēt produktu datus!")
        return

    try:
        # Calculate pagination
        items_per_page = 20
        total_items = len(df)
        total_pages = math.ceil(total_items / items_per_page)
        
        # Validate page number
        if page < 1 or page > total_pages:
            await interaction.response.send_message(f"Nederīgs lapas numurs! Pieejamās lapas: 1-{total_pages}")
            return
        
        # Get items for current page
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_items = df.iloc[start_idx:end_idx]
        
        # Create embed
        embed = discord.Embed(
            title=f"Produktu saraksts (Lapa {page}/{total_pages})",
            color=discord.Color.red()
        )
        
        # Add products to embed
        product_list = []
        for _, product in page_items.iterrows():
            product_list.append(f"**{product['Produkta kods']}** - {product['Nosaukums']}")
        
        embed.description = "\n".join(product_list)
        embed.set_footer(text=f"Kopā {total_items} produkti • Izmanto /list <lapa> lai skatītu citas lapas")
        
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        await interaction.response.send_message(f"Kļūda parādot produktu sarakstu: {str(e)}")

# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("Error: DISCORD_BOT_TOKEN not found in environment variables!")
        exit(1)
    bot.run(token)