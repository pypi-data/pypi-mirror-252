from distutils.core import setup
import setuptools
packages = ['txdpy']
setup(name='txdpy',
    version='6.7.8',
    author='唐旭东',
    packages=packages,
    package_dir={'requests': 'requests'},
    install_requires=[
        "lxml","loguru","redis","requests","tqdm","lxpy","colorama","xlrd","pymysql","xlsxwriter","selenium"
    ])