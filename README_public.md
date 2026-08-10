# mikrotik-split-rsc-generator

自动从多个可信在线数据源获取 IP 地址段和域名列表，生成 MikroTik RouterOS `.rsc` 脚本文件。可直接导入路由器，用于创建防火墙地址列表和 DNS 静态条目，实现路由分流、流量过滤或 DNS 分离。

Automatically fetches IP address ranges and domain names from trusted online sources, then generates MikroTik RouterOS `.rsc` script files. These can be imported directly into a router to create firewall address lists and DNS static entries for routing, filtering, or split-DNS.

---

## 功能 / Features

| Source | Type | Output | Description |
|--------|------|--------|-------------|
| CNIPsV4 | IPv4 CIDR | `cn-ips-v4.rsc` | 中国大陆 IPv4 地址段(来源：[iwik.org](https://www.iwik.org/ipcountry/CN.cidr))/ China mainland IPv4 ([iwik.org](https://www.iwik.org/ipcountry/CN.cidr)) |
| BogonsIPsV4 | IPv4 CIDR | `bogons-ips-v4.rsc` | 保留/未分配 IPv4 地址段(来源：[Team Cymru](https://team-cymru.org/Services/Bogons/fullbogons-ipv4.txt))/ Bogon IPv4 ([Team Cymru](https://team-cymru.org/Services/Bogons/fullbogons-ipv4.txt)) |
| CloudflareIPsV4 | IPv4 CIDR | `cloudflare-ips-v4.rsc` | Cloudflare IPv4 地址段(来源：[Cloudflare](https://www.cloudflare.com/ips-v4)) / Cloudflare IPv4 ranges ([cloudflare.com](https://www.cloudflare.com/ips-v4)) |

## 环境要求 / Prerequisites

- Python 3.8+
- pip

## 快速开始 / Quick Start

```bash
# 克隆仓库 / Clone
git clone <repo-url>
cd mikrotik-split-rsc-generator

# 创建虚拟环境（推荐）/ Create virtualenv (recommended)
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 运行 / Run
python main.py
```

生成文件位于 `rsc/` 目录下。输出示例：

Generated files are in `rsc/`. Example output:

```
Success  CNIPsV4              →   cn-ips-v4.rsc (12345 entries)
Success  BogonsIPsV4          →   bogons-ips-v4.rsc (4321 entries)
...
Done: 3 Total, 3 Success, 0 Failures
```

## 在 MikroTik 上使用 / Usage on MikroTik

1. 通过 FTP 将 `rsc/` 目录下的 `.rsc` 文件上传到路由器。
Upload `.rsc` files from `rsc/` to your MikroTik router via FTP.
2. 在 RouterOS 终端中导入：
Import in RouterOS terminal:

```bash
/import file-name=cn-ips-v4.rsc
/import file-name=bogons-ips-v4.rsc.rsc
```

## RSC 脚本行为 / Script Behavior

每个生成的 `.rsc` 脚本遵循幂等设计，可反复导入而不会产生重复条目：

Each script is idempotent—safe to import repeatedly without creating duplicates:

1. **定义条目** — 将 IP/域名存入本地数组
**Define** — store all IPs/domains in a local array
2. **清理** — 移除地址列表中已不再存在于数据源的过期条目
**Cleanup** — remove stale entries no longer in the source
3. **添加** — 添加新条目，通过 `on-error={}` 跳过已存在的条目
**Add** — add new entries, skipping duplicates via `on-error={}`


## CI/CD

Actions 工作流支持以下触发方式：

The Actions workflow supports:

- 每日北京时间 03:00 自动运行 / Daily at 03:00 Asia/Shanghai
- 推送到主分支时运行 / On push to main branch

工作流自动生成 RSC 文件，提交变更并推送。

The workflow generates fresh RSC files, commits and pushes changes.

## License

MIT