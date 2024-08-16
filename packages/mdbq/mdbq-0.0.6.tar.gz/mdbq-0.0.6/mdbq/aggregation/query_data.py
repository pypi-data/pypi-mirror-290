# -*- coding: UTF-8 –*-
from mdbq.mongo import mongo
from mdbq.mysql import s_query
from mdbq.config import get_myconf
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import platform
import getpass
import json
import os


class MongoDatasQuery:
    """
    从 数据库 中下载数据
    self.output: 数据库默认导出目录
    self.is_maximize: 是否最大转化数据
    """
    def __init__(self, target_service):
        # target_service 从哪个服务器下载数据
        self.is_maximize = True
        if platform.system() == 'Darwin':
            self.output = os.path.join('/Users', getpass.getuser(), '数据中心/数据库导出')
        elif platform.system() == 'Windows':
            self.output = os.path.join('C:\\同步空间\\BaiduSyncdisk\\数据库导出')
        else:
            self.output = os.path.join('数据中心/数据库导出')

        # 实例化一个下载类
        username, password, host, port = get_myconf.select_config_values(target_service=target_service, database='mongodb')
        self.download = mongo.DownMongo(username=username, password=password, host=host, port=port, save_path=None)

    def tg_wxt(self):
        self.download.start_date, self.download.end_date = self.months_data(num=1)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '主体id': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '自然流量曝光量': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
        }
        df = self.download.data_to_df(db_name='天猫数据2', collection_name='推广数据_宝贝主体报表', projection=projection)
        df.rename(columns={
            '场景名字': '营销场景',
            '主体id': '商品id',
            '总购物车数': '加购量',
            '总成交笔数': '成交笔数',
            '总成交金额': '成交金额'
        }, inplace=True)
        df = df.astype({
            '花费': float,
            '展现量': int,
            '点击量': int,
            '加购量': int,
            '成交笔数': int,
            '成交金额': float,
            '自然流量曝光量': int,
            '直接成交笔数': int,
            '直接成交金额': float,
        }, errors='raise')
        df.fillna(0, inplace=True)
        if self.is_maximize:
            df = df.groupby(['日期', '营销场景', '商品id', '花费', '展现量', '点击量'], as_index=False).agg(
                **{'加购量': ('加购量', np.max),
                   '成交笔数': ('成交笔数', np.max),
                   '成交金额': ('成交金额', np.max),
                   '自然流量曝光量': ('自然流量曝光量', np.max),
                   '直接成交笔数': ('直接成交笔数', np.max),
                   '直接成交金额': ('直接成交金额', np.max)
                   }
            )
        else:
            df = df.groupby(['日期', '营销场景', '商品id', '花费', '展现量', '点击量'], as_index=False).agg(
                **{'加购量': ('加购量', np.min),
                   '成交笔数': ('成交笔数', np.min),
                   '成交金额': ('成交金额', np.min),
                   '自然流量曝光量': ('自然流量曝光量', np.min),
                   '直接成交笔数': ('直接成交笔数', np.max),
                   '直接成交金额': ('直接成交金额', np.max)
                   }
            )
        df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
        # print(df)
        return df

    @staticmethod
    def days_data(days, end_date=None):
        """ 读取近 days 天的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        return pd.to_datetime(start_date), pd.to_datetime(end_date)

    @staticmethod
    def months_data(num=0, end_date=None):
        """ 读取近 num 个月的数据, 0 表示读取当月的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - relativedelta(months=num)  # n 月以前的今天
        start_date = f'{start_date.year}-{start_date.month}-01'  # 替换为 n 月以前的第一天
        return pd.to_datetime(start_date), pd.to_datetime(end_date)

    def as_csv(self, df, filename, path=None, encoding='utf-8_sig',
               index=False, header=True, st_ascend=None, ascend=None, freq=None):
        """
        path: 子文件夹，可以不传，默认导出目录 self.output
        st_ascend: 排序参数
        ascend: 升降序
        freq: 将创建子文件夹并按月分类存储,  freq='Y'，或 freq='M'
        """
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if not os.path.exists(path):
            os.makedirs(path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        if freq:
            if '日期' not in df.columns.tolist():
                return print(f'{filename}: 数据缺少日期列，无法按日期分组')
            groups = df.groupby(pd.Grouper(key='日期', freq=freq))
            for name1, df in groups:
                if freq == 'M':
                    sheet_name = name1.strftime('%Y-%m')
                elif freq == 'Y':
                    sheet_name = name1.strftime('%Y年')
                else:
                    sheet_name = '_未分类'
                new_path = os.path.join(path, filename)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                new_path = os.path.join(new_path, f'{filename}{sheet_name}.csv')
                if st_ascend and ascend:  # 这里需要重新排序一次，原因未知
                    try:
                        df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
                    except:
                        print(f'{filename}: sort_values排序参数错误！')

                df.to_csv(new_path, encoding=encoding, index=index, header=header)
        else:
            df.to_csv(os.path.join(path, filename + '.csv'), encoding=encoding, index=index, header=header)

    def as_json(self, df, filename, path=None, orient='records', force_ascii=False, st_ascend=None, ascend=None):
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        df.to_json(os.path.join(path, filename + '.json'),
                   orient=orient, force_ascii=force_ascii)

    def as_excel(self, df, filename, path=None, index=False, header=True, engine='openpyxl',
                 freeze_panes=(1, 0), st_ascend=None, ascend=None):
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        df.to_excel(os.path.join(path, filename + '.xlsx'),
                    index=index, header=header, engine=engine, freeze_panes=freeze_panes)


class MysqlDatasQuery:
    """
    从 数据库 中下载数据
    self.output: 数据库默认导出目录
    self.is_maximize: 是否最大转化数据
    """
    def __init__(self, target_service):
        # target_service 从哪个服务器下载数据
        self.is_maximize = True
        if platform.system() == 'Darwin':
            self.output = os.path.join('/Users', getpass.getuser(), '数据中心/数据库导出')
        elif platform.system() == 'Windows':
            self.output = os.path.join('C:\\同步空间\\BaiduSyncdisk\\数据库导出')
        else:
            self.output = os.path.join('数据中心/数据库导出')
        self.months = 1  # 下载几个月数据, 0 表示当月, 1 是上月 1 号至今

        # 实例化一个下载类
        username, password, host, port = get_myconf.select_config_values(target_service=target_service, database='mysql')
        self.download = s_query.QueryDatas(username=username, password=password, host=host, port=port)

    def tg_wxt(self):
        start_date, end_date = self.months_data(num=self.months)
        df = self.download.data_to_df(db_name='天猫数据2', tabel_name='推广数据_宝贝主体报表', start_date=start_date, end_date=end_date)
        return df

    @staticmethod
    def days_data(days, end_date=None):
        """ 读取近 days 天的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        return pd.to_datetime(start_date), pd.to_datetime(end_date)

    @staticmethod
    def months_data(num=0, end_date=None):
        """ 读取近 num 个月的数据, 0 表示读取当月的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - relativedelta(months=num)  # n 月以前的今天
        start_date = f'{start_date.year}-{start_date.month}-01'  # 替换为 n 月以前的第一天
        return pd.to_datetime(start_date), pd.to_datetime(end_date)

    def as_csv(self, df, filename, path=None, encoding='utf-8_sig',
               index=False, header=True, st_ascend=None, ascend=None, freq=None):
        """
        path: 子文件夹，可以不传，默认导出目录 self.output
        st_ascend: 排序参数
        ascend: 升降序
        freq: 将创建子文件夹并按月分类存储,  freq='Y'，或 freq='M'
        """
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if not os.path.exists(path):
            os.makedirs(path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        if freq:
            if '日期' not in df.columns.tolist():
                return print(f'{filename}: 数据缺少日期列，无法按日期分组')
            groups = df.groupby(pd.Grouper(key='日期', freq=freq))
            for name1, df in groups:
                if freq == 'M':
                    sheet_name = name1.strftime('%Y-%m')
                elif freq == 'Y':
                    sheet_name = name1.strftime('%Y年')
                else:
                    sheet_name = '_未分类'
                new_path = os.path.join(path, filename)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                new_path = os.path.join(new_path, f'{filename}{sheet_name}.csv')
                if st_ascend and ascend:  # 这里需要重新排序一次，原因未知
                    try:
                        df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
                    except:
                        print(f'{filename}: sort_values排序参数错误！')

                df.to_csv(new_path, encoding=encoding, index=index, header=header)
        else:
            df.to_csv(os.path.join(path, filename + '.csv'), encoding=encoding, index=index, header=header)

    def as_json(self, df, filename, path=None, orient='records', force_ascii=False, st_ascend=None, ascend=None):
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        df.to_json(os.path.join(path, filename + '.json'),
                   orient=orient, force_ascii=force_ascii)

    def as_excel(self, df, filename, path=None, index=False, header=True, engine='openpyxl',
                 freeze_panes=(1, 0), st_ascend=None, ascend=None):
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        df.to_excel(os.path.join(path, filename + '.xlsx'),
                    index=index, header=header, engine=engine, freeze_panes=freeze_panes)


def main():
    sdq = MysqlDatasQuery(target_service='company')
    sdq.months = 0
    df = sdq.tg_wxt()
    print(df)


if __name__ == '__main__':
    main()
