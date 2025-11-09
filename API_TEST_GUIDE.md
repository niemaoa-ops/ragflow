# RAGFlow 知识库实体配置 API 测试指南

## 功能说明

本次更新为 RAGFlow 知识库的 GraphRAG 配置增加了以下功能：
- **entity_descriptions**: 实体类型的自定义解释（字典类型，key 为实体类型，value 为解释）
- **relation_descriptions**: 关系类型的自定义解释（列表类型）

这些配置会被保存到数据库，并在 GraphRAG 提取实体和关系时传递给大模型，帮助模型更准确地理解和识别实体。

## API 接口

### 1. 更新知识库配置（POST /kb/update）

#### 请求示例

```json
{
  "kb_id": "your_kb_id_here",
  "name": "测试知识库",
  "description": "测试知识库描述",
  "parser_id": "general",
  "parser_config": {
    "chunk_token_num": 128,
    "delimiter": "\n",
    "graphrag": {
      "use_graphrag": true,
      "entity_types": ["organization", "person", "technology", "product", "location"],
      "entity_descriptions": {
        "organization": "公司、企业、机构等组织实体，包括但不限于科技公司、研究机构、政府部门等",
        "person": "人物实体，包括工程师、科学家、管理人员、专家等",
        "technology": "技术、工艺、方法等技术性实体",
        "product": "产品、设备、系统等实物或软件产品",
        "location": "地理位置、地点、区域等"
      },
      "relation_descriptions": [
        "从属关系：表示一个实体隶属于另一个实体，如员工属于公司",
        "使用关系：表示一个实体使用或应用了另一个实体，如产品使用了某项技术",
        "合作关系：表示两个实体之间存在协作或合作关系",
        "位于关系：表示一个实体位于某个地点或区域"
      ],
      "method": "general",
      "community": false,
      "resolution": false
    }
  }
}
```

#### 响应示例

```json
{
  "code": 0,
  "data": {
    "kb_id": "your_kb_id_here",
    "name": "测试知识库",
    "description": "测试知识库描述",
    "parser_config": {
      "graphrag": {
        "use_graphrag": true,
        "entity_types": ["organization", "person", "technology", "product", "location"],
        "entity_descriptions": {
          "organization": "公司、企业、机构等组织实体，包括但不限于科技公司、研究机构、政府部门等",
          "person": "人物实体，包括工程师、科学家、管理人员、专家等",
          "technology": "技术、工艺、方法等技术性实体",
          "product": "产品、设备、系统等实物或软件产品",
          "location": "地理位置、地点、区域等"
        },
        "relation_descriptions": [
          "从属关系：表示一个实体隶属于另一个实体，如员工属于公司",
          "使用关系：表示一个实体使用或应用了另一个实体，如产品使用了某项技术",
          "合作关系：表示两个实体之间存在协作或合作关系",
          "位于关系：表示一个实体位于某个地点或区域"
        ],
        "method": "general",
        "community": false,
        "resolution": false
      }
    }
  },
  "message": "success"
}
```

### 2. 获取知识库详情（GET /kb/detail）

#### 请求参数
- `kb_id`: 知识库 ID（URL 参数）

#### 请求示例
```
GET /kb/detail?kb_id=your_kb_id_here
```

#### 响应示例

```json
{
  "code": 0,
  "data": {
    "id": "your_kb_id_here",
    "name": "测试知识库",
    "description": "测试知识库描述",
    "parser_config": {
      "graphrag": {
        "use_graphrag": true,
        "entity_types": ["organization", "person", "technology", "product", "location"],
        "entity_descriptions": {
          "organization": "公司、企业、机构等组织实体，包括但不限于科技公司、研究机构、政府部门等",
          "person": "人物实体，包括工程师、科学家、管理人员、专家等",
          "technology": "技术、工艺、方法等技术性实体",
          "product": "产品、设备、系统等实物或软件产品",
          "location": "地理位置、地点、区域等"
        },
        "relation_descriptions": [
          "从属关系：表示一个实体隶属于另一个实体，如员工属于公司",
          "使用关系：表示一个实体使用或应用了另一个实体，如产品使用了某项技术",
          "合作关系：表示两个实体之间存在协作或合作关系",
          "位于关系：表示一个实体位于某个地点或区域"
        ],
        "method": "general",
        "community": false,
        "resolution": false
      }
    }
  },
  "message": "success"
}
```

## Postman 测试步骤

### 1. 设置环境变量

在 Postman 中创建环境变量：
- `base_url`: RAGFlow API 地址（如：`http://localhost:9380`）
- `token`: 登录后获取的 token

### 2. 测试更新配置

1. 创建新的 POST 请求
2. URL: `{{base_url}}/api/kb/update`
3. Headers:
   - `Content-Type`: `application/json`
   - `Authorization`: `Bearer {{token}}`
4. Body (选择 raw JSON):
   - 粘贴上述请求示例 JSON
   - 修改 `kb_id` 为实际的知识库 ID
5. 点击 Send

### 3. 测试获取配置

1. 创建新的 GET 请求
2. URL: `{{base_url}}/api/kb/detail?kb_id=your_kb_id_here`
3. Headers:
   - `Authorization`: `Bearer {{token}}`
4. 点击 Send
5. 检查响应中的 `parser_config.graphrag.entity_descriptions` 和 `relation_descriptions` 字段

## 配置说明

### entity_descriptions（可选）
- 类型：对象（字典）
- 格式：`{ "实体类型": "实体类型说明" }`
- 作用：为每个实体类型提供详细说明，帮助大模型更准确地识别该类型的实体
- 示例：
  ```json
  {
    "organization": "公司、企业、机构等组织实体",
    "person": "人物实体，包括工程师、科学家等"
  }
  ```

### relation_descriptions（可选）
- 类型：数组（列表）
- 格式：字符串数组
- 作用：提供关系类型的说明，帮助大模型理解和提取实体间的关系
- 示例：
  ```json
  [
    "从属关系：表示一个实体隶属于另一个实体",
    "使用关系：表示一个实体使用或应用了另一个实体"
  ]
  ```

## 实现原理

1. **配置保存**：自定义的实体和关系解释会保存在知识库的 `parser_config.graphrag` 配置中
2. **提示词注入**：在 GraphRAG 执行时，这些解释会被注入到提示词中
3. **模型理解**：大模型会根据这些说明更准确地提取和分类实体及关系

### 提示词注入示例

配置了 `entity_descriptions` 后，提示词会变成：

```
entity_type: 以下类型之一：[organization, person, technology]
实体类型说明：
  - organization: 公司、企业、机构等组织实体，包括但不限于科技公司、研究机构、政府部门等
  - person: 人物实体，包括工程师、科学家、管理人员、专家等
  - technology: 技术、工艺、方法等技术性实体
```

## 注意事项

1. 配置字段都是可选的，如果不提供则使用默认行为
2. `entity_descriptions` 的 key 必须存在于 `entity_types` 中
3. 配置会立即保存到数据库，下次文档解析时生效
4. 修改配置后，需要重新解析文档才能应用新的实体和关系解释
