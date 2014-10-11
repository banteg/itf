from setuptools import setup

setup(
    name='itf',
    version='1.2.0',
    description='Download iTunes Festival London 2014 Streams',
    url='https://gist.github.com/banteg/105bfb581bfa5c738312',
    py_modules=['itf'],
    install_requires=['requests'],
    entry_points={
        'console_scripts': ['itf = itf:main'],
    }
)
