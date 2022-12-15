from setuptools import setup

install_requires = ['xlsxwriter', 'pypdf2', 'requests', 'PyYAML']

setup(
    #basic package data
    name = 'Export Report',
    version = '0.1',
    author = 'Shakeel Ansari',
    author_email = 'shakeel.ansari@gmail.com',
    license = '',
    url='https://github.com/shakeelansari63/python-exporter',
    description=(''),
    long_description='',
    keywords = ('export pdf xlsx'),
    classifiers = [],
    packages=['pyexport'],
    install_requires=install_requires,
)