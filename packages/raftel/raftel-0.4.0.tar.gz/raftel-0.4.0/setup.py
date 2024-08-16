# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raftel']

package_data = \
{'': ['*']}

install_requires = \
['monochromap>=0.3.0', 's2sphere>=0.2.5', 'seaborn>=0.11.1', 'staticmap>=0.5.5']

setup_kwargs = {
    'name': 'raftel',
    'version': '0.4.0',
    'description': 'the easiest way to plot s2id',
    'long_description': '# Raftel\n\nRaftel is a library to easily plot s2id cell into map and other basic operation related to s2id mapping.\nBasicaly a thinly veiled wrapper of the excellent [s2sphere](https://github.com/sidewalklabs/s2sphere), the native python implementation of the outstanding [s2-geometry](https://github.com/google/s2geometry) package from Google, and simple mapping function using staticmap library.\n\n## Installation\nInstall directly from pyPI by running `pip install raftel`\n\n## Example\nFollow the example in the notebook for basic usage.\n',
    'author': 'M Iqbal Tawakal',
    'author_email': 'mit.iqi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mitbal/raftel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
