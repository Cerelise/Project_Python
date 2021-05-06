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





def get_data():
    sql = """
        select * from hotel_bookings
    """
    df  = pd.DataFrame(
        exe_sql(sql),
        columns=
        ['hotel','is_canceled','lead_time','arrival_date_year',
         'arrival_date_month','arrival_date_week_number',
         'arrival_date_day','stays_in_weekend','stays_in_week_nights',
         'adults','children','babies','meal','country','market',
         'distribution','repeated','previous_cancellations',
         'previous_bookings','reserved','assigned','booking',
         'deposit','agent','company','days','customer',
         'adr','parking','total','reservation_status',
         'status_date'])

    return



