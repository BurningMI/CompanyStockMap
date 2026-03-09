from config.Conf import Conf
import pandas as pd


class CdealRawData:
  def __init__(self, conf):
      self.conf = conf
      
        
  def deal_comp_mangagers(self):
    df = pd.read_csv(self.conf.RawCompMangagersPath)

        
      # 先把缺失日期补成空字符串，避免拼接时报错
    df["begin_date"] = df["begin_date"].fillna("不明")
    df["end_date"] = df["end_date"].fillna("至今")
    
      
    
    for col in ["name", "gender", "birthday", "national", "lev", "title", "begin_date", "end_date", "edu"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)

    # 去掉像 1990.0 / 20191126.0 这种尾巴
        def clean_num_str(x):
            x = str(x).strip()
            if x.endswith(".0"):
                x = x[:-2]
            return x

    df["lev"] = df["lev"].fillna("").astype(str)
    df["title"] = df["title"].fillna("").astype(str)
    df["birthday"] = df["birthday"].apply(clean_num_str)
    df["begin_date"] = df["begin_date"].apply(clean_num_str)
    df["end_date"] = df["end_date"].apply(clean_num_str)
        # 把 lev、title、日期拼成一个完整职位信息
    df["position"] = (
        df["lev"] + ":" + df["title"] +
        "(" + df["begin_date"].astype(str) + "~" + df["end_date"].astype(str) + ")"
    )

      # 按同一个人分组，把多个职位合并到一行
    df_result = (
        df.groupby(
            ["ts_code", "ann_date", "name", "gender", "edu", "national", "birthday"],
            as_index=False
        )
        .agg({
            "position": lambda x: ";".join(x)
        })
    )

    df_result["biz_key"] = (
        df_result["name"].fillna("") + "|" +
        df_result["gender"].fillna("") + "|" +
        df_result["birthday"].fillna("") + "|" +
        df_result["national"].fillna("")
    )

    df_result.to_csv(self.conf.ProcessedCompMangagersPath, index=False)

    return df_result

  def deal_comp_shareholders(self):
    df = pd.read_csv(self.conf.RawCompShareholderPath)

    for col in ["holder_name", "holder_type"]:
        df[col] = df[col].fillna("").astype(str)
    df["hold_change"] = df["hold_change"].fillna(0)

    df["biz_key"] = df["holder_name"] + "|" + df["holder_type"]  # biz_key 作为业务主键 用于后续去重和合并

    df.to_csv(self.conf.ProcessedCompShareholderPath, index=False)
    return df

  def deal_manager_trades(self):
    # 处理高管增减持数据，in_de 字段：IN=增持 DE=减持
    df = pd.read_csv(self.conf.RawManagerTradesPath)

    for col in ["name", "share_type", "in_de"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)

    for col in ["change_vol", "change_ratio", "after_share", "after_ratio", "avg_price", "total_share"]:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    df.to_csv(self.conf.ProcessedManagerTradesPath, index=False)
    return df
        
        
        
        

        
        
if __name__ == '__main__':
  cdrd=CdealRawData(Conf())
#   cdrd.deal_comp_mangagers()
  # print(cdrd.conf.CompShareholderPath)
  cdrd.deal_comp_shareholders()