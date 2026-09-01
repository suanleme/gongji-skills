# 共绩算力 镜像预热 Skill

Agent Skill 入口：[SKILL.md](./SKILL.md)

通过共绩算力 Open API 创建、查询、更新、停止 镜像预热任务。

## 安装

```bash
npx skills add <owner>/<repo> --skill suanli-image-preheat
```

装全部、全局（`-g`）、列出仓库内 skill（`--list`）见仓库根 [README.md](../README.md)。Cursor 项目级默认 `.agents/skills/suanli-image-preheat/`，全局 `~/.cursor/skills/suanli-image-preheat/`。

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

### 创建 镜像预热任务 时建议提供

| 参数 | 说明 | 默认 |
|------|------|------|
| `task_name` | 任务名称 | 自动生成 |
| `points` | 期望节点数 | 无 |
| 资源规格 | GPU 型号、区域等；不指定时自动选有库存规格 | 自动 |

预热方式有两种，一种是**集群预热**，一种是**节点预热**（见 [SKILL.md](./SKILL.md)）。

### 可选

| 参数 | 说明 |
|------|------|
| 轮询 | 创建后是否持续查询预热情况，直到集群预热成功或有节点成功预热 |

### 停止 / 查询

| 操作 | 需要的信息 |
|------|------------|
| 停止单个任务 | `task_id` |
| 停止全部任务 | 说明「停止所有任务」即可 |
| 查询状态 | `task_id`，或按任务名 / 状态筛选 |

## 快速验证

```bash
export SUANLI_TOKEN="<密钥>"
./scripts/call.sh GET /api/task/image_preheat/search "status=Running&page=1&page_size=10"
```

## 文档

- 工作流与约定：[SKILL.md](./SKILL.md)
- API 字段详情：[api/](./api/)
