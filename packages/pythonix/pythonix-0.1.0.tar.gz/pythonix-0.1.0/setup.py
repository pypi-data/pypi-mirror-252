# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythonix',
 'pythonix.result',
 'pythonix.suffixes',
 'pythonix.suffixes.builtins',
 'pythonix.suffixes.itertools',
 'pythonix.suffixes.operators']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pythonix',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'jhok2013',
    'author_email': 'jhok2013@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
