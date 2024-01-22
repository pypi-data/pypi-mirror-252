# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biliarchiver',
 'biliarchiver.cli_tools',
 'biliarchiver.rest_api',
 'biliarchiver.utils']

package_data = \
{'': ['*'], 'biliarchiver': ['locales/*', 'locales/en/LC_MESSAGES/*']}

install_requires = \
['bilix==0.18.5',
 'browser-cookie3>=0.19.1,<0.20.0',
 'click-option-group>=0.5.6,<0.6.0',
 'click>=8.1.6,<9.0.0',
 'danmakuc>=0.3.6,<0.4.0',
 'internetarchive>=3.5.0,<4.0.0']

entry_points = \
{'console_scripts': ['biliarchiver = '
                     'biliarchiver.cli_tools.biliarchiver:biliarchiver']}

setup_kwargs = {
    'name': 'biliarchiver',
    'version': '0.1.8',
    'description': '',
    'long_description': '# biliarchiver\n\n> Archiving tool for Bilibili based on bilix\n\n[![PyPI version](https://badge.fury.io/py/biliarchiver.svg)](https://badge.fury.io/py/biliarchiver)\n\n## Install\n\n```bash\npip install biliarchiver\n```\n\n## Usage\n\n```bash\nbiliarchiver --help\n```\n\n### Basic usage\n\nFollow these steps to start archiving:\n\n1. Initialize a new workspace in current working directory:\n\n```bash\nbiliarchiver init\n```\n\n2. Provide cookies and tokens following instructions:\n\n```bash\nbiliarchiver auth\n```\n\n3. Download videos from BiliBili:\n\n```bash\nbiliarchiver down --bvids BVXXXXXXXXX\n```\n\n- This command also accepts a list of BVIDs or path to a file. Details can be found in `biliarchiver down --help`.\n\n4. Upload videos to Internet Archive:\n\n```bash\nbiliarchiver up --bvids BVXXXXXXXXX\n```\n\n- This command also accepts a list of BVIDs or path to a file. Details can be found in `biliarchiver up --help`.\n\n### Rest API\n\n1. Start server\n\n```bash\nbiliarchiver api\n```\n\n2. Add videos\n\n```bash\ncurl -X PUT -H "Content-Type: application/json" http://127.0.0.1:8000/archive/BVXXXXXX\n```\n\n## Develop\n\n### Install\n\nPlease use poetry to install dependencies:\n\n```sh\npoetry install\n```\n\nBuild English locale if necessary. Refer to the last section for details.\n\n### Run\n\n```sh\npoetry run biliarchiver --help\n```\n\n### Lint\n\n```sh\npoetry run ruff check .\n```\n\n### i18n\n\nTo generate and build locales, you need a GNU gettext compatible toolchain. You can install `mingw` and use `sh` to enter a bash shell on Windows.\n\nGenerate `biliarchiver.pot`:\n\n```sh\nfind biliarchiver/ -name \'*.py\' | xargs xgettext -d base -o biliarchiver/locales/biliarchiver.pot\n```\n\nAdd a new language:\n\n```sh\nmsginit -i biliarchiver/locales/biliarchiver.pot -o en.po -l en\n```\n\nUpdate a language:\n\n```sh\npnpx gpt-po sync --po biliarchiver/locales/en/LC_MESSAGES/biliarchiver.po --pot biliarchiver/locales/biliarchiver.pot\n```\n\n**(Important)** Build a language:\n\n```sh\nmsgfmt biliarchiver/locales/en/LC_MESSAGES/biliarchiver.po -o biliarchiver/locales/en/LC_MESSAGES/biliarchiver.mo\n```\n',
    'author': 'yzqzss',
    'author_email': 'yzqzss@yandex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
