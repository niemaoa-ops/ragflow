# Licensed under the MIT License
"""
Reference:
 - [LightRag](https://github.com/HKUDS/LightRAG)
 - [MiniRAG](https://github.com/HKUDS/MiniRAG)
"""
PROMPTS = {}

#系统中就使用了这个提示词
PROMPTS["minirag_query2kwd"] = """--- 角色 ---
你是一个乐于助人的助手，负责识别用户查询中的答案类型关键词和低层级关键词。

--- 目标 ---
给定查询内容，列出答案类型关键词和低层级关键词。
答案类型关键词聚焦于特定查询的答案类型，而低层级关键词则聚焦于具体实体、细节或具体术语。
答案类型关键词必须从答案类型池（Answer type pool）中选择。
该池以字典形式呈现，其中键代表你应选择的类型，值代表示例样本。

--- 说明 ---
- 以 JSON 格式输出关键词。
- JSON 应包含两个键：
  - "answer_type_keywords"：用于存放答案类型。在此列表中，可能性最高的类型应放在最前面。数量不超过 3 个。
  - "entities_from_query"：用于存放特定实体或细节。必须从查询中提取。
######################
- 示例 -
######################
示例 1：

Query: "全电环控系统如何提高军机的燃油效率？"
Answer type pool: 
{{
 "系统原理": ["工作机制", "能量转换流程"],
 "技术参数": ["功率消耗", "效率指标"],
 "部件组成": ["压缩机", "换热器"],
 "材料特性": ["钛合金强度", "复合材料耐温性"],
 "工艺方法": ["焊接工艺", "精密加工技术"],
 "机构职责": ["研制单位", "检测机构"],
 "应用场景": ["军机环境", "民机配置"]
}}
################
Output:
{{
  "answer_type_keywords": ["系统原理", "技术参数"],
  "entities_from_query": ["全电环控系统", "军机", "燃油效率", "能量转换"]
}}
#############################
示例 2：

Query: "TC4钛合金用于哪些机电系统部件的制造？"
Answer type pool: 
{{
 "部件名称": ["活塞杆", "导管", "壳体"],
 "系统类型": ["液压系统", "环控系统", "电源系统"],
 "材料特性": ["强度指标", "耐腐蚀性"],
 "工艺要求": ["锻造参数", "焊接标准"],
 "应用机型": ["C929", "翼龙 - 10", "运 - 20"],
 "供应机构": ["宝钛集团", "中航材料院"]
}}
################
Output:
{{
 "answer_type_keywords": ["部件名称", "系统类型"],
 "entities_from_query": ["TC4钛合金", "机电系统部件", "制造材料"]
}}
#############################
示例 3:

Query: "激光焊接工艺在液压管路连接中的优势是什么？"
Answer type pool: 
{{
 "工艺特性": ["连接强度", "密封性指标"],
 "性能提升": ["减重效果", "寿命延长"],
 "应用场景": ["高压环境", "低温工况"],
 "对比参数": ["与法兰连接的差异", "与螺纹连接的区别"],
 "实施机构": ["中航工业制造所", "西航发动机公司"]
}}
################
Output:
{{
  "answer_type_keywords": ["工艺特性", "性能提升"],
  "entities_from_query": ["激光焊接工艺", "液压管路连接", "连接优势"]
}}
#############################
示例 4:

Query: "中航机电系统有限公司负责研制哪些民机机电系统？"
Answer type pool: 
{{
 "系统名称": ["全电环控系统", "电源系统", "液压助力系统"],
 "机型适配": ["C929", "ARJ21", "C919"],
 "研制阶段": ["设计阶段", "测试阶段", "量产阶段"],
 "技术指标": ["可靠性参数", "国产化率"],
 "合作机构": ["中国商飞", "华为技术有限公司"]
}}
################
Output:
{{
  "answer_type_keywords": ["系统名称", "机型适配"],
  "entities_from_query": ["中航机电系统有限公司", "民机机电系统", "研制任务"]
}}
#############################

-Real Data-
######################
Query: {query}
Answer type pool:{TYPE_POOL}
######################
Output:

"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}
#############################""",
]
