from setuptools import setup, find_packages

setup(
   name='korean_financial_minute_data_miner',
   version='0.1',
   description='A module to mine minute-level data',
   author='Hyungjun Lim',
   author_email='sculd3@gmail.com',
   packages=find_packages(include=['ingest', 'fetch', 'util']),
   install_requires=['pandas'],
)
