from setuptools import setup, find_packages

setup(
    name='bnirs_algorithms',
    version='0.3.6',
    description='Python implementations of common bNIRS algorithms',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Archie Barraclough',
    author_email='a.barraclough@outlook.com',
    url='https://github.com/barraca07/bnirs_algorithms',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'bnirs_algorithms': ['values.csv'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy',
        'pandas',
    ]
)