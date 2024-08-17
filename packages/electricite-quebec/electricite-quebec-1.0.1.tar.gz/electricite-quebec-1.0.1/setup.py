from setuptools import setup, find_packages

setup(
    name='electricite-quebec',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.1.5',
        'requests>=2.25.1'
    ],
    author='Behdad Ehsani',
    author_email='behdad.ehsani@hec.ca',
    description='A Python package to fetch data from Hydro Quebec API.',
    keywords='hydro quebec api electricity data',
    url='https://electricite-quebec.info/',  # Optional project URL
)
