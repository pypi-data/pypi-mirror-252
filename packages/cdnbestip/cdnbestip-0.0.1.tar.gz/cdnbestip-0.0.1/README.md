# CDN Best IP

获取最优的 [GCore IP](https://api.gcore.com/cdn/public-ip-list) 和 [CloudFlare IP](https://www.cloudflare.com/ips/)。

## 使用说明

1. 依赖系统的 `ping`,`dig` 命令。

   ```bash
   # Debian 系
   apt install iputils-ping dnsutils
   ```

2. 使用 `pip` 安装工具。  
   **注意：** 依赖 `CloudFlare` 提供的 `DNS` 服务。

   ```bash
   pip install cdnbestip

   # 设置环境变量或配置文件，执行命令
   cdnbestip
   ```

## 设置环境变量

**优先级：** `命令行参数` > `环境变量` > `配置文件`

- **命令行参数**
<details>
  <summary>点击查看详细参数信息</summary>

```bash
# cdnbestip --help
usage: cdnbestip [-h] [-sct SAVE_CLOUDFLARE_TOKEN] [-scu SOURCE_CDN_URL] [-bt BARK_TOKEN] [-ct CHANIFY_TOKEN] [-lt LARK_TOKEN] [-ft FEISHU_TOKEN]
                 [-wt WECOM_TOKEN] [-gs {true,false}] [-gd GCORE_DOMAIN] [-cs {true,false}] [-cd CLOUDFLARE_DOMAIN] [-cr CLOUDFLARE_RANDOM]

options:
  -h, --help            show this help message and exit
  -sct SAVE_CLOUDFLARE_TOKEN, --save-cloudflare-token SAVE_CLOUDFLARE_TOKEN
                        Cloudflare token to save.
  -scu SOURCE_CDN_URL, --source-cdn-url SOURCE_CDN_URL
                        Source CDN URL.
  -bt BARK_TOKEN, --bark-token BARK_TOKEN
                        Bark token.
  -ct CHANIFY_TOKEN, --chanify-token CHANIFY_TOKEN
                        Chanify token.
  -lt LARK_TOKEN, --lark-token LARK_TOKEN
                        Lark token.
  -ft FEISHU_TOKEN, --feishu-token FEISHU_TOKEN
                        Feishu token.
  -wt WECOM_TOKEN, --wecom-token WECOM_TOKEN
                        Wecom token.
  -gs {true,false}, --gcore-skip {true,false}
                        Skip GCore CDN.
  -gd GCORE_DOMAIN, --gcore-domain GCORE_DOMAIN
                        GCore CDN domain.
  -cs {true,false}, --cloudflare-skip {true,false}
                        Skip Cloudflare CDN.
  -cd CLOUDFLARE_DOMAIN, --cloudflare-domain CLOUDFLARE_DOMAIN
                        Cloudflare CDN domain.
  -cr CLOUDFLARE_RANDOM, --cloudflare-random CLOUDFLARE_RANDOM
                        Random selection threshold for Cloudflare.
```

</details>

- **环境变量**
<details>
  <summary>点击查看环境变量信息</summary>

```bash
# Bark 通知环境变量 https://github.com/finb/bark
export BARK_TOKEN=''
# Chanify 通知环境变量 https://github.com/chanify/chanify
export CHANIFY_TOKEN=''
# Lark 通知环境变量 https://open.larksuite.com/document/client-docs/bot-v3/add-custom-bot#756b882f
export LARK_TOKEN=''
# FeiShu 通知环境变量 https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot#756b882f
export FEISHU_TOKEN=''

export SAVE_CLOUDFLARE_TOKEN='' # CloudFlare Token https://www.cloudflare.com/
export SOURCE_CDN_URL='' # 防墙，从源站获取 IP 列表

export GCORE_SKIP='true' # 设置此值时，若 GCORE_DOMAIN 可访问，则不重新获取IP
export GCORE_DOMAIN='gcore.xxx.xyz'

export CLOUDFLARE_SKIP='true' # 设置此值时，若 CLOUDFLARE_DOMAIN 可访问，则不重新获取IP
export CLOUDFLARE_DOMAIN='cloudflare.xxx.xyz'
export CLOUDFLARE_RANDOM=50 # 每个段随机取几个数值，不设置则默认50
```

</details>

- **配置文件**
<details>
  <summary>点击查看配置文件 config.toml 信息</summary>

```toml
[setting]
save_cloudflare_token = ""
source_cdn_url = ""

[notify]
bark = ""
chanify = ""
lark = ""
feishu = ""
wecom = ""

[domain]
gcore_skip = "true"
gcore_domain = ""

cloudflare_skip = "true"
cloudflare_domain = ""
cloudflare_random = 50
```

</details>

## 设置定时任务

> 每日检测最新的可用 IP 信息。  
> 部署到云服务器上，使用 crontab 定时执行，参考相关脚本 [cron](cron)。

## 仓库镜像

- https://git.jetsung.com/idev/cdnbestip
- https://framagit.org/idev/cdnbestip
- https://github.com/idevsig/cdnbestip
