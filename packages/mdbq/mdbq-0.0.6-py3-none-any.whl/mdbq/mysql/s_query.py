# -*- coding:utf-8 -*-
import datetime
import platform
import re
import time
from functools import wraps
import warnings
import pymysql
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os
import calendar
from mdbq.config import get_myconf

warnings.filterwarnings('ignore')


class QueryDatas:
    def __init__(self, username: str, password: str, host: str, port: int, charset: str = 'utf8mb4'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.config = {
            'host': self.host,
            'port': self.port,
            'user': self.username,
            'password': self.password,
            'charset': charset,  # utf8mb4 支持存储四字节的UTF-8字符集
            'cursorclass': pymysql.cursors.DictCursor,
        }

    def data_to_df(self, db_name, tabel_name, start_date, end_date, projection=[]):
        start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
        df = pd.DataFrame()

        connection = pymysql.connect(**self.config)  # 连接数据库
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
                database_exists = cursor.fetchone()
                if not database_exists:
                    print(f"Database <{db_name}>: 数据库不存在")
        finally:
            connection.close()  # 这里要断开连接
            time.sleep(0.2)

        self.config.update({'database': db_name})  # 添加更新 config 字段
        connection = pymysql.connect(**self.config)  # 重新连接数据库
        try:
            with connection.cursor() as cursor:
                # 1. 查询表是否存在
                sql = f"SHOW TABLES LIKE '{tabel_name}'"
                cursor.execute(sql)
                if not cursor.fetchone():
                    print(f'{db_name} -> <{tabel_name}>: 表不存在')
                    return df

                # 查询列
                for col in projection:
                    sql = ('SELECT 1 FROM information_schema.columns WHERE table_schema = %s AND table_name = %s AND '
                           'column_name = %s')
                    cursor.execute(sql, (db_name, {tabel_name}, col))
                    if cursor.fetchone() is None:  # 移除不存在的列
                        projection.remove(col)
        except Exception as e:
            print(e)
            return df
        finally:
            connection.close()  # 断开连接

        # before_time = time.time()
        # 读取数据
        self.config.update({'database': db_name})
        connection = pymysql.connect(**self.config)  # 重新连接数据库
        try:
            with connection.cursor() as cursor:
                if not projection:  # 如果未指定，则查询所有列，获取 cols_exist
                    sql = 'SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = %s AND table_name = %s'
                    cursor.execute(sql, (db_name, {tabel_name}))
                    columns = cursor.fetchall()
                    cols_exist = [col['COLUMN_NAME'] for col in columns]

                if '日期' in projection or '日期' in cols_exist:  # 指定含日期的 projection 或者未指定 projection 但表中有日期列
                    sql = f"SELECT * FROM {db_name}.{tabel_name} WHERE {'日期'} BETWEEN '%s' AND '%s'" % (start_date, end_date)
                elif projection:  # 指定未含日期的 projection
                    sql = f"SELECT '%s' FROM {db_name}.{tabel_name}" % (', '.join(projection))
                else:  # 未指定 projection 且表中无日期
                    sql = f"SELECT * FROM {db_name}.{tabel_name}"
                cursor.execute(sql)
                rows = cursor.fetchall()  # 获取查询结果
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(rows, columns=columns)
        except Exception as e:
            print(f'{e} {db_name} -> <{tabel_name}>: 表不存在')
            return df
        finally:
            connection.close()

        if len(df) == 0:
            print(f'database: {db_name}, table: {tabel_name} 查询的数据为空')
        # else:
        #     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        #     cost_time = int(time.time() - before_time)
        #     if cost_time < 1:
        #         cost_time = round(time.time() - before_time, 2)
        #     print(f'{now}mysql ({self.host}) 表: {tabel_name} 获取数据长度: {len(df)}, 用时: {cost_time} 秒')
        return df


def year_month_day(start_date, end_date):
    """
    使用date_range函数和DataFrame来获取从start_date至end_date之间的所有年月日
    calendar.monthrange： 获取当月第一个工作日的星期值(0,6) 以及当月天数
    """
    # 替换年月日中的日, 以便即使传入当月日期也有返回值
    try:
        start_date = f'{pd.to_datetime(start_date).year}-{pd.to_datetime(start_date).month}-01'
    except Exception as e:
        print(e)
        return []
    # 使用pandas的date_range创建一个日期范围，频率为'MS'代表每月开始
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    # 转换格式
    year_months = date_range.strftime('%Y-%m').drop_duplicates().sort_values()

    results = []
    for year_month in year_months:
        year = re.findall(r'(\d{4})', year_month)[0]
        month = re.findall(r'\d{4}-(\d{2})', year_month)[0]
        s, d = calendar.monthrange(int(year), int(month))
        results.append({'起始日期': f'{year_month}-01', '结束日期': f'{year_month}-{d}'})

    return results  # start_date至end_date之间的所有年月日


def download_datas(tabel_name, save_path, start_date):
    username, password, host, port = get_myconf.select_config_values(target_service='company', database='mysql')
    print(username, password, host, port)
    m = MysqlUpload(username=username, password=password, host=host, port=port)
    m.port = port
    results = year_month_day(start_date=start_date, end_date='today')
    # print(results)
    for result in results:
        start_date = result['起始日期']
        end_date = result['结束日期']
        # print(start_date, end_date)
        df = m.data_to_df(db_name='市场数据2', tabel_name=tabel_name, start_date=start_date, end_date=end_date)
        if len(df) == 0:
            continue
        path = os.path.join(save_path, f'{tabel_name}_{str(start_date)}_{str(end_date)}.csv')
        df['日期'] = df['日期'].apply(lambda x: re.sub(' .*', '', str(x)))
        df.to_csv(path, index=False, encoding='utf-8_sig', header=True)


if __name__ == '__main__':
    # username, password, host, port = get_myconf.select_config_values(target_service='company', database='mysql')
    # print(username, password, host, port)

    username, password, host, port = get_myconf.select_config_values(target_service='company', database='mysql')
    qd = QueryDatas(username=username, password=password, host=host, port=port)
    df = qd.data_to_df(db_name='市场数据2', tabel_name='市场排行_店铺', start_date='2024-08-13', end_date='2024-08-31')
    print(df)
