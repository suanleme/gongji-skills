---
name: suanli-deployment
description: >-
  通过共绩算力(suanli.cn) Open API 管理弹性部署服务任务全生命周期：创建、查询、修改、暂停、恢复、删除；
  管理节点（列表/扩缩/删除/日志/事件）、查询历史计费与设备资源、对象存储与 NAS 挂载。
  在用户提到弹性部署、Deployment、NAS 挂载、suanli、openapi.suanli.cn、发部署任务、节点、
  暂停/恢复/删除部署、账单/费用时启用。
---

# 共绩算力弹性部署服务 API

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

平台按**秒**计费，内部计量单位为**点**（与任务节点数 `points` 不同）。

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
| `billing_points` | 任务详情 | 计费中节点数 |

向用户展示金额时，将 `billing_value`、`forecast_value`、`billing_coin`、`discount_coin` 除以 `1,000,000` 转为元；预估费用可用「卡时价 × 运行小时数」或「每秒点数 × 运行秒数 / 1,000,000」。

**历史账单**（按时间段或任务汇总，适用于弹性部署/云主机）：

| 字段 | 来源 | 说明 |
|------|------|------|
| `billing_coin` | 计费查询接口 | 时间段/任务总账（点） |
| `discount_coin` | 计费查询接口 | 优惠抵扣（点） |

## 端点速查

| 操作 | 方法 | 路径 |
|------|------|------|
| 创建任务 | POST | `/task/deployment/create` |
| 任务详情 | GET | `/task/deployment/detail?task_id=` |
| 任务列表 | GET | `/deployment/task/search` |
| 修改任务 | POST | `/deployment/task/update` |
| 暂停任务 | POST | `/deployment/task/pause` |
| 恢复任务 | POST | `/deployment/task/recover` |
| 删除任务 | POST | `/deployment/task/stop` |
| 节点列表 | GET | `/deployment/task/points?task_id=` |
| 修改节点数 | POST | `/deployment/task/change_points` |
| 删除节点 | POST | `/deployment/task/delete_pod` |
| 节点日志 | GET | `/deployment/task/point_log?task_id=&point_id=&service_id=` |
| 节点事件 | GET | `/deployment/task/pod_event?point_id=` |
| 时间维度计费 | GET | `/billing/get_billing_record` |
| 任务维度计费 | GET | `/billing/get_task_billing_record` |
| 设备资源 | GET | `/deployment/resource/search` |
| 对象存储 | GET | `/storage/get_storage` |

完整字段见 [`api/`](api/) 下对应文档；**仅在构造复杂 body 时读取**，勿整篇加载。

## 任务生命周期

```
创建 → Pending → Running
                    ↓ pause（暂停，释放资源）
                  Paused
                    ↓ recover（恢复）
                  Running
                    ↓ stop（删除，不可恢复）
                   End
```

| 操作 | 适用状态 | 说明 |
|------|----------|------|
| 暂停 `pause` | Running | 临时停止，**可恢复**；暂停后资源释放 |
| 恢复 `recover` | Paused | 恢复已暂停任务 |
| 删除 `stop` | Running / Pending / Paused | **永久删除，不可恢复**；删除前须向用户确认 |

**状态字段**（`status`）：

| 值 | 含义 |
|----|------|
| Pending | 等待中 |
| Running | 运行中 |
| Paused | 已暂停 |
| End | 已删除 |

列表查询必填 query：`type=Deployment`；`status` 逗号分隔，如 `Running,Pending,Paused`。

## 工作流

询问用户是否要先进行镜像预热，提前把任务所需的镜像准备到目标计算资源附近，可以降低任务冷启动时间，如果使用者需要：请使用 suanli-preheat 这个 skill。

### 1. 创建任务

1. **查资源**（取 `mark` 与 `resource`）  
   `GET /deployment/resource/search?task_type=Deployment&device_type=GpuDevice`  
   （CPU 任务用 `device_type=CpuDevice`）  
   从 `data.results[].regions[]` 取 `inventory > 0` 的条目：`mark.mark`、`mark.resource`、`region_name`。

