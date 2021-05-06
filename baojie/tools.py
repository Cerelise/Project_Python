import pymysql
import pandas as pd
import numpy as np


def get_conn():
    conn = pymysql.connect(
        host='127.0.0.1',
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


def get_aver(data):
    if isinstance(data, str) and '-' in data:
        low, high = data.split('-')
        return (int(low)+int(high))/2
    else:
        return int(data)


def dw_None_dis(data):
    if data is None:
        return np.nan
    else:
        return int(data)


def dw_None_latlon(data):
    if data is None or data == '':
        return np.nan
    else:
        return float(data)


def get_data_price():
    sql = """
        select  * from data_sample
    """
    df = pd.DataFrame(exe_sql(sql),
                      columns=['_id', 'bathroom_num', 'bedroom_num', 'bizcircle_name', 'city', 'dist', 'distance',
                               'frame_orientation', 'hall_num', 'house_tag', 'house_title', 'latitude', 'layout',
                               'longitude', 'm_url', 'rent_area', 'rent_price_listing', 'rent_price_unit',
                               'resblock_name', 'type'])
    df.drop(columns='_id',inplace=True)
    df['rent_area'] = df['rent_area'].apply(get_aver)
    df.drop(df[df['rent_area'] < 5].index,inplace=True)
    df.drop(columns='rent_price_unit',inplace=True)
    df['rent_price_listing'] = df['rent_price_listing'].apply(get_aver)
    df.drop('m_url', inplace=True, axis=1)
    return df


def get_data_taitan():
    sql = """
        select pclass,survived,name,age,embarked,room,ticket,boat,sex from titanic
    """
    df = pd.DataFrame(
        exe_sql(sql),
        columns=['pclass','survived','name','age','embarked','room','ticket','boat','sex'])
    return df
