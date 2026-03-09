from config.Conf import Conf

Conf = Conf()

def CleanCity():

    regions = set()

    # 读取并清洗
    with open(Conf.RawCityListPath, "r", encoding="utf-8") as f:
        for line in f:
            region = line.strip()  # 去掉空格和换行符

            if region:  # 跳过空行
                regions.add(region)

    # 排序（建议按长度排序，方便名称清洗）
    regions = sorted(regions, key=len, reverse=True)

    # 写入新文件
    with open(Conf.ProcessedCityListPath, "w", encoding="utf-8") as f:
        for region in regions:
            f.write(region + "\n")

    print(f"清洗完成，共 {len(regions)} 条，已写入 {Conf.ProcessedCityListPath}")
    
    
    
    
if __name__ == "__main__":
  CleanCity()