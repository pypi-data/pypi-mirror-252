from setuptools import setup, find_packages
import sys
sys.path[0:0] = ['src/tallyerp']


setup(
    name='tallyerp',
    version='0.0.1',
    description='Tally ERP python',
    long_description='Tally ERP',
    author='muthugit',
    author_email='base.muthupandian@gmail.com',
    url='https://muthupandian.in',
    packages=(find_packages(where="src")),
    package_dir={"": "src"},
    requires=['requests', 'loguru', 'xsdata'],
)