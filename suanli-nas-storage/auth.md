# 共绩 Open API 加签与加密

摘自官方文档：[Open API RSA 模式使用指南](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/)。  
**只在简易模式不够、或加签/加密失败时读本文。** 日常调用走脚本，不要根据本文现场重写一整套加签代码。

| 场景 | 用什么 |
|------|--------|
| 存储卷 CRUD、SFTP 获取/关闭、互传列表/详情/停止/删除 | [`scripts/call.sh`](scripts/call.sh)（简易模式，不签不加密） |
| `/encrypt/s3/create`、`/retry`、`/check` | [`scripts/call_encrypt.py`](scripts/call_encrypt.py)（先加密再加签） |

脚本传入的 path **不要**带 `/api`（脚本会加）。依赖：`pip install cryptography requests`。

---

## 1. 两种模式，不能混用

创建密钥时选定模式，Token 与调用方式必须匹配。

| | 简易模式（Token） | RSA 加验签模式 |
|--|-------------------|----------------|
| Header | `token` + `timestamp` + `version` | 再加 `sign_str` |
| 私钥 | 不需要 | 客户端持有，用于**签名** |
| 用户公钥 | 不需要 | 上传到平台，用于**验签** |
| 平台公钥 | 不需要 | 创建密钥时平台返回，用于**加密请求体** |
| 请求体加密 | **不支持** | 接口文档「是否需要加密 = 是」时必须 |
| 本 skill | 卷 CRUD、SFTP、互传查询/停止/删除 | S3 创建 / 重试 / 校验 |

本 skill 三个加密接口**不能**用简易 Token 发明文 JSON。缺 `SUANLI_RSA_PRIVATE_KEY` 或 `SUANLI_PLATFORM_PUBLIC_KEY` 时向用户索取。

密钥管理：<https://console.suanli.cn/settings/key>

**两套密钥勿混用**：加密用**平台公钥**；签名用**你的私钥**。用户上传到平台的公钥只用于平台验签。

---

## 2. 请求头

| Header | 必填 | 说明 |
|--------|------|------|
| `token` | 是 | 平台 API Token |
| `version` | 是 | 固定 `1.0.0` |
| `timestamp` | 是 | **毫秒** Unix 时间戳（13 位），与 NTP 偏差 < 5 分钟 |
| `sign_str` | RSA 模式是 | RSA-SHA256 签名的 Base64 |
| `Content-Type` | POST 是 | 普通 JSON：`application/json`；本 skill 加密接口：`text/plain`（以该接口 Apifox 为准；通用指南示例有时写成 `application/json`） |

基址：`https://openapi.suanli.cn`

---

## 3. 加签

1. 拼待签字符串（5 段，用 `\n` 连接，末段后**没有**多余换行）：

```
{path}\n{version}\n{timestamp}\n{token}\n{body}
```

| 字段 | 规则 |
|------|------|
| `path` | 以 `/api` 开头。GET 含 query 时签完整 `path?query`，编码与实际 URL 一致 |
| `version` / `timestamp` / `token` | 与 Header 完全一致 |
| `body` | GET 或无 Body 用空串 `""`（不要 `null` / `{}`）。加密接口填**加密后的 Base64**，不是原始 JSON |

2. 用户 RSA **私钥** + SHA-256 + PKCS#1 v1.5 签名  
3. 签名结果 Base64 → Header `sign_str`  
4. 原始签名字节数须为 **256**（RSA-2048）；不是则换新 `timestamp` 重签  

**顺序**：若该接口要加密，必须 **先加密 body，再用密文 Base64 去签名**。

---

## 4. 请求体加密

仅当接口文档「是否需要加密 = 是」。本 skill：`POST /api/storage/nas/v1/encrypt/s3/{create,retry,check}`。

| 项目 | 值 |
|------|-----|
| 公钥 | **平台返回的** RSA 公钥 |
| 算法 | RSA + PKCS#1 v1.5 |
| 分段 | 2048 位密钥每段最多 **244** 字节明文 |
| JSON | 紧凑：`separators=(',', ':')`，`ensure_ascii=False` |
| 输出 | 各段密文**字节拼接**后，**整体** Base64（不要每段单独 Base64 再拼接） |

步骤：

1. `dict` → 紧凑 JSON 字符串 → UTF-8 字节  
2. 按 244 字节切开，逐段用平台公钥加密  
3. 拼接密文块 → Base64 = `encrypted_body`  
4. HTTP Body 发送 `encrypted_body`  
5. 签名里的 `body` 也用 `encrypted_body`

AccessKey / SecretKey 只出现在加密前的 JSON 里，不要写入日志或回复用户。

---

## 5. 环境变量

```bash
SUANLI_TOKEN="<API Token>"
SUANLI_BASE_URL="https://openapi.suanli.cn"          # 可选
SUANLI_RSA_PRIVATE_KEY="<PEM 或 Base64 PKCS#8>"      # 签名
SUANLI_PLATFORM_PUBLIC_KEY="<平台公钥 PEM>"           # 加密；不是用户上传的那把
```

私钥丢失无法恢复，需重新生成密钥对并在控制台建新密钥。

---

## 6. 排错

| 检查项 | 正确 | 常见错误 |
|--------|------|----------|
| timestamp | 13 位毫秒 | 10 位秒级 |
| version | `"1.0.0"` | `1` 或平台版本号 |
| path | `/api/...`，GET 带 query | 漏 `/api` 或漏 query |
| body | 无 Body 用 `""` | GET 填 `{}` |
| 签名顺序 | path → version → timestamp → token → body | 字段顺序错或分隔符不是 `\n` |
| 加密顺序 | 先加密，再签密文 | 先签原始 JSON 再加密 |
| 公钥 | 加密用平台公钥 | 用了用户自己的公钥加密 |
| 时钟 | 偏差 < 5 分钟 | 本地时间不准 |

失败时向用户输出接口 `code` + `message`。加签失败：先核对模式是否匹配，再检查私钥/平台公钥；非加密接口可建议改用简易模式 Token。
