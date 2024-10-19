import discord
from discord.ext import tasks, commands
import requests
from apis import *

# Get the bot token from the environment
import os
from dotenv import load_dotenv
load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot with intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True  


bot = commands.Bot(command_prefix='!', intents=intents)

# Channels need to be voice channels to have less strict formatting rules for their names
CHANNEL_IDS = {
    "price":1175645689968070747,
    "zeph-circulating":1175645938585456750,
    "zsd-circulating":1175645973121343488,
    "zeph-market-cap":1175645991492407317,
    "hashrate": 1175646013168549959,
    "miner-reward": 1175646329461035059,
    "reserve-reward": 1175646351497908275,
    "reserve-ratio": 1175650093504921680,
    "reserve-ratio-ma": 1175650191857168394,
    "zrs-price": 1176604759730442341,
    "zrs-price-ma": 1176604781846986784,
    "assets": 1176604803045007360,
    "equity": 1176604819973230673,
    "reserve": 1182915934197927936,
    "floating" : 1182916004670611567,
    "zys-price": 1295197893543723072,
    "yield-reserve": 1295197948514144290,
    "yield-reward": 1297064363018158161,
}

# Task to update channel names
@tasks.loop(minutes=6) # Beware of rate limiting
async def update_stats():
    try:
        channel_price = bot.get_channel(CHANNEL_IDS["price"])
        channel_zeph_circulating = bot.get_channel(CHANNEL_IDS["zeph-circulating"])
        channel_zsd_circulating = bot.get_channel(CHANNEL_IDS["zsd-circulating"])
        channel_market_cap = bot.get_channel(CHANNEL_IDS["zeph-market-cap"])
        channel_hashrate = bot.get_channel(CHANNEL_IDS["hashrate"])
        channel_miner_reward, channel_reserve_reward = bot.get_channel(CHANNEL_IDS["miner-reward"]), bot.get_channel(CHANNEL_IDS["reserve-reward"])
        channel_reserve_ratio, channel_reserve_ratio_ma = bot.get_channel(CHANNEL_IDS["reserve-ratio"]), bot.get_channel(CHANNEL_IDS["reserve-ratio-ma"])
        channel_zrs_price, channel_zrs_price_ma = bot.get_channel(CHANNEL_IDS["zrs-price"]), bot.get_channel(CHANNEL_IDS["zrs-price-ma"])
        channel_assets, channel_equity = bot.get_channel(CHANNEL_IDS["assets"]), bot.get_channel(CHANNEL_IDS["equity"])
        channel_reserve, channel_floating = bot.get_channel(CHANNEL_IDS["reserve"]), bot.get_channel(CHANNEL_IDS["floating"])
        channel_zys_price, channel_yield_reserve = bot.get_channel(CHANNEL_IDS["zys-price"]), bot.get_channel(CHANNEL_IDS["yield-reserve"])
        channel_yield_reward = bot.get_channel(CHANNEL_IDS["yield-reward"]) 

        print("Updating stats...")
        zeph_circ = getCirculatingSupply('ZEPH')
        zsd_circ = getCirculatingSupply('ZSD')
        await channel_price.edit(name=f"Price: {getCurrentPrice(format=True)}")
        await channel_zeph_circulating.edit(name=f"ZEPH Circ: {getCirculatingSupply('ZEPH', format=True)}")
        await channel_zsd_circulating.edit(name=f"ZSD Circ: {getCirculatingSupply('ZSD', format=True)}")
        await channel_market_cap.edit(name=f"MCap: {getMarketCap()}")
        await channel_hashrate.edit(name=f"Hashrate: {getHashrate()}")
        
        miner_reward, reserve_reward, yield_reward = getLastRewards()
        await channel_miner_reward.edit(name=f"Miner Reward: {miner_reward}")
        await channel_reserve_reward.edit(name=f"Res Reward: {reserve_reward}")
        await channel_yield_reward.edit(name=f"Yield Reward: {yield_reward}")

        reserve_ratio, reserve_ratio_ma, zrs_price, zrs_price_ma, assets, equity, zeph_reserve, zys_price, zyield_reserve = getReserveInfo(True)


        if reserve_ratio is not None:
            total_percentage_of_zeph_in_reserve = f"{float(zeph_reserve) / zeph_circ * 100:,.2f}"   
            total_percentage_of_zsd_in_yield_reserve = f"{float(zyield_reserve) / zsd_circ * 100:,.2f}"
            await channel_reserve_ratio.edit(name=f"Res Ratio: {reserve_ratio}")
            await channel_reserve_ratio_ma.edit(name=f"Res Ratio MA: {reserve_ratio_ma}")

            await channel_zrs_price.edit(name=f"ZRS: {zrs_price}")
            await channel_zrs_price_ma.edit(name=f"ZRS[MA]: {zrs_price_ma}")

            await channel_assets.edit(name=f"Assets: {assets}")
            await channel_equity.edit(name=f"Equity: {equity}")

            floating = float(zeph_circ) - float(zeph_reserve)
            if zeph_reserve < 1e6:
                zeph_reserve = f"{zeph_reserve/1e3:.2f}K"
            elif zeph_reserve < 1e9:
                zeph_reserve = f"{zeph_reserve/1e6:.2f}M"

            if floating < 1e6:
                floating = f"{floating/1e3:.2f}K"
            elif floating < 1e9:
                floating = f"{floating/1e6:.2f}M"

            await channel_reserve.edit(name=f"Res: {zeph_reserve} Ƶ ({total_percentage_of_zeph_in_reserve}%)")
            await channel_floating.edit(name=f"Float: {floating} Ƶ ({100 - float(total_percentage_of_zeph_in_reserve):,.2f}%)")

            await channel_zys_price.edit(name=f"ZYS: {zys_price}")

            if zyield_reserve < 1e6:
                zyield_reserve = f"{zyield_reserve/1e3:.2f}K"
            elif zyield_reserve < 1e9:
                zyield_reserve = f"{zyield_reserve/1e6:.2f}M"

            await channel_yield_reserve.edit(name=f"Yield Res: {zyield_reserve} ƵSD ({total_percentage_of_zsd_in_yield_reserve}%)")
            

        print("Stats updated!")
    except Exception as e:
        print(f"An error occurred during update_stats: {e}")


# Event listener for when the bot has connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    update_stats.start() 

# Run the bot
bot.run(BOT_TOKEN)
