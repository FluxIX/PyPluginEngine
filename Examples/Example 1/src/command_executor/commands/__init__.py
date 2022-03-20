from typing import Dict

from multiprocessing import RLock
from plugin_engine.plugin_importer import PluginImporter
from .command import Command
from . import plugins
from .plugins import _commands

_lock: RLock = RLock()
_plugin_importer: PluginImporter = None

def get_registered_commands() -> Dict[ str, Command ]:
    """
    Gets the registered commands.
    """

    global _lock, _plugin_importer

    with _lock:
        if _plugin_importer is None:
            _plugin_importer = PluginImporter( plugins )
            _plugin_importer.import_modules( recursive = True )

        return _commands
