# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License
"""
Reference:
 - [GraphRAG](https://github.com/microsoft/graphrag/blob/main/graphrag/prompts/index/extract_graph.py)
"""

GRAPH_EXTRACTION_PROMPT = """
- 目标 -
给定一个可能与该主题相关的文本文档和实体类型列表，从文本中识别出所有属于这些类型的实体，以及已识别实体之间的所有关系。

- 步骤 -
1、识别所有实体。对于每个识别出的实体，提取以下信息：
entity_name: 实体名称，首字母大写，使用 "文本" 中的语言
entity_type: 以下类型之一：[{entity_types}]
entity_description: {entity_description_instruction}
每个实体格式：("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2、从步骤 1 中识别的实体中，识别所有明显相关的 (源实体，目标实体) 对。
对于每对相关实体，提取以下信息：
source_entity: 源实体名称，如步骤 1 中所识别
target_entity: 目标实体名称，如步骤 1 中所识别
relationship_description: {relationship_description_instruction}
relationship_strength: 表示源实体和目标实体之间关系强度的数字评分
每个关系格式：("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_strength>)

3、将输出作为步骤 1 和步骤 2 中识别的所有实体和关系的单个列表返回。使用 **{record_delimiter}** 作为列表分隔符。
4、完成后，输出 {completion_delimiter}

######################
- 示例 -
######################
示例 1：

Entity_types：[机型，系统，部件，机构，人员]
Text：
中航工业集团研发的运-20大型运输机配备了先进的液压系统，该系统由西安航空制动科技有限公司提供的液压泵和管路组件组成。王工程师负责该液压系统的集成测试工作，他表示该系统的可靠性达到了国际先进水平。

################
Output：
("entity"{tuple_delimiter}"运-20"{tuple_delimiter}"机型"{tuple_delimiter}"中航工业集团研发的大型运输机"){record_delimiter}
("entity"{tuple_delimiter}"液压系统"{tuple_delimiter}"系统"{tuple_delimiter}"运-20配备的先进系统，可靠性达到国际先进水平"){record_delimiter}
("entity"{tuple_delimiter}"液压泵"{tuple_delimiter}"部件"{tuple_delimiter}"西安航空制动科技有限公司提供的液压系统组件"){record_delimiter}
("entity"{tuple_delimiter}"管路组件"{tuple_delimiter}"部件"{tuple_delimiter}"西安航空制动科技有限公司提供的液压系统组件"){record_delimiter}
("entity"{tuple_delimiter}"中航工业集团"{tuple_delimiter}"机构"{tuple_delimiter}"运-20 的研发机构"){record_delimiter}
("entity"{tuple_delimiter}"西安航空制动科技有限公司"{tuple_delimiter}"机构"{tuple_delimiter}"为运-20 液压系统提供液压泵和管路组件的公司"){record_delimiter}
("entity"{tuple_delimiter}"王工程师"{tuple_delimiter}"人员"{tuple_delimiter}"负责运-20液压系统集成测试工作的工程师"){record_delimiter}
("relationship"{tuple_delimiter}"运-20"{tuple_delimiter}"液压系统"{tuple_delimiter}"运-20配备了该液压系统"{tuple_delimiter} 9){record_delimiter}
("relationship"{tuple_delimiter}"液压系统"{tuple_delimiter}"液压泵"{tuple_delimiter}"液压泵是液压系统的组成部分"{tuple_delimiter} 10){record_delimiter}
("relationship"{tuple_delimiter}"液压系统"{tuple_delimiter}"管路组件"{tuple_delimiter}"管路组件是液压系统的组成部分"{tuple_delimiter} 10){record_delimiter}
("relationship"{tuple_delimiter}"中航工业集团"{tuple_delimiter}"运-20"{tuple_delimiter}"中航工业集团研发了运-20"{tuple_delimiter} 9){record_delimiter}
("relationship"{tuple_delimiter}"西安航空制动科技有限公司"{tuple_delimiter}"液压泵"{tuple_delimiter}"西安航空制动科技有限公司提供了液压泵"{tuple_delimiter} 8){record_delimiter}
("relationship"{tuple_delimiter}"王工程师"{tuple_delimiter}"液压系统"{tuple_delimiter}"王工程师负责液压系统的集成测试工作"{tuple_delimiter} 8){completion_delimiter}
#############################
示例 2：

Entity_types：[技术，项目，标准，机构，机型]
Text：
C919大型客机的航电系统项目采用了DO-178B软件标准，该标准由美国航空无线电技术委员会制定。中国商飞联合华为公司共同开发了符合该标准的航电核心处理技术，这项技术的应用使C919的航电系统性能达到世界领先水平。

################
Output：
("entity"{tuple_delimiter}"C919"{tuple_delimiter}"机型"{tuple_delimiter}"采用先进航电系统的大型客机"){record_delimiter}
("entity"{tuple_delimiter}"航电系统项目"{tuple_delimiter}"项目"{tuple_delimiter}"C919的航电子系统研发项目"){record_delimiter}
("entity"{tuple_delimiter}"DO-178B"{tuple_delimiter}"标准"{tuple_delimiter}"航电系统软件标准，由美国航空无线电技术委员会制定"){record_delimiter}
("entity"{tuple_delimiter}"航电核心处理技术"{tuple_delimiter}"技术"{tuple_delimiter}"符合DO-178B标准，由中国商飞联合华为公司开发"){record_delimiter}
("entity"{tuple_delimiter}"美国航空无线电技术委员会"{tuple_delimiter}"机构"{tuple_delimiter}"制定DO-178B软件标准的机构"){record_delimiter}
("entity"{tuple_delimiter}"中国商飞"{tuple_delimiter}"机构"{tuple_delimiter}"联合华为公司开发航电核心处理技术的机构"){record_delimiter}
("entity"{tuple_delimiter}"华为公司"{tuple_delimiter}"机构"{tuple_delimiter}"与中国商飞共同开发航电核心处理技术的公司"){record_delimiter}
("relationship"{tuple_delimiter}"C919"{tuple_delimiter}"航电系统项目"{tuple_delimiter}"C919包含航电系统项目"{tuple_delimiter} 9){record_delimiter}
("relationship"{tuple_delimiter}"航电系统项目"{tuple_delimiter}"DO-178B"{tuple_delimiter}"航电系统项目采用了DO-178B软件标准"{tuple_delimiter} 8){record_delimiter}
("relationship"{tuple_delimiter}"美国航空无线电技术委员会"{tuple_delimiter}"DO-178B"{tuple_delimiter}"美国航空无线电技术委员会制定了 DO-178B 标准"{tuple_delimiter} 10){record_delimiter}
("relationship"{tuple_delimiter}"中国商飞"{tuple_delimiter}"华为公司"{tuple_delimiter}"中国商飞联合华为公司共同开发航电核心处理技术"{tuple_delimiter} 9){record_delimiter}
("relationship"{tuple_delimiter}"航电核心处理技术"{tuple_delimiter}"DO-178B"{tuple_delimiter}"航电核心处理技术符合DO-178B标准"{tuple_delimiter} 7){record_delimiter}
("relationship"{tuple_delimiter}"航电核心处理技术"{tuple_delimiter}"C919"{tuple_delimiter}"航电核心处理技术应用于C919，提升了其航电系统性能"{tuple_delimiter} 8){completion_delimiter}
#############################
示例 3：

Entity_types：[部件，技术，问题，解决方案，机构，人员]
Text：
某型直升机的燃油泵在高温环境下出现密封不良问题，导致燃油泄漏。611所的张教授团队研发了新型氟橡胶密封技术，该技术应用于燃油泵后，成功解决了密封不良问题，使燃油泵在高温环境下的可靠性提升了40%。

################
Output：
("entity"{tuple_delimiter}"燃油泵"{tuple_delimiter}"部件"{tuple_delimiter}"某型直升机的部件，在高温环境下存在密封问题"){record_delimiter}
("entity"{tuple_delimiter}"密封不良问题"{tuple_delimiter}"问题"{tuple_delimiter}"燃油泵在高温环境下出现的问题，导致燃油泄漏"){record_delimiter}
("entity"{tuple_delimiter}"燃油泄漏"{tuple_delimiter}"问题"{tuple_delimiter}"由密封不良问题导致的结果"){record_delimiter}
("entity"{tuple_delimiter}"新型氟橡胶密封技术"{tuple_delimiter}"技术"{tuple_delimiter}"由611所张教授团队研发的密封技术"){record_delimiter}
("entity"{tuple_delimiter}"611所"{tuple_delimiter}"机构"{tuple_delimiter}"张教授团队所在的研究机构"){record_delimiter}
("entity"{tuple_delimiter}"张教授团队"{tuple_delimiter}"人员"{tuple_delimiter}"研发新型氟橡胶密封技术的团队"){record_delimiter}
("relationship"{tuple_delimiter}"燃油泵"{tuple_delimiter}"密封不良问题"{tuple_delimiter}"燃油泵在高温环境下出现密封不良问题"{tuple_delimiter} 9){record_delimiter}
("relationship"{tuple_delimiter}"密封不良问题"{tuple_delimiter}"燃油泄漏"{tuple_delimiter}"密封不良问题导致燃油泄漏"{tuple_delimiter} 10){record_delimiter}
("relationship"{tuple_delimiter}"611所"{tuple_delimiter}"张教授团队"{tuple_delimiter}"张教授团队隶属于611所"{tuple_delimiter} 8){record_delimiter}
("relationship"{tuple_delimiter}"张教授团队"{tuple_delimiter}"新型氟橡胶密封技术"{tuple_delimiter}"张教授团队研发了新型氟橡胶密封技术"{tuple_delimiter} 10){record_delimiter}
("relationship"{tuple_delimiter}"新型氟橡胶密封技术"{tuple_delimiter}"燃油泵"{tuple_delimiter}"新型氟橡胶密封技术应用于燃油泵"{tuple_delimiter} 9){record_delimiter}
("relationship"{tuple_delimiter}"新型氟橡胶密封技术"{tuple_delimiter}"密封不良问题"{tuple_delimiter}"新型氟橡胶密封技术成功解决了密封不良问题"{tuple_delimiter} 10){completion_delimiter}
#############################
-真实数据-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:"""

CONTINUE_PROMPT = "上次抽取遗漏了许多实体。请使用相同格式在下方补充这些实体：\n"
LOOP_PROMPT = "看起来可能仍有一些实体被遗漏。如果仍有需要补充的实体，请回答 Y；如果没有，请回答 N。请仅用一个字母 Y 或 N 回答。\n"

SUMMARIZE_DESCRIPTIONS_PROMPT = """
你是一个乐于助人的助手，负责对下方提供的数据生成一份全面的总结。
给定一个或两个实体，以及一系列描述，所有这些都与同一个实体或一组实体相关。
请将所有这些内容合并成一个全面的描述。确保包含从所有描述中收集的信息。
如果提供的描述存在矛盾，请解决这些矛盾，并提供一个连贯的总结。
确保使用第三人称撰写，并包含实体名称，以便我们了解完整的背景。
使用 中文 作为输出语言。
#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
"""