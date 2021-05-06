import pandas as pd
import numpy as np
import jieba
import pymysql
from flask import Flask, render_template
import json

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = Flask(
    import_name=__name__,
    static_folder='static',
    template_folder='template'
)


def get_conn():
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='big_data')
    cur = conn.cursor()
    return conn, cur


def close_conn(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()


def get_data(sql, *args):
    conn, cur = get_conn()
    cur.execute(sql)
    ret = cur.fetchall()
    close_conn(conn, cur)
    return ret


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main', methods=['post'])
def main():
    sql = 'select * from hr_comma_sep'
    data = pd.dataFrame(get_data(sql),
                        columns=['level', 'evaluation', 'project', 'avg_hours', 'time_spend', 'work', 'left', 'years5',
                                 'sales', 'salary'])
    data['sales'] = data['sales'].astype('category')
    data['salary'] = data['salary'].astype('category')
    left = data.groupby('left').size()
    time_spend = data.groupby('time_spend').mean()['level']
    sales = data.groupby(['left', 'sales']).count()['level'].unstack()
    salary = data.groupby(['salary', 'sales']).count()['level'].unstack()
    leftSalary = data.groupby(['left', 'salary']).count()['level'].unstack()
    level = data.groupby(['left', 'level']).count()['salary'].unstack().fillna(0)

    text = {}
    text['left'] = left.values.tolist()
    text['spendTime'] = time_spend.index.tolist()
    text['spendNum'] = time_spend.values.tolist()
    text['zaizhi'] = sales.loc[0].values.tolist()
    text['lizhi'] = sales.loc[1].values.tolist()
    text['salesColumns'] = sales.columns.tolist()
    text['salary'] = salary.columns.tolist()
    text['high'] = salary.loc['high'].values.tolist()
    text['low'] = salary.loc['low'].values.tolist()
    text['medium'] = salary.loc['medium'].values.tolist()
    text['salaryName'] = leftSalary.columns.tolist()
    text['zaizhiS'] = leftSalary.loc[0].values.tolist()
    text['lizhiS'] = leftSalary.loc[1].values.tolist()
    text['level'] = level.columns.tolist()
    text['zaizhiL'] = level.loc[0].values.tolist()
    text['lizhiL'] = level.loc[1].values.tolist()

    return text


@app.route('/pro')
def pro():
    return render_template('pro.html')


@app.route('/production', methods=['post'])
def production():
    sql = 'select * from production'
    df = pd.dataFrame(get_data(sql),
                      columns=['area', 'year', 'total_value', 'one_value', 'two_value', 'three_value', 'zero_value',
                               'inout', 'population', 'pay', 'student', 'hospital', 'realty'])
    df['realty'] = df['realty'].fillna(value=df['realty'].mean())
    total_value = df.groupby(['year', 'area']).sum()['total_value'].unstack()
    one_value = df.groupby(['year', 'area']).sum()['one_value'].unstack()
    two_value = df.groupby(['year', 'area']).sum()['two_value'].unstack()
    zero_value = df.groupby(['year', 'area']).sum()['zero_value'].unstack()
    inout = df.groupby(['year', 'area']).sum()['inout'].unstack()
    pay = df.groupby(['year', 'area']).sum()['pay'].unstack()
    student = df.groupby(['year', 'area']).sum()['student'].unstack()
    hospital = df.groupby(['year', 'area']).sum()['hospital'].unstack()
    realty = df.groupby(['year', 'area']).sum()['realty'].unstack()

    text = {}
    text['city'] = total_value.columns.tolist()
    text['total15'] = total_value.loc[2015].values.tolist()
    text['total16'] = total_value.loc[2016].values.tolist()
    text['total17'] = total_value.loc[2017].values.tolist()

    text['one15'] = one_value.loc[2015].values.tolist()
    text['one16'] = one_value.loc[2016].values.tolist()
    text['one17'] = one_value.loc[2017].values.tolist()

    text['two15'] = two_value.loc[2015].values.tolist()
    text['two16'] = two_value.loc[2016].values.tolist()
    text['two17'] = two_value.loc[2017].values.tolist()

    text['zero15'] = zero_value.loc[2015].values.tolist()
    text['zero16'] = zero_value.loc[2016].values.tolist()
    text['zero17'] = zero_value.loc[2017].values.tolist()

    text['inout15'] = inout.loc[2015].values.tolist()
    text['inout16'] = inout.loc[2016].values.tolist()
    text['inout17'] = inout.loc[2017].values.tolist()

    text['pay15'] = pay.loc[2015].values.tolist()
    text['pay16'] = pay.loc[2016].values.tolist()
    text['pay17'] = pay.loc[2017].values.tolist()

    text['student15'] = student.loc[2015].values.tolist()
    text['student16'] = student.loc[2016].values.tolist()
    text['student17'] = student.loc[2017].values.tolist()

    text['hospital15'] = hospital.loc[2015].values.tolist()
    text['hospital16'] = hospital.loc[2016].values.tolist()
    text['hospital17'] = hospital.loc[2017].values.tolist()

    text['realty15'] = realty.loc[2015].values.tolist()
    text['realty16'] = realty.loc[2016].values.tolist()
    text['realty17'] = realty.loc[2017].values.tolist()

    return text


@app.route('/super')
def super():
    return render_template('super.html')


@app.route('/superstore', methods=['post'])
def superstore():
    sql = 'select * from superstore'
    data = pd.DataFrame(get_data(sql),
                        columns=['rowId', 'orderId', 'orderdata', 'shipdata', 'shipMode', 'customerId', 'customerName',
                                 'segment', 'city', 'state', 'country', 'postalCode', 'market', 'region', 'productId',
                                 'category', 'subCategory', 'productName', 'sales', 'quantity', 'discount', 'profit',
                                 'shipping', 'orderPriority'])
    data1 = data.loc[0:19628, :]
    data2 = data.loc[19628:50129, :]
    data1['orderdata'] = pd.to_datetime(data['orderdata'], format='%d/%m/%Y', errors='coerce')
    data2['orderdata'] = pd.to_datetime(data['orderdata'], format='%d-%m-%Y', errors='coerce')
    data = pd.concat([data1, data2], axis=0)
    data.sort_values(by='orderdata', ascending=True, na_position='first', inplace=True)
    data.dropna(inplace=True)
    data['month'] = data['orderdata'].dt.month
    data['year'] = data['orderdata'].dt.year
    data['price'] = data['sales'] / data['quantity']
    data_sale = data.groupby('year').sum()[['sales', 'profit', 'quantity']]
    data_sale['rate'] = data_sale['profit'] / data_sale['sales']
    data_sale_month = pd.pivot_table(data, index='month', columns='year', values=['sales', 'profit', 'quantity'],
                                     aggfunc='sum')

    text = {}

    text['year_sale'] = data_sale.index.astype(int).tolist()
    text['sales'] = data_sale['sales'].astype(int).tolist()
    text['profit'] = data_sale['profit'].astype(int).tolist()
    text['quantity'] = data_sale['quantity'].astype(int).tolist()

    text['month'] = data_sale_month['sales'].index.astype(int).tolist()
    text['sales_11'] = data_sale_month['sales'][2011.0].astype(int).tolist()
    text['sales_12'] = data_sale_month['sales'][2012.0].astype(int).tolist()
    text['sales_13'] = data_sale_month['sales'][2013.0].astype(int).tolist()
    text['sales_14'] = data_sale_month['sales'][2014.0].astype(int).tolist()

    text['profit_11'] = data_sale_month['profit'][2011.0].astype(int).tolist()
    text['profit_12'] = data_sale_month['profit'][2012.0].astype(int).tolist()
    text['profit_13'] = data_sale_month['profit'][2013.0].astype(int).tolist()
    text['profit_14'] = data_sale_month['profit'][2014.0].astype(int).tolist()

    text['quantity_11'] = data_sale_month['quantity'][2011.0].astype(int).tolist()
    text['quantity_12'] = data_sale_month['quantity'][2012.0].astype(int).tolist()
    text['quantity_13'] = data_sale_month['quantity'][2013.0].astype(int).tolist()
    text['quantity_14'] = data_sale_month['quantity'][2014.0].astype(int).tolist()

    growth = data_sale_month['sales'].pct_change(axis='columns')
    profi = data.groupby(['region', 'year']).sum()['profit'].unstack()
    text['salary2012'] = growth[2012.0].tolist()
    text['salary2013'] = growth[2013.0].tolist()
    text['salary2014'] = growth[2014.0].tolist()
    text['pro2011'] = profi[2011].astype(int).tolist()
    text['pro2012'] = profi[2012].astype(int).tolist()
    text['pro2013'] = profi[2013].astype(int).tolist()
    text['pro2014'] = profi[2014].astype(int).tolist()
    text['proIndex'] = profi.index.tolist()

    discount = data.groupby('discount').sum()
    text['disSales'] = discount['sales'].values.tolist()
    text['disPro'] = discount['profit'].values.tolist()
    text['disIndex'] = discount.index.tolist()

    category = data.groupby('subCategory').sum()
    text['subCat'] = category.index.tolist()
    text['subSales'] = category['sales'].tolist()
    text['subPro'] = category['profit'].tolist()

    segment = data.groupby('segment')['sales'].count()
    text['segment'] = segment.index.tolist()
    text['segnum'] = segment.values.tolist()

    return text


@app.route('/air')
def air():
    return render_template('air.html')


@app.route('/airData', methods=['post'])
def airData():
    sql = 'select * from air_data'
    data = pd.DataFrame(get_data(sql),
                        columns=['MEMBER_NO', 'FFP_DATE', 'FIRST_FLIGHT_DATE', 'GENDER', 'FFP_TIER', 'WORK_CITY',
                                 'WORK_PROVINCE', 'WORK_COUNTRY', 'AGE', 'LOAD_TIME', 'FLIGHT_COUNT', 'BP_SUM',
                                 'EP_SUM_YR_1', 'EP_SUM_YR_2', 'SUM_YR_1', 'SUM_YR_2', 'SEG_KM_SUM',
                                 'WEIGHTED_SEG_KM', 'LAST_FLIGHT_DATE', 'AVG_FLIGHT_COUNT',
                                 'AVG_BP_SUM', 'BEGIN_TO_FIRST', 'LAST_TO_END', 'AVG_INTERVAL',
                                 'MAX_INTERVAL', 'ADD_POINTS_SUM_YR_1', 'ADD_POINTS_SUM_YR_2',
                                 'EXCHANGE_COUNT', 'AVG_DISCOUNT', 'P1Y_Flight_Count', 'L1Y_Flight_Count',
                                 'P1Y_BP_SUM', 'L1Y_BP_SUM', 'EP_SUM', 'ADD_Point_SUM', 'Eli_Add_Point_Sum',
                                 'L1Y_ELi_Add_Points', 'Points_Sum', 'L1Y_Points_Sum', 'Ration_L1Y_Flight_Count',
                                 'Ration_P1Y_Flight_Count', 'Ration_P1Y_BPS', 'Ration_L1Y_BPS', 'Point_NotFlight'])
    explore = data.describe(percentiles=[], include='all').T
    explore['null'] = len(data) - explore['count']
    explore = explore[['null', 'max', 'min']]
    explore.columns = [u'空数值', u'最大值', u'最小值']
    data['FFP_DATE'] = pd.to_datetime(data['FFP_DATE'], format='%Y/%m/%d')
    FFP = data.groupby(data['FFP_DATE'].dt.year).size()
    text = {}
    text['yearFFP'] = FFP.index.tolist()
    text['numFFP'] = FFP.values.tolist()
    age = data.groupby(['FFP_TIER', 'AGE']).mean()['MEMBER_NO']
    text['age4'] = age[4].index.tolist()
    text['age5'] = age[5].index.tolist()
    text['age6'] = age[6].index.tolist()
    text['lastToEnd'] = data['LAST_TO_END'].values.tolist()
    data_corr = data[['FFP_TIER', 'FLIGHT_COUNT', 'LAST_TO_END',
                      'SEG_KM_SUM', 'EXCHANGE_COUNT', 'Points_Sum']]
    data_corr['AGE'] = data['AGE'].fillna(0).astype('int')
    data_corr['ffp_year'] = data['FFP_DATE'].dt.year
    df_corr = data_corr.corr(method='pearson')
    text['reX'] = df_corr.columns.tolist()
    text['reY'] = df_corr.index.tolist()
    df_corr.index = [0, 1, 2, 3, 4, 5, 6, 7]
    df_corr.columns = [0, 1, 2, 3, 4, 5, 6, 7]
    lis = []
    for i in df_corr.columns:
        for j in df_corr.index:
            lis.append([i, j, round(df_corr[j][i], 2)])
    text['dataS'] = lis
    data = data.loc[data['SUM_YR_1'].notnull() & data['SUM_YR_2'].notnull(), :]
    index1 = data['SUM_YR_1'] != 0
    index2 = data['SUM_YR_2'] != 0
    index3 = (data['SEG_KM_SUM'] > 0) & (data['AVG_DISCOUNT'] != 0)
    index4 = data['AGE'] > 100
    airline = data[(index1 | index2) & index3 & ~index4]
    airline_selection = airline[['FFP_DATE', 'LOAD_TIME', 'LAST_TO_END',
                                 'FLIGHT_COUNT', 'SEG_KM_SUM', 'AVG_DISCOUNT']]
    L = pd.to_datetime(airline_selection['LOAD_TIME']) - \
        pd.to_datetime(airline_selection['FFP_DATE'])
    L = L.astype('str').str.split().str[0]
    L = L.astype('int') / 30
    airline_features = pd.concat([L, airline_selection.iloc[:, 2:]], axis=1)
    airline_features.columns = ['L', 'R', 'F', 'M', 'C']

    data = StandardScaler().fit_transform(airline_features)
    kmeans_model = KMeans(n_clusters=5, n_jobs=4, random_state=123)
    fit_kmeans = kmeans_model.fit(data)
    kmeans_cc = kmeans_model.cluster_centers_

    kmeans_labels = kmeans_model.labels_

    r1 = pd.Series(kmeans_model.labels_).value_counts()

    cluster_center = pd.DataFrame(kmeans_model.cluster_centers_, \
                                  columns=['ZL', 'ZR', 'ZF', 'ZM', 'ZC'])
    cluster_center.index = pd.DataFrame(kmeans_model.labels_). \
                               drop_duplicates().iloc[:, 0]
    text['cus0'] = cluster_center.T[0].values.tolist()
    text['cus1'] = cluster_center.T[1].values.tolist()
    text['cus2'] = cluster_center.T[2].values.tolist()
    text['cus3'] = cluster_center.T[3].values.tolist()
    text['cus4'] = cluster_center.T[4].values.tolist()
    text['cName'] = cluster_center.index.tolist()
    return text


@app.route('/goods')
def goods ():
    return render_template('goods.html')

@app.route('/goodType',methods=['post'])
def goodType():
    sql1 = 'select * from goodsorder'
    sql2 = 'select * from goodstypes'
    data1 = pd.DataFrame(get_data(sql1),columns=['id','goods'])
    data2 = pd.DataFrame(get_data(sql2),columns=['goods','types'])

    group = data1.groupby('goods').count().reset_index().sort_values('id',ascending=False).head(10)

    text = {}
    text['countY'] = group['goods'].tolist()
    text['countX'] = group['id'].tolist()



    return text

if __name__ == '__main__':
    app.run(debug=True)
