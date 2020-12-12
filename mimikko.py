# -*- coding: UTF-8 -*-
"""
 * @author  zfj
 * @date  2020/9/26 15:39
"""

from hoshino import *
from nonebot import *
from hoshino import Service

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sv = Service('zfjbot-mimikko',enable_on_default=False)
group_id="426770092"
bot=get_bot()

app_id = 'wjB7LOP2sYkaMGLC'
Version='3.1.2'
Authorization='c5d8dba1-eaae-4fd9-8112-6759ab8a8c34'

apiPath = 'http://api1.mimikko.cn/client/user/GetUserSignedInformation'
# apiPath1 = 'http://api1.mimikko.cn/client/user/LoginWithPayload'
apiPath2 = 'http://api1.mimikko.cn/client/dailysignin/log/30/0'
# post_data = {"password": "d8a598c998d82c1943cd719dff2627a6ce728ce1a8c5b15746f066b07ce00ac9", "id": "320336328@qq.com"}
sign_path='https://api1.mimikko.cn/client/RewardRuleInfo/SignAndSignInformationV3'

def GetUserSignedInformation(url, app_id):
    headers_get = {
        'Cache-Control': 'Cache-Control:public,no-cache',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'Mozilla/5.0(Linux;Android6.0.1;MuMu Build/V417IR;wv)AppleWebKit/537.36(KHTML,'
                      'like Gecko)Version/4.0 Chrome/52.0.2743.100MobileSafari / 537.36',
        'AppID': app_id,
        'Version': '3.1.2',
        'Authorization': Authorization,
        'Connection': 'Keep-Alive',
        'Host': 'api1.mimikko.cn'
    }
    headers_post = {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache',
        'AppID': app_id,
        'Version': '3.1.2',
        'Content-Type': 'application/json',
        'Host': 'api1.mimikko.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.1',
    }

    try:
        with requests.get(url, headers=headers_get, verify=False,timeout=300) as resp:
            res = resp.json()
            return res

    except Exception as ex:
        return ex
        print(ex)


@sv.on_fullmatch('mimikko check')
async def mimikko_check(bot, ev):
    login_data = GetUserSignedInformation(apiPath, app_id)
    print(login_data)
    login_history = GetUserSignedInformation(apiPath2, app_id)
    print(login_history)

    await bot.send(ev, login_data)
    await bot.send(ev, login_history)


@sv.on_fullmatch('mimikko sign')
async def mimikko_sign_in(bot, ev):
    sign_data = GetUserSignedInformation(sign_path, app_id)
    print(sign_data)
    login_data = GetUserSignedInformation(apiPath2, app_id)
    print(login_data)

    # await bot.send(ev, login_data)
    # await bot.send(ev, login_history)
    
    await bot.send_group_msg(group_id=group_id,message=sign_data)
    await bot.send_group_msg(group_id=group_id,message=login_data)

async def mimikko_sign_in_auto():
    sign_data = GetUserSignedInformation(sign_path, app_id)
    print(sign_data)
    login_data = GetUserSignedInformation(apiPath2, app_id)
    print(login_data)

    # await bot.send(ev, login_data)
    # await bot.send(ev, login_history)
    
    await bot.send_group_msg(group_id=group_id,message=sign_data)
    await bot.send_group_msg(group_id=group_id,message=login_data)


scheduler.add_job(mimikko_sign_in_auto, 'cron',hour='12')
# scheduler.add_job(mimikko_sign_in, 'cron', hour='5',minute='30')