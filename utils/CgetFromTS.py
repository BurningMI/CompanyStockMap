import tinyshare as ts
from config.Conf import Conf
import os
import logging

class CgetFromTS:

    def __init__(self):
        """
        初始化 tinyshare 客户端
        """
        try:
            self.conf = Conf()
            ts.set_token(self.conf.TsToken)
            self.pro = ts.pro_api()
        except Exception as e:
            logging.error(f"初始化失败: {e}")
            raise 
        """
        获取股票基础信息

        返回：
            pandas.DataFrame：包含股票基础信息的数据表
        """
    def get_stock_basic(self):
        # 调用 tinyshare / tushare 的接口 stock_basic
        # self.pro 是在类初始化时通过 ts.pro_api() 创建的接口对象
        df = self.pro.stock_basic(

            # exchange 表示交易所
            # '' 代表获取所有交易所股票
            # SSE = 上交所
            # SZSE = 深交所
            exchange='',

            # list_status 表示股票上市状态
            # L = 已上市
            # D = 退市
            # P = 暂停上市
            # 这里 L 表示只获取当前上市股票
            list_status='L',

            # fields 表示返回哪些字段
            # ts_code   股票代码
            # name      股票名称
            # area      所在地区
            # industry  行业
            # list_date 上市日期
            fields='ts_code,name,area,industry,list_date'
        )
        
        file_path=self.conf.RawCompListPath         #raw数据文件路径
        print(f'文件路径: {file_path}')
            
            
        if not os.path.exists(file_path):
            logging.info("文件不存在，创建并写入数据:, {file_path}")
            
        else:
            logging.info("文件已存在，覆盖写入:, {file_path}")

        
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        logging.info("数据写入完成")
        # 返回 pandas DataFrame 数据
        return df




if __name__ == '__main__':
    gts=CgetFromTS()
    # print(gts.conf.TsToken)    
    
    df=gts.get_stock_basic()
    # print(df[:5])
    

    
    
    
