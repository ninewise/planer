"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# I don't have a long description (yet)
#with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#    long_description = f.read()

version_scope = {}
with open("./planer/version.py") as version_file:
    exec(version_file.read(), version_scope)

setup(
    name='planer',
    version=version_scope["__version__"],
    description='A plat calendar application',
    #long_description=long_description,
    url='https://github.com/FelixVanderJeugt/planer',
    author='Felix Van der Jeugt',
    author_email='felix.vanderjeugt@gmail.com',
    license='MIT',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        #'Environment :: Console :: Curses', not yet
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop', # well, some of them
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        # 'Operating System :: POSIX', I'll try, but I can't promise yet.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4', # That's what it's tested on.
        'Topic :: Office/Business :: Scheduling',
    ],
    keywords='planer planner calendar',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'sortedcontainers',
        'pony',
        'pyxdg',
        'Flask',
    ],
    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'planer': ['config/planer.conf']
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'planer-daemon=planer.daemon:main',
            'planer-remote=planer.remote:main'
        ],
    },
)
