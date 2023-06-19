import csv
import datetime
import json
import requests
from bs4 import BeautifulSoup


def get_html_text(url):  # 请求获得网页内容
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("成功访问")
        return r.text
    except:
        print("访问错误")
        return " "


def get_content(html):  # 处理得到有用信息保存数据文件
    bs = BeautifulSoup(html, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body

    # 下面爬取当天24小时的数据
    final_day = []  # 存放当天的数据
    data2 = body.find_all('div', {'class': 'left-div'})
    text = data2[2].find('script').string
    text = text[text.index('=') + 1:-2]  # 移除改var data=将其变为json数据
    jd = json.loads(text)
    dayone = jd['od']['od2']  # 找到当天的数据
    count = 0
    for i in dayone:
        temp = []
        if count <= 23:
            temp.append(i['od21'])  # 添加时间
            temp.append(i['od22'])  # 添加当前时刻温度
            temp.append(i['od24'])  # 添加当前时刻风力方向
            temp.append(i['od25'])  # 添加当前时刻风级
            temp.append(i['od26'])  # 添加当前时刻降水量
            temp.append(i['od27'])  # 添加当前时刻相对湿度
            temp.append(i['od28'])  # 添加当前时刻空气质量
            # print(temp)
            final_day.append(temp)
        count = count + 1
    final_day = final_day[::-1]  # 列表逆置

    # 下面爬取7天的数据
    final = []  # 初始化一个列表保存数据
    data = body.find('div', {'id': '7d'})  # 找到div标签且id = 7d
    ul = data.find('ul')  # 找到所有的ul标签
    li = ul.find_all('li')  # 找到左右的li标签
    i = 0  # 控制爬取的天数
    for day in li:  # 遍历找到的每一个li
        if 7 > i > 0:
            temp = []  # 临时存放每天的数据
            date = day.find('h1').string  # 得到日期
            date = date[0:date.index('日')]  # 取出日期号
            temp.append(date)
            inf = day.find_all('p')  # 找出li下面的p标签,提取第一个p标签的值，即天气
            temp.append(inf[0].string)

            tem_low = inf[1].find('i').string  # 找到最低气温

            if inf[1].find('span') is None:  # 天气预报可能没有最高气温
                tem_high = None
            else:
                tem_high = inf[1].find('span').string  # 找到最高气温
            temp.append(tem_low[:-1])
            if tem_high[-1] == '℃':
                temp.append(tem_high[:-1])
            else:
                temp.append(tem_high)

            wind = inf[2].find_all('span')  # 找到风向
            for j in wind:
                temp.append(j['title'])

            wind_scale = inf[2].find('i').string  # 找到风级
            index1 = wind_scale.index('级')
            temp.append(int(wind_scale[index1 - 1:index1]))
            final.append(temp)
        i = i + 1

    return final_day, final


def get_content2(html):  # 处理得到有用信息保存数据文件
    bs = BeautifulSoup(html, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body

    # 下面爬取8-14天的数据
    final = []  # 初始化一个列表保存数据
    data = body.find('div', {'id': '15d'})  # 找到div标签且id = 15d
    ul = data.find('ul')  # 找到所有的ul标签
    li = ul.find_all('li')  # 找到左右的li标签
    i = 0  # 控制爬取的天数
    for day in li:  # 遍历找到的每一个li
        if i < 8:
            temp = []  # 临时存放每天的数据
            date = day.find('span', {'class': 'time'}).string  # 得到日期
            date = date[date.index('（') + 1:-2]  # 取出日期号
            temp.append(date)
            weather = day.find('span', {'class': 'wea'}).string  # 找到天气
            temp.append(weather)
            tem = day.find('span', {'class': 'tem'}).text  # 找到温度
            temp.append(tem[tem.index('/') + 1:-1])  # 找到最低气温
            temp.append(tem[:tem.index('/') - 1])  # 找到最高气温
            wind = day.find('span', {'class': 'wind'}).string  # 找到风向
            if '转' in wind:  # 如果有风向变化
                temp.append(wind[:wind.index('转')])
                temp.append(wind[wind.index('转') + 1:])
            else:  # 如果没有风向变化，前后风向一致
                temp.append(wind)
                temp.append(wind)
            wind_scale = day.find('span', {'class': 'wind1'}).string  # 找到风级
            index1 = wind_scale.index('级')
            temp.append(int(wind_scale[index1 - 1:index1]))
            final.append(temp)
    return final


def write_to_csv(file_name, data, day=14):  # 保存为csv文件
    with open(file_name, 'a', errors='ignore', newline='') as f:
        if day == 14:
            header = ['日期', '天气', '最低气温', '最高气温', '风向1', '风向2', '风级']
        else:
            header = ['小时', '温度', '风力方向', '风级', '降水量', '相对湿度', '空气质量']
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(data)

