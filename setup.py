from setuptools import setup,find_packages
from setuptools.command.install import install
from setup_common import BuildExt,InstallExt
from setup_common import list_files
from configure_package import configure
import leomp3
from Cython.Build import cythonize
from Cython.Distutils import build_ext

class LeoMP3Install(install):

    def run(self):
        install.run(self)
        configure()

enable_cythonize=False
py_files = list_files('leomp3','.py',['__init__.py'])

if enable_cythonize:
    setup(name="leomp3",
          version=leomp3.__version__,
          description="Leo MP3 Player",
          url='',
          author='',
          author_email='',
          license='Proprietary',
          cmdclass={
              'install': LeoMP3Install,
              'build_ext': BuildExt
          },
          scripts=['bin/leomp3'],
          packages=find_packages(),
          ext_modules=cythonize(py_files, build_dir='leomp3-cy'),
          zip_safe=False)
else:
    setup(name="leomp3",
          version=leomp3.__version__,
          description="Leo MP3 Player",
          url='',
          author='',
          author_email='',
          license='Proprietary',
          cmdclass={
              'install': LeoMP3Install,
              'build_ext': BuildExt
          },
          scripts=['bin/leomp3'],
          packages=find_packages(),
          zip_safe=False)
