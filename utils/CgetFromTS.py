import tinyshare as ts
from config.Conf import Conf
import os
import logging
import pandas as pd
# from pprint import pprint


class CgetFromTS:

    def __init__(self, conf):
        """
        初始化 tinyshare 客户端
        """
        try:
            self.conf = conf  # 创建配置对象
            ts.set_token(self.conf.TsToken)  # 设置 tushare token
            self.pro = ts.pro_api()  # 创建 tinyshare 接口对象
            self.ts_codes = None  # 存储股票代码列表，供后续获取股东信息使用
        except Exception as e:
            logging.error(f"初始化失败: {e}")
            raise
        """
        获取股票基础信息

        返回：
            pandas.DataFrame：包含股票基础信息的数据表
        """

    # 获取股票基础信息
    def get_stock_basic(self):
        # 调用 tinyshare / tushare 的接口 stock_basic
        # self.pro 是在类初始化时通过 ts.pro_api() 创建的接口对象
        df = self.pro.stock_basic(
            # exchange 表示交易所
            # '' 代表获取所有交易所股票
            # SSE = 上交所
            # SZSE = 深交所
            exchange="",
            # list_status 表示股票上市状态
            # L = 已上市
            # D = 退市
            # P = 暂停上市
            # 这里 L 表示只获取当前上市股票
            list_status="L",
            # fields 表示返回哪些字段
            # ts_code   股票代码
            # name      股票名称
            # area      所在地区
            # industry  行业
            # list_date 上市日期
            fields="ts_code,name,area,industry,list_date",
        )

        print(f"文件路径: {self.conf.RawCompListPath}")

        if not os.path.exists(self.conf.RawCompListPath):
            logging.info("文件不存在，创建并写入数据:, {self.conf.RawCompListPath}")

        else:
            logging.info("文件已存在，覆盖写入:, {self.conf.RawCompListPath}")

        df.to_csv(self.conf.RawCompListPath, index=False, encoding="utf-8-sig")
        logging.info("数据写入完成")
        return df

    # 获取公司前十大流通股东
    def get_company_shareholder(self):
        # 读取公司名称/代码 获取十大股东问题
        self.conf.RawCompListPath
        df = pd.read_csv(self.conf.RawCompListPath, usecols=["ts_code"])
        self.ts_codes = df["ts_code"].tolist()

        for ts_code in self.ts_codes[:10]:
            df = self.pro.top10_floatholders(
                ts_code=ts_code,
                start_date=self.conf.LastQuartBeg,
                end_date=self.conf.LastQuartEnd,
            )

            if df.empty:
                logging.warning(
                    f"股票代码 {ts_code} 在 {self.conf.LastQuartBeg} 至 {self.conf.LastQuartEnd} 期间没有前十大流通股东数据"
                )
                df = self.pro.top10_floatholders(
                    ts_code=ts_code,
                    start_date=self.conf.LLastQuartBeg,
                    end_date=self.conf.LLastQuartEnd,
                )

                if df.empty:
                    logging.warning(
                        f"股票代码 {ts_code} 在 {self.conf.LLastQuartBeg} 至 {self.conf.LLastQuartEnd} 期间也没有前十大流通股东数据"
                    )
                    continue

            # 如果执行到这里说明 df 已经有数据
            df.to_csv(
                self.conf.RawCompShareholderPath,
                index=False,
                mode="a",
                header=not os.path.exists(self.conf.RawCompShareholderPath),
                encoding="utf-8-sig",
            )

            logging.info(f"已获取 {ts_code} 的十大流通股东信息并写入文件")
            print(f"已获取 {ts_code} 的十大流通股东信息并写入文件")
            
            
    def get_company_mangagers(self):

        #获取公司高管信息

        self.conf.RawCompListPath
        df = pd.read_csv(self.conf.RawCompListPath, usecols=["ts_code"])
        #为了测试，只获取前5只股票的高管信息
        #todo 后续删除测试代码
        self.ts_codes = df["ts_code"].tolist()[:5]
        if os.path.exists(self.conf.RawCompMangagersPath):
            os.remove(self.conf.RawCompMangagersPath)

        first_write = True

        for ts_code in self.ts_codes:
            try:
                df = self.pro.stk_managers(ts_code=ts_code)

                if df.empty:
                    logging.warning(f"{ts_code} 未获取到高管信息")
                    continue

                df.to_csv(
                    self.conf.RawCompMangagersPath,
                    index=False,
                    mode="a",
                    header=first_write,
                    encoding="utf-8-sig",
                )

                first_write = False

                logging.info(f"已获取 {ts_code} 的高管信息并写入文件")
                print(f"已获取 {ts_code} 的高管信息并写入文件")

            except Exception as e:
                logging.error(f"{ts_code} 获取高管信息失败: {e}")
                print(f"{ts_code} 获取高管信息失败: {e}")

    def get_manager_trades(self):
        # 获取高管增减持记录，接口：stk_holdertrade
        df = pd.read_csv(self.conf.RawCompListPath, usecols=["ts_code"])
        ts_codes = df["ts_code"].tolist()[:5]

        if os.path.exists(self.conf.RawManagerTradesPath):
            os.remove(self.conf.RawManagerTradesPath)

        first_write = True

        for ts_code in ts_codes:
            try:
                df = self.pro.stk_holdertrade(
                    ts_code=ts_code,
                    start_date=self.conf.LastQuartBeg,
                    end_date=self.conf.LastQuartEnd,
                )

                if df.empty:
                    continue

                df.to_csv(
                    self.conf.RawManagerTradesPath,
                    index=False,
                    mode="a",
                    header=first_write,
                    encoding="utf-8-sig",
                )
                first_write = False
                logging.info(f"已获取 {ts_code} 的高管增减持信息并写入文件")
                print(f"已获取 {ts_code} 的高管增减持信息并写入文件")

            except Exception as e:
                logging.error(f"{ts_code} 获取高管增减持失败: {e}")
                print(f"{ts_code} 获取高管增减持失败: {e}")
    

     

if __name__ == "__main__":
    conf=Conf()
    gts = CgetFromTS(conf)
    # print(gts.conf.TsToken)

    df=gts.get_stock_basic()
    # print(df[:5])
    # gts.get_company_shareholder()
    # gts.get_company_mangagers()
    gts.get_manager_trades()
