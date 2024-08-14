from setuptools import setup, find_packages

with open('Readme.md', 'r') as f:
    read_me = f.read()

setup(
    name='mrn_behave',
    version='0.0.3',
    packages=find_packages(include=['data', 'disrnn', 'linear_switching', 'logistic_regrssion']),
    description='behavioral modeling for MRN paper',
    long_description=read_me,
    long_description_content_type='text/markdown',
    url='https://github.com/jeremyschroeter/mrn-behave',
    author='Jeremy Schroeter',
    author_email='jeremyschroeter@gmail.com',
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn',
        'matplotlib',
        'torch',
        'pyyaml'
    ]
)