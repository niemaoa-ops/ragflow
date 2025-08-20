#
#  Copyright 2024 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

ENTITY_RESOLUTION_PROMPT = """
- 目标 -
请按照要求回答以下问题

- 步骤 -
1、按照要求识别每一条问题
2、以中文返回步骤 1 中每个问题的答案，形成一个列表。使用 **{record_delimiter}** 作为列表分隔符。
######################
- 示例 -
######################
示例 1：

Question：
判断两个机电系统部件是否为同一实体时，应仅关注其核心功能和技术参数，忽略名称表述的细微差异。

示范 1：部件 A 名称：“高压液压泵”，部件 B 名称：“高压油压泵” ，是，部件 A 和部件 B 为同一实体。
Question 1：部件 A 名称：“某型环控系统”，部件 B 名称：“环境控制系统”
Question 2：部件 A 名称：“航电核心处理单元”，部件 B 名称：“飞控计算机”
Question 3：部件 A 名称：“钛合金液压管路”，部件 B 名称：“TC4钛合金液压导管”
Question 4：部件 A 名称：“电动作动器”，部件 B 名称：“液压作动器” 

利用机电系统部件的领域知识理解文本，并按以下格式回答上述 4 个问题：对于问题 i，是，部件 A 和部件 B 为同一实体。或 否，部件 A 和部件 B 为不同实体。对于问题 i+1，（重复上述格式）
################
Output:
(For question {entity_index_delimiter} 1 {entity_index_delimiter}, {resolution_result_delimiter} 是 {resolution_result_delimiter}, 部件 A 和部件 B 为同一实体。){record_delimiter}
(For question {entity_index_delimiter} 2 {entity_index_delimiter}, {resolution_result_delimiter} 否 {resolution_result_delimiter}, 部件 A 和部件 B 为不同实体。){record_delimiter}
(For question {entity_index_delimiter} 3 {entity_index_delimiter}, {resolution_result_delimiter} 是 {resolution_result_delimiter}, 部件 A 和部件 B 为同一实体。){record_delimiter}
(For question {entity_index_delimiter} 4 {entity_index_delimiter}, {resolution_result_delimiter} 否 {resolution_result_delimiter}, 部件 A 和部件 B 为不同实体。){record_delimiter}
#############################

示例 2：

Question：
判断两个机电系统相关技术是否为同一技术时，应仅关注其核心原理和应用场景，忽略表述方式的差异。

示范 1：技术 A 名称：“3D 打印成型技术”，技术 B 名称：“增材制造技术” ，是，技术 A 和技术 B 为同一技术。
Question 1：技术 A 名称：“精密铸造工艺”，技术 B 名称：“失蜡铸造工艺”
Question 2：技术 A 名称：“分子筛制氧技术”，技术 B 名称：“化学制氧技术”
Question 3：技术 A 名称：“光纤传感技术”，技术 B 名称：“光纤传感工艺”
Question 4：技术 A 名称：“液压传动技术”，技术 B 名称：“电传操纵技术”

利用机电系统技术的领域知识理解文本，并按以下格式回答上述 4 个问题：对于问题 i，是，技术 A 和技术 B 为同一技术。或 否，技术 A 和技术 B 为不同技术。对于问题 i+1，（重复上述格式）
################
Output:
(For question {entity_index_delimiter} 1 {entity_index_delimiter}, {resolution_result_delimiter} 是 {resolution_result_delimiter}, 技术 A 和技术 B 为同一技术。){record_delimiter}
(For question {entity_index_delimiter} 2 {entity_index_delimiter}, {resolution_result_delimiter} 否 {resolution_result_delimiter}, 技术 A 和技术 B 为不同技术。){record_delimiter}
(For question {entity_index_delimiter} 3 {entity_index_delimiter}, {resolution_result_delimiter} 是 {resolution_result_delimiter}, 技术 A 和技术 B 为同一技术。){record_delimiter}
(For question {entity_index_delimiter} 4 {entity_index_delimiter}, {resolution_result_delimiter} 否 {resolution_result_delimiter}, 技术 A 和技术 B 为不同技术。){record_delimiter}
#############################

-真实数据-
######################
Question:{input_text}
######################
Output:
"""
