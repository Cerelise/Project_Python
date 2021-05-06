import requests
import json
import pandas as pd
import time
from fake_useragent import UserAgent

headers = {
    UserAgent().random,
}
###基金类型
dict_type = {"股票型": 1, "混合型": 3, "债券型": 2, "指数型": 5, "QDII型": 11}
###时间
dict_time = {'近一周': '1w', '近一月': '1m', '近三月': '3m', '近六月': '6m', '近1年': '1y', '近2年': '2y', '近3年': '3y', '近5年': '5y'}


def analysis1():
    Res = pd.DataFrame()

    for key in dict_type:
        # SIZE为数量；order_by对应时间
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(dict_type[key]) + "&order_by=3m&size=200&page=1"

        res = requests.get(url, headers=headers)
        time.sleep(0.5)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        s = s['data']['items']

        for i in range(0, len(s)):
            result = {
                '基金类型': key,
                '基金名称': s[i]['fd_name'],
                '净值': s[i]['yield'],
                '时间': '近三月'
            }

            print(result)
            Res = Res.append(result, ignore_index=True)

    Res.to_excel('基金近三月.xlsx', index=False)
    print('ok')


##2：基金各个阶段涨跌幅
def analysis2():
    name = ['近1周', '近1月', '近3月', '近6月', '近1年', '近3年', '近5年']
    ##五类基金
    dict_value = {}

    for key in dict_type:
        #### 获取排名第一名基金代号
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(dict_type[key]) + "&order_by=1w&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        ###取第一名
        fd_code = s['data']['items'][0]['fd_code']

        #### 获取排名第一名基金各个阶段情况
        fu_url = "https://danjuanapp.com/djapi/fund/derived/" + str(fd_code)
        res = requests.get(fu_url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        data = s['data']

        valuess = []

        ####防止基金最长时间不够1年、2年、5年的情况报错，用0填充
        ##近1周
        try:
            valuess.append(data['nav_grl1w'])
        except:
            valuess.append(0)
        ##近1月
        try:
            valuess.append(data['nav_grl1m'])
        except:
            valuess.append(0)
        ##近3月
        try:
            valuess.append(data['nav_grl3m'])
        except:
            valuess.append(0)
        ##近6月
        try:
            valuess.append(data['nav_grl6m'])
        except:
            valuess.append(0)
        ##近1年
        try:
            valuess.append(data['nav_grl1y'])
        except:
            valuess.append(0)
        ##近3年
        try:
            valuess.append(data['nav_grl3y'])
        except:
            valuess.append(0)
        ##近5年
        try:
            valuess.append(data['nav_grl5y'])
        except:
            valuess.append(0)

        dict_value[key] = valuess

    print(dict_value)


###3：近30个交易日净值情况
def analysis3():
    Res = pd.DataFrame()
    for key in dict_type:
        #### 获取排名第一名基金代号
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(
            dict_type[key]) + "&order_by=1w&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        # print(s)
        ###取第一名
        fd_code = s['data']['items'][0]['fd_code']
        fd_name = s['data']['items'][0]['fd_name']

        #### 获取排名第一名基金近30个交易日净值情况
        fu_url = "https://danjuanapp.com/djapi/fund/nav/history/" + str(fd_code) + "?size=30&page=1"
        res = requests.get(fu_url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        # print(s)
        data = s['data']['items']
        # name=[]
        # value=[]
        for k in range(0, len(data)):
            # name.append(data[k]['date'])
            # value.append(data[k]['nav'])
            result = {
                '基金类型': key,
                '基金名称': fd_name,
                '净值': data[k]['nav'],
                '时间': data[k]['date'],
            }

            print(result)
            Res = Res.append(result, ignore_index=True)

    Res.to_excel('第一名基金近30个交易日净值情况.xlsx', index=False)
    print('ok')