#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""suanli-nas-storage：Apifox 官方文档实时查询（read-through，仅标准库）。

Agent 构造复杂请求前优先运行本脚本，从 Apifox 分享文档拉取**最新**接口定义，
不依赖本地静态文件；网络失败时回退读 api/ 目录（exit 2 会提示）。

用法：
  python scripts/apidoc.py list                     # 本 skill 全部端点
  python scripts/apidoc.py search "扩容"             # 按关键词搜端点
  python scripts/apidoc.py get /storage/nas/v1/create   # 按路径查完整文档
  python scripts/apidoc.py get nas-create           # 按短名（api/*.md 文件名）
"""
import argparse
import json
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

SHARE_HOST = "https://s.apifox.cn"
SHARE_ID = "6aa360d3-d8f2-471e-b841-3a35c33a7b7c"
RETRY_TIMES = 3
RETRY_BACKOFF = 1.5
TIMEOUT = 30
TREE_CACHE_MAX_AGE = 600  # 秒
UA = "Mozilla/5.0 suanli-skill-apidoc/1.0"

# 本 skill 负责的端点路径前缀（list/search 用）
SKILL_PREFIXES = [
    "/api/storage/nas/",
]

# api/*.md 文件名（去 .md）→ (method, path)；get 短名匹配用
FILE_ALIAS = {
    "nas-summary": ("get", "/api/storage/nas/v1/summary"),
    "nas-dictionaries": ("get", "/api/storage/nas/v1/dictionaries"),
    "nas-pre-create": ("get", "/api/storage/nas/v1/pre-create"),
    "nas-list": ("get", "/api/storage/nas/v1/list"),
    "nas-create": ("post", "/api/storage/nas/v1/create"),
    "nas-expand": ("post", "/api/storage/nas/v1/expand"),
    "nas-delete": ("post", "/api/storage/nas/v1/delete"),
    "nas-rename": ("post", "/api/storage/nas/v1/rename"),
    "s3-list": ("get", "/api/storage/nas/v1/s3/list"),
    "s3-detail": ("get", "/api/storage/nas/v1/s3/detail"),
    "s3-create": ("post", "/api/storage/nas/v1/encrypt/s3/create"),
    "s3-retry": ("post", "/api/storage/nas/v1/encrypt/s3/retry"),
    "s3-delete": ("post", "/api/storage/nas/v1/s3/delete"),
    "s3-stop": ("post", "/api/storage/nas/v1/s3/stop"),
    "s3-check": ("post", "/api/storage/nas/v1/encrypt/s3/check"),
    "sftp-obtain": ("post", "/api/storage/nas/v1/sftp/obtain"),
    "sftp-destroy": ("post", "/api/storage/nas/v1/sftp/destroy"),
}


def _get_json(url: str, params: dict = None) -> dict:
    if params:
        from urllib.parse import urlencode
        url = f"{url}?{urlencode(params)}"
    last_exc = None
    for attempt in range(1, RETRY_TIMES + 1):
        try:
            req = urllib.request.Request(url, headers={
                "Accept": "application/json", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, OSError, ValueError) as exc:
            last_exc = exc
            if attempt < RETRY_TIMES:
                time.sleep(RETRY_BACKOFF ** attempt)
    raise last_exc


def _cache_path() -> Path:
    # 缓存放在系统临时目录，不污染 skill 仓库
    d = Path(tempfile.gettempdir()) / "suanli-apidoc"
    d.mkdir(parents=True, exist_ok=True)
    return d / "tree.json"


def load_tree(refresh: bool = False) -> list:
    cp = _cache_path()
    if not refresh and cp.exists():
        try:
            cache = json.loads(cp.read_text(encoding="utf-8"))
            if time.time() - cache.get("fetched_at", 0) < TREE_CACHE_MAX_AGE:
                return cache["tree"]
        except (json.JSONDecodeError, KeyError, OSError):
            pass
    payload = _get_json(f"{SHARE_HOST}/api/v1/shared-docs/{SHARE_ID}/http-api-tree")
    if not payload.get("success"):
        raise RuntimeError(f"API 树拉取失败: {json.dumps(payload)[:200]}")
    tree = payload["data"]
    try:
        cp.write_text(json.dumps({"fetched_at": time.time(), "tree": tree},
                                 ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    return tree


def flatten_tree(tree: list) -> list:
    out = []

    def walk(nodes, prefix):
        for n in nodes or []:
            if n.get("type") == "apiDetailFolder":
                walk(n.get("children"), prefix + [n.get("name", "")])
            elif n.get("type") == "apiDetail":
                api = n.get("api") or {}
                out.append({"id": api.get("id"),
                            "method": (api.get("method") or "").lower(),
                            "path": api.get("path") or "",
                            "name": api.get("name") or "",
                            "folder": "/".join(prefix)})

    walk(tree, [])
    return out


def fetch_detail(api_id) -> dict:
    payload = _get_json(
        f"{SHARE_HOST}/api/v1/shared-docs/{SHARE_ID}/http-apis/{api_id}")
    if not payload.get("success"):
        raise RuntimeError(f"端点详情拉取失败: {json.dumps(payload)[:200]}")
    return payload["data"]


# ---------------- 渲染 ----------------

def _simple_type(schema: dict) -> str:
    if not isinstance(schema, dict):
        return "any"
    t = schema.get("type")
    if isinstance(t, list):
        t = " | ".join(str(x) for x in t)
    return str(t or "any")


def _schema_to_md_lines(schema: dict, indent: int = 0) -> list:
    lines = []
    pad = "  " * indent
    if not isinstance(schema, dict):
        return lines
    stype = schema.get("type")
    if isinstance(stype, list):
        stype = " | ".join(str(t) for t in stype)
    if stype == "array":
        item = schema.get("items", {})
        lines.append(f"{pad}- **array<{_simple_type(item)}>**")
        lines.extend(_schema_to_md_lines(item, indent + 1))
        return lines
    if stype == "object" or "properties" in schema:
        props = schema.get("properties", {})
        order = schema.get("x-apifox-orders") or list(props.keys())
        required = set(schema.get("required") or [])
        for key in order:
            if key not in props:
                continue
            sub = props[key]
            req = " **(必填)**" if key in required else ""
            title = sub.get("title") or ""
            desc = (sub.get("description") or "").strip().replace("\n", " ")
            enum = sub.get("enum")
            enum_str = ""
            if isinstance(enum, list):
                enum_str = f"，枚举: `{'`/`'.join(str(e) for e in enum[:12])}`"
            meta = " — ".join(x for x in [title, desc] if x)
            meta = (f"：{meta}" if meta else "")
            lines.append(f"{pad}- `{key}` `{_simple_type(sub)}`{req}{meta}{enum_str}")
            lines.extend(_schema_to_md_lines(sub, indent + 1))
        return lines
    return lines


def render_api_md(detail: dict, folder: str) -> str:
    method = (detail.get("method") or "").upper()
    path = detail.get("path") or ""
    name = detail.get("name") or ""
    desc = (detail.get("description") or "").strip()
    updated = detail.get("updatedAt") or ""

    lines = [f"# {name}", ""]
    lines.append(f"> Apifox 实时查询 · 分组：{folder}")
    if updated:
        lines.append(f"> 远端最后更新：{updated}")
    lines.append(f"> 端点：`{method} {path}`")
    lines.append("")
    if desc:
        lines.append(desc)
        lines.append("")

    params = detail.get("parameters") or {}
    for loc in ("query", "header", "path", "cookie"):
        items = params.get(loc) or []
        if not items:
            continue
        lines.append(f"## {loc} 参数")
        lines.append("")
        lines.append("| 参数 | 类型 | 必填 | 说明 |")
        lines.append("| --- | --- | --- | --- |")
        for p in items:
            ptype = p.get("type") or _simple_type(p.get("schema") or {})
            req = "是" if p.get("required") else "否"
            pdesc = (p.get("description") or "").strip().replace("\n", " ")
            sample = p.get("sampleValue")
            if sample not in (None, ""):
                pdesc = f"{pdesc}（示例：{sample}）".strip()
            lines.append(f"| `{p.get('name')}` | {ptype} | {req} | {pdesc or '—'} |")
        lines.append("")

    body = detail.get("requestBody") or {}
    if body.get("type") not in (None, "none"):
        lines.append("## 请求体")
        lines.append("")
        lines.append(f"Content-Type: `{body.get('type')}`")
        lines.append("")
        js = body.get("jsonSchema")
        if js:
            sl = _schema_to_md_lines(js)
            if sl:
                lines.extend(sl)
                lines.append("")
        for ex in body.get("examples") or []:
            lines.append(f"**请求示例（{ex.get('name') or '示例'}）**：")
            lines.append("")
            lines.append("```json")
            try:
                parsed = json.loads(ex.get("value") or "{}")
                lines.append(json.dumps(parsed, ensure_ascii=False, indent=2))
            except (json.JSONDecodeError, TypeError):
                lines.append(str(ex.get("value") or ""))
            lines.append("```")
            lines.append("")

    responses = detail.get("responses") or []
    for resp in responses:
        code = resp.get("code")
        lines.append(f"## 响应（{code}）")
        lines.append("")
        rjs = resp.get("jsonSchema")
        if rjs:
            sl = _schema_to_md_lines(rjs)
            if sl:
                lines.extend(sl)
                lines.append("")
        name_ = resp.get("name")
        if name_:
            lines.append(f"响应名：{name_}")
            lines.append("")

    for rex in detail.get("responseExamples") or []:
        lines.append(f"**响应示例（{rex.get('name') or '示例'}）**：")
        lines.append("")
        lines.append("```json")
        try:
            parsed = json.loads(rex.get("data") or "{}")
            lines.append(json.dumps(parsed, ensure_ascii=False, indent=2))
        except (json.JSONDecodeError, TypeError):
            lines.append(str(rex.get("data") or ""))
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------- 命令 ----------------

def _match(api: dict) -> bool:
    return any(api["path"].startswith(p) for p in SKILL_PREFIXES)


def cmd_list(args):
    flat = [a for a in flatten_tree(load_tree(refresh=args.refresh)) if _match(a)]
    if not flat:
        print("[未找到] 本 skill 无匹配端点")
        return 4
    print(f"suanli-nas-storage 相关端点（{len(flat)} 个）：\n")
    print(f"{'方法':<7}{'路径':<58}{'名称'}")
    for a in flat:
        print(f"{a['method'].upper():<7}{a['path']:<58}{a['name']}")
    print("\n查看完整文档：python scripts/apidoc.py get <路径|短名>")
    return 0


def cmd_search(args):
    flat = [a for a in flatten_tree(load_tree(refresh=args.refresh)) if _match(a)]
    q = args.query.lower()
    hits = [a for a in flat if q in f"{a['name']} {a['path']} {a['folder']}".lower()]
    if not hits:
        print(f"[未找到] 关键词「{args.query}」无匹配端点（--refresh 可刷新缓存重试）")
        return 4
    print(f"共 {len(hits)} 个匹配端点：\n")
    print(f"{'方法':<7}{'路径':<58}{'名称'}")
    for a in hits:
        print(f"{a['method'].upper():<7}{a['path']:<58}{a['name']}")
    print("\n查看完整文档：python scripts/apidoc.py get <路径|短名>")
    return 0


def _resolve_target(key: str, flat: list):
    key = key.strip()
    k = key.lower().lstrip("/")
    # 1) 短名别名（api/*.md 文件名）
    if k.endswith(".md"):
        k = k[:-3]
    if k in FILE_ALIAS:
        m, p = FILE_ALIAS[k]
        for a in flat:
            if a["method"] == m and a["path"] == p:
                return a, f"短名 {k} → {m.upper()} {p}"
    # 2) 路径匹配（带/不带 /api 前缀）
    if not k.startswith("/"):
        k = "/" + k
    cands = [a for a in flat if a["path"] == k]
    if not cands:
        cands = [a for a in flat if a["path"] == "/api" + k]
    if len(cands) == 1:
        return cands[0], "路径匹配"
    if len(cands) > 1:
        return None, "多个端点匹配：" + "; ".join(
            f"{c['method'].upper()} {c['path']}({c['name']})" for c in cands)
    return None, f"未找到端点：{key}（可先 search 关键词）"


def cmd_get(args):
    flat = flatten_tree(load_tree(refresh=args.refresh))
    api, note = _resolve_target(args.key, flat)
    if api is None:
        print(f"[未找到] {note}")
        return 4
    md = render_api_md(fetch_detail(api["id"]), api["folder"])
    if args.output:
        Path(args.output).write_text(md, encoding="utf-8", newline="\n")
        print(f"[OK] 已写入 {args.output}（{note}）")
    else:
        sys.stdout.write(md)
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="suanli-nas-storage Apifox 文档实时查询（read-through）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list", help="列出本 skill 全部端点")
    p.add_argument("--refresh", action="store_true")
    p.set_defaults(func=cmd_list)
    p = sub.add_parser("search", help="按关键词搜端点")
    p.add_argument("query")
    p.add_argument("--refresh", action="store_true")
    p.set_defaults(func=cmd_search)
    p = sub.add_parser("get", help="查端点完整文档（markdown 实时渲染）")
    p.add_argument("key", help="接口路径或短名（如 nas-create）")
    p.add_argument("-o", "--output", help="写入文件（默认打印）")
    p.add_argument("--refresh", action="store_true")
    p.set_defaults(func=cmd_get)
    args = ap.parse_args()
    try:
        sys.exit(args.func(args) or 0)
    except (urllib.error.URLError, OSError) as exc:
        print(f"[网络错误] {type(exc).__name__}: {exc}", file=sys.stderr)
        print("网络不可用，请回退读取 api/ 目录下的静态文档。", file=sys.stderr)
        sys.exit(2)
    except RuntimeError as exc:
        print(f"[错误] {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
