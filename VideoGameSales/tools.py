import pandas as pd
import pymysql
import numpy as np
import datetime


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
    if cur :
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
        select 
        rank,name,platform,year,genre,publisher,NA_sales,eu_sales,jp_sales,other_sales,global_sales 
        from vgsales
    """
    df = pd.DataFrame(exe_sql(sql),columns=['rank','name','platform','year','genre','publisher','na_sales','eu_sales','jp_sales','other_sales','global_sales'])
    return df