2. **（可选）挂载存储**（三类字段勿混用）  

   | 字段 | 用途 | `storage_id` 来源 |
   |------|------|-------------------|
   | `storage_config` | 对象存储加速（JuiceFS） | `/storage/get_storage` |
   | `share_storage_config` | 共享存储 | `/storage/get_storage` |
   | `nas_storage_config` | **NAS 集群存储卷** | `suanli-nas-storage` 的 `/storage/nas/v1/list` |

   JuiceFS：`GET /storage/get_storage?storage_type=Juicefs&status=Activate`。  
   NAS：卷须 **Active**，地域与任务 `resources[].region_name` 一致；写入 `services[].nas_storage_config`：`[{ "storage_id": <卷ID>, "target_dir": "/mnt/nas" }]`。创建/扩容卷切到 `suanli-nas-storage`。  
   见 [api/object-storage.md](api/object-storage.md)。

3. 提交创建。

**必填 body 字段**：`task_name`、`resources`、`services`（含 `service_name`、`service_image`、`remote_ports`）。

创建 body 示例：

```json
{
  "task_name": "<名称>",
  "points": 1,
  "resources": [{
    "mark": "<mark>",
    "resource": { /* 来自资源接口 */ },
    "region_name": "<区域名>"
  }],
  "services": [{
    "service_name": "container-01",
    "service_image": "<镜像>",
    "remote_ports": [{ "service_port": 8080 }],
    "start_script_v2": { "command": null, "args": [] },
    "nas_storage_config": [{ "storage_id": 1001, "target_dir": "/mnt/nas" }]
  }]
}
```

- `points`：节点数量，默认 `1`。
- NAS：`nas_storage_config[].storage_id` + `target_dir`；不挂 NAS 时省略。
- 私有镜像：创建时传 `repository_username` / `repository_password`（仅写字段，创建后不可更新）。
- 弹性扩缩容：配置 `dynamic_pod_strategy`（含 `min_workers`、`max_workers`、`benchmark` 等）。
- 负载均衡：配置 `load_balance.type`（RoundRobin / LeastConnection 等）。
- 成功返回 `data.task_id`。

示例与可选字段：[api/task-create.md](api/task-create.md)

### 2. 查询状态

- **单任务**：`GET /task/deployment/detail?task_id=<id>`
- **列表**：`GET /deployment/task/search?type=Deployment&status=Running&page=1&page_size=20`  
  可选 query：`search_value`（任务名，URL 编码）、分页。

关注字段：`status`、`points`（节点数）、`runing_points`（运行中节点）、`billing_value` / `forecast_value`（消耗，见计费节）、`services[].remote_ports`（访问地址）、`services[].nas_storage_config`（NAS 挂载）。

轮询建议：间隔 ≥10s，Running/Paused/End 或用户取消时停止。

详情：[api/task-detail.md](api/task-detail.md) · 列表：[api/task-list.md](api/task-list.md)

### 3. 修改任务

```json
POST /deployment/task/update
{ /* 完整任务配置 */ }
```

**整体覆盖更新**，不支持局部修改。流程：

1. `GET /task/deployment/detail?task_id=<id>` 获取完整配置
2. 在返回的 `data` 上修改目标字段
3. 将完整配置 POST 到 `/deployment/task/update`

见 [api/task-edit.md](api/task-edit.md)

### 4. 暂停任务

```json
POST /deployment/task/pause
{ "task_id": <id> }
```

仅对 **Running** 有效；暂停后资源释放。见 [api/task-puase.md](api/task-puase.md)

### 5. 恢复任务

```json
POST /deployment/task/recover
{ "task_id": <id> }
```

仅对 **Paused** 有效。见 [api/task-recover.md](api/task-recover.md)

### 6. 删除任务

```json
POST /deployment/task/stop
{ "task_id": <id> }
```

**不可恢复**；删除前必须向用户确认。见 [api/task-stop.md](api/task-stop.md)

批量删除：先 `GET /deployment/task/search?type=Deployment&status=Running,Pending,Paused`，再逐个调用 `stop`。

### 7. 节点管理

- **列表**：`GET /deployment/task/points?task_id=<id>`  
  可选 `status`（逗号分隔 Running/Pending/Succeeded/Failed/End/Unknown）、分页。  
  关注 `point_id`、`status`、`billing_value`（点）、`containers`、`describe_dto.restart_count`。

- **扩缩节点数**：`POST /deployment/task/change_points`  
  `{ "task_id": <id>, "points": <目标节点数> }`

- **删除单个节点**（删除后平台会重新分配）：  
  `POST /deployment/task/delete_pod` · `{ "point_id": <id> }`  
  删除前向用户确认。

