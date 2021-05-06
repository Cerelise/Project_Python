import pymysql
import pandas as pd
import numpy as np
from flask import Flask, render_template
import json
import random

app = Flask(
    import_name=__name__,
    static_folder='static',
    template_folder='template'
)



def get_comm():
    conn = pymysql.connect(host='localhost',user='root',password='123456',db='big_data')
    cur = conn.cursor()

    return conn,cur

def close_conn(conn,cur):
    if cur:
        cur.close()
    if conn:
        conn.close()

def get_data(sql,*args):
    conn,cur = get_comm()
    cur.execute(sql)
    ret = cur.fetchall()
    close_conn(conn,cur)
    return ret

@app.route('/')
def index():
    return render_template('index.html')


def clean_industry(industry):
    industry = industry.split(',')
    if industry[0] == '移动互联网' and len(industry) > 1:
        return industry[1]
    else:
        return industry[0]


@app.route('/indexData', methods=['post'])
def indexData():

    sql = "select * from lagou"
    data = pd.DataFrame(
        get_data(sql),
        columns=['id', '_id', 'adWord', 'appShow', 'approve', 'businessZones',
                 'city', 'companyFullName', 'companyId', 'companyLabelList',
                 'companyLogo', 'companyShortName', 'companySize', 'createTime',
                 'deliver', 'district', 'education', 'explain', 'financeStage',
                 'firstType', 'formatCreateTime', 'gradeDescription', 'hitags',
                 'imState', 'industryField', 'industryLables', 'isHotHire',
                 'isSchoolJob', 'jobNature', 'lastLogin', 'latitude', 'linestaion',
                 'longitude', 'pcShow', 'plus', 'positionAdvantage', 'positionId',
                 'positionLables', 'positionName', 'promotionScoreExplain',
                 'publisherId', 'resumeProcessDay', 'resumeProcessRate', 'salary',
                 'score', 'secondType', 'skillLables', 'stationname', 'subwayline',
                 'thirdType', 'workYear', 'job_detail'])
    data["salary"] = data["salary"].str.lower() \
        .str.extract(r'(\d+)[k]-(\d+)k') \
        .applymap(lambda x: int(x)) \
        .mean(axis=1)

    demand = data.groupby('city').size().sort_values()[:11]
    industry = data["industryField"].value_counts().sort_values()[190:]
    salary = round(data.groupby('city').mean()['salary'], 0)

    text = {}
    text['demand'] = demand.index.tolist()
    text['demand_val'] = demand.values.tolist()
    text['industry'] = industry.index.tolist()
    text['industry_val'] = industry.values.tolist()
    text['salary'] = salary.index.tolist()
    text['salary_val'] = salary.values.tolist()
    data_city = data[(data['city'] == '北京') | (data['city'] == '广州') | (data['city'] == '上海') | (data['city'] == '深圳')]
    data_salary = data_city[['city', 'salary', 'createTime']]
    data_salary['time'] = pd.to_datetime(data_salary['createTime']).dt.day
    data_salary = round(data_salary.groupby(['city', 'time']).sum())
    data_salary = data_salary.unstack()

    text['city'] = data_city['salary'].tolist()

    return text


@app.route('/student', methods=['post'])
def student():

    sql = 'select * from `student-mat`'

    data = pd.DataFrame(
        get_data(sql),
        columns=['school', 'sex', 'age', 'address', 'famsize', 'pstatus', 'medu',
                 'fedy', 'mjob', 'fjob', 'reason', 'guardian', 'traveltime',
                 'studytime', 'failures', 'schoolsup', 'famsup', 'paid',
                 'activities', 'nursery', 'higher', 'internet', 'romantic',
                 'famrel', 'freetime', 'goout', 'dalc', 'walc', 'health',
                 'absences', 'g1', 'g2', 'g3'])


    data['dalc'] = data['dalc'] + data['walc']
    lis = []
    for i in range(11):
        lis.append(len(data[data.dalc == i]))

    text = {}
    text['dalc'] = lis

    sizes = []
    for i in range(2, 11):
        sizes.append(sum(data[data.dalc == i].g3))
    text['grade'] = sizes

    lis2 = []
    for i in range(2, 11):
        lis2.append(sum(data[data.dalc == i].g3) / float(len(data[data.dalc == i])))

    text['alcohol'] = lis2

    return text


