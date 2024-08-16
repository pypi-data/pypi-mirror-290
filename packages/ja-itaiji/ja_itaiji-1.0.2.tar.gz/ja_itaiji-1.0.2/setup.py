# Author: Kenta Ryuji Chiba <manchuria.museum@gmail.com>
# Copyright (c) 2024 Manchuria Museum
# License: BSD 3 clause

from setuptools import setup
import ja_itaiji

DESCRIPTION = "ja-itaiji: handling Japanese 異体字 (itaiji), which are variant forms of kanji characters"
NAME = 'ja-itaiji'
AUTHOR = 'Ryuji Chiba'
AUTHOR_EMAIL = 'manchuria.museum@gmail.com'
MAINTAINER = '満洲開拓資料館'
MAINTAINER_EMAIL = 'manchuria.museum@gmail.com'
URL = 'https://github.com/RjChiba/ja_itaiji'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/RjChiba/ja_itaiji'
VERSION = ja_itaiji.__version__
PYTHON_REQUIRES = ">=3.9"

PACKAGES = [
    'ja_itaiji'
]

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: Japanese',
    'Programming Language :: Python :: 3',
    'Topic :: Text Processing :: General',
]

with open('README.md', 'r') as fp:
    readme = fp.read()
long_description = readme

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      license=LICENSE,
      include_package_data=True,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )
