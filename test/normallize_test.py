import re
from dataclasses import dataclass
from typing import List, Tuple, Optional

from rapidfuzz import fuzz


@dataclass
class MatchResult:
    name1: str
    name2: str
    norm1: str
    norm2: str
    score: float
    is_match: bool


class EntityNormalizer:
    """
    用于公司/股东名称的归一化和匹配
    适合中文公司名、机构名、基金名的初步清洗
    """

    def __init__(self):
        # 常见公司/机构后缀
        self.suffix_patterns = [
            r"股份有限公司$",
            r"有限责任公司$",
            r"有限公司$",
            r"集团股份有限公司$",
            r"集团有限公司$",
            r"控股股份有限公司$",
            r"控股有限公司$",
            r"科技股份有限公司$",
            r"科技有限公司$",
            r"投资股份有限公司$",
            r"投资有限公司$",
            r"发展股份有限公司$",
            r"发展有限公司$",
            r"管理有限公司$",
            r"企业管理有限公司$",
            r"合伙企业\(有限合伙\)$",
            r"合伙企业（有限合伙）$",
            r"有限合伙$",
            r"股份公司$",
            r"集团$",
        ]

        # 一些无实际区分意义的符号
        self.symbol_pattern = re.compile(r"[（）()【】\[\]\-—_·,.，。/\\\s]+")

    def normalize_name(self, name: str) -> str:
        """
        名称归一化：
        1. 去空格和标点
        2. 统一括号
        3. 去常见公司后缀
        4. 转小写（主要兼容英文）
        """
        if name is None:
            return ""

        name = str(name).strip().lower()

        # 去除多余符号和空白
        name = self.symbol_pattern.sub("", name)

        # 去常见后缀
        for pattern in self.suffix_patterns:
            name = re.sub(pattern, "", name)

        return name

    def calc_similarity(self, name1: str, name2: str) -> Tuple[str, str, float]:
        """
        返回两个名字的：
        - 归一化结果
        - 相似度分数
        """
        norm1 = self.normalize_name(name1)
        norm2 = self.normalize_name(name2)

        if not norm1 or not norm2:
            return norm1, norm2, 0.0

        # 综合多个相似度分数
        score_ratio = fuzz.ratio(norm1, norm2)
        score_partial = fuzz.partial_ratio(norm1, norm2)
        score_token = fuzz.token_sort_ratio(norm1, norm2)

        # 取一个加权平均
        final_score = 0.5 * score_ratio + 0.3 * score_partial + 0.2 * score_token

        return norm1, norm2, round(final_score, 2)

    def is_same_entity(
        self,
        name1: str,
        name2: str,
        threshold: float = 85.0
    ) -> MatchResult:
        """
        判断两个名字是否可能是同一实体
        threshold 默认 85，可按你的数据调
        """
        norm1, norm2, score = self.calc_similarity(name1, name2)

        # 一个很实用的小规则：
        # 归一化后完全相同，直接视为同一实体
        if norm1 == norm2 and norm1 != "":
            return MatchResult(
                name1=name1,
                name2=name2,
                norm1=norm1,
                norm2=norm2,
                score=100.0,
                is_match=True
            )

        return MatchResult(
            name1=name1,
            name2=name2,
            norm1=norm1,
            norm2=norm2,
            score=score,
            is_match=score >= threshold
        )

    def deduplicate_entities(
        self,
        names: List[str],
        threshold: float = 85.0
    ) -> List[List[str]]:
        """
        对一批名称进行简单聚类去重
        返回结果示例：
        [
            ["百度科技有限公司", "百度", "百度在线网络技术(北京)有限公司"],
            ["阿里巴巴集团控股有限公司", "阿里巴巴"]
        ]
        """
        groups: List[List[str]] = []

        for name in names:
            placed = False

            for group in groups:
                # 与组内第一个名称比较
                result = self.is_same_entity(name, group[0], threshold=threshold)
                if result.is_match:
                    group.append(name)
                    placed = True
                    break

            if not placed:
                groups.append([name])

        return groups


if __name__ == "__main__":
    normalizer = EntityNormalizer()

    test_pairs = [
        ("百度科技有限公司", "百度"),
        ("百度在线网络技术(北京)有限公司", "百度"),
        ("阿里巴巴集团控股有限公司", "阿里巴巴"),
        ("腾讯科技（深圳）有限公司", "腾讯"),
        ("香港中央结算有限公司", "香港中央结算"),
        ("招商银行股份有限公司", "招商银行"),
        ("中国平安保险（集团）股份有限公司", "中国平安"),
        ("中信证券股份有限公司", "中信建投"),
    ]

    print("=== 两两匹配测试 ===")
    for a, b in test_pairs:
        result = normalizer.is_same_entity(a, b, threshold=85)
        print(
            f"{a}  <->  {b}\n"
            f"归一化: {result.norm1}  <->  {result.norm2}\n"
            f"分数: {result.score}, 是否同一实体: {result.is_match}\n"
        )

    print("=== 批量去重测试 ===")
    names = [
        "百度科技有限公司",
        "百度",
        "百度在线网络技术(北京)有限公司",
        "阿里巴巴集团控股有限公司",
        "阿里巴巴",
        "腾讯科技（深圳）有限公司",
        "腾讯",
        "香港中央结算有限公司",
        "香港中央结算",
        "中信证券股份有限公司",
        "中信建投证券股份有限公司",
    ]

    groups = normalizer.deduplicate_entities(names, threshold=85)
    for idx, group in enumerate(groups, 1):
        print(f"组{idx}: {group}")