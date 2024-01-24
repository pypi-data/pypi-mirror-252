from setuptools import find_packages, setup

with open("README.md", "r") as f:
    descriptionRead = f.read()

setup(
    name='KouziPy',
    version='0.0.2',
    package=find_packages(),
    description='A deep deep learning librairy',
    long_description=descriptionRead,
    long_description_content_type='text/markdown'
)

