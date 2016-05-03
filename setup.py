# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup, find_packages

print os.path.join(os.path.dirname(__file__), 'redtrics', '__init__.py')
with open(os.path.join(os.path.dirname(__file__), 'redtrics', '__init__.py')) as f:
    version = re.search("__version__ = '([^']+)'", f.read()).group(1)

with open('requirements.txt', 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name="redtrics",
    version=version,
    description="Redtrics generates metrics about the use of Github by developers.",
    license="MIT",
    long_description_markdown_filename='README.md',
    author="RedMart Ltd",
    author_email="oss@redmart.com",
    keywords="github metrics redmart commits size age",
    url="http://github.com/RedMart/redtrics",
    packages=find_packages(),
    install_requires=requires,
    setup_requires=['setuptools-markdown'],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        redtrics-generate = redtrics.cli.app:main
    """,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Topic :: Utilities",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
