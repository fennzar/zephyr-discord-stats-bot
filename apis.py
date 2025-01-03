import requests
from daemon import get_reserve_info


def getCurrentPrice(format=False):
    try:
        url = "https://api.mexc.com/api/v3/ticker/price?symbol=ZEPHUSDT"
        response = requests.get(url, timeout=5)
        data = response.json()
        if format:
            return f"${float(data['price']):,.2f}"
        return float(data['price'])
    except Exception as e:
        print("\tError in getCurrentPrice:", e)
        return "..."

def getCirculatingSupply(ticker, format=False):
    try:
        if ticker == 'ZEPH':
            url = 'https://explorer.zephyrprotocol.com/api/circulating'
        elif ticker == 'ZSD':
            url = 'https://explorer.zephyrprotocol.com/api/circulating/zsd'
        elif ticker == 'ZRS':
            url = 'https://explorer.zephyrprotocol.com/api/circulating/zrs'
        elif ticker == "ZYS":
            url = 'https://explorer.zephyrprotocol.com/api/circulating/zys'

        if format:
            return f"{round(requests.get(url, timeout=10).json(),2):,.2f}"
        
        return round(requests.get(url, timeout=5).json(),2)
    except Exception as e:
            print("\tError in getCirculatingSupply:", e)
            return "..."

def getMarketCap():
    try:
        price = getCurrentPrice()
        circulating = getCirculatingSupply('ZEPH')
        marketCap = price * circulating
        return f"${marketCap:,.2f}"
    except Exception as e:
        print("\tError in getMarketCap:", e)
        return "..."

def getHashrate():
    try:
        url = 'https://explorer.zephyrprotocol.com/api/networkinfo'
        response = requests.get(url, timeout=10)
        data = response.json()
        hash_rate = data['data']['hash_rate']

        if hash_rate < 1e9:
            return f"{hash_rate / 1e6:.2f} MH/s"
        # Convert to GH/s otherwise
        else:
            return f"{hash_rate / 1e9:.2f} GH/s"
    except Exception as e:
        print("\tError in getHashrate:", e)
        return "..."

def getLastRewards():
    try:
        price_unformatted = getCurrentPrice(format=False)
        url = 'https://explorer.zephyrprotocol.com/api/networkinfo'
        response = requests.get(url, timeout=10)
        data = response.json()
        height = data['data']['height']

        url = f'https://explorer.zephyrprotocol.com/api/block/{height-1}'
        response = requests.get(url, timeout=10)
        data = response.json()

        txs = data['data']['txs']
        reward = 0
        for tx in txs:
            if tx['coinbase'] == True:
                reward = float(tx['xmr_outputs']) / 1e12
                break

        total_reward = reward / .65
        miner_reward = f"Ƶ{round(total_reward * .65,2)}" 
        reserve_reward = f"Ƶ{round(total_reward * .30,2)}"
        yield_reward = f"{round(total_reward * .05 * price_unformatted,2)} ƵSD"

        return miner_reward, reserve_reward, yield_reward
    except Exception as e:
            print("\tError in getLastRewards:", e)
            return "...", "...", "..."

def getReserveInfo(format=False):
    try:
        info = get_reserve_info()
        # print(info)
        reserve_ratio = float(info['result']['reserve_ratio'])
        reserve_ratio_ma = float(info['result']['reserve_ratio_ma'])

    
        spot = float(info['result']['pr']['spot']) / 1e12
        ma = float(info['result']['pr']['moving_average']) / 1e12

        zrs_zeph_price = float(info['result']['pr']['reserve']) / 1e12
        zrs_zeph_price_ma = float(info['result']['pr']['reserve_ma']) / 1e12

        zrs_usd_price = spot * zrs_zeph_price
        zrs_usd_price_ma = ma * zrs_zeph_price_ma

        zrs_price = zrs_zeph_price
        zrs_price_ma = zrs_zeph_price_ma

        zys_price = float(info['result']['pr']['yield_price']) / 1e12

        assets = float(info['result']['assets']) / 1e12
        equity = float(info['result']['equity']) / 1e12

        zeph_reserve = float(info['result']['zeph_reserve']) / 1e12
        yield_reserve = float(info['result']['zyield_reserve']) / 1e12

        if format:
            reserve_ratio = f"{round(reserve_ratio * 100,2)}%"
            reserve_ratio_ma = f"{round(reserve_ratio_ma * 100,2)}%"

            zrs_price = f"Ƶ{zrs_zeph_price:,.4f} (${zrs_usd_price:,.2f})"
            zrs_price_ma = f"Ƶ{zrs_zeph_price_ma:,.4f} (${zrs_usd_price_ma:,.2f})"

            zys_price = f"{zys_price:,.4f}ƵSD"

            if assets < 1e6:
                assets = f"${assets/1e3:.2f}K"
            elif assets < 1e9:
                assets = f"${assets/1e6:.2f}M"
            elif assets < 1e12:
                assets = f"${assets:,.2f}"
            else:
                assets = f"${assets/1e12:.2f}T"

            if equity < 1e6:
                equity = f"${equity/1e3:.2f}K"
            elif equity < 1e9:
                equity = f"${equity/1e6:.2f}M"
            elif equity < 1e12:
                equity = f"${equity/1e9:.2f}B"
            else:
                equity = f"${equity:,.2f}"

            # zeph_reserve = f"{zeph_reserve:,.2f}"

        return reserve_ratio, reserve_ratio_ma, zrs_price, zrs_price_ma, assets, equity, zeph_reserve, zys_price, yield_reserve
    except Exception as e:
        print("\tError getting reserve info, daemon may not be running?")
        print("\t", e)
        return None, None, None, None, None, None, None, None, None
    

