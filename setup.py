"""A Python wrapper for Stanford CoreNLP's SUTime.

See:
nlp.stanford.edu/software/sutime.shtml
"""

from setuptools import setup


setup(
    name='sutime',
    version='0.2.0',
    description='A Python wrapper for Stanford CoreNLP\'s SUTime',
    url='https://github.com/FraBle/python-sutime',
    author='Frank Blechschmidt',
    author_email='frank.blechschmidt@sap.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='stanford corenlp sutime datetime parser parsing nlp',
    packages=['sutime'],
    install_requires=[
        'JPype1'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'python-dateutil', 'aniso8601'],
    package_data={
        'sutime': [
            'jars/stanford-corenlp-sutime-python-1.0.0.jar'
        ],
    },
    package_dir={'sutime': 'sutime'},
    include_package_data=True,
    zip_safe=False
)
