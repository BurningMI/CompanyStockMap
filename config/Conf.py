import os
import logging


class Conf(object):
    def __init__(self):
        self.TsToken = "Your Token"       # tushare token
        self.RootPath=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))               #项目根目录
        self.RawCompListPath = os.path.join(self.RootPath,'data', 'raw_comp_list.csv')          #原始公司列表文件路径
        self.LogPath=os.path.join(self.RootPath,'logs')                                         #日志目录
        
        
        
        
        #配置logging
        log_file = os.path.join(self.LogPath, "app.log")
        os.makedirs(self.LogPath, exist_ok=True)

        logging.basicConfig(
            encoding="utf-8-sig",
            level=logging.INFO,
            filename=log_file,
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s"
        )




if __name__ == '__main__':
    conf = Conf()
    # print(conf.TsToken)
    print(conf.RootPath)
    
    
    print(conf.RawCompListPath)