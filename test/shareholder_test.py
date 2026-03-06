import tinyshare as ts
from config.Conf import Conf
import pandas as pd


def get_company_shareholder():
    conf = Conf()
    ts.set_token(conf.TsToken)
    pro = ts.pro_api()
    df = pro.top10_floatholders(ts_code='600000.SH', start_date='20250701', end_date='20250931')
    df.to_csv(conf.CompShareholderPath, index=False)
    print(df)


def read_company_name():
    conf = Conf()
    df = pd.read_csv(conf.RawCompListPath, usecols=["ts_code"])  
    ts_codes = df["ts_code"].tolist()
    return ts_codes


if __name__ == '__main__':
    get_company_shareholder()
    # company_df = read_company_name()
    # print(company_df)