from setuptools import setup, find_packages

with open('Readme.md', 'r') as f:
    read_me = f.read()

setup(
    name='mrn-behave',
    version='1.0.0',
    description='behavioral modeling for MRN paper',
    long_description=read_me,
    long_description_content_type='text/markdown',
    url='https://github.com/jeremyschroeter/mrn-behave',
    author='Jeremy Schroeter',
    author_email='jeremyschroeter@gmail.com',
    install_requires=[
        'numpy==1.26.4',
        'scipy==1.13.1',
        'scikit-learn==1.5.1',
        'matplotlib==3.8.4',
        'pytorch==2.4.0'
    ]
)