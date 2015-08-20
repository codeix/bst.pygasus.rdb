
from setuptools import setup, find_packages
import os

version = '0.1'

def read(*rnames):
        return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.rst')
    + '
' +
    'Contributors
'
    '============
'
    + '
' +
    read('docs', 'CONTRIBUTORS.txt')
    + '
' +
    read('docs', 'CHANGES.txt')
    + '
')

setup(
      name='bst.pygasus.rdb',
      version=version,
      description='This is the first version of bst.pygasus.rdb',
      long_description=long_description,
      keywords='',
      author='Thomas Oexl',
      author_email='thomas.oexl@biel-bienne.ch',
      url='nourl',
      license='ZPL',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data = True,
      namespace_packages=['bst.pygasus'],
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      """,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      )
