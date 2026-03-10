from CrawlerConf import CrawlerConf
import pymysql
import logging
from NewsCrawler import NewsCrawler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CMysql:
    def __init__(self, conf):
        self.conf = conf
        self.host = self.conf.MYSQL_HOST
        self.port = self.conf.MYSQL_PORT
        self.user = self.conf.MYSQL_USER
        self.password = self.conf.MYSQL_PASSWORD
        self.db = self.conf.MYSQL_DB
        self.charset = self.conf.charset

        try:
            # 先不指定数据库，连接到MySQL服务器
            self.con = pymysql.connect(
                host=self.host, port=self.port,
                user=self.user, password=self.password,
                charset=self.charset
            )
            # 检查目标数据库是否存在，不存在则创建
            with self.con.cursor() as cursor:
                cursor.execute(f"SHOW DATABASES LIKE '{self.db}'")
                if cursor.fetchone() is None:
                    # 数据库不存在，创建它
                    cursor.execute(f"CREATE DATABASE `{self.db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    logger.info(f"数据库 '{self.db}' 不存在，已自动创建")
                    print(f"[INFO] 数据库 '{self.db}' 不存在，已自动创建")
                else:
                    logger.info(f"数据库 '{self.db}' 已存在")
                    print(f"[INFO] 数据库 '{self.db}' 已存在")
            # 切换到目标数据库
            self.con.select_db(self.db)
            logger.info(f"成功连接到数据库 '{self.db}'（{self.host}:{self.port}）")
            print(f"[INFO] 成功连接到数据库 '{self.db}'（{self.host}:{self.port}）")
        except pymysql.Error as e:
            logger.error(f"数据库连接失败：{e}")
            print(f"[ERROR] 数据库连接失败：{e}")
            raise


    def write_in(self, data, table_name):
        """将data列表写入指定表，表不存在则自动创建，使用content_hash去重"""
        with self.con.cursor() as cursor:
            # 表不存在则创建
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    time DATETIME,
                    title VARCHAR(255),
                    content TEXT,
                    content_hash CHAR(32) UNIQUE
                ) CHARACTER SET utf8mb4
            """)
            # 批量插入，重复hash则忽略
            sql = f"INSERT IGNORE INTO `{table_name}` (time, title, content, content_hash) VALUES (%s, %s, %s, %s)"
            rows = [(d["time"], d["title"], d["content"], d["content_hash"]) for d in data]
            cursor.executemany(sql, rows)
        self.con.commit()
        logger.info(f"表 '{table_name}' 写入 {cursor.rowcount} 条新数据（共 {len(data)} 条）")
        print(f"[INFO] 表 '{table_name}' 写入 {cursor.rowcount} 条新数据（共 {len(data)} 条）")




if __name__ == '__main__':
    cc=CrawlerConf()
    nc=NewsCrawler()
    mysql_conn = CMysql(cc)
    results = nc.run()
    for table, items in results.items():
        mysql_conn.write_in(items, table)
