import argparse
import os
from argparse import RawTextHelpFormatter

import toml


class Config:
    _default_config = {
        'save_cloudflare_token': '',
        'source_cdn_url': '',
        'bark_token': '',
        'chanify_token': '',
        'lark_token': '',
        'feishu_token': '',
        'wecom_token': '',
        'gcore_skip': 'true',
        'gcore_domain': '',
        'cloudflare_skip': 'true',
        'cloudflare_domain': '',
        'cloudflare_random': 50,
    }

    def __init__(self):
        self.config = self._default_config.copy()
        self.config_path = 'config.toml'

    def _load_toml(self):
        try:
            with open(self.config_path) as toml_file:
                toml_data = toml.load(toml_file)
                setting = toml_data.get('setting')
                if setting:
                    self.config.update({k: v for k, v in setting.items() if v})
                notify = toml_data.get('notify')
                if notify:
                    self.config.update(
                        {k + '_token': v for k, v in notify.items() if v}
                    )
                domain = toml_data.get('domain')
                if domain:
                    for key, value in domain.items():
                        if not value:
                            continue
                        if key == 'cloudflare_random':
                            self.config[key] = int(value)
                        elif key == 'gcore_skip' or key == 'cloudflare_skip':
                            self.config[key] = value == 'true'
                        else:
                            self.config[key] = value
        # except FileNotFoundError:
        # print("config.toml file not found")
        except Exception:
            # print(f"Error loading config.toml: {e}")
            pass

    def _load_env(self):
        """
        从环境变量中检索数据并将它们分配给相应的配置键。
        """
        ENV_VARIABLES = {
            'save_cloudflare_token': 'SAVE_CLOUDFLARE_TOKEN',
            'source_cdn_url': 'SOURCE_CDN_URL',
            'bark_token': 'BARK_TOKEN',
            'chanify_token': 'CHANIFY_TOKEN',
            'lark_token': 'LARK_TOKEN',
            'feishu_token': 'FEISHU_TOKEN',
            'wecom_token': 'WECOM_TOKEN',
            'gcore_skip': 'GCORE_SKIP',
            'gcore_domain': 'GCORE_DOMAIN',
            'cloudflare_skip': 'CLOUDFLARE_SKIP',
            'cloudflare_domain': 'CLOUDFLARE_DOMAIN',
            'cloudflare_random': 'CLOUDFLARE_RANDOM',
        }

        for key, env_var in ENV_VARIABLES.items():
            value = os.getenv(env_var, '')
            if not value:
                continue
            # print('key: %s, value: %s' % (key, value))
            if key == 'cloudflare_random':
                self.config[key] = int(value)
            elif key == 'gcore_skip' or key == 'cloudflare_skip':
                self.config[key] = value == 'true'
            else:
                self.config[key] = value

    def _load_cli(self):
        """
        解析命令行参数并更新 self.config 字典。
        """
        parser = argparse.ArgumentParser(
            description='', formatter_class=RawTextHelpFormatter
        )
        parser.add_argument(
            '-sct',
            '--save-cloudflare-token',
            type=str,
            help='Cloudflare token to save.',
        )
        parser.add_argument(
            '-scu', '--source-cdn-url', type=str, help='Source CDN URL.'
        )
        parser.add_argument('-bt', '--bark-token', type=str, help='Bark token.')
        parser.add_argument('-ct', '--chanify-token', type=str, help='Chanify token.')
        parser.add_argument('-lt', '--lark-token', type=str, help='Lark token.')
        parser.add_argument('-ft', '--feishu-token', type=str, help='Feishu token.')
        parser.add_argument('-wt', '--wecom-token', type=str, help='Wecom token.')
        parser.add_argument(
            '-gs',
            '--gcore-skip',
            type=str,
            choices=['true', 'false'],
            help='Skip GCore CDN.',
        )
        parser.add_argument('-gd', '--gcore-domain', type=str, help='GCore CDN domain.')
        parser.add_argument(
            '-cs',
            '--cloudflare-skip',
            type=str,
            choices=['true', 'false'],
            help='Skip Cloudflare CDN.',
        )
        parser.add_argument(
            '-cd', '--cloudflare-domain', type=str, help='Cloudflare CDN domain.'
        )
        parser.add_argument(
            '-cr',
            '--cloudflare-random',
            type=int,
            help='Random selection threshold for Cloudflare.',
        )

        args = parser.parse_args()

        for arg in vars(args):
            value = getattr(args, arg)
            if not value:
                continue
            config_key = arg.replace('-', '_')
            if config_key == 'cloudflare_random':
                self.config[config_key] = int(value)
            elif config_key == 'gcore_skip' or config_key == 'cloudflare_skip':
                self.config[config_key] = value == 'true'
            else:
                self.config[config_key] = value

    def new(self):
        self._load_toml()
        self._load_env()
        self._load_cli()
        return self.config
