import importlib
import os
import pkgutil
from argparse import ArgumentParser
from collections import ChainMap
from pathlib import Path, PosixPath
from types import ModuleType


class CLI:
    def __init__(self):
        self.commands = self.get_commands()
        self.parser = ArgumentParser()
        self.process_commands(self.parser.add_subparsers(dest='command'))

    def run(self) -> None:
        '''
        Run specified command.
        '''
        args = self.parser.parse_args().__dict__
        command = args.pop('command')
        if command is None:
            if len(self.commands) == 0:
                print('No commands available.')
                return

            print('Available commands:')
            command_names = self.get_commands().keys()
            for name in command_names:
                print(f"\t{name}")
            return

        self.commands[command].handle(**args)

    def process_commands(self, subparsers):
        '''
        Load all command classes and attach command parsers to subparser.
        '''
        for name, instance in self.commands.items():
            command_parser = subparsers.add_parser(name)
            instance.add_arguments(command_parser)

    def get_module_path(self, command_dir: PosixPath) -> str:
        '''
        Convert PosixPath into valid python module path.
        '''
        module = command_dir.as_posix().replace(Path(__file__).parents[2].as_posix(), '')
        return module.replace(os.sep, '.').lstrip('.')

    def load_command_class(self, module_name: str):
        '''
        Return instance of Command from module
        '''
        module = importlib.import_module(module_name)
        command_class = getattr(module, 'Command')
        return command_class()

    def find_commands(self, command_dir: PosixPath) -> dict[str, ModuleType]:
        '''
        Given a path to a command directory,
        return all commands that are available.
        '''
        module_name = self.get_module_path(command_dir)
        return {
            name: self.load_command_class(f'{module_name}.{name}')
            for _, name, is_pkg in pkgutil.iter_modules(path=[command_dir])
            if not is_pkg and not name.startswith('_')
        }

    def get_commands(self) -> dict[str, ModuleType]:
        '''
        Return dictionary mapping available command names to modules.
        '''
        command_dirs = Path(__file__).parents[1].rglob('commands')
        commands = [self.find_commands(dir) for dir in command_dirs]
        return dict(ChainMap(*commands))


def cli():
    CLI().run()