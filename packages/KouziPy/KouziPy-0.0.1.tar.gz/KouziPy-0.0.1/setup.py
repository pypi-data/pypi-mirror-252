from setuptools import find_packages, setup

with open("app/Readme.md", "r") as f:
    long_description = f.read()

setup(
    name="KouziPy",
    version="0.0.1",
    description="deep learning librairy",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Jérôme Delatour",
    author_email="kouzipy@gmail.com",
    license="MIT",
    classifiers=["License :: OSI Approved :: MIT License", "Programming Language :: Python :: 3.9", "Operating System :: Microsoft :: Windows :: Windows 11"],
)



"""classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9.1'
]

setup(
    name='KouziPy',
    version='0.0.1',
    url='',
    author='Jérôme Delatour',
    author_email='kouzipy@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Deep learning',
    packages=find_packages(),
    install_requires=['random','math']
)"""

#description='A deep learning librairy',
#long_description='All the explanations are on the KouziPy website',

#long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
#long_description_content_type='text/markdown'

