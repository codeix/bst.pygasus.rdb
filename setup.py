
from setuptools import setup, find_packages
import os

version = '0.1-dev'


long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
      name='bst.pygasus.rdb',
      version=version,
      description='This is the first version of bst.pygasus.rdb',
      long_description=long_description,
      keywords='',
      author='Thomas Oexl',
      author_email='thomas.oexl@biel-bienne.ch',
      url='https://github.com/bielbienne/bst.pygasus.rdb',
      license='ZPL',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data = True,
      namespace_packages=['bst', 'bst.pygasus'],
      zip_safe=False,
      install_requires=[
          'setuptools',
          'SQLAlchemy'
      ],
      entry_points="""
      """,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'License :: OSI Approved :: Zope Public License',
          'Operating System :: OS Independent',
          'Development Status :: 4 - Beta'
      ]
      )
