# CompanyStockMap

基于 Tushare 数据构建的 A 股公司知识图谱，集成新闻爬取、NLP 意图识别、新闻影响预测与量化策略回测功能。

## 系统架构

```
用户输入
   │
   ├─► 闲聊识别模型（TextCNN / FastText）
   │       └─ 是闲聊 → 直接回复
   │
   └─► 意图识别模型（BiLSTM + CRF 槽位填充）
           └─ 提取实体槽位（公司/行业/时间/指标）
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
     MySQL       Neo4j     回测引擎
    (新闻库)   (知识图谱)  (量化策略)
        │
        ▼
   新闻清洗 & 分类
        │
        ▼
   板块影响预测（FinBERT / LSTM）
```

## 图谱结构（Neo4j）

```
(Manager)-[:MANAGES]->(Company)-[:BELONGS_TO]->(Industry)
(Manager)-[:TRADES]->(Company)
(Shareholder)-[:HOLDS]->(Company)
```

| 节点 | 唯一键 | 主要属性 |
|------|--------|----------|
| Company | ts_code | name, area, industry, list_date |
| Manager | biz_key (name\|gender\|birthday\|national) | name, gender, birthday, national, edu |
| Shareholder | biz_key (holder_name\|holder_type) | holder_name, holder_type |
| Industry | name | - |

| 关系 | 主要属性 |
|------|----------|
| MANAGES | position, ann_date |
| HOLDS | hold_amount, hold_ratio, hold_change, end_date |
| TRADES | in_de(IN/DE), change_vol, avg_price, ann_date |
| BELONGS_TO | - |

## 项目结构

```
├── config/Conf.py              # 配置：路径、Tushare token、季度日期
├── utils/
│   ├── CgetFromTS.py           # 从 Tushare 拉取原始数据
│   ├── CdealRawData.py         # 清洗处理原始数据
│   └── Cwrite2Neo4j.py         # 写入 Neo4j
├── crawler/
│   ├── CrawlerConf.py          # 爬虫配置
│   ├── NewsCrawler.py          # 财经新闻爬取
│   └── CMysql.py               # MySQL 新闻存储（content_hash 去重）
├── nlp/
│   ├── intent/
│   │   ├── chat_classifier.py  # 闲聊识别模型（TextCNN）
│   │   └── slot_filler.py      # 意图+槽位填充（BiLSTM+CRF）
│   └── news/
│       ├── news_cleaner.py     # 新闻清洗（去噪、去重、分句）
│       ├── news_classifier.py  # 新闻板块分类
│       └── impact_predictor.py # 板块影响预测（涨/跌/中性）
├── backtest/
│   └── engine.py               # 量化策略回测引擎
├── data/
│   ├── Raw/                    # 原始数据
│   └── Processed/              # 清洗后数据
```

## NLP 模块说明

### 1. 闲聊识别

- 模型：TextCNN / FastText 二分类
- 输入：用户原始文本
- 输出：`chat`（闲聊）/ `query`（查询意图）
- 训练数据：通用闲聊语料 + 金融查询语料

### 2. 意图识别 & 槽位填充（BiLSTM + CRF）

- 模型：字符级 BiLSTM + CRF（序列标注）
- 槽位定义：

| 槽位 | 示例 |
|------|------|
| `B-COMPANY / I-COMPANY` | 贵州茅台、比亚迪 |
| `B-INDUSTRY / I-INDUSTRY` | 新能源、半导体 |
| `B-TIME / I-TIME` | 最近一周、2024年Q3 |
| `B-METRIC / I-METRIC` | 股价、市值、净利润 |

- 意图类别：`query_company`、`query_industry`、`query_news`、`query_backtest`

### 3. 新闻清洗 & 分类

- 清洗：去除广告词、HTML 标签、重复句、无关段落
- 分类：按板块打标签（科技/金融/能源/消费/医药/地产等）
- 存储：清洗结果回写 MySQL，新增 `category`、`clean_content` 字段

### 4. 板块影响预测

- 模型：FinBERT 微调 / 双向 LSTM
- 输入：清洗后新闻文本 + 板块标签
- 输出：`positive` / `negative` / `neutral` + 置信度
- 特征：情感极性、关键词权重、历史同类新闻涨跌统计

## 量化策略回测

- 数据源：Tushare 日线行情（`daily`）
- 支持策略：均线交叉、动量、新闻情感驱动
- 输出指标：年化收益、最大回撤、夏普比率、胜率
- 用法：

```python
from backtest.engine import BacktestEngine

engine = BacktestEngine(ts_code="000001.SZ", start="20230101", end="20241231")
engine.run(strategy="news_sentiment")
engine.report()
```

## 使用流程

```bash
pip install tushare neo4j pandas pymysql torch transformers backtrader
```

1. 在 `config/Conf.py` 填入 Tushare token 和 MySQL/Neo4j 连接信息
2. 依次运行：

```bash
# 知识图谱构建
python utils/CgetFromTS.py      # 拉取原始数据
python utils/CdealRawData.py    # 清洗数据
python utils/Cwrite2Neo4j.py    # 写入 Neo4j

# 新闻爬取与存储
python crawler/CMysql.py

# NLP 处理
python nlp/news/news_cleaner.py     # 清洗新闻
python nlp/news/news_classifier.py  # 板块分类
python nlp/news/impact_predictor.py # 影响预测
```

## 已完成

- [x] 拉取公司基础信息（stock_basic）
- [x] 拉取十大流通股东（top10_floatholders）
- [x] 拉取高管信息（stk_managers）
- [x] 拉取高管增减持（stk_holdertrade）
- [x] 清洗高管数据（biz_key、职位合并）
- [x] 清洗股东数据
- [x] 清洗高管增减持数据
- [x] 写入 Company / Manager / Shareholder / Industry 节点
- [x] 写入 MANAGES / HOLDS / TRADES / BELONGS_TO 关系
- [x] 财经新闻爬取（MySQL 存储，content_hash 去重）

## 待完成

- [ ] `CgetFromTS.py` 中的测试限制（`[:5]`、`[:10]`）改为全量拉取
- [ ] `CdealRawData.py` 中各方法未在主流程统一调用
- [ ] 缺少统一入口脚本（main.py）串联全流程
- [ ] Neo4j 索引未创建（建议对 Company.ts_code、Manager.biz_key 建索引）
- [ ] 股权质押数据（pledge_stat）
- [ ] 财务指标数据（fina_indicator）
- [ ] 闲聊识别模型训练与部署
- [ ] BiLSTM+CRF 槽位填充模型训练与部署
- [ ] 新闻清洗管线实现
- [ ] 板块分类模型训练
- [ ] 板块影响预测模型训练（FinBERT 微调）
- [ ] 量化回测引擎实现
- [ ] 新闻情感驱动策略实现
- [ ] 统一对话入口（接入意图识别 → 查询/回测路由）
