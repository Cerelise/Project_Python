import re

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


def comment_p(x):
    x = x.replace(r'+','')
    if '万' in x:
        x = x.replace(r'万','')
        x = float(x)*10000
        return x
    else:
        return x


def new_group(frame):
    test_group = []
    for i in range(len(frame)):
        if frame.iloc[i,4].find('自营')>=0:
            test_group.append('京东自营')
        elif frame.iloc[i,4].find('旗舰店')>=0:
            test_group.append('旗舰店')
        elif frame.iloc[i,4].find('专营店')>=0:
            test_group.append('专营店')
        else:
            test_group.append('其他')
    frame['newgroup'] = test_group

def get_data():

    sql = """
        select price,name,url,comment,shopname from csvjd
    """
    data = pd.DataFrame(exe_sql(sql),columns=['price','name','url','comment','shopname'])
    data.drop_duplicates(inplace=True)
    data['new_comment'] = data['comment'].apply(lambda x:comment_p(x)).astype(int)
    return data
