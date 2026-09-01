# 共绩算力 Agent Skills

通过共绩算力（[suanli.cn](https://suanli.cn)）Open API 管理弹性部署、Job 批处理、裸金属、集群存储与镜像预热。

[![skills.sh](https://skills.sh/b/<owner>/<repo>)](https://skills.sh/<owner>/<repo>)

将 `<owner>/<repo>` 换成本仓库的 GitHub 地址（例如 `acme/gj-skills`）。

## 安装

```bash
npx skills add <owner>/<repo>
```

CLI 会把 skill 装到当前 Agent 对应目录。Cursor 项目级默认 `.agents/skills/`，全局为 `~/.cursor/skills/`。

### 常用变体

```bash
# 列出仓库内 skill，不安装
npx skills add <owner>/<repo> --list

# 只装某一个
npx skills add <owner>/<repo> --skill suanli-deployment

# 全局安装（跨项目可用）
npx skills add <owner>/<repo> -g

# 装全部 skill 到已检测到的 Agent
npx skills add <owner>/<repo> --all
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

## 更新

```bash
npx skills update
```