@app.route('/price', methods=['post'])
def vehicles():
    sql = 'select * from test'

    data = pd.DataFrame(get_data(sql), columns=['id', 'name', 'price', 'comment', 'city'])

    lis = []
    for i in data['comment']:
        start = i.split('条')[0].replace(',', ' ').replace(' ', '')
        lis.append(start)
    data['comment'] = lis
    price = round(data.groupby('city').mean()['price'], 2)

    text = {}
    text['price'] = price.values.tolist()
    text['Pname'] = price.index.tolist()
    data['comment'] = data['comment'].astype(int)
    comment = data.groupby('city').sum()['comment']
    text['comment'] = comment.values.tolist()
    Cdata = data.sort_values('comment')
    Cdata = Cdata.iloc[123:]

    text['nametop'] = Cdata['name'].tolist()
    text['pricetop'] = Cdata['price'].tolist()
    text['commenttop'] = Cdata['comment'].tolist()
    text['citytop'] = Cdata['city'].tolist()

    Sdata = data.groupby('city').size()
    text['Ccity'] = Sdata.index.tolist()
    text['Csize'] = Sdata.values.tolist()

    lis = []
    lis2 = []
    for i in range(len(data)):
        lis.append(random.randint(0, 1))
        lis2.append(1)
    data['lv'] = lis
    data['lv2'] = lis2
    dataA = data.groupby(['city', 'lv']).size().unstack()
    lv = round(dataA[0] / data.groupby('city').count()['lv2'] * 100, 2)
    lv.dropna(inplace=True)
    text['city'] = lv.index.tolist()
    text['lv'] = lv.values.tolist()

    return text


def get_name(data):
    a = data['province']
    if a == '山东' or a == '江苏' or a == '安徽' or a == '浙江' or a == '江西' or a == '福建' or a == '上海':
        name = '华东地区'
    elif a == '广东' or a == '广西' or a == '海南':
        name = '华南地区'
    elif a == '湖北' or a == '湖南' or a == '河南':
        name = '华中地区'
    elif a == '北京' or a == '天津' or a == '河北' or a == '山西' or a == '内蒙古':
        name = '华北地区'
    elif a == '宁夏' or a == '新疆' or a == '青海' or a == '陕西' or a == '甘肃':
        name = '西北地区'
    elif a == '四川' or a == '云南' or a == '贵州' or a == '西藏' or a == '重庆':
        name = '西南地区'
    else:
        name = '东北地区'
    return name


@app.route('/pinfen', methods=['post'])
def tttttt():
    sql = "select * from hotel"

    data = pd.DataFrame(get_data(sql), columns=['name', 'comment', 'grade', 'city', 'province'])

    data['area'] = data.apply(lambda x: get_name(x), axis=1)
    data1 = data.groupby(['area', 'comment']).size().unstack()
    text = {}
    text['youyi'] = data1['优异的'].tolist()
    text['hao'] = data1['好'].tolist()
    text['haojil'] = data1['好极了'].tolist()
    text['henb'] = data1['很棒'].tolist()
    text['feic'] = data1['非常好'].tolist()
    text['index'] = data1.index.tolist()

    number, day, lis, lis2, order, actual = [], [], [], [], [], []

    for i in range(len(data)):
        lis.append(random.randint(1, 5))
        lis2.append(1)
        number.append(random.randint(123, 389))
        day.append(random.randint(1, 30))
        tmp = random.randint(123, 299)
        order.append(tmp)
        actual.append((tmp - random.randint(30, 90)))
    data['rate'] = lis
    data['whole'] = lis2
    data['day'] = day
    data['number'] = number
    data['order'] = order
    data['actual'] = actual
    diqu = round(data[data['rate'] > 3].groupby('area').count()['rate'] / data.groupby('area').count()['whole'],
                 6).sort_values(ascending=False)
    text['diqu'] = diqu.index.tolist()
    text['chuzu'] = diqu.values.tolist()
    data['amount'] = data['day'] * data['number']
    test = data.groupby('province').sum()
    text['city'] = test.index.tolist()
    text['amount'] = test['amount'].tolist()
    stay = data.groupby('province').agg({'city': np.size,
                                         'order': np.sum,
                                         'actual': np.sum}).sort_values('city', ascending=False).head(5)

    text['top5name'] = stay.index.tolist()
    text['top5city'] = stay['city'].tolist()
    text['top5order'] = stay['order'].tolist()
    text['top5actual'] = stay['actual'].tolist()
    zhushu = data.groupby('province').sum()['order'].sort_values(ascending=False)
    text['ti1key'] = zhushu.index.tolist()
    text['ti1value'] = zhushu.values.tolist()
    zhushu.head(5)

    return text


