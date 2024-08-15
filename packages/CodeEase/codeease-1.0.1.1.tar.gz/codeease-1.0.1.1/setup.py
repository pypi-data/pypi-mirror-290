from setuptools import setup, find_packages
import os
import codecs

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

# Corrected the open function call
with open("README.md", encoding="utf-8") as f:
    readme = f.read()

project_name = 'CodeEase'
version = '1.0.1.1'
author = 'Spark'
author_email = 'YIYUANChina@outlook.com'
description = 'CodeEase is from China and the developer is 16 years old.'

url = 'https://github.com/Spark-Code-China/CodeEase'
license = 'GPL-3.0'

install_requires = [
    'requests==2.32.3',
]

python_requires = '>=3.7'


setup(
    name=project_name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=readme,
    long_description_content_type='text/markdown',  # 添加这一行
    url=url,
    license=license,
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=python_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
    ],
)