import os

from setuptools import setup, find_packages

import alfredo

ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(ROOT, 'README.rst')) as file_obj:
    long_description = file_obj.read()

setup(
    name='alfredo-py',
    version=alfredo.__version__,
    description=long_description.splitlines()[0],
    long_description=long_description,
    keywords='alfredo python sdk',
    url='https://github.com/rstorsauce/alfredo-python-sdk',
    license='LGPL 2.1',
    author='RStor',
    author_email='christopher@rstor.io',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'requests',
        'ruamel.yaml',
        'docopt',
    ],
    entry_points={
        'console_scripts': [
            'alfredo=alfredo.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
