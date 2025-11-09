---
sidebar_position: 30
slug: /postman_verify_graphrag_prompts
---

# 使用 Postman 验证 GraphRAG 自定义提示

本文演示如何在没有前端页面的情况下，使用 Postman 完成以下验证：

- 调用登录接口并获取访问令牌；
- 在知识库/数据集配置中写入 `entity_description_prompt` 与 `relationship_description_prompt`；
- 通过详情接口确认自定义提示已被持久化；
- 触发后端重新解析文档，让提示词被注入到大模型调用链路。

## 1. 启动后端服务

```bash
python -m api.ragflow_server
```

服务默认监听在 `0.0.0.0:<PORT>`（端口在 `conf/app.toml` 中配置）。Postman 中的基础 URL 形如 `http://<HOST>:<PORT>`。

## 2. 登录并获取令牌

1. 使用项目提供的脚本对明文密码进行 RSA 加密：
   ```bash
   python -m api.utils.t_crypt <YourPlainPassword>
   ```
   复制输出的 Base64 字符串。
2. 在 Postman 中向 `POST /v1/user/login` 发送 JSON：
   ```json
   {
     "email": "someone@example.com",
     "password": "<上一步生成的Base64密文>"
   }
   ```
3. 响应头 `Authorization` 会返回会话令牌。后续所有请求都需要在 Header 中加入：
   ```
   Authorization: <响应头中的令牌>
   ```

## 3. 查询现有知识库或数据集 ID

- 如果使用知识库接口，调用 `GET /v1/kb/list` 或 `POST /v1/kb/list`（请求体可为空对象）来获取 `kb_id`。
- 如果使用 SDK 数据集接口，调用 `GET /api/v1/sdk/datasets` 获取 `id`。

> **提示**：若尚无知识库，可通过 `POST /v1/kb/create`（需在请求体提供 `name` 等字段）或 `POST /api/v1/sdk/datasets` 新建。

## 4. 在配置中写入 GraphRAG 提示

### 4.1 通过知识库接口

向 `POST /v1/kb/update` 发送如下 JSON（`kb_id` 填写目标知识库 ID）：

```json
{
  "kb_id": "<知识库ID>",
  "name": "保持原有名称",
  "description": "保持原有描述",
  "parser_id": "naive",
  "parser_config": {
    "graphrag": {
      "use_graphrag": true,
      "method": "light",
      "entity_description_prompt": "实体解释应该如何写？",
      "relationship_description_prompt": "关系解释应该包含哪些重点？"
    }
  }
}
```

### 4.2 通过 SDK 数据集接口

向 `PUT /api/v1/sdk/datasets/<dataset_id>` 发送需要修改的字段，例如：

```json
{
  "parser_config": {
    "graphrag": {
      "entity_description_prompt": "实体提示",
      "relationship_description_prompt": "关系提示"
    }
  }
}
```

后台会自动与已有配置合并，因此只需在请求体中放入需修改的字段。

## 5. 验证提示是否持久化

- 调用 `GET /v1/kb/detail?kb_id=<知识库ID>`，在响应的 `parser_config.graphrag` 节点中应能看到刚才写入的两个字段；
- 或者调用 `GET /api/v1/sdk/datasets?id=<dataset_id>`，检查返回体的 `parser_config.graphrag` 是否包含自定义提示。

如果字段缺失，请确认更新请求中 `parser_config.graphrag.use_graphrag` 设为 `true`，并重试第 4 步。

## 6. 触发文档重新解析

为了验证提示词会注入到 GraphRAG 流程，可针对某个文档调用 `POST /v1/document/change_parser`：

```json
{
  "doc_id": "<文档ID>",
  "parser_id": "naive",
  "parser_config": {
    "graphrag": {
      "use_graphrag": true,
      "entity_description_prompt": "实体提示",
      "relationship_description_prompt": "关系提示"
    }
  }
}
```

该接口会将文档状态重置为待处理，任务执行时会读取知识库/数据集中存储的 GraphRAG 提示，并在构图阶段把它们传递给大模型。

## 7. 常见排查

- **401/403**：确认 `Authorization` 头是否携带最新令牌。
- **更新后提示缺失**：检查 `parser_config` 是否被整体覆盖，可先通过第 5 步读取现有配置，再在 Postman 中局部修改需要的字段。
- **GraphRAG 未生效**：确保上传的新文档或重新触发解析后再检查知识图谱结果。

按照以上步骤，即可在 Postman 中验证自定义实体解释和关系解释是否正确写入配置并贯穿到 GraphRAG 流程。
