from cleo.io.outputs.output import Verbosity
from poetry.console.commands.command import Command

from poetry_ycf_plugin import config
from poetry_ycf_plugin.deploy_manager import DeployManager
from poetry_ycf_plugin.exceptions import plugin_exception_wrapper


class YcfDeployCommand(Command):
    name = 'ycf-deploy'
    description = 'Deploy new release on YC function'

    def auth(self):
        self.io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Authorization')
        self.dm.auth()

        self.io.write_line(
            f'<b>{config.PLUGIN_NAME}</b>: Authorization | Created temporary AWSAccessKey: {self.dm.cfg.access_key_id}',
            Verbosity.VERBOSE,
        )

    def building(self):
        self.io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Building')
        self.dm.build()

        for included_file in self.dm.include_files:
            self.io.write_line(
                f'<b>{config.PLUGIN_NAME}</b>: Building | File added: {included_file}', Verbosity.VERBOSE
            )

        self.io.write_line(
            f'<b>{config.PLUGIN_NAME}</b>: Building | File added: temporary requirements.txt', Verbosity.VERBOSE
        )

        self.io.write_line(
            f'<b>{config.PLUGIN_NAME}</b>: Building | Builded zip for uploading: {self.dm.release_zip_path}',
            Verbosity.VERBOSE,
        )

    def uploading(self):
        self.io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Uploading')
        self.dm.upload()

        self.io.write_line(
            f'<b>{config.PLUGIN_NAME}</b>: Uploading | Release uploaded to S3: {self.dm.cfg.s3_bucket_name} -> {self.dm.release_zip_name}',
            Verbosity.VERBOSE,
        )

    def releasing(self):
        self.io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Releasing')
        self.dm.release()

    def cleaning(self):
        self.io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Cleaning')
        self.dm.clean()

        self.io.write_line(
            f'<b>{config.PLUGIN_NAME}</b>: Cleaning | Deleted temporary AWSAccessKey: {self.dm.cfg.access_key_id}',
            Verbosity.VERBOSE,
        )

    @plugin_exception_wrapper
    def handle(self) -> None:  # pragma: no cover
        self.io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Init', Verbosity.VERBOSE)

        self.dm = DeployManager(self.poetry)

        self.io.write_line(
            f'<b>{config.PLUGIN_NAME}</b>: Launched deploying YCF "{self.dm.cfg.id}": new release "{self.poetry.package.pretty_string}"'
        )

        try:
            self.auth()
            self.building()
            self.uploading()
            self.releasing()

        except BaseException as ex:
            try:
                self.cleaning()

            except BaseException:
                pass

            raise ex

        self.cleaning()
