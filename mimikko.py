# -*- coding: UTF-8 -*-
"""
 * @author  zfj
 * @date  2020/9/26 15:39
"""

from hoshino import *
from nonebot import *
from hoshino import Service
from .mimikkoAutoSignIn.mimikko import mimikko,timeStamp2time
from .config import *

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from .PilCalendar import drawMonth
from .PilMimikkoSignCard import drawSigncard
import datetime
import re
import os

sv = Service('zfjbot-mimikko',enable_on_default=False)

group_id=GROUP_ID
app_id=APP_ID
authorization=AUTHORIZATION

bot=get_bot()
plugin_path=os.path.dirname(__file__)

@sv.on_fullmatch('mimikko check')
async def mimikko_check(bot, ev):
    sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id,authorization)
    res="Sign Data:\n"
    res +=f"获得成长值Reward：{sign_data['body']['Reward']}\n"
    res +=f"获得硬币GetCoin：{sign_data['body']['GetCoin']}\n"
    if sign_data['code']=='0':
        res +=f"[CQ:image,file=file:///{drawSigncard(sign_data)}]\n"
    res +=f"================\nEnergy Info:\n"
    res +=f"code: {energy_info_data['code']}\n"
    res +=f"msg: {energy_info_data['msg']}\n"
    res +=f"经验：{energy_info_data['body']['Favorability']}/{energy_info_data['body']['MaxFavorability']}\n"
    res+=f"Energy: {energy_info_data['body']['Energy']}\n"
    res+="================\nEnergy Reward:\n"
    res+=f"{energy_reward_data}\n"
    res+="================\nSign Info:\n"
    res +=f"code: {sign_info['code']}\n"
    res +=f"IsSign: {sign_info['body']['IsSign']}\n"
    res +=f"连续登录天数: {sign_info['body']['ContinuousSignDays']}\n"
    res +="================\nSign History:\n"
    res +=f"code: {sign_history['code']}\n"
    res +=f"startTime: {timeStamp2time(sign_history['body']['startTime'])}\n"
    res +=f"endTime: {timeStamp2time(sign_history['body']['endTime'])}\n"
    res +='signLogs:'
    day_list=[]
    for item in sign_history['body']['signLogs']:
        rex_data=re.search('(?P<月>.*)月(?P<日>.*)日',timeStamp2time(item['signDate']))
        if rex_data.group('月') == re.search('(?P<月>.*)月(?P<日>.*)日',
            timeStamp2time(sign_history['body']['startTime'])).group('月'):
            day_list.append(rex_data.group('日'))
    img_path= drawMonth(datetime.datetime.now().month,day_list,plugin_path)
    res +=f'[CQ:image,file=file:///{plugin_path}/{img_path}]'
    await bot.send(ev,res)

@sv.on_fullmatch('mimikko sign')
async def mimikko_sign_in(bot, ev):
    sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id,authorization)
    res="Sign Data:\n"
    res +=f"code:, {sign_data['code']}\n"
    res +=f"获得成长值Reward：{sign_data['body']['Reward']}\n"
    res +=f"获得硬币GetCoin：{sign_data['body']['GetCoin']}\n"
    res +=f"================\nEnergy Info:\n"
    res +=f"code: {energy_info_data['code']}\n"
    res +=f"msg: {energy_info_data['msg']}\n"
    res +=f"经验：{energy_info_data['body']['Favorability']}/{energy_info_data['body']['MaxFavorability']}\n"
    res+=f"Energy: {energy_info_data['body']['Energy']}"
    await bot.send(ev, res)
   
   
@sv.on_fullmatch('mimikko energy')
async def mimikko_sign_in(bot, ev):
    sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id,authorization)
    res =f'Energy Info:\n'
    res +=f"code: {energy_info_data['code']}\n"
    res +=f"msg: {energy_info_data['msg']}\n"
    res +=f"经验：{energy_info_data['body']['Favorability']}/{energy_info_data['body']['MaxFavorability']}\n"
    res+=f"Energy: {energy_info_data['body']['Energy']}\n"
    res+="================\nEnergy Reward:\n"
    res+=f"{energy_reward_data}\n"
    await bot.send(ev, res)

async def mimikko_sign_in_auto():
    sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id,authorization)
    res="Sign Data:\n"
    res +=f"获得成长值Reward：{sign_data['body']['Reward']}\n"
    res +=f"获得硬币GetCoin：{sign_data['body']['GetCoin']}\n"
    if sign_data['code']=='0':
        res +=f"[CQ:image,file=file:///{drawSigncard(sign_data)}]\n"
    res +="================\nSign History:\n"
    day_list=[]
    for item in sign_history['body']['signLogs']:
        rex_data=re.search('(?P<月>.*)月(?P<日>.*)日',timeStamp2time(item['signDate']))
        if rex_data.group('月') == re.search('(?P<月>.*)月(?P<日>.*)日',
            timeStamp2time(sign_history['body']['startTime'])).group('月'):
            day_list.append(rex_data.group('日'))
    img_path= drawMonth(datetime.datetime.now().month,day_list,plugin_path)
    res +=f'[CQ:image,file=file:///{plugin_path}/{img_path}]'
    await bot.send_group_msg(group_id=group_id,message=res)


scheduler.add_job(mimikko_sign_in_auto, 'cron',hour='12')
# scheduler.add_job(mimikko_sign_in, 'cron', hour='5',minute='30')
