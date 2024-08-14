from setuptools import setup, find_packages

setup(
    name='SITS',
    packages=find_packages(where='sits'),
    package_dir={'': 'sits'},
    version='0.2',
    url='https://github.com/kenoz/SITS_utils',
    author='Kenji Ose',
    author_email='kenji.ose@ec.europa.eu',
    description='Create satellite time-series patches from STAC catalogs',
    install_requires=[],
)
