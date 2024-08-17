import os
import time
import platform
import tarfile
from subprocess import PIPE, Popen
from pathlib import Path
from threading import Thread
from io import BytesIO
from json import dump
from httpx import Client

from nonebot.log import logger
from nonebot.plugin import get_plugin_config

from .config import Config
from .lagrange import lagrange_config


def download(url: str):
    download_bytes = BytesIO()
    with Client() as client:
        try:
            with client.stream('GET', 'https://mirror.ghproxy.com/' + url) as stream:
                if stream.status_code != 200:
                    return False
                for chunk in stream.iter_bytes():
                    download_bytes.write(chunk)
                download_bytes.seek(0)
                return download_bytes
        except Exception as error:
            logger.error(F'Lagrange.Onebot 下载失败！错误信息 {error}')
            return False


class LagrangeManager(Thread):
    task: Popen = None
    config: Config = None

    lagrange_path: Path = None

    def __init__(self):
        Thread.__init__(self, name='Lagrange', daemon=True)
        self.config = get_plugin_config(Config)
        self.path = Path(self.config.lagrange_path)
        for path in self.path.rglob('Lagrange.OneBot*'):
            self.lagrange_path = path
        if self.lagrange_path and self.config.lagrange_auto_start:
            logger.info('Lagrange.Onebot 已经安装，正在启动……')
            self.start()
        elif self.config.lagrange_auto_install:
            logger.info('Lagrange.Onebot 未安装，正在安装……')
            self.install()

    def stop(self):
        if self.task:
            self.task.terminate()
            self.task = None

    def run(self):
        last_log = ''
        self.update_config()
        command = str(self.lagrange_path) if os.name == 'nt' else ('./' + self.lagrange_path.name)
        self.task = Popen(command, stdout=PIPE, cwd=self.path)
        logger.success('Lagrange.Onebot 启动成功！请扫描目录下的图片或控制台中的二维码登录。')
        while self.task and (self.task.poll() is None):
            if line := self.task.stdout.readline():
                line = line.decode('Utf-8').strip()
                if line.startswith('█') or line.startswith('▀'):
                    logger.info(line)
                    continue
                elif line.startswith('warn'):
                    logger.warning('[Lagrange] ' + line)
                    continue
                elif line.startswith('at'):
                    if not last_log.startswith('at'):
                        logger.error('[Lagrange] ' + last_log)
                    logger.error('[Lagrange] ' + line)
                    continue
                logger.debug('[Lagrange] ' + line)
                time.sleep(0.5)
                last_log = line
        logger.info('Lagrange.Onebot 已退出！如若没有正常使用，请检查日志。')

    def update_config(self):
        config_path = (self.path / 'appsettings.json')
        lagrange_config['Implementations'][0]['Host'] = self.config.host
        lagrange_config['Implementations'][0]['Port'] = self.config.port
        lagrange_config['Implementations'][0]['AccessToken'] = self.config.onebot_access_token
        with config_path.open('w', encoding='Utf-8') as file:
            dump(lagrange_config, file)
            logger.success('Lagrange.Onebot 配置文件更新成功！')
            return True

    def install(self):
        if self.lagrange_path:
            logger.warning('Lagrange.Onebot 已经安装，无需再次安装！')
            return True
        if not self.path.exists():
            self.path.mkdir()
        self.path.chmod(0o755)
        system, architecture = self.parse_platform()
        logger.info(F'检测到当前的系统架构为 {system} {architecture} 正在下载对应的安装包……')
        if response := download(
                F'https://github.com/LagrangeDev/Lagrange.Core/releases/download/nightly/Lagrange.OneBot_{system}-{architecture}_net8.0_SelfContained.tar.gz'):
            logger.success(F'Lagrange.Onebot 下载成功！正在安装……')
            with tarfile.open(fileobj=response) as zip_file:
                for member in zip_file.getmembers():
                    if member.isfile():
                        with zip_file.extractfile(member) as file:
                            file_name = file.name.split('/')[-1]
                            with open((self.path / file_name), 'wb') as target_file:
                                target_file.write(file.read())
            logger.success('Lagrange.Onebot 安装成功！')
            self.lagrange_path = next(self.path.rglob('Lagrange.OneBot*'))
            self.lagrange_path.chmod(0o755)
            return self.update_config()
        logger.error('Lagrange.Onebot 安装失败！')
        return False

    @staticmethod
    def parse_platform():
        system = platform.system()
        architecture = platform.machine()
        system_mapping = {'Linux': 'linux', 'Darwin': 'osx', 'Windows': 'win'}
        if system == 'Windows':
            architecture = 'x64' if architecture == 'AMD64' else 'x86'
        elif system == 'Darwin':
            architecture = 'x64' if architecture == 'x86_64' else 'arm64'
        elif system == 'Linux':
            architecture = 'x64' if architecture == 'x86_64' else 'arm'
        return system_mapping[system], architecture
