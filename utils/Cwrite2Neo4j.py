from config.Conf import Conf
from neo4j import GraphDatabase
import pandas as pd
import logging


class Cwrite2Neo4j:

    def __init__(self, conf, uri, user, password):
        self.conf = conf
        # 创建 Neo4j 驱动连接
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # 关闭数据库连接
        self.driver.close()

    def write_companies(self):
        # 读取公司列表，写入 Company 节点，以 ts_code 为唯一键
        df = pd.read_csv(self.conf.RawCompListPath)
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (c:Company {ts_code: $ts_code})
                    SET c.name = $name, c.area = $area,
                        c.industry = $industry, c.list_date = $list_date
                    """,
                    ts_code=row["ts_code"], name=row["name"],
                    area=row.get("area", ""), industry=row.get("industry", ""),
                    list_date=str(row.get("list_date", ""))
                )
        logging.info("公司节点写入完成")
        print("公司节点写入完成")

    def write_managers(self):
        # 读取处理后的高管数据，写入 Manager 节点及 MANAGES 关系
        # Manager 以 biz_key（name|gender|birthday|national）为唯一键去重
        # MANAGES 关系携带职位信息和公告日期
        df = pd.read_csv(self.conf.ProcessedCompMangagersPath)
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (m:Manager {biz_key: $biz_key})
                    SET m.name = $name, m.gender = $gender,
                        m.birthday = $birthday, m.national = $national, m.edu = $edu
                    WITH m
                    MATCH (c:Company {ts_code: $ts_code})
                    MERGE (m)-[r:MANAGES]->(c)
                    SET r.position = $position, r.ann_date = $ann_date
                    """,
                    biz_key=row["biz_key"], name=row["name"],
                    gender=row.get("gender", ""), birthday=row.get("birthday", ""),
                    national=row.get("national", ""), edu=row.get("edu", ""),
                    ts_code=row["ts_code"], position=row.get("position", ""),
                    ann_date=str(row.get("ann_date", ""))
                )
        logging.info("高管节点及关系写入完成")
        print("高管节点及关系写入完成")

    def write_shareholders(self):
        # 读取处理后的股东数据，写入 Shareholder 节点及 HOLDS 关系
        # Shareholder 以 biz_key（holder_name|holder_type）为唯一键去重
        # HOLDS 关系以 end_date（报告期）区分不同季度的持股记录
        df = pd.read_csv(self.conf.ProcessedCompShareholderPath)
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (s:Shareholder {biz_key: $biz_key})
                    SET s.holder_name = $holder_name, s.holder_type = $holder_type
                    WITH s
                    MATCH (c:Company {ts_code: $ts_code})
                    MERGE (s)-[r:HOLDS {end_date: $end_date}]->(c)
                    SET r.hold_amount = $hold_amount, r.hold_ratio = $hold_ratio,
                        r.hold_change = $hold_change, r.ann_date = $ann_date
                    """,
                    biz_key=row["biz_key"], holder_name=row["holder_name"],
                    holder_type=row.get("holder_type", ""),
                    ts_code=row["ts_code"], end_date=str(row.get("end_date", "")),
                    hold_amount=float(row.get("hold_amount", 0)),
                    hold_ratio=float(row.get("hold_ratio", 0)),
                    hold_change=float(row.get("hold_change", 0)),
                    ann_date=str(row.get("ann_date", ""))
                )
        logging.info("股东节点及关系写入完成")
        print("股东节点及关系写入完成")

    def write_industries(self):
        # 从公司列表提取行业，写入 Industry 节点及 BELONGS_TO 关系
        df = pd.read_csv(self.conf.RawCompListPath, usecols=["ts_code", "industry"])
        df["industry"] = df["industry"].fillna("未知").astype(str)
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (i:Industry {name: $industry})
                    WITH i
                    MATCH (c:Company {ts_code: $ts_code})
                    MERGE (c)-[:BELONGS_TO]->(i)
                    """,
                    industry=row["industry"], ts_code=row["ts_code"]
                )
        logging.info("行业节点及关系写入完成")
        print("行业节点及关系写入完成")

    def write_manager_trades(self):
        # 读取处理后的高管增减持数据，写入 TRADES 关系到对应 Manager 和 Company
        # in_de 字段：IN=增持 DE=减持，作为关系属性保留
        df = pd.read_csv(self.conf.ProcessedManagerTradesPath)
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MATCH (c:Company {ts_code: $ts_code})
                    MATCH (m:Manager {name: $name})
                    MERGE (m)-[r:TRADES {ann_date: $ann_date}]->(c)
                    SET r.in_de = $in_de, r.change_vol = $change_vol,
                        r.change_ratio = $change_ratio, r.avg_price = $avg_price,
                        r.after_share = $after_share
                    """,
                    ts_code=row["ts_code"], name=row.get("name", ""),
                    ann_date=str(row.get("ann_date", "")),
                    in_de=row.get("in_de", ""),
                    change_vol=float(row.get("change_vol", 0)),
                    change_ratio=float(row.get("change_ratio", 0)),
                    avg_price=float(row.get("avg_price", 0)),
                    after_share=float(row.get("after_share", 0)),
                )
        logging.info("高管增减持关系写入完成")
        print("高管增减持关系写入完成")


if __name__ == "__main__":
    conf = Conf()
    writer = Cwrite2Neo4j(conf, conf.neo4j_uri, conf.neo4j_user, conf.neo4j_password)
    writer.write_companies()
    writer.write_industries()
    writer.write_managers()
    writer.write_shareholders()
    writer.write_manager_trades()
    writer.close()
