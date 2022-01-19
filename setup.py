from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Human-readable phrase id generator'
LONG_DESCRIPTION = 'A human-readable id generator that randomly generates nouns or adjective-noun pairs'

setup(
    name='readableidgen',
    version=VERSION,
    author='Stefan/Yuzhao Heng',
    author_email='stefan.hg@outlook.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['colorama', 'numpy'],
    keywords=['python', 'id', 'generator', 'nlp'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: MacOS X',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ]
)
