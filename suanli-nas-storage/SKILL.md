---
name: suanli-nas-storage
description: >-
  通过共绩算力(suanli.cn) Open API 管理集群存储（NAS）存储卷、SFTP 连接与对象存储 S3 互传：
  查询用量概览/字典/可创建配置、创建/扩容/改名/删除存储卷、获取/关闭 SFTP、
  创建/查询/重试/停止/删除互传任务、校验对象存储连接。
  在用户提到集群存储、NAS、存储卷、SFTP、S3互传、对象存储同步、suanli、openapi.suanli.cn 时启用。
---

# 共绩算力集群存储（NAS）API

本 skill 覆盖**集群存储卷**、**SFTP** 与 **S3 互传**。对象存储加速（JuiceFS）走 `suanli-job` / `suanli-deployment` 的 `/storage/get_storage`。把卷挂到 Job / 弹性部署时切到对应 skill，在 `services[].nas_storage_config` 传入 `{ "storage_id": <卷ID>, "target_dir": "<容器路径>" }`。

## 前置

向用户确认凭证（平台：右上角头像 → API 密钥）。模板见 [`.env.example`](.env.example)，复制为 `.env` 后填入，勿提交 `.env`。加签/加密算法、排错见 [`auth.md`](auth.md)，**优先跑脚本，勿手写签名或加密**。

| 变量 | 说明 |
|------|------|
| `SUANLI_TOKEN` | API 密钥。卷 CRUD、SFTP、互传列表/详情/停止/删除可用**简易模式** |
| `SUANLI_RSA_PRIVATE_KEY` | RSA 模式私钥（PEM 或 Base64），用于签名 |
| `SUANLI_PLATFORM_PUBLIC_KEY` | **平台公钥**（创建密钥时返回），仅加密用；不是用户上传的公钥 |
| `SUANLI_BASE_URL` | 默认 `https://openapi.suanli.cn` |

| 接口 | 模式 | 脚本 |
|------|------|------|
| 卷 CRUD、SFTP 获取/关闭、互传列表/详情/停止/删除 | 简易模式即可 | [`scripts/call.sh`](scripts/call.sh) |
| S3 创建 / 重试 / 校验连接 | **必须 RSA**（要加密） | [`scripts/call_encrypt.py`](scripts/call_encrypt.py) |

加密接口缺私钥或平台公钥时先向用户索取，**禁止**发明文 JSON。两种模式的 Token **不能混用**。脚本会加 `/api` 前缀，传入 path 时不要带 `/api`。

**响应**：`{ code, message, data }`；`code === "0000"` 成功，否则 `data` 为 null。

## 容量与价格

容量字段单位均为**字节**。对用户用 GiB，写入 API 再换成字节：

| 换算 | 公式 |
|------|------|
| GiB → 字节 | `total_size = GiB × 1,073,741,824` |
| 字节 → GiB | `GiB = bytes / 1,073,741,824` |

例：`1073741824` = **1 GiB**（与接口示例一致）。用户说「10GB」时按 **10 GiB** 写入，并口头确认。

`used_size === -1` 表示该存储**暂不支持查询已用容量**。对用户说明「已用容量暂不可查」，**不要**当成 0、不要转 GiB、不要据此算使用率或报错。

| 字段 | 来源 | 说明 |
|------|------|------|
| `used_size` | 用量概览 / 卷列表 | 已用容量（字节）；`-1` = 暂不支持查询 |
| `display_unit_price` | 配置 / 卷列表 | **展示单价**，元 / GB / 月；对用户优先用这个 |
| `unit_price` | 配置 / 卷列表 / 概览 `estimated_price` | 积分 / GB / 每 10 分钟 |
| `coin_sum_slice` | 用量概览 | 全部有效卷每 10 分钟预估消耗（接口单位：分） |
| `estimated_price` | 用量概览 | 有效卷 `unit_price` 算术平均；无卷时为 null |

向用户报价格时优先 `display_unit_price`（元/GB/月）× 容量 GiB；概览的 `coin_sum_slice` 原样带单位说明，勿与 Job 的「点 / 1,000,000 = 元」混用。

## 端点速查

### 存储卷

