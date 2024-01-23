## 支持[青龙面板](https://github.com/whyour/qinglong)

1.  `依赖管理` -> `Python` -> 添加依赖 `cloudflare`。
2.  `依赖管理` -> `Linux` -> 添加依赖：
    > **debian:** `iputils-ping`,`dnsutils`  
    > **alpine(latest):** `iputils`,`bind-tools`
3.  相关命令查看 **[官方教程](https://github.com/whyour/qinglong#%E5%86%85%E7%BD%AE%E5%91%BD%E4%BB%A4)**。

    ```bash
    ql repo https://framagit.org/idev/cdnbestip.git run "" "cloudflare|gcore|check|dns_cf" main

    # 或（不建议部署至海外平台，否则不保证该 IP 对国内有效）
    ql repo https://github.com/idev-sig/cdnbestip.git run "" "cloudflare|gcore|check|dns_cf" main
    ```
