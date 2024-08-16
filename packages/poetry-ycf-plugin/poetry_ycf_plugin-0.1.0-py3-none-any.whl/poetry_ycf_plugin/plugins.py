from __future__ import annotations

from cleo.io.io import IO
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry

from poetry_ycf_plugin.commands import YcfDeployCommand
from poetry_ycf_plugin.exceptions import plugin_exception_wrapper


class PoetryYcfPlugin(Plugin):
    """Плагин определения версии по гит тегу"""

    @plugin_exception_wrapper
    def activate(self, poetry: Poetry, io: IO):  # pragma: no cover
        return


class PoetryYcfApplicationPlugin(ApplicationPlugin):
    commands = [YcfDeployCommand]
