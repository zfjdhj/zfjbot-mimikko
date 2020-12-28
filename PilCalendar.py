from PIL import Image, ImageDraw, ImageFont
import calendar


def drawMonth(month=1,day_list):
    WEEK = ('SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT')
    MONTH = ('January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December')

    # create new blank picture
    bg= Image.open('indexPC.png').convert("RGBA")
    width, height = bg.size
    img = Image.new('RGBA',bg.size, color=(255,255,255,40))
    img.paste(bg,mask=bg)
    # rows = 2 titles + 5 rows of days + 2(head + footer)blank
    # cols = 7 cols of week + 1 blank for left + 1 col for right
    rows, cols = 9, len(WEEK) + 2
    colSpace, rowSpace = width // cols, height // rows
    
    white_block=Image.new('RGBA',size=(width-200, height-200), color=(255,255,255,90))
    img.paste(white_block,(100,100),mask=white_block)
    # define font and size
    month_font = r'./fonts/DancingScript-Bold.ttf'
    title_font = r'./fonts/DancingScript-Bold.ttf'
    day_font = r'C:./fonts/SitkaZ.ttc'
    month_size, title_size, day_size = 80, 60, 70
    ellipse_r=80

    draw = ImageDraw.Draw(img)
    for i in range(len(WEEK) + 1):
        # draw month title
        if i == 0:
            draw.text((colSpace, rowSpace), MONTH[month-1], fill=(0,0,0,), font=ImageFont.truetype(month_font, size=month_size))
            top = rowSpace // 10
            draw.line(xy=[(colSpace, rowSpace*2-top * 2), (colSpace*7.5, rowSpace*2-top * 2)], fill=(0,0,0))
            draw.line(xy=[(colSpace, rowSpace * 2 - top * 1), (colSpace * 7.5, rowSpace * 2 - top * 1)], fill=(0, 0, 0))
            continue
        # draw week title
        draw.text((colSpace*i, rowSpace*2), WEEK[i-1], fill=(0,0,0), font=ImageFont.truetype(title_font, size=title_size))

    # draw days
    cal = calendar.Calendar(firstweekday=0)
    row, col = 3, 2
    for day in cal.itermonthdays(2020, month):
        if day > 0:
            # if weekday, draw with red color
            if col == 1 or col == 7:
                fill = (255, 0, 0)
            else:
                fill = (255, 255, 255)
            # print(day)
            if day in day_list:    
                draw.ellipse((colSpace * col , rowSpace * row,colSpace * col+ellipse_r, rowSpace * row+ellipse_r),fill ='blue',outline='blue')
            if day <10: 
                draw.text((colSpace * col+ellipse_r/2, rowSpace * row), str(day), fill=fill, font=ImageFont.truetype(day_font, size=day_size))
            else:
                draw.text((colSpace * col-day_size/2+ellipse_r/2, rowSpace * row), str(day), fill=fill, font=ImageFont.truetype(day_font, size=day_size))
        col += 1
        # to a new week
        if col == 8:
            col = 1
            row += 1
    img.save(MONTH[month-1] + '.png')
    return MONTH[month-1] + '.png'
    

if __name__ == '__main__':
    res=drawMonth(month=12)
    print(res)