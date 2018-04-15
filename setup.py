"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

install_requires = ['matplotlib', 'numpy', 'seaborn', 'pandas', 'scipy', 'jupyter'],

setup(
    name='whatstk',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    # FIXME Is this version 0.x or 1.x?
    version='1.0.0',

    description='python analytical toolkit to analyse WhatsApp group chat logs '
                'using unsupervised learning',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/lucasrodes/whatstk',

    # Author details
    author='Lucas Rodés-Guirao',
    author_email='lucasrg@kth.se',

    # Choose your license
    license='GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      # FIXME What is the maturity of this project?
      'Development Status :: 4 - Beta',

      # Indicate who your project is intended for
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',

      # Pick your license as you wish (should match "license" above)
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'

      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      ###############################################################################
      # FIXME Are going to officially support Python 2.x? 
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      ###############################################################################
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      ],

    # What does your project relate to?
    keywords='whatsapp whatsapp-statistics whatsapp-group unsupervised-learning '
             'machine-learning self-organizing-map whatsapp-analysis '
             'whatsapp-parser',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['whatstk'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    # 'dev': ['check-manifest'],
    # 'test': ['coverage'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing
    # -additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    # 'console_scripts': [
    # 'sample=sample:main',
    # ],
    # },
    )