@app.route('/salary')
def salary():
    return render_template('salary.html')


def t(data):
    if data == '互联网' or data == '计算机软件' or \
            data == '移动互联网' or data == '电子商务' or \
            data == '数据服务' or data == '互联网金融' or \
            data == '游戏' or data == '在线教育' or \
            data == '生活服务' or data == 'O2O' or \
            data == '医疗健康' or data == '贸易/进出口' or \
            data == '企业服务' or data == '银行':
        name = data
    else:
        name = '其他行业'

    return name


@app.route('/job', methods=['post'])
def job():
    sql = 'select * from job'

    data = pd.DataFrame(get_data(sql), columns=['job', 'city', 'com', 'sal', 'edu', 'exe', 'ind'])

    data.drop_duplicates(keep='first', inplace=True)
    data = data[~data['job'].str.contains('实习')]
    data['bottom'] = data['sal'].str.extract('^(\d+).*')
    data['top'] = data['sal'].str.extract('^.*?-(\d+).*')
    data['top'].fillna(data['bottom'], inplace=True)
    lis = []
    for i in data['city']:
        city = i.split('·')[0]
        lis.append(city)
    data['city'] = lis
    data['com_pct'] = data['sal'].str.extract('^.*?·(\d{2})薪')
    data['com_pct'].fillna(12, inplace=True)
    data['com_pct'] = data['com_pct'].astype('float64')
    data['com_pct'] = data['com_pct'] / 12
    data['bottom'] = data['bottom'].astype(np.int64)
    data['top'] = data['top'].astype(np.int64)
    data['avgSal'] = (data['bottom'] + data['top']) / 2 * data['com_pct']
    data['avgSal'] = data['avgSal'].astype(np.int64)
    df = data[(data['avgSal'] > 2) & (data['avgSal'] < 55)]
    df['exe'].replace('5-10年学历', '5-10年', inplace=True)
    df['exe'].replace('3-5年学历', '3-5年', inplace=True)
    df['exe'].replace('经验不限学历', '经验不限', inplace=True)
    df['exe'].replace('1-3年学历', '1-3年', inplace=True)
    df['exe'].replace('1年以内学历', '1年以内', inplace=True)
    df['exe'].replace('经验不限中专/', '经验不限', inplace=True)
    df['exe'].replace('1年以内中专/', '1年以内', inplace=True)
    df['exe'].replace('1-3年中专/', '1-3年', inplace=True)
    df['ind'] = df['ind'].apply(lambda x: t(x))
    mean_median = df['avgSal'].groupby(df['city']).agg([np.mean, np.median])
    text = {}
    text['mean_sal'] = mean_median['mean'].astype(np.int64).tolist()
    text['median_sal'] = mean_median['median'].tolist()
    text['index_sal'] = mean_median.index.tolist()
    avg_sum = df.groupby('avgSal').size().head(30)
    text['xin'] = avg_sum.index.tolist()
    text['gang'] = avg_sum.values.tolist()
    big = df[df['avgSal'] > 6].groupby('city').size()
    small = df[df['avgSal'] < 6].groupby('city').size()
    text['bigKey'] = big.index.tolist()
    text['bigValue'] = big.values.tolist()
    text['smallValue'] = small.values.tolist()
    text['smallKey'] = small.index.tolist()

    text['bei'] = df[df['city'] == '北京']['avgSal'].values.tolist()
    text['shang'] = df[df['city'] == '上海']['avgSal'].values.tolist()
    text['guang'] = df[df['city'] == '广州']['avgSal'].values.tolist()
    text['shen'] = df[df['city'] == '深圳']['avgSal'].values.tolist()
    text['hang'] = df[df['city'] == '杭州']['avgSal'].values.tolist()

    text['meanSal'] = df['avgSal'].groupby(df['edu']).mean().astype(int).values.tolist()
    text['medianSal'] = df['avgSal'].groupby(df['edu']).median().astype(int).values.tolist()
    text['eduSal'] = df['avgSal'].groupby(df['edu']).median().index.tolist()
    text['diploma'] = df['edu'].value_counts().values.tolist()
    text['dipSal'] = df['edu'].value_counts().index.tolist()

    text['exeSalName'] = df.groupby('exe').mean()['avgSal'].index.tolist()
    text['exeSalMean'] = df.groupby('exe').mean()['avgSal'].astype(np.int64).values.tolist()
    text['exeSalMedian'] = df.groupby('exe').median()['avgSal'].values.tolist()
    text['experience'] = df['exe'].value_counts().index.tolist()
    text['exeIndex'] = df['exe'].value_counts().index.tolist()
    text['exeValue'] = df['exe'].value_counts().values.tolist()

    text['indName'] = df['avgSal'].groupby(df['ind']).mean().index.tolist()
    text['indMean'] = df['avgSal'].groupby(df['ind']).mean().astype(np.int64).values.tolist()
    text['indMedian'] = df['avgSal'].groupby(df['ind']).median().values.tolist()

    text['indName'] = df.groupby(['ind']).size().index.tolist()
    text['indValue'] = df.groupby(['ind']).size().values.tolist()

    return text



