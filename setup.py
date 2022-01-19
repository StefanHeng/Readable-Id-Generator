from setuptools import setup, find_packages

VERSION = '0.1.4'
DESCRIPTION = 'Human-readable phrase id generator'
LONG_DESCRIPTION = 'A human-readable id generator that randomly generates nouns or adjective-noun pairs'

setup(
    name='readableidgen',
    version=VERSION,
    license='MIT',
    author='Stefan/Yuzhao Heng',
    author_email='stefan.hg@outlook.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/StefanHeng/Readable-Id-Generator',
    download_url='https://github.com/StefanHeng/Readable-Id-Generator/archive/refs/tags/v0.1.tar.gz',
    packages=find_packages(),
    # packages=['readableidgen'],
    # package_dir={'readableidgen': 'readableidgen'},
    # package_data={'readableidgen': ['corpus/*.txt']},
    include_package_data=True,
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
