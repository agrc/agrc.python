from distutils.core import setup

setup(
    name='agrc',
    version='1.1.2',
    author='Scott Davis',
    author_email='Scott Davis',
    packages=['agrc', 'agrc.test'],
    url='https://github.com/agrc/agrc.python',
    license='LICENSE.txt',
    description='A collection of python modules that make life easier for us at AGRC.',
    long_description=open('README.txt').read(),
    install_requires=[
        'requests >= 2.8.1'
    ]
)
