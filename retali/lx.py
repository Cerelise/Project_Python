import pymysql
import datetime
import pandas as pd




def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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


def exe_sql(sql,*args):
    conn,cur = get_conn()
    cur.execute(sql)
    ret = cur.fetchall()
    close_conn(conn,cur)
    return ret



def get_data():
    sql = """
            select Invoice,StockCode,Description,Quantity,InvoiceDate,price,`Customer ID`,Country from online_data

        """
    online_data = pd.DataFrame(exe_sql(sql),
                               columns=['invoice', 'code', 'description', 'quantity', 'date', 'price', 'ID', 'country'])
    df = online_data.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = df['date'].dt.date
    df['time'] = pd.to_datetime(df['time'])
    df['UnitPrice'] = df['price']
    df['price'] = df.apply(lambda x: x[3] * x[5], axis=1)
    return df