- **节点日志**：`GET /deployment/task/point_log?task_id=<id>&point_id=<id>&service_id=<id>`  
  `service_id` 来自任务详情 `services[].service_id`；返回 `data.logs` 文本。

- **节点事件**：`GET /deployment/task/pod_event?point_id=<id>`  
  返回 `data.events[]`（reason、message、type、event_time）。

详情：[api/node-list.md](api/node-list.md) · [api/node-num-edit.md](api/node-num-edit.md) · [api/node-delete.md](api/node-delete.md) · [api/node-log.md](api/node-log.md) · [api/node-event.md](api/node-event.md)

### 8. 历史计费查询

必填 query：`range`（hour/day/week/month）、`start_time`、`end_time`（RFC3339，如 `2026-01-01T00:00:00+08:00`）。

- **按时间汇总**：`GET /billing/get_billing_record?range=day&start_time=...&end_time=...`  
  可选 `task_ids`（逗号分隔，空表示全部任务）、分页。  
  返回各时间段 `billing_coin`、`discount_coin`。

- **按任务汇总**：`GET /billing/get_task_billing_record?range=day&start_time=...&end_time=...`  
  可选分页。返回 `task_id`、`task_type`（Deployment/Development）、`task_name`、`billing_coin`、`discount_coin`。

展示金额时将 `billing_coin`、`discount_coin` 除以 `1,000,000` 转为元。

详情：[api/fee-time-query.md](api/fee-time-query.md) · [api/fee-task-query.md](api/fee-task-query.md)

## 对话执行约定

1. 缺 token 时先向用户索取，勿猜测。
2. **强烈建议用户先进行镜像预热**，提前把任务所需的镜像准备到目标计算资源附近，可以降低任务冷启动时间，如果使用者需要：请使用 suanli-preheat 这个 skill。
3. 创建前确认：镜像、端口（`remote_ports`）、节点数、资源规格（或让用户选 region/device）、启动命令；挂 NAS 时确认卷 `storage_id`、挂载路径、卷为 Active 且地域匹配。
4. 查资源时优先选 `inventory > 0` 的 region。
5. 创建成功后回报 `task_id` 及 `remote_ports` 访问地址（若已分配）；询问是否轮询。
6. **暂停 vs 删除**：用户说「停止」时先确认是临时暂停（可恢复）还是永久删除；未说明时默认询问。
7. 删除/批量删除前必须二次确认；成功后回报已删除的 `task_id` 列表。
8. 修改任务前先拉详情，基于完整配置改动后回传，勿手工拼局部字段。
9. 查节点日志/事件前先拉任务详情取得 `service_id` 与 `point_id`；删除节点前须确认。
10. 查历史账单时向用户确认时间范围与粒度（`range`）；`start_time`/`end_time` 用 RFC3339。
11. 错误时输出 `code` + `message`；加签失败时建议换简易模式密钥或提供私钥。

## 脚本

```bash
export SUANLI_TOKEN="<密钥>"
# GET
./scripts/call.sh GET /deployment/task/search "type=Deployment&status=Running&page=1&page_size=10"
./scripts/call.sh GET /task/deployment/detail "task_id=123"
./scripts/call.sh GET /deployment/task/points "task_id=123&status=Running&page=1&page_size=10"
./scripts/call.sh GET /deployment/task/point_log "task_id=123&point_id=1&service_id=1"
./scripts/call.sh GET /deployment/task/pod_event "point_id=1"
./scripts/call.sh GET /billing/get_billing_record "range=day&start_time=2026-01-01T00:00:00%2B08:00&end_time=2026-01-31T23:59:59%2B08:00"
./scripts/call.sh GET /billing/get_task_billing_record "range=day&start_time=2026-01-01T00:00:00%2B08:00&end_time=2026-01-31T23:59:59%2B08:00"
# POST
./scripts/call.sh POST /task/deployment/create @payload.json
./scripts/call.sh POST /deployment/task/pause '{"task_id":123}'
./scripts/call.sh POST /deployment/task/recover '{"task_id":123}'
./scripts/call.sh POST /deployment/task/stop '{"task_id":123}'
./scripts/call.sh POST /deployment/task/update @payload.json
./scripts/call.sh POST /deployment/task/change_points '{"task_id":123,"points":2}'
./scripts/call.sh POST /deployment/task/delete_pod '{"point_id":1}'
```
