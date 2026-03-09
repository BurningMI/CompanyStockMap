# CompanyStockMap

基于 Tushare 数据构建的 A 股公司知识图谱，使用 Neo4j 存储公司、高管、股东及行业之间的关联关系。

## 图谱结构

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
├── config/Conf.py          # 配置：路径、Tushare token、季度日期
├── utils/
│   ├── CgetFromTS.py       # 从 Tushare 拉取原始数据
│   ├── CdealRawData.py     # 清洗处理原始数据
│   └── Cwrite2Neo4j.py     # 写入 Neo4j
├── data/
│   ├── Raw/                # 原始数据
│   └── Processed/          # 清洗后数据
```

## 使用流程

```bash
pip install tinyshare neo4j pandas
```

1. 在 `config/Conf.py` 填入 Tushare token
2. 在 `Cwrite2Neo4j.py` 填入 Neo4j 密码
3. 依次运行：

```bash
python utils/CgetFromTS.py      # 拉取原始数据
python utils/CdealRawData.py    # 清洗数据
python utils/Cwrite2Neo4j.py    # 写入 Neo4j
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

## 待完成

- [ ] `CgetFromTS.py` 中的测试限制（`[:5]`、`[:10]`）改为全量拉取
- [ ] `CdealRawData.py` 中各方法未在主流程统一调用
- [ ] 缺少统一入口脚本（main.py）串联拉取→清洗→写入全流程
- [ ] Neo4j 索引未创建（建议对 Company.ts_code、Manager.biz_key 建索引提升性能）
- [ ] 股权质押数据（pledge_stat）
- [ ] 财务指标数据（fina_indicator）
