# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.startup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mojo-startup',
    'version': '0.0.2',
    'description': 'Automation Mojo Startup Package',
    'long_description': "=======================\nmojo-startup\n=======================\nThis package setups up a pattern for extremely early pre-configuration settings and behaviors.\n\n===========\nDescription\n===========\nThis module does one thing very important.  It establishes the path for all other 'mojo' packages\non where to load default config from.  This is very important because it provides extensibility\nas early as possible in the running of any code.\n\nThe pattern established for defaults is that a variable is:\n* Variable is set to a hard coded default\n* startup configuration is checked for an override\n* the environment variables are checked for an override\n\n=================\nCode Organization\n=================\n* .vscode - Common tasks\n* development - This is where the runtime environment scripts are located\n* repository-setup - Scripts for homing your repository and to your checkout and machine setup\n* userguide - Where you put your user guide\n* source/packages - Put your root folder here 'source/packages/(root-module-folder)'\n* source/sphinx - This is the Sphinx documentation folder\n* workspaces - This is where you add VSCode workspaces templates and where workspaces show up when homed.\n\n==========\nReferences\n==========\n\n- `User Guide <userguide/userguide.rst>`\n- `Coding Standards <userguide/10-00-coding-standards.rst>`\n",
    'author': 'Myron W. Walker',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
