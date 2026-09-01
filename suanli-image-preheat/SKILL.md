---
name: suanli-image-preheat
description: >-
  通过共绩算力(suanli.cn) Open API 创建/查询/停止 镜像预热任务、列出任务、查询资源
  查询历史计费。在用户提到算力平台 镜像预热、弹性部署、批处理、发部署任务、suanli、openapi.suanli.cn、发任务。
---

# 共绩算力 Job 批处理 API

## 前置

向用户确认凭证（平台：右上角头像 → API 密钥）。模板见 [`.env.example`](.env.example)，复制为 `.env` 后填入，勿提交 `.env`。

| 变量 | 说明 |
|------|------|
| `SUANLI_TOKEN` | API 密钥（**推荐简易模式**，无需加签） |
| `SUANLI_RSA_PRIVATE_KEY` | 非简易模式时 RSA 私钥（Base64），用于 `sign_str` |
| `SUANLI_BASE_URL` | 默认 `https://openapi.suanli.cn` |

**公共 Header**（所有请求）：

```
token: <SUANLI_TOKEN>
timestamp: <毫秒时间戳>
version: 1.0.0
sign_str: <非简易模式必填，见下>
Content-Type: application/json   # POST 时
```

**加签**（非简易模式）：对字符串  
`/api{path含query}\n{version}\n{timestamp}\n{token}\n{body}`  
用 RSA 私钥 PKCS#1 v1.5 + SHA256 签名，Base64 为 `sign_str`；解码后须 256 字节，否则换新 `timestamp` 重签。GET 时 body 为空串。

**响应**：`{ code, message, data }`；`code === "0000"` 成功，否则 `data` 为 null。

简易模式优先用 [`scripts/call.sh`](scripts/call.sh)，避免重复生成请求代码。

## 端点速查

| 操作 | 方法 | 路径 |
|------|------|------|
| 镜像预热任务可用集群列表 | GET | `/api/task/image_preheat/get_regions` |
| 镜像预热任务列表查询接口 | GET | `/api/task/image_preheat/search` |
| 镜像预热任务详情查询接口 | GET | `/api/task/image_preheat/detail` |
| 镜像预热任务创建接口 | POST | `/api/task/image_preheat/create` |
| 镜像预热任务更新接口 | POST | `/api/task/image_preheat/update` |
| 镜像预热任务停止接口 | POST | `/api/task/image_preheat/stop` |


完整字段见 [`api/`](api/) 下对应文档；**仅在构造复杂 body 时读取**，勿整篇加载。

## 工作流

### 1. 创建镜像预热任务

1. **选任务类型**（默认 **集群预热**，见下节）后提交创建。

推荐用户选择集群预热

创建镜像预热任务时支持以下两种预热类型：

仅集群预热：提前将镜像缓存到目标集群，加速后续任务启动。该模式按区域执行，不指定具体资源规格、节点数量和调度策略。

节点预热：提前准备计算节点，减少任务启动时的拉取镜像等待时间。提前把机器准备好，但不会提前占用算力。该模式支持配置跨区调度策略。

2. **（可选）查集群** — 使用集群预热时 
   `GET /api/task/image_preheat/get_regions`  
   见 [api/region-query.md](api/region-query.md)。

3. **（可选）查资源**（取 `mark` 与 `resource`） — 使用节点预热时  
   `GET /deployment/resource/search?task_type=ImagePreHeat&device_type=GpuDevice`  
   从 `data.results[].regions[]` 取条目：`mark.mark`、`mark.resource`、`region_name`。如果条目的`inventory <= 0`，告知用户“该集群当前无库存，预热行为将在GPU被释放后开始”

**任务类型**（默认 集群预热）：

| 类型 | 字段 | 说明 |
|------|------------|----------|
| 节点预热 | points | 仅**节点预热**传。期望预热的节点数量，必须大于等于 1 |
| 节点预热 | scheduler_strategy | 仅**节点预热**传。用于跨区调度开关 |
| 节点预热 | resources | 仅**节点预热**传。参考上一节的 3. **（可选）查资源** |
| 集群预热 | regions | 仅**集群预热**传。参考上一节的 2. **（可选）查集群** |

