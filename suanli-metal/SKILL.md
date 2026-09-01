---
name: suanli-metal
description: >-
  通过共绩算力(suanli.cn) Open API 创建/查询裸金属机器、查询订单和计费。在用户提到算力平台 裸金属、suanli、openapi.suanli.cn、开机器、
  查机器状态、订单/费用/账单时启用。
---

# 共绩算力 裸金属 API

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
Content-Type: application/json
```

**加签**（非简易模式）：对字符串  
`/api{path含query}\n{version}\n{timestamp}\n{token}\n{body}`  
用 RSA 私钥 PKCS#1 v1.5 + SHA256 签名，Base64 为 `sign_str`；解码后须 256 字节，否则换新 `timestamp` 重签。

**响应**：`{ code, message, data }`；`code === "0000"` 成功，否则 `data` 为 null。

简易模式优先用 [`scripts/call.sh`](scripts/call.sh)。脚本会自动加 `/api` 前缀，传入 path 时**不要**带 `/api`。

## 计费与价格

内部计量单位为**点**：`1 元 = 1,000,000 点`。向用户展示金额时，相关字段除以 `1,000,000`。

**计费方式**（时长包，下单与可购列表筛选均用）：

| 对用户说法 | `billing_type` | 含义 |
|------------|----------------|------|
| 小时包（**默认**） | `Hour` | 小时时长包 |
| 天包 | `Day` | 24 小时时长包 |
| 周包 | `Week` | 7 天时长包 |
| 月包 | `Month` | 30 天时长包 |

向用户询问时用「小时包 / 天包 / 周包 / 月包」，**默认小时包**；写入 API 时再映射为 `Hour`/`Day`/`Week`/`Month`。

**`buy_count`（时长包数量）**：表示购买**多少个**所选时长包（即买多久），不是设备台数。对用户说「时长包数量 / 买多少时长」，**默认 1**。  
例：小时包 × `buy_count=3` → 买 3 小时；天包 × `buy_count=2` → 买 2 个 24 小时包。组网时设备台数由可购列表的 `device_count` / `inner` 决定，勿与 `buy_count` 混淆。

**价格字段**（可购列表，单位：点）：

| 字段 | 说明 |
|------|------|
| `hour_price` / `day_price` / `week_price` / `month_price` | 对应时长包标价 |
| `*_price_discount` | 租户折扣价；非 null 时下单 `unit_price` 优先用折扣价 |

下单时按所选 `billing_type` 取对应价格写入 `unit_price`（`1000000 = 1 元`）。`unit_price` 仅用于「页面展示价与下单瞬间价不一致」的提示，不决定最终扣费。

**订单金额字段**（订单列表，单位：点）：

| 字段 | 说明 |
|------|------|
| `total_price` | 订单金额 |
| `discount_total_price` | 算力券消费 |
| `actually_total_price` | 余额消费 |
| `cancel_actually_total_price` / `cancel_discount_total_price` | 余额/算力券退款 |

## 端点速查

| 操作 | 方法 | 路径 | 文档 |
|------|------|------------------------------|------|
| 单机可购列表 | POST | `/output/v2/device-output/page_list_product_single_v2` | [api/single-product-list.md](api/single-product-list.md) |
| 组网可购列表 | POST | `/output/v2/device-output/page_list_product_network_v2` | [api/group-product-list.md](api/group-product-list.md) |
| 创建订单 | POST | `/output/v2/device_order/buy_v2` | [api/order-create.md](api/order-create.md) |
| 订单列表 | POST | `/output/v2/device_order/get_order_list_v2` | [api/order-list.md](api/order-list.md) |
| 已购单机列表 | POST | `/output/v2/device-output/list_rent_device_single_v2` | [api/rent-single-device-list.md](api/rent-single-device-list.md) |
| 已购组网列表 | POST | `/output/v2/device-output/list_rent_device_network_v2` | [api/rent-group-device-list.md](api/rent-group-device-list.md) |
| 设备详情（开机信息） | POST | `/output/v2/device_order/get_device_details_v2` | [api/device-detail.md](api/device-detail.md) |
| 开启自动续费 | POST | `/output/v2/auto_renew_device_config/set_auto_renew_config` | [api/auto-renew.md](api/auto-renew.md) |
| 取消自动续费 | POST | `/output/v2/auto_renew_device_config/delete_auto_renew_config` | [api/cancel-auto-renew.md](api/cancel-auto-renew.md) |

完整字段见 [`api/`](api/)；**仅在构造复杂 body 时读取**，勿整篇加载。

## 状态枚举

**订单 / 订单详情状态**：

| 值 | 含义 |
|----|------|
| `Default` | 默认 |
| `Waiting` | 等待中 |
| `Serving` | 服务中（已开机，才有 SSH/内网 IP/暴露端口） |
| `Finished` | 已结束 |
| `Canceled` | 已取消 |
| `CanceledRefunded` | 已取消并退款（仅订单详情） |

**组网网络类型**（组网可购必填）：`Ib` / `Roce` / `NVLinkSwitch` / `EthernetFast`

## 工作流

### 1. 创建裸金属订单

先确认：**单机还是组网**、计费（问「小时包 / 天包 / 周包 / 月包」，默认小时包）、时长包数量（问「买多少时长 / 几个时长包」，默认 1 → `buy_count`）；组网还需 `network_type`、`device_count`。

#### 1a. 查可购资源（取 `device_id` 与 `unit_price`）

**单机**：

```json
POST /output/v2/device-output/page_list_product_single_v2
{
  "page": 1,
  "page_size": 10,
  "conditional": {
    "billing_type": "Hour",
    "gpu_models": [],
    "zone_id": null,
    "gpu_count": null
  }
}
```

- `conditional.billing_type`、`gpu_models` 必填；`gpu_models: []` 表示全部卡型。
- 从 `data.results[]` 取 `device_id`，按 `billing_type` 取 `hour_price`/`day_price`/…（优先 `*_price_discount`）作为 `unit_price`。
- 注意 `max_buy_count`，`buy_count`（时长包数量）不可超过。
- 关注 `listing_mode`：`Single`（单机）、`Proxy`（网关代理）、`Direct`（网关直连）。**`Proxy` / `Direct` 设备下单后约 30 分钟可用**，展示候选或下单成功时须明确告知用户。

**组网**：

```json
POST /output/v2/device-output/page_list_product_network_v2
{
  "billing_type": "Hour",
  "device_count": 2,
  "network_type": "EthernetFast",
  "gpu_models": ["4090"],
  "gpu_count": 4,
  "zone_id": 1
}
```

- 必填：`billing_type`、`device_count`、`network_type`。
- 返回 `data[]`，组内设备在 `inner[]`；下单时 `inner` 需包含组内各台的 `device_id` + `unit_price`。

#### 1b. 提交创建

```json
POST /output/v2/device_order/buy_v2
{
  "billing_type": "Hour",
  "buy_count": 1,
  "inner": [{ "device_id": 690, "unit_price": 15000000 }],
  "software_init": false,
  "discount_relation_id": null
}
```

| 规则 | 说明 |
|------|------|
| 必填 | `billing_type`、`buy_count`（时长包数量）、`inner`、`software_init`、`discount_relation_id`（可 `null`） |
| 单机 `buy_count > 1` | 多买几个时长包；`inner` **仍只传 1 个** object |
| 组网 `buy_count > 1` | `inner` 传入**多台**，数量与实际设备数一致 |
| 成功 | 返回 `data.order_id`；若所选设备 `listing_mode` 为 `Proxy` 或 `Direct`，**必须告知用户：下单后约 30 分钟可用** |

### 2. 查询订单与已购设备

**订单列表**（可按设备型号/订单编号关键词搜）：

```json
POST /output/v2/device_order/get_order_list_v2
{
  "page": 1,
  "page_size": 10,
  "conditional": { "condition": "" }
}
```

**已购单机**（订单未结束）：`POST /output/v2/device-output/list_rent_device_single_v2`，body `{}`。  
关注：`device_id`、`order_detail_status`、`extranet_ip`/`intranet_ip`、`use_start_time`/`use_end_time`、`auto_renew_type`。

**已购组网**：`POST /output/v2/device-output/list_rent_device_network_v2`，body `{}`。  
按 `network_id` 分组，设备在 `inner[]`（字段含 `pub_ip`/`inner_ip`）。

### 3. 设备详情（开机 / SSH）

```json
POST /output/v2/device_order/get_device_details_v2
{ "device_id": 672 }
```

返回公网/内网 IP、`ssh_port`、`device_username`/`device_passwd`、`expose_ports[]`（`local_port`→`mapping_port`）等。  
**仅当设备已在服务中（Serving）才有内网 IP、暴露端口、SSH 端口**；否则相关字段可能为 null。

### 4. 自动续费

开启（扣费失败会自动取消续费）：

```json
POST /output/v2/auto_renew_device_config/set_auto_renew_config
{ "device_id": 250, "billing_type": "Hour", "use_discount": true }
```

取消：

```json
POST /output/v2/auto_renew_device_config/delete_auto_renew_config
{ "device_id": 250 }
```

## 对话执行约定

1. 缺 token 时先向用户索取，勿猜测。
2. 创建前确认：单机/组网、计费（问「小时包 / 天包 / 周包 / 月包」，默认小时包 → `Hour`）、时长包数量（问「买多少时长 / 几个时长包」，默认 1 → `buy_count`；勿说成笼统的「购买数量」）；组网另确认 `network_type`、设备台数；是否 `software_init`、是否用算力券（`discount_relation_id`）。
3. 查可购时按用户卡型/区域/GPU 数筛选；无库存或空列表时如实告知，勿编造 `device_id`。
4. 创建成功后回报 `order_id`；若设备 `listing_mode` 为 `Proxy`（网关代理）或 `Direct`（网关直连），**必须告知用户下单后约 30 分钟可用**；询问是否查订单状态或已购列表/开机信息。
5. 查 SSH/登录信息前确认设备 `order_detail_status === Serving`，否则先等开机（`Proxy`/`Direct` 约需 30 分钟）。
6. 金额一律用「点 / 1,000,000 = 元」展示。
7. 错误时输出 `code` + `message`；加签失败时建议换简易模式密钥或提供私钥。

## 脚本

```bash
export SUANLI_TOKEN="<密钥>"

# 单机可购
./scripts/call.sh POST /output/v2/device-output/page_list_product_single_v2 \
  '{"page":1,"page_size":10,"conditional":{"billing_type":"Hour","gpu_models":[]}}'

# 创建订单
./scripts/call.sh POST /output/v2/device_order/buy_v2 @payload.json

# 订单列表
./scripts/call.sh POST /output/v2/device_order/get_order_list_v2 \
  '{"page":1,"page_size":10,"conditional":{"condition":""}}'

# 已购单机 / 设备详情
./scripts/call.sh POST /output/v2/device-output/list_rent_device_single_v2 '{}'
./scripts/call.sh POST /output/v2/device_order/get_device_details_v2 '{"device_id":672}'

# 自动续费
./scripts/call.sh POST /output/v2/auto_renew_device_config/set_auto_renew_config \
  '{"device_id":250,"billing_type":"Hour","use_discount":true}'
./scripts/call.sh POST /output/v2/auto_renew_device_config/delete_auto_renew_config \
  '{"device_id":250}'
```
