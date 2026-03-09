from config.Conf import Conf

Conf = Conf()


def CleanSuffixes():
  suffixes = set()

  # 读取并清洗
  with open(Conf.RawCompSuffixesPath, "r", encoding="utf-8") as f:
      for line in f:
          region = line.strip()  # 去掉空格和换行符

          if region:  # 跳过空行
              suffixes.add(region)

  # 排序（建议按长度排序，方便名称清洗）
  suffixes = sorted(suffixes, key=len, reverse=True)

  # 写入新文件
  with open(Conf.ProcessedCompSuffixesPath, "w", encoding="utf-8") as f:
      for region in suffixes:
          f.write(region + "\n")

  print(f"清洗完成，共 {len(suffixes)} 条，已写入 {Conf.ProcessedCompSuffixesPath}")



if __name__ == "__main__":
  CleanSuffixes()