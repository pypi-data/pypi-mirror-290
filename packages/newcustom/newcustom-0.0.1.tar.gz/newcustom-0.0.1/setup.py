from setuptools import setup

setup(
    name='newcustom',  
    version='0.0.1',  
    description='A Python package for NLP tasks and utilities',
    url='https://github.com/KavyaGJS/nlppack',  
    author='KavyaGJS', 
    author_email='kavyamujk@gmail.com',  
    packages=['newcustom'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=["click", "pytz"]
)
