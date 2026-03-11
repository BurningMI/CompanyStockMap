import os
import logging
from datetime import datetime, timedelta


class Conf(object):
    def __init__(self):
        self.TsToken = " Your Token"  # tushare token
        self.RootPath = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )  # 项目根目录

        self.RawCompListPath = os.path.join(
            self.RootPath, "data", "Raw", "raw_comp_list.csv"
        )  # 原始公司列表文件路径

        self.RawCompShareholderPath = os.path.join(
            self.RootPath, "data", "Raw", "raw_comp_shareholder.csv"
        )  # 原始公司股东列表文件路径

        self.RawCompMangagersPath = os.path.join(
            self.RootPath, "data", "Raw", "raw_comp_mangagers.csv"
        )  # 原始公司管理层列表文件路径

        self.ProcessedCompListPath = os.path.join(
            self.RootPath, "data", "processed", "processed_comp_list.csv"
        )  # 处理过公司列表文件路径

        self.ProcessedCompShareholderPath = os.path.join(
            self.RootPath, "data", "processed", "processed_comp_shareholder.csv"
        )  # 处理过公司股东列表文件路径

        self.ProcessedCompMangagersPath = os.path.join(
            self.RootPath, "data", "processed", "processed_comp_mangagers.csv"
        )  # 处理过公司管理层列表文件路径

        self.RawManagerTradesPath = os.path.join(
            self.RootPath, "data", "Raw", "raw_manager_trades.csv"
        )  # 原始高管增减持文件路径

        self.ProcessedManagerTradesPath = os.path.join(
            self.RootPath, "data", "processed", "processed_manager_trades.csv"
        )  # 处理过高管增减持文件路径

        self.RawCityListPath = os.path.join(
            self.RootPath, "data", "Raw", "base", "raw_city.txt"
        )  # 原始城市列表文件路径

        self.ProcessedCityListPath = os.path.join(
            self.RootPath, "data", "Processed", "processed_city_list.txt"
        )  # 处理过城市列表文件路径

        self.RawIndustryListPath = os.path.join(
            self.RootPath, "data", "Raw", "base", "raw_industry_words.txt"
        )  # 原始行业列表文件路径

        self.ProcessedIndustryListPath = os.path.join(
            self.RootPath, "data", "Processed", "processed_industry_list.txt"
        )  # 处理过行业列表文件路径

        self.RawCompSuffixesPath = os.path.join(
            self.RootPath, "data", "Raw", "base", "raw_company_suffixes.txt"
        )  # 原始公司简称列表文件路径

        self.ProcessedCompSuffixesPath = os.path.join(
            self.RootPath, "data", "Processed", "processed_company_suffixes.txt"
        )  # 处理过公司简称列表文件路径

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
        
        self.neo4j_uri = "bolt://localhost:7687"  # Neo4j URI
        self.neo4j_user = "neo4j"  # Neo4j 用户名
        self.neo4j_password = "123456"  # Neo4j 密码
        


if __name__ == "__main__":
    conf = Conf()
    # print(conf.TsToken)
    # print(conf.RootPath)
    # print(conf.RawCompListPath)
    # print(conf.LastQuartBeg)
    # print(conf.LastQuartEnd)
    print(conf.LLastQuartBeg)
    print(conf.LLastQuartEnd)
