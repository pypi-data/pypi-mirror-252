from setuptools import setup, find_packages

import carton


setup(
    name='engiwiz-django-carton',
    version=carton.__version__,
    description=carton.__doc__,
    packages=find_packages(),
    url='https://github.com/engiwiz/engiwiz-django-carton',
    author='unkana',
    include_package_data=True,
)
