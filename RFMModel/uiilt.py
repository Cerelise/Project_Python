import datetime
import pymysql
import pandas as pd


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_conn():
    conn = pymysql.connect(
        host='10.178.98.32',
        user='root',
        password='123456',
        db='big_data'
    )
    cur = conn.cursor()
    return conn, cur


def close_conn(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()


def exe_sql(sql, *args):
    conn, cur = get_conn()
    cur.execute(sql, *args)
    ret = cur.fetchall()
    close_conn(conn, cur)
    return ret


def get_data():
    sql = """
        select
           invoice,StockCode,Description,Quantity,InvoiceDate,Price,`Customer ID`,Country
        from online_data    
    """
    data = pd.DataFrame(exe_sql(sql),
                        columns=['invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'Price',
                                 'Customer ID', 'Country'])
    data.drop(['Description'], axis=1, inplace=True)
    data['Customer ID'] = data['Customer ID'].fillna('U')
    data['amount'] = data['Quantity'] * data['Price']
    data['date'] = [x.split(' ')[0] for x in data['InvoiceDate']]
    data['time'] = [x.split(' ')[1] for x in data['InvoiceDate']]
    data.drop(['InvoiceDate'], axis=1, inplace=True)
    data['year'] = [x.split('/')[0] for x in data['date']]
    data['month'] = [x.split('/')[1] for x in data['date']]
    data['day'] = [x.split('/')[2] for x in data['date']]
    data['date'] = pd.to_datetime(data['date'])
    data = data.drop_duplicates()
    df1 = data.loc[data['Quantity']<=0]
    df2 = data.loc[data['Price']<=0]

    return data
