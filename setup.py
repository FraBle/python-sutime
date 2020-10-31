"""A Python wrapper for Stanford CoreNLP's SUTime.

See:
nlp.stanford.edu/software/sutime.shtml
"""

from io import open
from os import path

from setuptools import setup
THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='sutime',
    version='1.0.0',
    description='A Python wrapper for Stanford CoreNLP\'s SUTime',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/FraBle/python-sutime',
    author='Frank Blechschmidt',
    author_email='contact@frank-blechschmidt.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords='stanford corenlp sutime datetime parser parsing nlp',
    packages=['sutime'],
    install_requires=[
        'JPype1>=1.1.2'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'aniso8601>=8.0.0',
        'pytest>=6.1.2',
        'python-dateutil>=2.8.1'
    ],
    package_data={
        'sutime': [
            'jars/stanford-corenlp-sutime-python-1.4.0.jar'
        ],
    },
    package_dir={'sutime': 'sutime'},
    include_package_data=True,
    zip_safe=False
)
