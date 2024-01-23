from .config import Config
from .provider.cloudflare import CloudFlare
from .provider.gcore import GCore
from .utils.ns import refresh


class App:
    def __init__(self):
        self.cfg = self.config()

    def config(self):
        """
        toml -> env -> cli
        """
        return Config().new()

    def run(self):
        cfg = self.cfg
        gcore_ip = None
        cloudflare_ip = None
        save_cloudflare_token = cfg.get('save_cloudflare_token', '')
        print('save_cloudflare_token:', save_cloudflare_token)
        if save_cloudflare_token:
            source_cdn_url = cfg.get('source_cdn_url', '')
            print('source_cdn_url:', source_cdn_url)

            print('')
            gcore_skip = cfg.get('gcore_skip', '')
            print('gcore_skip:', gcore_skip)
            gcore_domain = cfg.get('gcore_domain', '')
            print('gcore_domain:', gcore_domain)
            serv = GCore(domain=gcore_domain, skip=gcore_skip)
            serv.set_cdn_url(source_cdn_url)
            gcore_ip = serv.run()
            print('gcore_ip:', gcore_ip)
            if gcore_domain and gcore_ip:
                refresh(
                    ip_address=gcore_ip,
                    record_name=gcore_domain,
                    token=save_cloudflare_token,
                )

            print('')
            cloudflare_skip = cfg.get('cloudflare_skip', '')
            print('cloudflare_skip:', cloudflare_skip)
            cloudflare_domain = cfg.get('cloudflare_domain', '')
            print('cloudflare_domain:', cloudflare_domain)
            cloudflare_random = cfg.get('cloudflare_random', 50)
            print('cloudflare_random:', cloudflare_random)
            serv = CloudFlare(domain=cloudflare_domain, skip=cloudflare_skip)
            serv.set_cdn_url(source_cdn_url).set_num(cloudflare_random)
            cloudflare_ip = serv.run()
            print('cloudflare_ip:', cloudflare_ip)
            if cloudflare_domain and cloudflare_ip:
                refresh(
                    ip_address=cloudflare_ip,
                    record_name=cloudflare_domain,
                    token=save_cloudflare_token,
                )
        return save_cloudflare_token != '', gcore_ip, cloudflare_ip


def entry():
    App().run()
