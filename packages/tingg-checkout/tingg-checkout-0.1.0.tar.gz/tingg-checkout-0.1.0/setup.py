from setuptools import setup, find_packages

VERSION = '0.1.0'

setup(
    name='tingg-checkout',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'pycryptodome',
    ],
    author='Muracia Ndungu',
    author_email='platforms@cellulant.io',
    description='A package to help you streamline your integration to the Tingg Checkout API',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ],
)