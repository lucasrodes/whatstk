"""setup script."""


from setuptools import setup, find_packages
import os
import glob


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf8') as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'requirements.txt')) as f:
    requirements = f.readlines()

with open(os.path.join(this_directory, 'requirements-test.txt')) as f:
    requirements_test = f.readlines()

with open(os.path.join(this_directory, 'requirements-flake.txt')) as f:
    requirements_flake = f.readlines()

with open(os.path.join(this_directory, 'requirements-docs.txt')) as f:
    requirements_docs = f.readlines()

requirements_gdrive = [
    "PyDrive2~=1.15.0",
    "PyYAML~=6.0",
]

requirements_generate = [
    "scipy~=1.10.0",
    "python-lorem==1.2.0",
]

requirements_full = requirements_gdrive + requirements_generate


extras_require = {
    "gdrive": requirements_gdrive,
    "generate": requirements_generate,
    "full": requirements_full,
    "dev": requirements_test + requirements_flake + requirements_docs,
}


setup(
    name='whatstk',
    version="0.6.0",
    description="Parser and analytics tools for WhatsApp group chats",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/lucasrodes/whatstk',
    author='Lucas Rodes-Guirao',
    license='GPL-v3',
    install_requires=requirements,
    packages=find_packages('.'),
    package_dir={'': '.'},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob.glob('./*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords='whatsapp analysis parser chat',
    project_urls={
        'Documentation': 'https://whatstk.readthedocs.io/en/stable/',
        'Github': 'http://github.com/lucasrodes/whatstk',
        'Bug Tracker': 'https://github.com/lucasrodes/whatstk/issues',
    },
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'whatstk-generate-chat=whatstk.scripts.generate_chats:main',
            'whatstk-to-csv=whatstk.scripts.txt_to_csv:main',
            'whatstk-graph=whatstk.scripts.graph:main'
        ]
    },
    package_data = {
        'whatstk': ['whatsapp/assets/header_format_support.json'],
    },
    extras_require=extras_require,
)
