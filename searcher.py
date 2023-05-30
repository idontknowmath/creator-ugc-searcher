import time
import json
import requests
from rich import print
from discord_webhook import DiscordWebhook, DiscordEmbed
import subprocess
import aiohttp
import asyncio
import json
import traceback
import logging


cookie = "rblx cookie here"

snipedIds = []
creatorID = None # put id of creator here

cookies = [[i, ""] for i in conf["cookie"]]
if type(conf["cookie"]) == str:
    with open(conf["cookie"], "r") as f:
        cookies = [[i, ""] for i in f.read().replace(";", "").splitlines()]



def betterPrint(text):
    now = time.strftime('%r')
    print(f"[bold grey53][{now}] [/] {text}")

def get_x_token(cookie):
    return requests.post('https://auth.roblox.com/v2/logout', headers={'cookie': '.ROBLOSECURITY='+ cookie}).headers['x-csrf-token']


async def get_item_info(items):
    print(f"Getting item info for {items}")
    details = await request_details(items)
    print(f"Received item details for {items}")
    return await extract_data(details)

async def request_details(items):
    xt = get_x_token(cookies[0][0])
    headers = {
        'cookie': f'.ROBLOSECURITY={cookies[0][0]};',
        'x-csrf-token': xt
    }
    payload = {"items": [{"itemType": "Asset", "id": int(items)}]}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://catalog.roblox.com/v1/catalog/items/details',
                                    json=payload,
                                    headers=headers) as response:
                response_data = await response.text()
        
                return json.loads(response_data)
    except Exception as e:
        print(e)
        return

async def extract_data(details):
    return details['data']
    


async def main():
    print('starting')
    while 1:
        try:
            ids = await latest()
            for id in ids:
                if id == creatorID:
                    betterPrint(f"[aquamarine1]NEW LIM ADDED {id}")
                    with open("limiteds.txt", "a") as f:
                        f.truncate(0)
                        f.write(f"{id}\n")
        except Exception as e:
            traceback.print_exc()
            print(f"Exception occurred: {str(e)}")
            pass
        await asyncio.sleep(6)


async def fetch_json(session, url, headersss):
    async with session.get(url, headers=headersss) as response:
        data = await response.json()
        return data
    

async def latest():
  async with aiohttp.ClientSession() as session:
      r = await session.get("https://catalog.roblox.com/v1/search/items/details?Category=11&salesTypeFilter=1&SortType=3&IncludeNotForSale=True&Limit=30")
      rData = await r.json()
      userid = rData['data'][0]['creatorTargetId']
      betterPrint(f"[aquamarine1]recent user id - {userid}")
      ids = []
      ids.append(userid)
      return ids

asyncio.run(main())
