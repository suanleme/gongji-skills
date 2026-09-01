---
name: suanli-job
description: >-
  通过共绩算力(suanli.cn) Open API 创建/查询/停止 Job 批处理任务、列出任务、查询资源与存储、
  挂载 NAS、查询 Job 任务队列任务组、查询历史计费。在用户提到算力平台 Job、批处理、
  NAS 挂载、任务队列、suanli、openapi.suanli.cn、发任务、查任务状态、账单/费用时启用。
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

## 计费与价格

平台按**秒**计费，内部计量单位为**点**（与 Job 完成次数 `points` 不同）。

| 换算 | 公式 |
|------|------|
| 元 ↔ 点 | `1 元 = 1,000,000 点` |
| 卡时价 → 每秒点数 | `点/秒 = 卡时价(元/小时) × 1,000,000 / 3600` |
| 点 → 用户消耗（元） | `元 = 点 / 1,000,000` |

**示例**：卡时价 1.98 元/小时 → 每秒 `1.98 × 1,000,000 / 3600 ≈ 550` 点；运行 1 小时消耗 `550 × 3600 = 1,980,000` 点 = **1.98 元**。

**出账周期**：平台每 **5 分钟**出账一次；出账前实时消耗见 `forecast_value`，已出账累计见 `billing_value`。

| 字段 | 来源 | 说明 |
|------|------|------|
| `price` / `discount_price` | 资源列表 `regions[]` | 设备卡时参考价（元/小时）；计费优先按 `discount_price` |
| `billing_value` | 任务详情/列表 | 已累计出账消耗（点） |
| `forecast_value` | 任务详情/列表 | 当前周期尚未出账的实时消耗（点） |
| `billing_points` | 任务详情 | 计费中 Pod 数 |

向用户展示金额时，将 `billing_value`、`forecast_value`、`billing_coin`、`discount_coin` 除以 `1,000,000` 转为元；预估费用可用「卡时价 × 运行小时数」或「每秒点数 × 运行秒数 / 1,000,000」。

**历史账单**（按时间段或任务汇总）：

| 字段 | 来源 | 说明 |
|------|------|------|
| `billing_coin` | 计费查询接口 | 时间段/任务总账（点） |
| `discount_coin` | 计费查询接口 | 优惠抵扣（点） |

## 端点速查

| 操作 | 方法 | 路径 |
|------|------|------|
| 创建 Job | POST | `/task/job/create` |
| 任务详情 | GET | `/task/job/detail?task_id=` |
| 任务列表 | GET | `/task/job/search` |
| 停止任务 | POST | `/task/job/stop` |
| 任务组列表 | GET | `/job/queue/group/search?queue_id=` |
| 任务组详情 | GET | `/job/queue/group/detail?group_id=` |
| 时间维度计费 | GET | `/billing/get_billing_record` |
| 任务维度计费 | GET | `/billing/get_task_billing_record` |
| 设备资源 | GET | `/deployment/resource/search` |
| 对象存储 | GET | `/storage/get_storage` |

完整字段见 [`api/`](api/) 下对应文档；**仅在构造复杂 body 时读取**，勿整篇加载。

## 工作流

询问用户是否要先进行镜像预热，提前把任务所需的镜像准备到目标计算资源附近，可以降低任务冷启动时间，如果使用者需要：请使用 suanli-preheat 这个 skill。

### 1. 创建 Job

1. **查资源**（取 `mark` 与 `resource`）  
   `GET /deployment/resource/search?task_type=Job&device_type=GpuDevice`  
   从 `data.results[].regions[]` 取 `inventory > 0` 的条目：`mark.mark`、`mark.resource`、`region_name`。

2. **（可选）挂载存储**（三类字段勿混用）  

   | 字段 | 用途 | `storage_id` 来源 |
   |------|------|-------------------|
   | `storage_config` | 对象存储加速（JuiceFS） | `/storage/get_storage` |
   | `share_storage_config` | 共享存储 | `/storage/get_storage` |
   | `nas_storage_config` | **NAS 集群存储卷** | `suanli-nas-storage` 的 `/storage/nas/v1/list` |

   JuiceFS：`GET /storage/get_storage?storage_type=Juicefs&status=Activate`。  
   NAS：卷须 **Active**，地域与任务 `resources[].region_name` 一致；创建/扩容卷切到 `suanli-nas-storage`。  
   见 [api/object-storage.md](api/object-storage.md) · [api/job-create.md](api/job-create.md)。

3. **选任务类型**（默认 **Spot**，见下节）后提交创建。

**任务类型**（默认 Spot）：

| 模式 | `sub_type` | 额外必填 |
|------|------------|----------|
| **Spot（默认）** | `"Spot"` | `job_support.estimated_exec_sec`（预估运行秒数，1–86400，略长于实际运行、略短于 timeout） |
| OnDemand | 不传或 `null` | 无 |

**默认 Spot；仅以下情况改发 OnDemand**：
- 用户明确要求 OnDemand / 按需任务
- 资源列表无可用库存（`inventory <= 0` 或无匹配 region/device），或 Spot 创建失败且错误指向资源不可用

Spot 创建 body 示例：

```json
{
  "task_name": "<名称>",
  "sub_type": "Spot",
  "resources": [{ "mark": "<mark>", "resource": { /* 来自资源接口 */ }, "region_name": "<区域名>" }],
  "points": 1,
  "job_support": {
    "estimated_exec_sec": 3600,
    "timeout_sec": 7200,
    "parallelism": 1,
    "mod_param": { "default": { "backoff_limit": 3, "restart_policy": "OnFailure" } }
  },
  "services": [{
    "service_name": "container-01",
    "service_image": "<镜像>",
    "resource_weight": { "cpu_weight": 1, "mem_weight": 1, "gpu_weight": 1 },
    "start_script": { "command": ["<cmd>"], "args": ["..."] },
    "nas_storage_config": [{ "storage_id": 1001, "target_dir": "/mnt/nas" }]
  }]
}
```

