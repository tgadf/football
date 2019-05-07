from distutils.core import setup
import setuptools

setup(
  name = 'football',
  py_modules = ['espngames', 'penalty', 'playYards', 'summary', 'playAnalysis',
                'teamPlayers', 'debug', 'possession', 'playClock',
                'historical', 'playbyplay', 'playStart', 'analyzeYards',
                'gamePlayers', 'changePossession', 'downloadESPN',
                'analyzeKicking', 'analyzePenalties',
                'playTypes', 'driveSummary', 'analyzePossession'],
  version = '0.0.1',
  description = 'Football Game Parsing Package',
  long_description = open('README.md').read(),
  author = 'Thomas Gadfort',
  author_email = 'tgadfort@gmail.com',
  license = "MIT",
  url = 'https://github.com/tgadf/football',
  keywords = ['stats', 'football'],
  classifiers = [
    'Development Status :: 3',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
  ],
  install_requires=['utils==0.0.1'],
  dependency_links=['git+ssh://git@github.com/tgadf/utils.git#egg=utils-0.0.1']
)