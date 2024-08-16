# Poetry Yandex Cloud Functions Plugin

Poetry plugin to set package version based on git tag.

[![PyPI](https://img.shields.io/pypi/v/poetry-ycf-plugin)](https://pypi.org/project/poetry-ycf-plugin/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poetry-ycf-plugin)](https://pypi.org/project/poetry-ycf-plugin/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/poetry-ycf-plugin)](https://gitlab.com/rocshers/python/poetry-ycf-plugin)
[![Docs](https://img.shields.io/badge/docs-exist-blue)](https://rocshers.gitlab.io/python/poetry-ycf-plugin/)

[![Test coverage](https://codecov.io/gitlab/rocshers:python/poetry-ycf-plugin/graph/badge.svg?token=3C6SLDPHUC)](https://codecov.io/gitlab/rocshers:python/poetry-ycf-plugin)
[![Downloads](https://static.pepy.tech/badge/poetry-ycf-plugin)](https://pepy.tech/project/poetry-ycf-plugin)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/poetry-ycf-plugin)](https://gitlab.com/rocshers/python/poetry-ycf-plugin)

## Functionality

- One-command deploy.
- Configure target files and dependency groups via pyproject
- Using only [`authorized_key.json`](https://yandex.cloud/docs/iam/concepts/authorization/key) for authentication.
- Deploy via ZIP and S3. [Details](https://yandex.cloud/ru/docs/functions/concepts/function).
- Setting up an `entrypoint` and `memory`

## Quick start

Install `poetry` and get [`authorized_key.json`](https://yandex.cloud/docs/iam/concepts/authorization/key)

```bash
poetry self add poetry-ycf-plugin
poetry ycf-deploy
```

## Configs

List of variables and brief description.

Supported configuration sources: `.env` files (prefixed with YCF_), `environment variables` (prefixed with YCF_), and `pyproject.toml` (under the [tool.poetry-ycf-plugin] section).

```bash
export YCF_ENTRYPOINT='test_project.entrypoint.index_entrypoint' 
# same as
echo "YCF_ENTRYPOINT=test_project.entrypoint.index_entrypoint" >> .env
# same as
[tool.poetry-ycf-plugin]
entrypoint = 'test_project.entrypoint.index_entrypoint'
```

### YCF Authorized Key

`tool.poetry-ycf-plugin.authorized_key` or `YCF_AUTHORIZED_KEY`

**Required.** String. Default: `Path('./authorized_key.json')`

The path to the [`authorized_key.json`](https://yandex.cloud/docs/iam/concepts/authorization/key) file.

### YCF Service Account ID

`tool.poetry-ycf-plugin.service_account_id` or `YCF_SERVICE_ACCOUNT_ID`

**Required.** String.

The ID of the service account used to perform operations in the cloud. The account must have access to the S3 bucket `YCF s3_bucket_name` and permissions to modify function versions `YCF id`.

### YCF Build Dependencies Groups

`tool.poetry-ycf-plugin.build_dependencies_groups` or `YCF_BUILD_DEPENDENCIES_GROUPS`

**Optional.** List of strings.

Specifies which Poetry dependency groups from `pyproject.toml`, in addition to the main group, are required for the function. All selected dependencies will be converted into `requirements.txt` and included in the build.

### YCF Build Include

`tool.poetry-ycf-plugin.build_include` or `YCF_BUILD_INCLUDE`

**Optional.** List of strings. Default: `['\*.py', '\*\*/\*.py', 'assess/\*']`

Specifies the file patterns that should be included in the build.

### YCF Build Exclude

`tool.poetry-ycf-plugin.build_exclude` or `YCF_BUILD_EXCLUDE`

**Optional.** List of strings. Default: `['.\*', '\*\*/\_\_pycache\_\_/\*\*', 'tests/\*', 'dist/\*']`

Specifies the file patterns that should be excluded from `build_include` and therefore not included in the build.

For example, if `build_include` contains the pattern `*.py` and `build_exclude` contains the pattern `.*`, the file `.old_realization.py` **will not** be included in the build.

### YCF S3 Bucket Name

`tool.poetry-ycf-plugin.s3_bucket_name` or `YCF_S3_BUCKET_NAME`

**Required.** String.

The name of the S3 bucket where releases will be saved as `.zip` archives.

### YCF S3 Bucket Path

`tool.poetry-ycf-plugin.s3_bucket_path` or `YCF_S3_BUCKET_PATH`

**Optional.** String. Default: `ycf-releases`

The directory in the S3 bucket where releases will be saved as `.zip` archives.

### YCF ID

`tool.poetry-ycf-plugin.id` or `YCF_ID`

**Required.** String.

The identifier of the target function.

### YCF Entrypoint

`tool.poetry-ycf-plugin.entrypoint` or `YCF_ENTRYPOINT`

**Optional.** String. Default: `main.handler`

The entry point for the Yandex Cloud function. This variable should contain a string reference to the function that will receive the input data.

### YCF Memory

`tool.poetry-ycf-plugin.memory` or `YCF_MEMORY`

**Optional.** Number. Default: `134217728`

Specifies the amount of memory that Yandex Cloud should allocate for the function.

### YCF Runtime

`tool.poetry-ycf-plugin.runtime` or `YCF_RUNTIME`

**Optional.** String. Default: `python312`

Specifies the runtime environment.

### YCF Environment

`tool.poetry-ycf-plugin.environment` or `YCF_ENVIRONMENT`

**Optional.** `Dict[str, str]`. Default: `{}`

An array of environment variables that will be accessible from the function.

## Commands

### poetry ycf-deploy

The deployment command initiates the deployment process, which is divided into several stages. Progress updates are displayed in the console.

```bash
$ poetry ycf-deploy
poetry-ycf-plugin: Launched deploying YCF "d4e0jp3jpnbrct06fogq": new release "poetry-ycf-plugin 0.0.0"
poetry-ycf-plugin: Authorization
poetry-ycf-plugin: Building
poetry-ycf-plugin: Uploading
poetry-ycf-plugin: Releasing
poetry-ycf-plugin: Cleaning
```

VERBOSE

```bash
$ poetry ycf-deploy
poetry-ycf-plugin: Launched deploying YCF "d4e0jp3jpnbrct06fogq": new release "poetry-ycf-plugin 0.0.0"
poetry-ycf-plugin: Authorization
poetry-ycf-plugin: Authorization | Created temporary AWSAccessKey: ajero9nn021apdpgn452
poetry-ycf-plugin: Building
poetry-ycf-plugin: Building | File added: poetry_ycf_plugin/deploy_manager.py
poetry-ycf-plugin: Building | File added: poetry_ycf_plugin/responses.py
poetry-ycf-plugin: Building | File added: poetry_ycf_plugin/plugins.py
poetry-ycf-plugin: Building | File added: poetry_ycf_plugin/commands.py
poetry-ycf-plugin: Building | File added: poetry_ycf_plugin/utils.py
poetry-ycf-plugin: Building | File added: poetry_ycf_plugin/__init__.py
poetry-ycf-plugin: Building | File added: poetry_ycf_plugin/config.py
poetry-ycf-plugin: Building | File added: poetry_ycf_plugin/exceptions.py
poetry-ycf-plugin: Building | File added: temporary requirements.txt
poetry-ycf-plugin: Building | Builded zip for uploading: /{full_path}}/dist/YC/ycf-releases/d4e0jp3jpnbrct06fogq-poetry-ycf-plugin-0-0-0.zip
poetry-ycf-plugin: Uploading
poetry-ycf-plugin: Uploading | Release uploaded to S3: releases-ycf -> ycf-releases/d4e0jp3jpnbrct06fogq-poetry-ycf-plugin-0-0-0.zip
poetry-ycf-plugin: Releasing
poetry-ycf-plugin: Cleaning
poetry-ycf-plugin: Cleaning | Deleted temporary AWSAccessKey: ajero9nn021apdpgn452
```

## Use cases

### Deploying a Python Yandex Cloud Function with GitLab CI/CD

In the CI/CD settings of your repository, create a variable named `YCF_AUTHORIZED_KEY` with the type set to `File`. You can obtain this file from the service account settings in Yandex Cloud: <https://yandex.cloud/docs/iam/concepts/authorization/key>.

.gitlab-ci.yml:

```yaml
pypi:
  stage: publishing
  image: rocshers/python-poetry:3.12.4-slim-1.8.3
  tags:
    - docker
  script:
    - poetry self add poetry-ycf-plugin
    - poetry ycf-deploy
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/poetry-ycf-plugin/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/poetry-ycf-plugin>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
