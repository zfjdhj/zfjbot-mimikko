# -*- coding: UTF-8 -*-
"""
 * @author  zfj
 * @date  2020/9/26 15:39
"""

from hoshino import *
from hoshino import Service
from nonebot import *
import json
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




def GetUserSignedInformation(url, app_id):
    header_get = {
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
    header_post = {
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
        with requests.get(url, headers=header_get, verify=False,timeout=300) as resp:
            res = resp.json()
            return res

    except Exception as ex:
        print(ex)

#{'code': '0', 'body': {'IsSign': True, 'ContinuousSignDays': 1236}}
#{'code': '0', 'body': {'startTime': 1607768579935, 'endTime': 1605110400000, 'registrationDate': None, 'signLogs': [{'signDate': 1607704340000}, {'signDate': 1607702399000}, {'signDate': 1607554484000}, {'signDate': 1607445531000}, {'signDate': 1607358558000}, {'signDate': 1607356445000}, {'signDate': 1607270399000}, {'signDate': 1607097750000}, {'signDate': 1607013153000}, {'signDate': 1606924954000}, {'signDate': 1606923005000}, {'signDate': 1606754031000}, {'signDate': 1606692016000}, {'signDate': 1606579223000}, {'signDate': 1606579184000}, {'signDate': 1606413553000}, {'signDate': 1606320975000}, {'signDate': 1606319999000}, {'signDate': 1606149066000}, {'signDate': 1606144022000}, {'signDate': 1606055679000}, {'signDate': 1605888061000}, {'signDate': 1605801626000}, {'signDate': 1605715271000}, {'signDate': 1605666645000}, {'signDate': 1605581826000}, {'signDate': 1605460258000}, {'signDate': 1605371114000}, {'signDate': 1605283545000}, {'signDate': 1605200950000}, {'signDate': 1605119449000}]}}


@sv.on_fullmatch('mimikko check')
async def mimikko_check(bot, ev):
    login_data = GetUserSignedInformation(apiPath, app_id)
    res=f'code:{login_data["code"]}\nIsSign:{login_data["body"]["IsSign"]}\nContinuousSignDays:{login_data["body"]["ContinuousSignDays"]}'
    print(login_data)
    login_history = json.dumps(GetUserSignedInformation(apiPath2, app_id))
    print(login_history)

    await bot.send(ev, res)
    await bot.send(ev, login_history)


@sv.on_fullmatch('mimikko sign in')
async def mimikko_sign_in(bot, ev):
    login_data = GetUserSignedInformation(apiPath, app_id)
    print(login_data)
    login_history = GetUserSignedInformation(apiPath2, app_id)
    print(login_history)

    await bot.send(ev, login_data)
    await bot.send(ev, login_history)

async def mimikko_sign_in_auto():
    login_data = GetUserSignedInformation(apiPath, app_id)
    res=f'code:{login_data["code"]}\nIsSign:{login_data["body"]["IsSign"]}\nContinuousSignDays:{login_data["body"]["ContinuousSignDays"]}'
    print(login_data)
    #login_history = GetUserSignedInformation(apiPath2, app_id)
    #print(login_history)

    # await bot.send(ev, login_data)
    # await bot.send(ev, login_history)
    await bot.send_group_msg(group_id=group_id,message=res)
#    await bot.send_group_msg(group_id=group_id,message=login_history)


scheduler.add_job(mimikko_sign_in_auto, 'cron',hour='22')
# scheduler.add_job(mimikko_sign_in, 'cron', hour='5',minute='30')

