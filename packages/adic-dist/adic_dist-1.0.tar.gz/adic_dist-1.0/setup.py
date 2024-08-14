from setuptools import setup

setup(
    name='adic_dist',
    version='1.0',
    description='A package for Gaussian and Binomial distributions',
    author='Adithya Chintala',
    packages=['adic_dist'],
    install_requires=[
        'matplotlib',
    ],
    zip_safe=False
)
