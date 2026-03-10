class CrawlerConf:
    def __init__(self):
        self.url = [
            {
                "url": "https://tushare.pro/news/fenghuang",
                "table_name": "news_table_fenghuang",
            },
            {
                "url": "https://tushare.pro/news/jinrongjie",
                "table_name": "news_table_jinrongjie",
            },
            {
                "url": "https://tushare.pro/news/10jqka",
                "table_name": "news_table_tonghuashun",
            },
            {
                "url": "https://tushare.pro/news/sina",
                "table_name": "news_table_xinlang",
            },
            {
                "url": "https://tushare.pro/news/sina#%E5%9B%BD%E9%99%85",
                "table_name": "news_table_xinlang",
            },
            {
                "url": "https://tushare.pro/news/sina#%E5%85%AC%E5%8F%B8",
                "table_name": "news_table_xinlang",
            },
            {
                "url": "https://tushare.pro/news/sina#%E7%84%A6%E7%82%B9",
                "table_name": "news_table_xinlang",
            },
            {
                "url": "https://tushare.pro/news/sina#%E5%AE%8F%E8%A7%82",
                "table_name": "news_table_xinlang",
            },
            {
                "url": "https://tushare.pro/news/sina#%E6%95%B0%E6%8D%AE",
                "table_name": "news_table_xinlang",
            },
            {
                "url": "https://tushare.pro/news/sina#%E5%AE%87%E8%A1%8C",
                "table_name": "news_table_xinlang",
            },
            {
                "url": "https://tushare.pro/news/yuncaijing",
                "table_name": "news_table_yuncaijing",
            },
            {
                "url": "https://tushare.pro/news/eastmoney",
                "table_name": "news_table_dongfangcaifu",
            },
            {
                "url": "https://tushare.pro/news/wallstreetcn#%E8%A6%81%E9%97%BB",
                "table_name": "news_table_huaerjie",
            },
            {
                "url": "https://tushare.pro/news/wallstreetcn#%E7%BE%8E%E8%82%A1",
                "table_name": "news_table_huaerjie",
            },
            {
                "url": "https://tushare.pro/news/wallstreetcn#%E5%A4%96%E6%B1%87",
                "table_name": "news_table_huaerjie",
            },
            {
                "url": "https://tushare.pro/news/wallstreetcn#A%E8%82%A1",
                "table_name": "news_table_huaerjie",
            },
            {
                "url": "https://tushare.pro/news/wallstreetcn#%E6%B8%AF%E8%82%A1",
                "table_name": "news_table_huaerjie",
            },
            {
                "url": "https://tushare.pro/news/wallstreetcn#%E9%87%91%E8%9E%8D",
                "table_name": "news_table_huaerjie",
            },
            {
                "url": "https://tushare.pro/news/wallstreetcn#%E5%80%BA%E5%88%B8",
                "table_name": "news_table_huaerjie",
            },
            {
                "url": "https://tushare.pro/news/wallstreetcn#%E5%A4%A7%E5%AE%97",
                "table_name": "news_table_huaerjie",
            },
            {
                "url": "https://tushare.pro/news/wallstreetcn#%E7%A7%91%E6%8A%80",
                "table_name": "news_table_huaerjie",
            },
        ]

        self.headers = {
                "referer": "https://tushare.pro/",
                "cookie": 'uid=2|1:0|10:1772614039|3:uid|8:ODIxNTc1|21aab3368465d06d5bd7ab0b15dab3a9a372900a7e3ff9cc934047e3fdfdd164; username=2|1:0|10:1772614039|8:username|12:MTgxKioqMjM2|16cd9814b6691eb31abf30f00e16079be146562898123e0bd36a1c4dbd32d0af',
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
            }
        
        
        
        self.MYSQL_HOST = "127.0.0.1"
        self.MYSQL_PORT = 3306
        self.MYSQL_USER = "root"
        self.MYSQL_PASSWORD = "123456"
        self.MYSQL_DB = "CompanyStockMap"#数据库名称
        self.charset = "utf8mb4" 