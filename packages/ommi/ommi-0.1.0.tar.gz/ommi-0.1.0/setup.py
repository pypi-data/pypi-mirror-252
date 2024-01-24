# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ommi', 'ommi.ext.drivers']

package_data = \
{'': ['*'], 'ommi': ['ext/*']}

install_requires = \
['tramp>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'ommi',
    'version': '0.1.0',
    'description': 'An object model mapper intended to provide a consistent interface for many underlying database implementations using whatever model implementations are desired.',
    'long_description': "# Ommi\n\n> [!CAUTION]\n> Ommi is under construction and much of the functionality is undergoing frequent revision. There is no guaratee future versions will be backwards compatible.\n\nAn object model mapper intended to provide a consistent interface for many underlying database implementations using whatever model implementations are desired.\n\n### Compatible Model Implementations\n\nMy test suite checks for compatibility with the following model implementations:\n\n- Python's `dataclass` model types\n- [Attrs](https://www.attrs.org/en/stable/comparison.html) model types\n- [Pydantic](https://docs.pydantic.dev/latest/) model types\n\n### Included Database Support\n\n- SQLite3 (⚠️Under Construction⚠️)\n",
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
