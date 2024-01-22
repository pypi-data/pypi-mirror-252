# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aia_utils', 'aia_utils.model', 'aia_utils.repositories']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.1,<7.0.0',
 'confluent-kafka>=2.3.0,<3.0.0',
 'coverage>=7.3.2,<8.0.0',
 'html2image>=2.0.4,<3.0.0',
 'pillow>=10.2.0,<11.0.0',
 'pymongo>=4.6.1,<5.0.0',
 'tomli>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'aia-utils',
    'version': '0.1.12',
    'description': '',
    'long_description': None,
    'author': 'Edgar Sánchez',
    'author_email': 'edgar.sanchez@mercadolibre.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
