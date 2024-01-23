import multiprocessing
import platform
import re
import subprocess

import requests
import urllib3

urllib3.disable_warnings()


class Check:
    def __init__(self, domain, scheme='http') -> None:
        self.domain = domain
        self.scheme = 'https' if scheme == 'https' else 'http'

    def curl(self, ip_address, timeout=5, redirect=False):
        """
        执行一个curl请求到指定的IP地址，并且在给定的超时时间内完成。

        参数:
            ip_address (str): 要请求的IP地址。
            timeout (int): 请求的超时时间（秒）。默认为5。

        返回:
            bool: 如果网站可以访问则为True，否则为False。
        """
        try:
            url = f'{self.scheme}://{ip_address}'
            headers = {'Host': self.domain}
            # print(url)
            response = requests.head(
                url,
                headers=headers,
                allow_redirects=redirect,
                verify=False,
                timeout=timeout,
            )
            # print(response.status_code)
            # print(ip_address, redirect, url, headers)
            if response.status_code in [200, 301, 302]:
                # print("网站可访问！")
                return True
            # else:
            # print(f"无法访问，状态码: {response.status_code}")
        except requests.RequestException:
            # print(f"发生错误: {e}")
            pass
        return False

    def dig(self, domain):
        """
        根据操作系统执行适当的 DNS 查找命令。

        参数:
            domain (str): 要进行 DNS 查找的域名。

        返回:
            CompletedProcess: 命令执行的结果。
        """
        # 根据操作系统选择正确的 ping 命令
        if platform.system() == 'Windows':
            cmd = ['nslookup', domain]
        else:  # Linux 和 macOS 使用不同的 ping 命令
            cmd = ['dig', domain]

        resp = subprocess.run(
            cmd, capture_output=True, text=True, check=True, timeout=5
        )
        # print(resp)
        return resp

    def ping(self, ip_address):
        # 根据操作系统选择正确的 ping 命令，发 5 个包
        if platform.system() == 'Windows':
            cmd = ['ping', '-n', '5', ip_address]
        else:  # Linux 和 macOS 使用不同的 ping 命令
            cmd = ['ping', '-c', '5', ip_address]

        return subprocess.run(
            cmd, capture_output=True, text=True, check=True, timeout=5
        )

    def check_ip(self, ip_address, result_queue):
        """
        使用 ping 检查 IP 地址的可用性并检索响应时间。

        参数:
            ip_address (str): 要检查的 IP 地址。
            result_queue (Queue): 用于存储可达 IP 地址及其响应时间的队列。

        返回:
            None
        """
        try:
            result = self.ping(ip_address)
            # print(f'result stdout: {result.stdout}')
            # print(f'result returncode: {result.returncode}')
            if result.returncode == 0:
                rtt = -1  # 无法解析响应时间

                if not self.curl(ip_address, timeout=3):
                    return False

                # 解析 ping 结果以获取响应时间（具体解析方法可能因操作系统而异）
                if platform.system() == 'Windows':
                    rtt_line = [
                        line
                        for line in result.stdout.splitlines()
                        if 'Average =' in line
                    ]
                    if rtt_line:
                        rtt_str = rtt_line[0].split('=')[-1].strip()
                        rtt = float(rtt_str.split(' ')[0])
                else:  # Linux 和 macOS 的 ping 命令输出格式不同，您可能需要根据实际情况进行解析
                    # 使用正则表达式匹配 "time=数字 单位" 格式的字符串
                    # pattern = r"time=(\d+\s?\.\s?\d*)\s?(\w+)"
                    pattern = r'time=(\d+\s?)\s?(\w+)'
                    matches = re.findall(pattern, result.stdout)
                    rtt = self.time2ms(matches[0])

                if rtt != -1:
                    result_queue.put(
                        (ip_address, rtt)
                    )  # 将可达的IP地址和响应时间放入结果队列
        except Exception:
            # print(f'err {e}')
            pass  # 发生异常，忽略

    def time2ms(self, match):
        """
        将带有单位的时间值转换为毫秒。

        :param match: 包含时间值及其单位的元组。
        :type match: tuple
        :return: 转换为毫秒的时间值。
        :rtype: float
        """
        value = str(match[0]).strip()
        unit = str(match[1]).lower()
        if unit == 'ms':
            return float(value)
        elif unit == 's':
            return float(value) * 1_000  # 将秒转换为毫秒
        elif unit == 'us':
            return float(value) / 1_000  # 将微秒转换为毫秒
        return float(value) * 10_000_000

    def run(self, ip_list):
        """
        使用多进程对 IP 地址列表执行 ping 检查。

        参数:
            ip_list (list): 需要进行 ping 检查的 IP 地址列表。

        返回:
            list: 响应 ping 检查的有效 IP 地址列表。
        """
        # 创建一个可在主进程和子进程之间共享的队列
        manager = multiprocessing.Manager()
        result_queue = manager.Queue()

        max_concurrency = 10  # 控制并发 ping 操作的数量
        pool = multiprocessing.Pool(max_concurrency)

        # 控制每次处理的 IP 地址的数量
        batch_size = 20  # 调整为适当的值
        for i in range(0, len(ip_list), batch_size):
            batch_ips = ip_list[i: i + batch_size]
            processes = []

            for ip in batch_ips:
                process = pool.apply_async(self.check_ip, args=(ip, result_queue))
                processes.append(process)

            for process in processes:
                process.get()  # 等待子进程完成

        pool.close()
        pool.join()

        valid_ips = []
        while not result_queue.empty():
            valid_ips.append(result_queue.get())
        return valid_ips

    def domain_ip(self, domain, timeout=3, redirect=False):
        """
        如果旧的IP地址有效，则返回该IP地址，否则尝试更新IP地址并返回None。

        :param domain: 要检索IP地址的域名。
        :return: 如果旧的IP地址有效，则返回该IP地址，否则返回None。
        """
        try:
            resp = self.dig(domain)
            # 若源IP有效，则不更新
            if resp.returncode == 0:
                ip_pattern = r'\d+\.\d+\.\d+\.\d+'
                # ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                match = re.search(ip_pattern, resp.stdout)
                if match:
                    old_ip = match.group()
                    if self.curl(old_ip, timeout=timeout, redirect=redirect):
                        return old_ip
        except Exception as e:
            print(f'domain_ip err {e}')
            pass
