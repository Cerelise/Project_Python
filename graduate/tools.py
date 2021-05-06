import pymysql
import pandas as pd
import numpy as np
import datetime
import re


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
    return conn,cur


def close_conn(conn,cur):
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


def tranform_num(x):
    if '-' in x:
        return 0
    else:
        return x



def get_data():
    sql = """
        select 年份,学校名称,院系名称,专业代码,专业名称,总分,政治__管综,外语,业务课_一,业务课_二 from graduate
    """
    df = pd.DataFrame(
        exe_sql(sql),
        columns=['年份','学校名称','院系名称','专业代码','专业名称','总分','政治__管综','外语','业务课_一','业务课_二'])
    df_all = df.drop_duplicates()
    df_all = df_all.dropna(axis=0,how='any')
    df_all['专业名称'] = df_all['专业名称'].str.replace('\(专业学位\)', '')
    df_all['专业名称'] = df_all['专业名称'].str.replace('★', '')
    return df_all