@app.route('/train')
def tarin():
    return render_template('train.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')


@app.route('/bike',methods=['post'])
def bike():
    sql = 'select * from train'

    data = pd.DataFrame(get_data(sql),columns=['date','season','holiday','workingday','weather','temp','atemp','humidity','windspeed','casual','registered','count'])

    data['date'] = pd.to_datetime(data['date'])

    countData = round(data.groupby(data['date'].dt.year).sum()['count'] / 1000, 0).astype(int)
    hourData = round(data.groupby(data['date'].dt.hour).mean()['count'],2)
    monthData = data.groupby(data['date'].dt.month).mean()['count'].astype(int)
    weather = data.groupby('weather').mean()['count'].astype(int)
    windspeed = data.groupby('windspeed').max()['count'].astype(int)
    data['temp'] = data['temp'].astype(int)
    temp = data.groupby('temp').mean()['count']
    monthW = data.groupby([data['date'].dt.month, 'weather']).count()['count'].unstack()

    text = {}

    text['countDate'] = countData.index.tolist()
    text['countData'] = countData.values.tolist()

    text['hourDate'] = hourData.index.tolist()
    text['hourData'] = hourData.values.tolist()

    text['monthDate'] = monthData.index.tolist()
    text['monthData'] = monthData.values.tolist()

    text['weatherData'] = weather.values.tolist()

    text['windspeedData'] = windspeed.index.astype(int).tolist()
    text['windspeedvalue'] = windspeed.values.tolist()

    text['tempName'] = temp.index.tolist()
    text['tempValue'] = temp.values.astype(int).tolist()

    text['qin'] = monthW.loc[:,1].tolist()
    text['yin'] = monthW.loc[:,2].tolist()
    text['xue'] = monthW.loc[:,3].tolist()

    return text


·

if __name__ == '__main__':
    app.run(debug=True)
