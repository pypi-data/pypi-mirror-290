import fnmatch
import glob
import json
import os
import time
import zipfile
from pathlib import Path

import boto3
import jwt
import requests
from poetry.poetry import Poetry
from poetry_plugin_export.exporter import Exporter as PoetryPluginDepsExporter

from poetry_ycf_plugin.config import PLUGIN_NAME, YcfPluginConfig
from poetry_ycf_plugin.utils import FakeCleoIoStringIO


class DeployManager(object):
    poetry: Poetry
    cfg: YcfPluginConfig
    include_files: set[str]
    exclude_files: set[str]
    requirements_txt_content: str

    def __init__(self, poetry: Poetry) -> None:
        self.poetry = poetry
        self.cfg = YcfPluginConfig()

        self.include_files = set()
        self.exclude_files = set()
        self.requirements_txt_content = ''

    @property
    def safely_release_version(self):
        return str(self.poetry.package.version).replace('.', '-')

    @property
    def release_name(self):
        return f'{self.cfg.id}-{self.poetry.package.name}-{self.safely_release_version}'

    @property
    def release_zip_name(self):
        return f'{self.cfg.s3_bucket_path}/{self.release_name}.zip'

    @property
    def release_zip_path(self):
        return Path.cwd() / 'dist' / 'YC' / self.release_zip_name

    def auth(self):
        auth_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

        now = int(time.time())
        payload = {
            'aud': auth_url,
            'iss': self.cfg.service_account_id,
            'iat': now,
            'exp': now + 3600,
        }

        # Формирование JWT.
        encoded_token = jwt.encode(
            payload,
            self.cfg.authorized_key_data.private_key,
            algorithm='PS256',
            headers={
                'kid': self.cfg.authorized_key_data.id,
            },
        )

        response = requests.post(
            auth_url,
            headers={
                'Content-Type': 'application/json',
            },
            json={
                'jwt': encoded_token,
            },
        )

        response.raise_for_status()

        self.cfg.set_iam_token(response.json())

        # Make the POST request
        response = requests.post(
            'https://iam.api.cloud.yandex.net/iam/aws-compatibility/v1/accessKeys',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {self.cfg.iam_token}",
            },
            json={
                'serviceAccountId': self.cfg.service_account_id,
                'description': f'Temporary AwsAccessKeys created by {PLUGIN_NAME}',
            },
        )

        response.raise_for_status()

        self.cfg.set_static_keys(response.json())

    def __build_include_files(self):
        for files_glob in self.cfg.build_include:
            for file in glob.glob(files_glob, root_dir=Path.cwd(), recursive=True):
                self.include_files.add(file)

        for target_file in self.include_files:
            for files_glob in self.cfg.build_exclude:
                if fnmatch.fnmatch(target_file, files_glob):
                    self.exclude_files.add(target_file)

        self.include_files = self.include_files - self.exclude_files
        self.include_files = {i for i in self.include_files if os.path.isfile(i)}

        if 'requirements.txt' in self.include_files:
            self.include_files.remove('requirements.txt')

    def __build_requirements_txt(self):
        exporter = PoetryPluginDepsExporter(self.poetry, FakeCleoIoStringIO())
        exporter.with_hashes(False)
        exporter.only_groups(['main'] + self.cfg.build_dependencies_groups)

        buffer = FakeCleoIoStringIO()
        exporter.export('requirements.txt', None, buffer)
        buffer.seek(0)
        self.requirements_txt_content = buffer.getvalue().encode('utf-8')
        buffer.close()

    def __build_zip(self):
        self.release_zip_path.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(self.release_zip_path, 'w') as zipf:
            for file in self.include_files:
                zipf.write(file, file)

            zipf.writestr('requirements.txt', self.requirements_txt_content)

    def build(self):
        self.__build_include_files()
        self.__build_requirements_txt()
        self.__build_zip()

    def upload(self):
        s3 = boto3.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            region_name='ru-central1',
            aws_access_key_id=self.cfg.aws_access_key_id,
            aws_secret_access_key=self.cfg.aws_secret_access_key,
        )
        s3.upload_file(
            self.release_zip_path,
            self.cfg.s3_bucket_name,
            self.release_zip_name,
        )

    def release(self):
        data = {
            'functionId': self.cfg.id,
            'runtime': self.cfg.runtime,
            'entrypoint': self.cfg.entrypoint,
            'resources': {'memory': str(self.cfg.memory)},
            'executionTimeout': '5s',
            'serviceAccountId': self.cfg.service_account_id,
            'package': {
                'bucketName': self.cfg.s3_bucket_name,
                'objectName': self.release_zip_name,
            },
            'environment': self.cfg.environment,
            'description': self.poetry.package.pretty_string,
            'tag': ['ycf', self.poetry.package.name, 'v' + self.safely_release_version.strip('v')],
        }

        response = requests.post(
            'https://serverless-functions.api.cloud.yandex.net/functions/v1/versions',
            headers={
                'Authorization': f'Bearer {self.cfg.iam_token}',
            },
            data=json.dumps(data),
        )
        response.raise_for_status()

    def clean(self):
        response = requests.delete(
            f'https://iam.api.cloud.yandex.net/iam/aws-compatibility/v1/accessKeys/{self.cfg.access_key_id}',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {self.cfg.iam_token}",
            },
        )
        response.raise_for_status()
