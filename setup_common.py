import shutil
import os

from setuptools import setup, find_packages
from setuptools.command.install import install
from Cython.Build import cythonize
from Cython.Distutils import build_ext


def list_files(path, ext, exclude):
    file_list = []

    for f in os.listdir(path):
        filepath = os.path.join(path, f)

        if os.path.isdir(filepath):
            file_list += list_files(filepath, ext, exclude)
        elif filepath.endswith(ext):
            if not f in exclude:
                print('{}'.format(filepath))
                file_list.append(filepath)

    return file_list


def rm_files(path, ext, exclude):
    files = list_files(path, ext, exclude)

    for f in files:
        os.remove(f)


class BuildExt(build_ext):

    def run(self):
        build_ext.run(self)

        package_dir = self.distribution.get_name()
        init_files = list_files(package_dir, '__init__.py', [])

        for f in init_files:
            dst = os.path.join(self.build_lib, os.path.dirname(f))
            print(f, dst)
            shutil.copy(f, dst)


class InstallExt(install):

    def run(self):
        install.run(self)

        self.configure()

    def configure(self):
        print('Configure...')
