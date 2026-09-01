# 共绩算力 Job 批处理 Skill

Agent Skill 入口：[SKILL.md](./SKILL.md)

通过共绩算力 Open API 创建、查询、停止 Job 批处理任务。

## 安装

```bash
npx skills add <owner>/<repo> --skill suanli-job
```

装全部、全局（`-g`）、列出仓库内 skill（`--list`）见仓库根 [README.md](../README.md)。Cursor 项目级默认 `.agents/skills/suanli-job/`，全局 `~/.cursor/skills/suanli-job/`。

## 凭证配置

复制本目录 [`.env.example`](.env.example) 为 `.env`（勿提交）：

```bash
cp .env.example .env
```

填入 `SUANLI_TOKEN`。可选 `SUANLI_BASE_URL`、`SUANLI_RSA_PRIVATE_KEY`（非简易模式）。

API 密钥获取路径：共绩算力平台 → 右上角头像 → **API 密钥**（推荐使用**简易模式**密钥，无需加签）。

使用前在 skill 目录加载环境变量：

```bash
set -a && source .env && set +a
```

## 使用前请提供的信息

与 Agent 对话时，请尽量明确以下参数；未说明时 Agent 会按默认值处理或主动询问。

### 必提供

| 参数 | 说明 |
|------|------|
| `SUANLI_TOKEN` | API 密钥（见上方凭证配置） |
| `service_image` | 容器镜像，如 `harbor.suanleme.cn/bala/job-task-demonstration:v1` |

### 创建 Job 时建议提供

| 参数 | 说明 | 默认 |
|------|------|------|
| `task_name` | 任务名称 | 自动生成 |
| `sub_type` | 任务类型：`Spot` / `OnDemand` | `Spot` |
| `estimated_exec_sec` | Spot 预估运行秒数（1–86400） | 按场景估算 |
| `timeout_sec` | 任务超时秒数 | `7200` |
| `points` | 任务总数（完成次数） | `1` |
| `parallelism` | 并发 Pod 数 | `1` |
| 资源规格 | GPU 型号、区域等；不指定时自动选有库存规格 | 自动 |
| `start_script` | 启动命令 `{ "command": [...], "args": [...] }` | 使用镜像默认入口 |

### 队列 / 批量任务

需要「任务总数 N、并发 M」时，请直接说明，例如：

> 任务总数 100，并发 10 个

对应 API 字段：`points=100`，`job_support.parallelism=10`；多节点并行建议使用**索引模式**（见 [SKILL.md](./SKILL.md)）。

查询 **Job 任务队列** 任务组时，请提供 `queue_id` 或 `group_id`；详情里的 NAS 挂载见 `task_dto.services[].nas_storage_config`。

### 可选

| 参数 | 说明 |
|------|------|
| 对象存储 / 共享卷 / NAS | 需挂载 S3、共享盘或 NAS 时说明路径；NAS 用卷 ID + 容器挂载路径 |
| 环境变量 `env` | 容器内所需环境变量 |
| 轮询 | 创建后是否持续查询状态直至完成 |

### 停止 / 查询

| 操作 | 需要的信息 |
|------|------------|
| 停止单个任务 | `task_id` |
| 停止全部任务 | 说明「停止所有任务」即可 |
| 查询状态 | `task_id`，或按任务名 / 状态筛选 |
| 历史计费 | 时间范围（RFC3339）、粒度 `range`（hour/day/week/month）；可选 `task_ids` |

## 计费说明

平台**按秒计费**，内部单位为**点**（`1 元 = 1,000,000 点`）：

- **每秒点数** = 卡时价(元/小时) × 1,000,000 / 3600  
  例：1.98 元/小时 → 约 550 点/秒
- **用户消耗(元)** = 累计点数 / 1,000,000
- **出账周期**：每 5 分钟出账；`billing_value` 为已出账消耗，`forecast_value` 为当前周期实时消耗（均为点，展示时除以 1,000,000）
- **历史账单**：`/billing/get_billing_record`（按时间）、`/billing/get_task_billing_record`（按任务）；返回 `billing_coin`、`discount_coin`（点）

详见 [SKILL.md § 计费与价格](./SKILL.md#计费与价格)。

## 快速验证

```bash
export SUANLI_TOKEN="<密钥>"
./scripts/call.sh GET /task/job/search "status=Running&page=1&page_size=10"
```

## 文档

- 工作流与约定：[SKILL.md](./SKILL.md)
- API 字段详情：[api/](./api/)
