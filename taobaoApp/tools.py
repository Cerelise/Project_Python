import pymysql
import pandas as pd
import datetime

def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



def get_conn():

    conn =pymysql.connect(
        host='10.178.98.32',
        user='root',
        password='123456',
        db='big_data'
    )
    cur = conn.cursor()
    return conn,cur


def close_conn(conn,cur):
    if cur:
        cur.close()
    if conn:
        conn.close()

def exe_sql(sql,*args):
    conn,cur = get_conn()
    cur.execute(sql,*args)
    ret = cur.fetchall()
    close_conn(conn,cur)
    return ret


def get_data():
    sql = """
        select user_id,item_id,item_category,behavior_type,time from userbehavior limit 2500000
    """
    df = pd.DataFrame(exe_sql(sql),
                      columns=['user','item','category','behavior','time'])
    df['time'] = pd.to_datetime(df['time'],unit='s').astype(str)
    df['date'] = df['time'].str[0:10]
    df['hour'] = df['time'].str[11:]
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = pd.to_datetime(df['time'])
    df['hour'] = pd.to_datetime(df['hour'])
    df.sort_values('time',ascending=True,inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

