import pymysql
import datetime
import pandas as pd

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
    cur.execute(sql,*args)
    ret = cur.fetchall()
    close_conn(conn,cur)

    return ret