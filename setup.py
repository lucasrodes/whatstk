"""setup script"""
import configparser
from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [req.strip() for req in f.readlines()]


setup(
    name='whatstk',
    version="0.1.0",
    description="Parser and analytics tools for WhatsApp group chats",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/lucasrodes/whatstk',
    author='Lucas Rodes-Guirao',
    author_email='hi@lcsrg.me',
    license='MIT',
    install_requires=requirements,
    packages=["whatstk"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
