import requests

from ..utils.check import Check
from ._provider import Provider


class GCore(Provider):
    cdn_url = ''

    def set_cdn_url(self, cdn_url):
        cdn_url = '' if not cdn_url else cdn_url.rstrip('/') + '/'
        self.cdn_url = cdn_url
        return self

    def fetch(self):
        """
        拉取数据并转为迭代器
        """
        ip_url = f'{self.cdn_url}https://api.gcore.com/cdn/public-ip-list'
        response = requests.get(ip_url, timeout=5)
        if response.status_code != 200:
            raise ValueError(f'status code {response.status_code}')
        resp = response.json()
        return [str(address).split('/')[0] for address in resp['addresses']]

    def run(self):
        if not self.domain:
            return False

        try:
            check_domain = 'gcore.com'
            check = Check(check_domain)

            # 源IP有效开关。检测是否使用旧IP。
            if self.skip:
                old_ip = check.domain_ip(self.domain, redirect=False)
                # 源IP有效则返回
                if old_ip:
                    return old_ip

            ip_list = self.fetch()
            print(f'ip count: {len(ip_list)}')
            # ip_list = ip_list[-1:]
            # print(ip_list)
            valid_ips = check.run(ip_list)
            print(f'valid ip count: {len(valid_ips)}')
            if len(valid_ips) == 0:
                raise ValueError('No valid ip address')

            # 按响应时间从小到大排序
            valid_ips.sort(key=lambda x: x[1])
            # print(f'有效IP地址列表（按响应时间排序）:')
            # for ip, rtt in valid_ips:
            #     print(f'{ip} - 响应时间: {rtt}ms')
            print(f'fast gcore ip: {valid_ips[0]}')
            return valid_ips[0][0]

        except Exception as e:
            print(f'Failed to get gcore best ip. {e}')
            return None
