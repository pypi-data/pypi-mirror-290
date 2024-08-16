import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

from poetry_ycf_plugin.responses import IamTokenResponse, StaticKeyResponse

logger = logging.getLogger('poetry_ycf_plugin')

ENV_FILE = Path.cwd() / '.env'
TOML_FILE = Path.cwd() / 'pyproject.toml'

PLUGIN_NAME = 'poetry-ycf-plugin'


class AuthorizedKey(BaseModel):
    id: str
    service_account_id: str
    created_at: datetime
    key_algorithm: str
    public_key: str
    private_key: str


class YcfPluginConfig(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file=TOML_FILE,
        pyproject_toml_table_header=('tool', PLUGIN_NAME),
        env_file=ENV_FILE,
        env_prefix='YCF_',
        extra='ignore',
        case_sensitive=False,
    )

    authorized_key: Path = Path('authorized_key.json')
    service_account_id: str

    build_dependencies_groups: list[str] = []
    build_include: list[str] = ['*.py', '**/*.py', 'assess/*']
    build_exclude: list[str] = ['.*', '**/__pycache__/**', 'tests/*', 'dist/*']

    s3_bucket_name: str
    s3_bucket_path: str = 'ycf-releases'

    id: str
    entrypoint: str = 'main.handler'
    memory: int = 134217728
    runtime: str = 'python312'
    environment: dict[str, Any] = {}

    iam_token: str | None = None
    access_key_id: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            PyprojectTomlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
        )

    @property
    def authorized_key_data(self) -> AuthorizedKey:
        return AuthorizedKey.model_validate_json(self.authorized_key.read_text())

    def set_iam_token(self, data: dict[str, Any]):
        iam_token_data = IamTokenResponse.model_validate(data)
        self.iam_token = iam_token_data.iamToken

    def set_static_keys(self, data: dict[str, Any]):
        data_obj = StaticKeyResponse.model_validate(data)
        self.access_key_id = data_obj.accessKey.id
        self.aws_access_key_id = data_obj.accessKey.keyId
        self.aws_secret_access_key = data_obj.secret
