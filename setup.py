"""A Python wrapper for Stanford CoreNLP's SUTime.

See:
nlp.stanford.edu/software/sutime.shtml
"""

from io import open
from os import path

from setuptools import setup
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='sutime',
    version='1.0.0rc2',
    description='A Python wrapper for Stanford CoreNLP\'s SUTime',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/FraBle/python-sutime',
    author='Frank Blechschmidt',
    author_email='contact@frank-blechschmidt.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords='stanford corenlp sutime datetime parser parsing nlp',
    packages=['sutime'],
    install_requires=[
        'JPype1>=0.6.0'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'aniso8601',
        'pytest',
        'python-dateutil'
    ],
    package_data={
        'sutime': [
            'jars/stanford-corenlp-sutime-python-1.1.0.jar'
        ],
    },
    package_dir={'sutime': 'sutime'},
    include_package_data=True,
    zip_safe=False
)
