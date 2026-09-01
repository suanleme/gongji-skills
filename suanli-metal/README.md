# 共绩算力 裸金属 Skill

Agent Skill 入口：[SKILL.md](./SKILL.md)

通过共绩算力 Open API 创建、查询裸金属任务。

## 安装

```bash
npx skills add <owner>/<repo> --skill suanli-metal
```

装全部、全局（`-g`）、列出仓库内 skill（`--list`）见仓库根 [README.md](../README.md)。Cursor 项目级默认 `.agents/skills/suanli-metal/`，全局 `~/.cursor/skills/suanli-metal/`。

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

### 创建 裸金属 订单时建议提供

| 参数 | 说明 | 默认 |
|------|------|------|
| `billing_type` | 计费方式（小时包/天包/周包/月包） | 小时包 |
| `buy_count` | 时长包数量（买多少时长） | 1 |

## 计费说明

有四种计费方式：

1. Hour-小时时长包
2. Day-24小时时长包
3. Week-7天时长包
4. Month-30天时长包

平台**按秒计费**，内部单位为**点**（`1 元 = 1,000,000 点`）：

- **用户消耗(元)** = 累计点数 / 1,000,000
- **出账周期**：每 5 分钟出账；`billing_value` 为已出账消耗，`forecast_value` 为当前周期实时消耗（均为点，展示时除以 1,000,000）
- **历史账单**：`/billing/get_billing_record`（按时间）、`/billing/get_task_billing_record`（按任务）；返回 `billing_coin`、`discount_coin`（点）

详见 [SKILL.md § 计费与价格](./SKILL.md#计费与价格)。

## 文档

- 工作流与约定：[SKILL.md](./SKILL.md)
- API 字段详情：[api/](./api/)
