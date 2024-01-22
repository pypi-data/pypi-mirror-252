# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['endf_parserpy', 'endf_parserpy.endf_recipes', 'endf_parserpy.fortsource']

package_data = \
{'': ['*'],
 'endf_parserpy.fortsource': ['backup/*',
                              'daniel_20220906/*',
                              'daniel_220808/*']}

install_requires = \
['appdirs>=1.4.0', 'lark>=1.0.0']

setup_kwargs = {
    'name': 'endf-parserpy',
    'version': '0.3.0',
    'description': "A package to read and write ENDF files'",
    'long_description': 'None',
    'author': 'Georg Schnabel',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
