from setuptools import setup, find_packages

# Read requirements.txt and store its contents in the 'requirements' variable
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='AssayingAnomalies',
    version='1.2.1',
    author='Joshua Lawson',
    author_email='jlaws13@simon.rochester.edu',
    description='A brief description of your package',
    packages=find_packages(),
    install_requires=requirements,
    long_description='Package installed successfully. Please run \'setup_library\' to configure your settings and begin ' \
                                                                               'using the toolkit'

)