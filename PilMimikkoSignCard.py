import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


plugin_path='C:/tmp/xcwbot/xcwbot/HoshinoBot_go/hoshino/modules/zfjbot-mimikko/'
# plugin_path='./'

description_font = os.path.join(plugin_path,'fonts/思源黑体SourceHanSansCN-Medium.otf')
description_font_size = 32



NotLoadImUrlTxtPath=os.path.join(plugin_path,'NotLoadImUrls.txt')
LogTxtPath=os.path.join(plugin_path,'Log.txt')
ImSetDir=os.path.join(plugin_path,'ImSet')
if not os.path.isdir(ImSetDir):
    os.makedirs(ImSetDir)

def drawSigncard(sign_data):
    if sign_data['code'] == '0':
        ImUrl=sign_data['body']['PictureUrl']
        ImDescription=sign_data['body']['Description']
        ImPictureName=sign_data['body']['Name']
        with open(NotLoadImUrlTxtPath,'w') as FId,open(LogTxtPath,'w') as FId2:
            _, ImName = os.path.split(ImUrl.strip())
            SaveImPath = os.path.join(ImSetDir, ImName)
            try:
                r = requests.get(ImUrl.strip())
            except Exception as error:
                FId.writelines(ImUrl)
                MsgTxt='not download {} Connection refused\n'.format(ImName)
                print(MsgTxt)
                FId2.writelines(MsgTxt)
                return error
            StatCode = r.status_code
            if StatCode == 403 or StatCode == 404:
                FId.writelines(ImUrl)
                MsgTxt = 'not download {} {} error\n'.format(ImName,StatCode)
                print(MsgTxt)
                FId2.writelines(MsgTxt)
            try:
                Im=Image.open(BytesIO(r.content))
                # print(Im.size) # 900,540
                # 保存原图
                Im.save(SaveImPath)
                # 绘制背景
                bg=Image.new(mode='RGB',size=(964,833),color="white")
                bg.paste(Im,(32,32))
                
                # 绘制文字
                draw = ImageDraw.Draw(bg)
                font=ImageFont.truetype(description_font, size=description_font_size)

                # 文字分割换行
                strList = []
                newStr = ''
                index = 0
                for item in ImDescription:
                    newStr += item
                    if len(newStr) > 25 or index == len(ImDescription)-1:
                        strList.append(newStr)
                        newStr = ''
                    index += 1
                index=0
                for item in strList:
                    draw.text(
                        (80, 600+int(index*1.2*description_font_size)),
                        item, 
                        fill=(129,129,129,), 
                        font=font)
                    index += 1

                # 绘制pictureName
                font_width, font_height = draw.textsize(ImPictureName, font)
                draw.text(
                    (bg.size[0]-font_width-80, bg.size[1]-font_height-60),
                    ImPictureName, 
                    fill=(168,168,168,), 
                    font=font)   

                # 绘制pluginName
                text='MimikkoAutoSign'
                font_width, font_height = draw.textsize(text, font)
                draw.text(
                    ((bg.size[0]-font_width)/2, bg.size[1]-font_height-16),
                    text=text, 
                    fill=(135,135,135,), 
                    font=font
                    )        

                bg.save(os.path.join(ImSetDir, 'SignCard.jpg'))
                MsgTxt='download {} with requests.get({})\n'.format(ImName,ImUrl)
                FId2.writelines(MsgTxt)
                return os.path.join(ImSetDir, 'SignCard.jpg')
            except Exception as error:
                FId.writelines(ImUrl)
                MsgTxt ='not download {} with ERROR: {}\n'.format(ImName,error)
                FId2.writelines(MsgTxt)
                return error
    else:
        return 'sign_data error'