if __name__ == '__main__':

    price = getCurrentPrice(format=True)
    print(f"Price: {price}")

    circulating = getCirculatingSupply('ZEPH', format=True)

    print(f"Circulating: {circulating}")

    marketCap = getMarketCap()
    print(f"Market Cap: {marketCap}")

    hashrate = getHashrate()
    print(f"Hashrate: {hashrate}")

    miner_reward, reserve_reward, yield_reward = getLastRewards()
    print(f"Miner Reward: {miner_reward}")
    print(f"Reserve Reward: {reserve_reward}")
    print(f"Yield Reward: {yield_reward}")

    reserve_ratio, reserve_ratio_ma, zrs_price, zrs_price_ma, assets, equity, zeph_reserve, zys_price, zyield_reserve = getReserveInfo(True)
    print(f"Reserve Ratio: {reserve_ratio}")
    print(f"Reserve Ratio MA: {reserve_ratio_ma}")
    print(f"ZRS Price: {zrs_price}")
    print(f"ZRS Price MA: {zrs_price_ma}")
    print(f"ZYS Price: {zys_price}")
    print(f"Assets: {assets}")
    print(f"Equity: {equity}")
    print("--------------------")
    print(f"ZEPH Reserve: {zeph_reserve}")

    try:
        zeph_circ = getCirculatingSupply('ZEPH')
        total_percentage_of_zeph_in_reserve = f"{float(zeph_reserve) / zeph_circ * 100:,.2f}"
        print(f"Total % of ZEPH in Reserve: {total_percentage_of_zeph_in_reserve}%")
        floating = float(zeph_circ) - float(zeph_reserve)
        
        if zeph_reserve < 1e6:
            zeph_reserve = f"{zeph_reserve/1e3:.2f}K"
        elif zeph_reserve < 1e9:
            zeph_reserve = f"{zeph_reserve/1e6:.2f}M"

        if floating < 1e6:
            floating = f"{floating/1e3:.2f}K"
        elif floating < 1e9:
            floating = f"{floating/1e6:.2f}M"

        print(f"Res: {zeph_reserve} Ƶ ({total_percentage_of_zeph_in_reserve}%)")
        print(f"Float: {floating} Ƶ ({100 - float(total_percentage_of_zeph_in_reserve):,.2f}%)")
    except Exception as e:
        print("\tError calculating ZEPH Reserve and floating supply:", e)

    print("--------------------")
    print(f"Yield Reserve: {zyield_reserve}")

    try:
        zsd_circ = getCirculatingSupply('ZSD')
        total_percentage_of_zsd_in_yield_reserve = f"{float(zyield_reserve) / zsd_circ * 100:,.2f}"
        print(f"Total % of ZSD in Yield Reserve: {total_percentage_of_zsd_in_yield_reserve}%")
        floating = float(zsd_circ) - float(zyield_reserve)

        if zyield_reserve < 1e6:
            zyield_reserve = f"{zyield_reserve/1e3:.2f}K"
        elif zyield_reserve < 1e9:
            zyield_reserve = f"{zyield_reserve/1e6:.2f}M"

        if floating < 1e6:
            floating = f"{floating/1e3:.2f}K"
        elif floating < 1e9:
            floating = f"{floating/1e6:.2f}M"

        print(f"Res: {zyield_reserve} ZSD ({total_percentage_of_zsd_in_yield_reserve}%)")
        print(f"Float: {floating} ZSD ({100 - float(total_percentage_of_zsd_in_yield_reserve):,.2f}%)")
    except Exception as e:
        print("\tError calculating ZSD Yield Reserve and floating supply:", e)



    print("--------------------")
    






    




