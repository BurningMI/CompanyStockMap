import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
from CrawlerConf import CrawlerConf


class NewsCrawler:
    def __init__(self, method="GET"):
        conf = CrawlerConf()
        self.url_list = conf.url                # 全部URL配置列表
        self.url = None                         # 当前爬取的URL
        self.table_name = None                  # 当前对应的表名
        self.method = method.upper()            # 请求方式 GET/POST
        self.headers = conf.headers             # 请求头（含cookie）
        self.payload = {}                       # 请求参数
        self.session = requests.Session()       # 复用TCP连接的会话
        self.result = []                        # 存储所有URL的解析结果

    def fetch_page(self):
        """请求页面，返回HTML文本，失败返回None"""
        try:
            if self.method == "POST":
                response = self.session.post(self.url, headers=self.headers, data=self.payload, timeout=10)
            else:
                response = self.session.get(self.url, headers=self.headers, params=self.payload, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"请求失败: {self.url}\n错误信息: {e}")
            return None

    def _parse_title_content(self, text):
        """从【标题】正文格式中拆分标题和正文，无标题格式则标题为None"""
        if "【" in text and "】" in text:
            return text.split("】")[0].replace("【", "").strip(), text.split("】", 1)[1].strip()
        return None, text

    def parse_page(self, html):
        """解析HTML，提取新闻时间、标题、正文及内容哈希"""
        soup = BeautifulSoup(html, "html.parser")
        current_date = datetime.now().strftime("%m月%d日")  # 默认日期为今天
        current_year = datetime.now().year                  # 缓存年份，避免循环内重复调用
        result_list = []

        for item in soup.find_all("div", class_="news_item"):
            # 日期分隔行，更新当前日期后跳过
            if "news_day" in item.get("class", []):
                current_date = item.get_text(strip=True)
                continue

            time_tag = item.find("div", class_="news_datetime")
            content_tag = item.find("div", class_="news_content")
            if not (time_tag and content_tag):
                continue

            # 拼接日期+时间并解析为datetime对象
            try:
                full_time = datetime.strptime(
                    f"{current_date} {time_tag.get_text(strip=True)}", "%m月%d日 %H:%M"
                ).replace(year=current_year)
            except Exception as e:
                print(f"时间解析失败：{current_date} {time_tag.get_text(strip=True)}，错误：{e}")
                continue

            content_str = content_tag.get_text(strip=True)
            title, content = self._parse_title_content(content_str)
            result_list.append({
                "time": full_time.strftime("%Y-%m-%d %H:%M:%S"),
                "title": title,
                "content": content,
                "content_hash": hashlib.md5(content.encode("utf-8")).hexdigest(),  # 用于去重
            })

        self.result = result_list

    def run(self):
        """遍历所有URL依次爬取和解析，返回 {table_name: [结果列表]} 的字典"""
        all_results = {}
        for item in self.url_list[:2]:
            self.url = item["url"]
            self.table_name = item["table_name"]
            html = self.fetch_page()
            if html:
                self.parse_page(html)
                # 同一表名的结果合并
                if self.table_name not in all_results:
                    all_results[self.table_name] = []
                all_results[self.table_name].extend(self.result)
        return all_results


if __name__ == '__main__':
    nc = NewsCrawler()
    results = nc.run()
    for table, items in results.items():
        print(f"[{table}] 共 {len(items)} 条")
        print(items)