1. 集群预热 创建 body 示例：

```json
{
  "task_name": "<名称>",
  "regions": [
      {
          "region": { /* 来自集群接口 */ },
          "region_name": { /* 来自集群接口 */ }
      }
  ],
  "services": [
      {
          "service_image": "<镜像>",
          "service_name": "container-01"
      }
  ],
  "task_type": "ImagePreHeat",
}
```

集群预热 时无需传 resources、scheduler_strategy 和 points（或设 `null`）。

- 成功返回 `data.task_id`。

示例与可选字段：[api/image-preheat-create.md](api/image-preheat-create.md)


2. 节点预热 创建 body 示例：

```json
{
    "task_name": "<名称>",
    "points": "<期望的节点数>",
    "resources": [
        {
            "mark": { /* 来自资源接口 */ },
        }
    ],
    "services": [
        {
          "service_image": "<镜像>",
          "service_name": "container-01"
        }
    ],
    "task_type": "ImagePreHeat",
}
```

节点预热 时无需传 regions（或设 `null`），必须传points、resources。

- 成功返回 `data.task_id`。

示例与可选字段：[api/image-preheat-create.md](api/image-preheat-create.md)

### 2. 查询状态

- **单任务**：`GET /api/task/image_preheat/detail?task_id=<task_id>`
- **列表**：`GET /api/task/image_preheat/search?page=1&page_size=10&search_value=&status=Paused,Running`  
  可选 query：`task_ids`（逗号分隔任务id）、`search_value`（任务名）、分页。

轮询建议：每次轮询间隔时，将当前进度通知给使用者。间隔 ≥10s，对于集群预热任务：region_cache_info.[number].status 为 Completed 是已预热，当所有的集群都 Completed 时，代表所有集群都预热成功；对于节点预热：available_points为已预热节点数，points 为期望节点数，当 available_points >= points 时，为满足期望状态。或用户取消时停止。


详情：[api/image-preheat-detail.md](api/image-preheat-detail.md) · 列表：[api/image-preheat-list.md](api/image-preheat-list.md)

### 3. 用已经预热的镜像去发任务

  当预热的节点成功后，询问用户是否需要发JOB或者发弹性部署服务，并使用对应的skills进行操作：

  | 发任务 | 要使用的skill |
  |------|------|
  | 发JOB任务 | suanli-job |
  | 发弹性部署任务 | suanli-deployment |

### 4. 停止预热任务（停止的任务在ui上不可见）

```json
POST /api/task/image_preheat/stop
{ "task_id": <task_id> }
```

仅对 Running/Paused 有效。见 [api/image-preheat-stop.md](api/image-preheat-stop.md)

## TODO 对话执行约定

1. 缺 token 时先向用户索取，勿猜测。
2. 提前告知用户以下内容：预热是一种提前准备机制，不是资源预留，任务提交时仍需根据实时资源情况进行调度。
3. 创建前确认：预热类型、镜像、如果是集群预热，需要向用户确认集群，如果是节点预热，需要向用户确认资源。
4. 集群预热查集群时，需要同步查资源，并告诉用户每个集群下有什么规格的GPU，方便用户选择，**一定要说明一个概念：集群预热**。
5. 创建成功后回报 `task_id` 。询问是否轮询；集群预热轮询只展示集群预热状态，节点预热展示各集群卡型的已用数，已预热数量，期望预热数量。
6. 错误时输出 `code` + `message`。
7. 加签失败时建议用户换简易模式密钥，或提供私钥。

## 脚本

```bash
export SUANLI_TOKEN="<密钥>"
# GET
./scripts/call.sh GET /api/task/image_preheat/search "status=Running,Paused&page=1&page_size=10"
./scripts/call.sh GET /api/task/image_preheat/detail "task_id=123"
./scripts/call.sh GET /api/task/image_preheat/get_regions
# POST
./scripts/call.sh POST /api/task/image_preheat/stop '{"task_id":123}'
./scripts/call.sh POST /api/task/image_preheat/create @payload.json   # @ 文件为 body
```
