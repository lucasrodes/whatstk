"""setup script"""
import configparser
from setuptools import setup
import os

# this_directory = os.path.abspath(os.path.dirname(__file__))
this_directory = '/Users/lucasrodes/repos/whatstk'

with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [req.strip() for req in f.readlines()]

config = configparser.ConfigParser()
config.read(os.path.join(this_directory, 'version-info.cfg'))
version_number = config["version"]["number"]

setup(name='whatstk',
    version=version_number,
    description='Parser and analytics tools for WhatsApp group chats',
    long_description=long_description,
    url='http://github.com/lucasrodes/whatstk',
    author='Lucas Rodes-Guirao',
    author_email='hi@lcsrg.me',
    license='MIT',
    install_requires=requirements,
    packages=["whatstk"],
    zip_safe=False
)