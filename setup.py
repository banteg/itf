from setuptools import setup

setup(
    name='itf',
    version='2.1',
    description='Download Apple Music Festival 2015 Streams',
    url='https://github.com/banteg/itf',
    py_modules=['itf'],
    install_requires=['requests', 'click'],
    entry_points={
        'console_scripts': ['itf = itf:main'],
    }
)
