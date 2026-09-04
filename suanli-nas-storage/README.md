# 共绩算力集群存储（NAS）Skill

Agent Skill 入口：[SKILL.md](./SKILL.md)

通过共绩算力 Open API 管理集群存储卷（创建 / 扩容 / 改名 / 删除 / 查询）、SFTP 连接，以及对象存储 S3 互传任务。

## 安装

```bash
npx skills add suanleme/gongji-skills --skill suanli-nas-storage
```

装全部、全局（`-g`）、列出仓库内 skill（`--list`）见仓库根 [README.md](../README.md)。Cursor 项目级默认 `.agents/skills/suanli-nas-storage/`，全局 `~/.cursor/skills/suanli-nas-storage/`。

## 凭证配置

复制本目录 [`.env.example`](.env.example) 为 `.env`（勿提交）：

```bash
cp .env.example .env
```

填入 `SUANLI_TOKEN`。可选 `SUANLI_BASE_URL`、`SUANLI_RSA_PRIVATE_KEY`。S3 创建 / 重试 / 校验还需 `SUANLI_PLATFORM_PUBLIC_KEY`。

API 密钥获取路径：共绩算力平台 → 右上角头像 → **API 密钥**。

- 存储卷 CRUD、SFTP 获取/关闭、互传列表/详情/停止/删除：可用**简易模式**密钥（无需加签）。
- S3 **创建 / 重试 / 校验连接**：必须使用 **RSA 加验签模式**，并配置创建密钥时平台返回的公钥（`SUANLI_PLATFORM_PUBLIC_KEY`）。请求体含 AccessKey/SecretKey，须加密后以 `text/plain` 提交。

使用前在 skill 目录加载环境变量：

```bash
set -a && source .env && set +a
```

加密脚本额外依赖：

```bash
pip install cryptography requests
```

## 使用前请提供的信息

与 Agent 对话时，请尽量明确以下参数；未说明时 Agent 会按默认值处理或主动询问。

### 必提供

| 参数 | 说明 |
|------|------|
| `SUANLI_TOKEN` | API 密钥（见上方凭证配置） |

### 创建存储卷时建议提供

| 参数 | 说明 | 默认 |
|------|------|------|
| `name` | 卷名称（1–32 字符） | 询问用户 |
| 地域 / 规格 | 对应 `pre-create` 里的配置 | 有库存的 Available 配置 |
| 容量 | GiB；写入 API 为字节（× 1,073,741,824） | 询问用户 |

### 创建 S3 互传时建议提供

| 参数 | 说明 | 默认 |
|------|------|------|
| `storage_id` | 已 Active 的卷 ID | 询问或从列表选取 |
| `direction` | 1：S3→NAS；2：NAS→S3 | 询问用户 |
| `s3_supplier` / `s3_endpoint` / `s3_bucket` | 对象存储连接信息 | 无 |
| AccessKey / SecretKey | 仅当次请求使用，平台不保存 | 无 |
| `overwrite_policy` | 1 覆盖 / 2 跳过重名 / 3 哈希比较 | `2` |
| `s3_prefix` / `nas_path` | 两侧路径 | 根路径 |

### 扩容 / 删除 / 改名

| 操作 | 需要的信息 |
|------|------------|
| 扩容 | `storage_id`、目标容量（须大于当前） |
| 改名 | `storage_id`、新名称 |
| 删除卷 | `storage_id`；**不可恢复，Agent 会二次确认后才删除**。有进行中互传时是否 `force` 也要再确认 |
| 停止/删除/重试互传 | 任务 `id`；重试还需再次提供 S3 密钥 |
| 获取 / 关闭 SFTP | 卷 `storage_id` |

### 轮询

创建卷、扩容、删卷、SFTP 开通中、创建/重试互传成功后，Agent 会先问要不要跟踪进度。同意后每 **10 秒**回报一次当前状态，说停即停。

## 计费说明

集群存储按容量计费，对用户优先展示 `display_unit_price`（**元 / GB / 月**）。

- 容量字段为字节，展示时除以 `1,073,741,824` 转为 GiB
- `used_size === -1` 表示暂不支持查询已用容量，不要按字节换算
- `unit_price` 为积分 / GB / 每 10 分钟；用量概览 `coin_sum_slice` 为全部有效卷每 10 分钟预估消耗
- 勿与 Job / 弹性部署的「点 / 1,000,000 = 元」混用

详见 [SKILL.md § 容量与价格](./SKILL.md#容量与价格)。

## 快速验证

```bash
export SUANLI_TOKEN="<密钥>"
./scripts/call.sh GET /storage/nas/v1/summary
./scripts/call.sh GET /storage/nas/v1/list "page=1&page_size=10"
```

## 文档

- 工作流与约定：[SKILL.md](./SKILL.md)
- 加签与加密：[auth.md](./auth.md)（官方规范的精简版；完整原文见 [RSA 模式使用指南](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/)）
- API 字段详情：[api/](./api/)
