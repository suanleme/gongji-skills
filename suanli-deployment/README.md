# 共绩算力弹性部署服务 Skill

Agent Skill 入口：[SKILL.md](./SKILL.md)

通过共绩算力 Open API 管理弹性部署服务（Deployment）任务全生命周期：创建、查询、修改、暂停、恢复、删除。

## 安装

```bash
npx skills add <owner>/<repo> --skill suanli-deployment
```

装全部、全局（`-g`）、列出仓库内 skill（`--list`）见仓库根 [README.md](../README.md)。Cursor 项目级默认 `.agents/skills/suanli-deployment/`，全局 `~/.cursor/skills/suanli-deployment/`。

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
| `service_image` | 容器镜像 |
| `remote_ports` | 对外暴露端口，如 `8080` |

### 创建部署时建议提供

| 参数 | 说明 | 默认 |
|------|------|------|
| `task_name` | 任务名称 | 自动生成 |
| `points` | 节点数量 | `1` |
| 资源规格 | GPU/CPU 型号、区域等；不指定时自动选有库存规格 | 自动 |
| `start_script_v2` | 启动命令 `{ "command": "...", "args": [...] }` | 使用镜像默认入口 |
| `load_balance.type` | 负载均衡策略 | 按需配置 |
| `dynamic_pod_strategy` | 弹性扩缩容（最小/最大节点、队列策略等） | 按需配置 |

### 生命周期操作

| 操作 | 需要的信息 | 说明 |
|------|------------|------|
| 查询详情 | `task_id` | — |
| 查询列表 | 可选：状态、任务名 | 状态：`Running` / `Pending` / `Paused` / `End` |
| 修改配置 | `task_id` + 变更说明 | Agent 会先拉详情再整体回传 |
| **暂停** | `task_id` | 临时停止，**可恢复**，释放资源 |
| **恢复** | `task_id` | 恢复已暂停任务 |
| **删除** | `task_id` | **永久删除，不可恢复**；Agent 会二次确认 |

> 说「停止任务」时，请说明是**暂停**（可恢复）还是**删除**（不可恢复）。

### 节点操作

| 操作 | 需要的信息 | 说明 |
|------|------------|------|
| 节点列表 | `task_id` | 可选按 `status` 筛选 |
| 扩缩节点 | `task_id` + 目标节点数 | 调用 `change_points` |
| 删除节点 | `point_id` | 删除后平台会重新分配；Agent 会确认 |
| 节点日志 | `task_id` + `point_id` + `service_id` | `service_id` 来自任务详情 |
| 节点事件 | `point_id` | — |

### 历史计费

| 操作 | 需要的信息 |
|------|------------|
| 按时间汇总 | `range`、`start_time`、`end_time`（RFC3339）；可选 `task_ids` |
| 按任务汇总 | `range`、`start_time`、`end_time`（RFC3339） |

### 可选

| 参数 | 说明 |
|------|------|
| 私有镜像凭证 | `repository_username` / `repository_password`（仅创建时有效） |
| 对象存储 / 共享卷 / NAS | 需挂载 S3、共享盘或 NAS 时说明路径；NAS 用卷 ID + 容器挂载路径 |
| 健康检查 | `health_checks` 配置 |
| 环境变量 | `services[].env` |
| 轮询 | 创建后是否持续查询状态 |

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
./scripts/call.sh GET /deployment/task/search "type=Deployment&status=Running&page=1&page_size=10"
```

## 文档

- 工作流与约定：[SKILL.md](./SKILL.md)
- API 字段详情：[api/](./api/)
