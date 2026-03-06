import os
import logging
from datetime import datetime, timedelta


class Conf(object):
    def __init__(self):
        self.TsToken = " your token"  # tushare token
        self.RootPath = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )  # 项目根目录
        self.RawCompListPath = os.path.join(
            self.RootPath, "data", "raw_comp_list.csv"
        )  # 原始公司列表文件路径
        self.CompShareholderPath = os.path.join(
            self.RootPath, "data", "comp_shareholder.csv"
        )  # 公司股东列表文件路径
        self.CompMangagersPath = os.path.join(
            self.RootPath, "data", "comp_mangagers.csv"
        )  # 公司管理层列表文件路径
        self.LogPath = os.path.join(self.RootPath, "logs")  # 日志文件目录

        today = datetime.now()
        q = (today.month - 1) // 3

        start = (
            datetime(today.year, q * 3 - 2, 1)
            if q > 0
            else datetime(today.year - 1, 10, 1)
        )
        end = (
            (datetime(today.year, q * 3, 1) - timedelta(days=1))
            if q > 0
            else (datetime(today.year, 1, 1) - timedelta(days=1))
        )

        self.LastQuartBeg = start.strftime("%Y%m%d")  # 上季度开始时间
        self.LastQuartEnd = end.strftime("%Y%m%d")  # 上季度结束时间

        # 上上季度结束 = 上季度开始 - 1天
        prev2_end = start - timedelta(days=1)
        prev2_q = (prev2_end.month - 1) // 3
        prev2_start = datetime(prev2_end.year, prev2_q * 3 + 1, 1)

        self.LLastQuartBeg = prev2_start.strftime("%Y%m%d")  # 上上季度开始
        self.LLastQuartEnd = prev2_end.strftime(
            "%Y%m%d"
        )  # 上上季度结束# 上季度结束时间

        # 配置logging
        log_file = os.path.join(self.LogPath, "app.log")
        os.makedirs(self.LogPath, exist_ok=True)

        logging.basicConfig(
            encoding="utf-8-sig",
            level=logging.INFO,
            filename=log_file,
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
        )


if __name__ == "__main__":
    conf = Conf()
    # print(conf.TsToken)
    # print(conf.RootPath)
    # print(conf.RawCompListPath)
    # print(conf.LastQuartBeg)
    # print(conf.LastQuartEnd)
    print(conf.LLastQuartBeg)
    print(conf.LLastQuartEnd)
