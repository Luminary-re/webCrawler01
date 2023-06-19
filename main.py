import datetime

from webCrawler import get_html_text, get_content, get_content2, write_to_csv


def main():  # 主函数，程序入口
    print("Weather test")
    # 这里地区是连云港城区
    # 切换城市只需要更改url后'/101191001.shtml'的'101191001'
    # 例如江苏省南京市建邺区是101190110
    # 因此其7天天气中国天气网地址是'http://www.weather.com.cn/weather/101190110.shtml'
    # 8-15天天气中国天气网是'http://www.weather.com.cn/weather15d/101190110.shtml'
    url1 = 'http://www.weather.com.cn/weather/101191001.shtml'  # 7天天气中国天气网
    url2 = 'http://www.weather.com.cn/weather15d/101191001.shtml'  # 8-15天天气中国天气网

    html1 = get_html_text(url1)
    data1, data1_7 = get_content(html1)  # 获得1-7天和当天的数据

    html2 = get_html_text(url2)
    data8_14 = get_content2(html2)  # 获得8-14天数据
    data14 = data1_7 + data8_14
    # print(data)
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    print(current_time)
    filename14 = '未来14天天气_' + current_time + '.csv'
    filename1 = '未来24小时天气_' + current_time + '.csv'
    write_to_csv(filename14, data14, 14)  # 保存为csv文件
    write_to_csv(filename1, data1, 1)
    print("文件已保存")


if __name__ == '__main__':
    main()