OnDemand 时去掉 `sub_type`（或设 `null`），并移除 `estimated_exec_sec`。

- 共享卷：先声明 `share_disk_volumes` / `share_mem_volumes`，再在 `services` 配 `share_disk_config` / `share_mem_config`。
- NAS：`nas_storage_config[].storage_id` + `target_dir`（容器内挂载路径）；不挂 NAS 时省略该字段。
- 成功返回 `data.task_id`。

示例与可选字段：[api/job-create.md](api/job-create.md)

### 2. 查询状态

- **单任务**：`GET /task/job/detail?task_id=<id>`
- **列表**：`GET /task/job/search?status=Running&page=1&page_size=20`  
  可选 query：`status`（逗号分隔 Pending/Running/Paused/End）、`search_value`（任务名，URL 编码）、分页。

**状态字段**：

| 字段 | 值 | 含义 |
|------|-----|------|
| `status` | Pending / Running / Paused / End | 任务生命周期 |
| `job_status.status` | Pending / Manual / Running / Complete / Failed | Job 执行状态 |
| `schedule_status` | Scheduled / Queued | 仅 Spot |

轮询建议：间隔 ≥10s，Complete/Failed/Paused/End 或用户取消时停止。关注消耗时可一并展示 `billing_value`、`forecast_value`（换算见计费节）；有 NAS 时看 `services[].nas_storage_config`。

详情：[api/job-detail.md](api/job-detail.md) · 列表：[api/job-tasks.md](api/job-tasks.md)

### 3. 停止任务

```json
POST /task/job/stop
{ "task_id": <id> }
```

仅对 Running/Pending 有效。见 [api/job-stop.md](api/job-stop.md)

### 4. Job 任务队列

查询已有队列下的任务组。返回的 `task_dto.services[].nas_storage_config` 为 NAS 挂载配置。

- **列表**：`GET /job/queue/group/search?queue_id=<id>&page=1&page_size=10`
- **详情**：`GET /job/queue/group/detail?group_id=<id>`

见 [api/job-queue-list.md](api/job-queue-list.md) · [api/job-queue-detail.md](api/job-queue-detail.md)

### 5. 历史计费查询

必填 query：`range`（hour/day/week/month）、`start_time`、`end_time`（RFC3339，如 `2026-01-01T00:00:00+08:00`）。

- **按时间汇总**：`GET /billing/get_billing_record?range=day&start_time=...&end_time=...`  
  可选 `task_ids`（逗号分隔，空表示全部任务）、分页。  
  返回各时间段 `billing_coin`、`discount_coin`。

- **按任务汇总**：`GET /billing/get_task_billing_record?range=day&start_time=...&end_time=...`  
  可选分页。返回 `task_id`、`task_type`、`task_name`、`billing_coin`、`discount_coin`。

Job **实时消耗**优先看任务详情/列表的 `billing_value`、`forecast_value`；历史汇总用上述计费接口。展示金额时将 `billing_coin`、`discount_coin` 除以 `1,000,000` 转为元。

详情：[api/fee-time-query.md](api/fee-time-query.md) · [api/fee-task-query.md](api/fee-task-query.md)

## 对话执行约定

1. 缺 token 时先向用户索取，勿猜测。
2. **强烈建议用户先进行镜像预热**，提前把任务所需的镜像准备到目标计算资源附近，可以降低任务冷启动时间，如果使用者需要：请使用 suanli-preheat 这个 skill。
3. 创建前确认：镜像、资源规格（或让用户选 region/device）、启动命令、并行度/完成次数；挂 NAS 时确认卷 `storage_id`、挂载路径、卷为 Active 且地域匹配。**未指定任务类型时默认 Spot**，并向用户确认 `estimated_exec_sec`（或根据脚本/命令时长估算）。
4. 查资源时优先选 `inventory > 0` 的 region；全无库存再告知用户并改发 OnDemand（或换规格）。
5. 创建成功后回报 `task_id` 及任务类型（Spot/OnDemand）；Spot 任务关注 `schedule_status`（Scheduled/Queued）。询问是否轮询；轮询只展示 status、job_status、succeeded_pods/failed_pods。
6. 错误时输出 `code` + `message`；资源类错误尝试 OnDemand 降级前先征得用户同意（若用户未明确要求 OnDemand）。
7. 查历史账单时向用户确认时间范围与粒度（`range`）；`start_time`/`end_time` 用 RFC3339。
8. 加签失败时建议用户换简易模式密钥，或提供私钥。

## 脚本

```bash
export SUANLI_TOKEN="<密钥>"
# GET
./scripts/call.sh GET /task/job/search "status=Running&page=1&page_size=10"
./scripts/call.sh GET /job/queue/group/search "queue_id=1&page=1&page_size=10"
./scripts/call.sh GET /job/queue/group/detail "group_id=1"
./scripts/call.sh GET /billing/get_billing_record "range=day&start_time=2026-01-01T00:00:00%2B08:00&end_time=2026-01-31T23:59:59%2B08:00&task_ids=123"
./scripts/call.sh GET /billing/get_task_billing_record "range=day&start_time=2026-01-01T00:00:00%2B08:00&end_time=2026-01-31T23:59:59%2B08:00"
# POST
./scripts/call.sh POST /task/job/stop '{"task_id":123}'
./scripts/call.sh POST /task/job/create @payload.json   # @ 文件为 body
```
