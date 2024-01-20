from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.rst') as f:
    license = f.read()

setup(
    name='sportspicker',
    version='0.0.3',
    description='Update Me',
    long_description=readme,
    author='Peter D Bethke',
    author_email='pdbethke@siteshell.net',
    url='https://github.com/pdbethke/sportspicker',
    license=license,
    packages=find_packages(),
    include_package_data=True,
    package_dir={'sportspicker': 'sportspicker'},
    install_requires=[
        'django',
        'num2words',
        'django-solo',
        'requests',
        'django-select2',
        'django-classy-tags',
        'sportradar',
    ],
)
