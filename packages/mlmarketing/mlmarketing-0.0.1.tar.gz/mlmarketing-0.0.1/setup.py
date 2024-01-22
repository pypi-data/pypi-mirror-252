# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlmarketing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mlmarketing',
    'version': '0.0.1',
    'description': 'Machine Learning for Marketing',
    'long_description': '# Machine Learning for Marketing',
    'author': 'Thomas Pinder',
    'author_email': 'tompinder@live.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