| 操作 | 方法 | 路径 | 加密 |
|------|------|------|------|
| 用量概览 | GET | `/storage/nas/v1/summary` | 否 |
| 字典（地域/规格） | GET | `/storage/nas/v1/dictionaries` | 否 |
| 可创建配置 | GET | `/storage/nas/v1/pre-create` | 否 |
| 卷列表 | GET | `/storage/nas/v1/list` | 否 |
| 创建卷 | POST | `/storage/nas/v1/create` | 否 |
| 扩容 | POST | `/storage/nas/v1/expand` | 否 |
| 删除 | POST | `/storage/nas/v1/delete` | 否 |
| 改名 | POST | `/storage/nas/v1/rename` | 否 |

### SFTP

| 操作 | 方法 | 路径 | 加密 |
|------|------|------|------|
| 获取连接 | POST | `/storage/nas/v1/sftp/obtain` | 否 |
| 关闭连接 | POST | `/storage/nas/v1/sftp/destroy` | 否 |

### S3 互传

| 操作 | 方法 | 路径 | 加密 |
|------|------|------|------|
| 任务列表 | GET | `/storage/nas/v1/s3/list` | 否 |
| 任务详情 | GET | `/storage/nas/v1/s3/detail?id=` | 否 |
| 创建任务 | POST | `/storage/nas/v1/encrypt/s3/create` | **是** |
| 重试任务 | POST | `/storage/nas/v1/encrypt/s3/retry` | **是** |
| 删除任务 | POST | `/storage/nas/v1/s3/delete` | 否 |
| 停止任务 | POST | `/storage/nas/v1/s3/stop` | 否 |
| 校验连接 | POST | `/storage/nas/v1/encrypt/s3/check` | **是** |

完整字段见 [`api/`](api/)；**仅在构造复杂 body 时读取**，勿整篇加载。

## 状态枚举

**卷状态**（`status`）：

| 值 | 含义 |
|----|------|
| Creating | 创建中 |
| Active | 可用（可扩容、可开 SFTP、可建互传、可挂载） |
| Expanding | 扩容中 |
| Deleting | 删除中 |
| Deleted | 已删除（列表 `statuses` 中的 Deleted 会被忽略） |
| Exception | 异常（可删除） |

```
创建 → Creating → Active
                    ↓ expand
                 Expanding → Active
                    ↓ delete
                 Deleting → Deleted
Exception → delete → Deleted
```

**互传任务状态**：

| 值 | 含义 |
|----|------|
| Queuing | 排队中 |
| Pending | 处理中 |
| Running | 运行中（可停止） |
| Stopped | 已停止 |
| Completed | 已完成 |
| Error / Exception | 失败 / 异常（可重试） |
| Deleted | 已删除 |

**SFTP 会话状态**：

| 值 | 含义 |
|----|------|
| Pending | 开通中；连接信息尚未就绪，稍后再次 `obtain` |
| Running | 可连接；此时才有用户名/密码/地址 |
| Exception | 异常；看 `error_code` / `error_message` |

**传输方向** `direction`：`1` 对象存储 → 集群存储；`2` 集群存储 → 对象存储。  
**同名策略** `overwrite_policy`：`1` 强制覆盖；`2` 跳过重名（**默认**）；`3` 按内容哈希比较。

## 轮询约定

异步操作**成功受理后**先问用户要不要轮询，未同意不要自己循环。已是终态（如 SFTP 第一次就是 Running）则直接展示，不必问。

用户同意后：

1. 间隔固定 **10 秒**，不要更短。
2. **每个 10 秒结束必须推送当前情况**（状态 + 下表字段），不要闷到终态才说话。
3. 到达终态、或用户说停，立刻停止。

| 操作 | 查询 | 每次展示 | 停止轮询 |
|------|------|----------|----------|
| 创建卷 | `GET /storage/nas/v1/list?storage_ids=<id>` | `status`、`name`、`error_message` | Active / Exception |
| 扩容 | 同上 | `status`、`total_size`（转 GiB）、`used_size`（`-1` 见容量节） | Active / Exception |
| 删卷（Deleting） | 同上 | `status`；列表没有该卷视为已删完 | 列表无此卷 |
| 获取 SFTP（Pending） | 再 `POST .../sftp/obtain` | `status`；Running 再给连接信息 | Running / Exception |
| 创建/重试互传 | `GET .../s3/detail?id=` | `status`、已传/总文件、已传/总字节（转 GiB）、`bps`、`remaining_seconds` | Completed / Stopped / Error / Exception |

改名、关 SFTP、停/删互传、校验连接不轮询。

## 工作流

### 1. 查询用量与字典

- **概览**：`GET /storage/nas/v1/summary`  
  仅统计 Creating / Active / Expanding。关注 `volume_count`、`total_size`、`used_size`（`-1` 见上节，否则转 GiB）、`estimated_price`、`coin_sum_slice`。
