from config.Conf import Conf

Conf = Conf()


def CleanIndustry():
  industry = set()

  # 读取并清洗
  with open(Conf.RawIndustryListPath, "r", encoding="utf-8") as f:
      for line in f:
          region = line.strip()  # 去掉空格和换行符

          if region:  # 跳过空行
              industry.add(region)

  # 排序（建议按长度排序，方便名称清洗）
  industry = sorted(industry, key=len, reverse=True)

  # 写入新文件
  with open(Conf.ProcessedIndustryListPath, "w", encoding="utf-8") as f:
      for region in industry:
          f.write(region + "\n")

  print(f"清洗完成，共 {len(industry)} 条，已写入 {Conf.ProcessedIndustryListPath}")



if __name__ == "__main__":
  CleanIndustry()