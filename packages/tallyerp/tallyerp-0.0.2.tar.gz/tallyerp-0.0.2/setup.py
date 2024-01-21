from setuptools import setup, find_packages
import sys
sys.path[0:0] = ['src/tallyerp']


setup(
    name='tallyerp',
    version='0.0.2',
    description='Tally ERP python',
    long_description='Tally ERP',
    author='citrisys',
    author_email='dev@citrisys.com',
    url='https://citrisys.com',
    packages=(find_packages(where="src")),
    package_dir={"": "src"},
    requires=['requests', 'loguru', 'xsdata'],
)