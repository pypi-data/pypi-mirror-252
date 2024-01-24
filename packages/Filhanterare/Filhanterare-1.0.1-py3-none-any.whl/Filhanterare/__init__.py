import os, sys


__version__ = '1.0.1'


class FileManager:
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.appdata_path = self.get_appdata_path()


    def get_appdata_path(self):
        if sys.platform == 'win32':
            return os.path.join(os.getenv('APPDATA'), self.app_name)

        if sys.platform == 'darwin':
            return os.path.join(os.getenv('HOME'), 'Library', 'Application Support', self.app_name)

        if sys.platform == 'linux':
            return os.path.join(os.getenv('HOME'), '.local', 'share', self.app_name)

        raise NotImplementedError(f'Platform {sys.platform} is not supported.')

    def set_file(self, filename: str, data: str):
        with open(os.path.join(self.appdata_path, filename), 'w') as f:
            f.write(data)

    def get_file(self, filename: str):
        with open(os.path.join(self.appdata_path, filename), 'r') as f:
            return f.read()

    def file_exists(self, filename: str):
        return os.path.exists(os.path.join(self.appdata_path, filename))

    def create_file(self, filename: str, value: str = ''):
        if not self.file_exists(filename):
            self.set_file(filename, value)

    def create_dir(self, dirname: str):
        if not self.dir_exists(dirname):
            os.mkdir(os.path.join(self.appdata_path, dirname))

    def dir_exists(self, dirname: str):
        return os.path.exists(os.path.join(self.appdata_path, dirname))

    def create_files(self, file_list: dict):
        for filename, value in file_list.items():
            self.create_file(filename, value)
