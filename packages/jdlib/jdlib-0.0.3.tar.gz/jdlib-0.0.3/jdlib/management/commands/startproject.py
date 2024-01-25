import os
from pathlib import Path

from jdlib import BASE_DIR, SECRET_KEY_INSECURE_PREFIX, get_random_secret_key
from jdlib.management.command import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('project_name')

    def handle(self, **options):
        template_dir = BASE_DIR / 'conf' / 'project_template'
        project_name = options['project_name']
        variable_map = {
            '{{ docs_version }}': '5.0',
            '{{ project_name }}': project_name,
            '{{ secret_key }}': SECRET_KEY_INSECURE_PREFIX + get_random_secret_key(),
        }

        if (Path.cwd() / project_name).exists():
            raise Exception('Project already exists.')

        prefix_length = len(str(template_dir)) + 1
        for root, dirs, files in os.walk(template_dir):
            relative_root = root[prefix_length:].replace('{{ project_name }}', project_name)

            for dir in dirs:
                if dir in ['.git', '__pycache__']:
                    continue

                if dir in variable_map.keys():
                    os.makedirs(Path.cwd() / relative_root / variable_map[dir])
                else:
                    os.makedirs(Path.cwd() / relative_root / dir)

            for file in files:
                if file.endswith(('.pyc', '.pyo', '.pyd', '.py.class', '.DS_Store')):
                    continue

                target_file = Path.cwd() / relative_root / file
                if target_file.suffix == '.py-tpl':
                    target_file = target_file.with_suffix('.py')

                with open(Path(root) / file, 'r') as old_file:
                    data = old_file.read()
                for var, val in variable_map.items():
                    data = data.replace(var, val)
                with open(target_file, 'w') as new_file:
                    new_file.write(data)
        