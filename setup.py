# -*- coding: UTF-8 -*-

from setuptools import setup

setup(
    name='wpydumps',
    version='0.0.1',
    author='Baptiste Fontaine',
    author_email='b@ptistefontaine.fr',
    py_modules=['wpydumps'],
    url='https://github.com/bfontaine/wpydumps',
    license='MIT License',
    description='Work with Wikipedia dumps',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "libarchive",
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
