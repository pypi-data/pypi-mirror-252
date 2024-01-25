from argparse import ArgumentParser


class BaseCommand:
    def add_argument(self, parser: ArgumentParser) -> None:
        '''
        Add arguments to parser.
        '''
        return None
    
    def handle(self, **options):
        raise NotImplementedError(f'{self.__class__.__name__} must implement `.handle(self, **options)`')