- **字典**：`GET /storage/nas/v1/dictionaries`  
  `regions[].tag/name`、`storage_classes[].storage_class/storage_class_name`。

见 [api/nas-summary.md](api/nas-summary.md) · [api/nas-dictionaries.md](api/nas-dictionaries.md)

### 2. 创建存储卷

1. **查可创建配置**  
   `GET /storage/nas/v1/pre-create`  
   从 `data.configs[]` 取 `status === Available` 的项：`id`（即创建时的 `nas_config_id`）、`region`、`storage_class_name`、`display_unit_price`、剩余容量（`total_capacity - allocated_capacity`）。  
   `Unavailable` 告知用户暂不可选，勿用来创建。

2. 向用户确认：卷名（1–32 字符）、配置、容量（GiB）。

3. 提交创建：

```json
POST /storage/nas/v1/create
{ "name": "my-volume", "nas_config_id": 10, "total_size": 1073741824 }
```

- `total_size` 必须 **> 0**，单位字节。
- 成功返回 `data.storage_id`，`status` 为 **Creating**。开通完成后变为 Active。
- 按 [轮询约定](#轮询约定) 询问是否跟踪到 Active。

见 [api/nas-pre-create.md](api/nas-pre-create.md) · [api/nas-create.md](api/nas-create.md)

### 3. 查询存储卷

```
GET /storage/nas/v1/list?page=1&page_size=10
```

可选 query（逗号分隔）：`regions`、`storage_class`、`statuses`（Creating/Active/Expanding/Deleting/Exception；Deleted 会被忽略）、`storage_ids`。`page`≤0 按 1；`page_size`≤0 按 10，最大 100。

关注：`storage_id`、`name`、`status`、`total_size`/`used_size`（`used_size === -1` 时说明暂不支持查询已用容量）、`display_unit_price`、`instance_count`、`instances[]`（挂载的计算实例）、`claim_name`、`error_message`。

见 [api/nas-list.md](api/nas-list.md)

### 4. 扩容

仅 **Active** 可扩容；目标容量必须 **大于当前** `total_size`（只扩不缩）。

```json
POST /storage/nas/v1/expand
{ "id": 1001, "total_size": 2147483648 }
```

受理后 `status` 为 Expanding。向用户确认目标 GiB 后再提交。按 [轮询约定](#轮询约定) 询问是否跟踪到 Active。见 [api/nas-expand.md](api/nas-expand.md)

### 5. 改名

```json
POST /storage/nas/v1/rename
{ "id": 1001, "name": "renamed-volume" }
```

新名称同样 1–32 字符。成功返回当前卷 `status`。见 [api/nas-rename.md](api/nas-rename.md)

### 6. 删除存储卷

**不可恢复**。第一次「删这个卷」只用来锁定对象，**禁止立刻调删除接口**。

二次确认流程：

1. 拉卷列表，并查该卷的互传任务。核对 `storage_id`、名称、状态、`instance_count` / `instances[]`、进行中互传。
2. 向用户列出：卷 ID 与名称、容量、挂载实例、进行中互传、数据将一并清除且不可恢复。对象对不上就停住再问。
3. 等用户明确回复 **「确认删除」** 或 **「确认删 卷名或 ID」**。  
   「删吧」「嗯」「继续」「你看着办」不够，再问一次。
4. 只有这一步之后才 `POST /storage/nas/v1/delete`，默认 `force: false`。

```json
POST /storage/nas/v1/delete
{ "id": 1001, "force": false }
```

| 规则 | 说明 |
|------|------|
| Active | 受理后 `status` 为 Deleting；按 [轮询约定](#轮询约定) 询问是否跟踪到删除完成 |
| Exception | 删除后直接 Deleted，不必轮询 |
| 进行中互传 / 仍有挂载 | 默认不删。只有用户明确同意 `force: true` 才跳过校验；这是**另一次**确认，不能和上面的「确认删除」合并 |
| `reason` | 可选删除原因 |

见 [api/nas-delete.md](api/nas-delete.md)

### 7. SFTP

卷须已存在（建议 **Active**）。两个接口均为 POST，body 仅 `storage_id`（必须 > 0）。无需加密，用 `call.sh`。

#### 7a. 获取连接

可重复调用：已开通则返回当前会话，开通中则返回 Pending。

```json
POST /storage/nas/v1/sftp/obtain
{ "storage_id": 1001 }
```

| `data.status` | 处理 |
|---------------|------|
| Running | 展示 `sftp_url`（`host:port`）、`username`、`password`、`web_url`、`webdav_url`、`expire_at`。用户需要密码才能连，**可以展示**，不要写入无关日志 |
| Pending | 告知开通中；按 [轮询约定](#轮询约定) 询问是否跟踪到 Running |
| Exception | 输出 `error_code` + `error_message` |

`username` / `password` / 三类 URL / `expire_at` **仅 Running 时有值**，其它状态为 null，勿当成失败字段缺失。

#### 7b. 关闭连接

关闭会话并**清除凭证**；之后再 `obtain` 会生成**新**凭证。关闭前须向用户确认。

```json
POST /storage/nas/v1/sftp/destroy
{ "storage_id": 1001 }
```

成功时 `data` 为 null。见 [api/sftp-obtain.md](api/sftp-obtain.md) · [api/sftp-destroy.md](api/sftp-destroy.md)

### 8. S3 互传

关联卷必须为 **Active**。AccessKey / SecretKey **仅用于当次请求，平台不保存**；对话中不要回显完整密钥。

#### 8a. 校验连接（建议创建前先做）

请求体字段名与创建接口不同（`ak`/`sk`/`supplier`/`endpoint`/`prefix`）：

```json
POST /storage/nas/v1/encrypt/s3/check
{
  "supplier": "tencent",
  "endpoint": "cos.ap-guangzhou.myqcloud.com",
  "ak": "<AccessKey>",
  "sk": "<SecretKey>",
  "bucket": "my-bucket",
  "prefix": "/data/"
}
```

HTTP `code === "0000"` 只表示接口成功，**以 `data.pass` 判断连接是否通过**。`supplier` 如 `tencent`、`aws`、`aliyun`、`minio`。

#### 8b. 创建互传

向用户确认：卷、方向（S3→NAS / NAS→S3）、厂商与 Endpoint、Bucket、前缀、NAS 路径、同名策略（默认跳过重名）。

```json
POST /storage/nas/v1/encrypt/s3/create
{
  "storage_id": 1001,
  "name": "prod-backup-sync",
  "direction": 1,
  "s3_supplier": "tencent",
  "s3_endpoint": "cos.ap-guangzhou.myqcloud.com",
  "s3_access_key": "<AccessKey>",
  "s3_secret_key": "<SecretKey>",
  "s3_bucket": "company-backups",
  "s3_prefix": "nas-sync/",
  "nas_path": "/data/incoming",
  "overwrite_policy": 2,
  "ignore_patterns": [".log", ".tmp"]
}
```

- 必填：`storage_id`、`direction`、`s3_supplier`、`s3_endpoint`、`s3_access_key`、`s3_secret_key`、`s3_bucket`
- `name` / `s3_prefix` / `nas_path` 可空（名称系统生成；路径默认根）
- `ignore_patterns`：按文件名后缀过滤；空则不过滤
- 成功返回 `data.id`，`status` 为 **Queuing**。按 [轮询约定](#轮询约定) 询问是否跟踪进度。

#### 8c. 查询进度

- 列表：`GET /storage/nas/v1/s3/list?storage_id=1001&page=1&page_size=10`  
  可选 `statuses`（非法值返回 `S002`）。`count` 受筛选影响；`status_counts` 为各状态数量（不含 Deleted，不受 `statuses` 影响）。应答**不含** AccessKey/SecretKey。
- 详情：`GET /storage/nas/v1/s3/detail?id=501`（`id` 必须 > 0）

展示：`status`、`ready_files`/`total_files`、`transferred_bytes`/`total_bytes`（转 GiB）、`bps`（字节/秒；`speed` 已废弃）、`remaining_seconds`、`error_code`/`error_message`。`total_files`/`total_bytes` 尚未统计完时可能为 0。

持续跟踪时按 [轮询约定](#轮询约定)：**先问要不要轮询**；同意后每 10 秒推送上述字段一次。

#### 8d. 停止 / 删除 / 重试

- **停止**：仅 **Running**。`POST /storage/nas/v1/s3/stop` · `{ "id": 501 }` → Stopped
- **删除**：`POST /storage/nas/v1/s3/delete` · `{ "id": 501 }` → Deleted；已删除再调仍成功。删除前确认。
- **重试**：仅 **Exception / Error**。原任务标 Deleted，**新建**任务；应答 `id` 为新任务 ID，`status` 为 Queuing。请求体在创建字段基础上多必填 `id`（原任务 ID）；`storage_id` 可换但必须 Active。同样要加密，且须再次提供 AccessKey/SecretKey。按 [轮询约定](#轮询约定) 询问是否跟踪新任务。

见 [api/s3-list.md](api/s3-list.md) · [api/s3-detail.md](api/s3-detail.md) · [api/s3-check.md](api/s3-check.md) · [api/s3-create.md](api/s3-create.md) · [api/s3-retry.md](api/s3-retry.md) · [api/s3-stop.md](api/s3-stop.md) · [api/s3-delete.md](api/s3-delete.md)

## 对话执行约定

1. 缺 token 时先向用户索取，勿猜测。S3 创建/重试/校验还要 RSA 私钥与**平台公钥**。
2. 创建卷前先拉 `pre-create`，只选 `Available`；确认名称、配置、容量（GiB → 字节）。
3. 扩容只放大、不缩小。**删除 NAS 卷必须二次确认**：先核对对象并说明不可恢复，等用户回复「确认删除」或「确认删 卷名或 ID」后再调接口；「删吧 / 嗯 / 继续」不够。有挂载或进行中互传时默认不删；`force: true` 须再单独征得同意。删除互传记录也要确认，但不能当成删卷。
4. 创建卷 / 扩容 / 删卷（Deleting）/ SFTP 开通中 / 创建或重试互传：先回报受理结果，再**询问是否轮询**。同意后每 10 秒推送一次当前情况，规则见 [轮询约定](#轮询约定)。未同意不要自己循环。
5. 互传进度展示文件数、字节、`bps`，不要回显 S3 密钥。SFTP 仅 Running 时展示地址和密码。
6. 校验连接看 `data.pass`，不要只看 HTTP/`code`。
7. 用户说「停止」时确认对象：停互传、关 SFTP，还是删存储卷。关 SFTP 前说明凭证会作废。
8. 错误时输出 `code` + `message`。加签/加密失败先读 [`auth.md`](auth.md) 排错表；非加密接口可建议换简易模式 Token。
9. 容量一律 GiB 展示，价格优先 `display_unit_price`。`used_size === -1` 时说「已用容量暂不可查」，勿当 0 或负容量。
10. 关闭 SFTP 会作废当前凭证，须确认。轮询中用户说停就立刻停。

## 脚本

```bash
export SUANLI_TOKEN="<密钥>"

# 概览 / 字典 / 可创建配置
./scripts/call.sh GET /storage/nas/v1/summary
./scripts/call.sh GET /storage/nas/v1/dictionaries
./scripts/call.sh GET /storage/nas/v1/pre-create

# 卷列表 / 创建 / 扩容 / 改名 / 删除
./scripts/call.sh GET /storage/nas/v1/list "page=1&page_size=10&statuses=Active"
./scripts/call.sh POST /storage/nas/v1/create '{"name":"my-volume","nas_config_id":10,"total_size":1073741824}'
./scripts/call.sh POST /storage/nas/v1/expand '{"id":1001,"total_size":2147483648}'
./scripts/call.sh POST /storage/nas/v1/rename '{"id":1001,"name":"renamed-volume"}'
./scripts/call.sh POST /storage/nas/v1/delete '{"id":1001,"force":false}'

# SFTP（无需加密）
./scripts/call.sh POST /storage/nas/v1/sftp/obtain '{"storage_id":1001}'
./scripts/call.sh POST /storage/nas/v1/sftp/destroy '{"storage_id":1001}'

# 互传列表 / 详情 / 停止 / 删除（无需加密）
./scripts/call.sh GET /storage/nas/v1/s3/list "storage_id=1001&page=1&page_size=10"
./scripts/call.sh GET /storage/nas/v1/s3/detail "id=501"
./scripts/call.sh POST /storage/nas/v1/s3/stop '{"id":501}'
./scripts/call.sh POST /storage/nas/v1/s3/delete '{"id":501}'

# 校验 / 创建 / 重试（必须加密 + RSA 加签）
export SUANLI_RSA_PRIVATE_KEY="<私钥 PEM 或 Base64>"
export SUANLI_PLATFORM_PUBLIC_KEY="<平台公钥 PEM>"
python3 scripts/call_encrypt.py POST /storage/nas/v1/encrypt/s3/check @check.json
python3 scripts/call_encrypt.py POST /storage/nas/v1/encrypt/s3/create @payload.json
python3 scripts/call_encrypt.py POST /storage/nas/v1/encrypt/s3/retry @retry.json
```
