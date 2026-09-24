# 共绩算力 Agent Skills

通过共绩算力（[suanli.cn](https://suanli.cn)）Open API 管理弹性部署、Job 批处理、裸金属、集群存储与镜像预热。

[![skills.sh](https://skills.sh/b/suanleme/gongji-skills)](https://skills.sh/suanleme/gongji-skills)

线上仓库：[github.com/suanleme/gongji-skills](https://github.com/suanleme/gongji-skills)

## 安装

```bash
npx skills add suanleme/gongji-skills
```

CLI 会把 skill 装到当前 Agent 对应目录。Cursor 项目级默认 `.agents/skills/`，全局为 `~/.cursor/skills/`。

### 常用变体

```bash
# 列出仓库内 skill，不安装
npx skills add suanleme/gongji-skills --list

# 只装某一个
npx skills add suanleme/gongji-skills --skill suanli-deployment

# 全局安装（跨项目可用）
npx skills add suanleme/gongji-skills -g

# 装全部 skill 到已检测到的 Agent
npx skills add suanleme/gongji-skills --all
```

本地开发可直接指向本目录：

```bash
npx skills add . --list
```

## Skills

| Skill | 说明 |
|-------|------|
| [suanli-deployment](suanli-deployment/) | 弹性部署任务全生命周期、节点、计费、对象存储与 NAS 挂载 |
| [suanli-job](suanli-job/) | Job 批处理：创建 / 查询 / 停止、任务队列、资源与计费 |
| [suanli-metal](suanli-metal/) | 裸金属机器、订单与计费 |
| [suanli-nas-storage](suanli-nas-storage/) | 集群存储卷、SFTP、S3 互传 |
| [suanli-image-preheat](suanli-image-preheat/) | 镜像预热任务：创建 / 查询 / 更新 / 停止 |

## 凭证

安装后进入对应 skill 目录，复制模板再填密钥（**不要提交 `.env`**）：

```bash
cp .env.example .env
```

必填 `SUANLI_TOKEN`（平台右上角头像 → **API 密钥**，推荐简易模式）。可选 `SUANLI_BASE_URL`、`SUANLI_RSA_PRIVATE_KEY`。`suanli-nas-storage` 在 S3 创建 / 重试 / 校验时还需要 `SUANLI_PLATFORM_PUBLIC_KEY`。

## 接口文档：Apifox 实时查询

各 skill 的 `api/` 目录是接口文档的**静态快照**（离线回退用）。要拿**最新**接口定义，用各 skill 自带的 `scripts/apidoc.py`（仅 Python 标准库，无第三方依赖）直接读 Apifox 官方分享文档：

```bash
python scripts/apidoc.py list                 # 本 skill 全部端点
python scripts/apidoc.py search "关键词"       # 搜索端点
python scripts/apidoc.py get /task/job/create # 完整文档（实时渲染，含参数/请求体/响应）
python scripts/apidoc.py get job-create       # 短名 = api/*.md 文件名
```

共绩在 Apifox 上更新接口后，skill 无需发版，Agent 每次查询拿到的都是最新定义；网络不可用时自动提示回退读 `api/` 静态文档。

## 更新

```bash
npx skills update
```
