import ipaddress
import os
import random
import subprocess

import requests

from ..utils.check import Check
from ._provider import Provider


class CloudFlare(Provider):
    cdn_url = ''
    num = 50

    def set_cdn_url(self, cdn_url):
        cdn_url = '' if not cdn_url else cdn_url.rstrip('/') + '/'
        self.cdn_url = cdn_url
        return self

    def set_num(self, num):
        self.num = 50 if not num else int(num)
        return self

    def ip_from_fetch(self):
        """
        从 url 文件中读取 IP 段
        https://www.cloudflare.com/ips/
        """
        ip_url = f'{self.cdn_url}https://www.cloudflare.com/ips-v4'
        response = requests.get(ip_url)
        if response.status_code != 200:
            raise ValueError(f'status code {response.status_code}')
        ip_string = response.text
        ip_list = ip_string.strip().splitlines()
        return [ip.strip() for ip in ip_list if ip.strip()]

    def ip_from_file(self):
        """
        从 ip.txt 文件中读取 IP 段
        https://www.cloudflare.com/ips/
        """
        ip_url = 'https://www.cloudflare.com/ips-v4'
        # 若不存在此 ip.txt 文件，则从网络上下载
        if not os.path.exists('ip.txt'):
            subprocess.call(['wget', '-O', 'ip.txt', ip_url])

        with open('ip.txt') as file:
            return file.read().splitlines()

    def ip_from_string(self):
        """
        IP 段作为 string
        """
        ip_string = """
        173.245.48.0/20
        103.21.244.0/22
        103.22.200.0/22
        103.31.4.0/22
        141.101.64.0/18
        108.162.192.0/18
        190.93.240.0/20
        188.114.96.0/20
        197.234.240.0/22
        198.41.128.0/17
        162.158.0.0/15
        104.16.0.0/12
        172.64.0.0/17
        172.64.128.0/18
        172.64.192.0/19
        172.64.224.0/22
        172.64.229.0/24
        172.64.230.0/23
        172.64.232.0/21
        172.64.240.0/21
        172.64.248.0/21
        172.65.0.0/16
        172.66.0.0/16
        172.67.0.0/16
        131.0.72.0/22
        """
        # 将上述的 ip_str 转为 list
        ip_list = ip_string.strip().splitlines()
        return [ip.strip() for ip in ip_list if ip.strip()]

    def run(self):
        if not self.domain:
            return False

        try:
            check_domain = 'cloudflare.com'
            check = Check(check_domain)

            # 源IP有效开关。检测是否使用旧IP。
            if self.skip:
                old_ip = check.domain_ip(self.domain, redirect=False)
                # 源IP有效则返回
                if old_ip:
                    return old_ip

            ip_ranges = self.ip_from_fetch()
            # ip_ranges = ip_from_file()
            # ip_ranges = ip_from_string()

            ip_list = []
            # 遍历每个 IP 段
            for ip_range in ip_ranges:
                # 解析 IP 段
                ip_network = ipaddress.IPv4Network(ip_range, strict=False)

                # 随机选择 3 个 IP 地址
                num_ips = min(
                    self.num, ip_network.num_addresses - 2
                )  # 减去网络地址和广播地址
                ips = [
                    str(ip) for ip in random.sample(list(ip_network.hosts()), num_ips)
                ]
                ip_list.extend(ips)

            print(f'ip count: {len(ip_list)}')
            valid_ips = check.run(ip_list)
            print(f'valid ip count: {len(valid_ips)}')
            if len(valid_ips) == 0:
                raise ValueError('No valid IP address')

            # 按响应时间从小到大排序
            valid_ips.sort(key=lambda x: x[1])
            print(f'fast cloudflare ip: {valid_ips[0]}')
            best_ip = valid_ips[0][0]
            return best_ip

        except Exception as e:
            print(f'Failed to get cloudflare best ip.  {e}')
