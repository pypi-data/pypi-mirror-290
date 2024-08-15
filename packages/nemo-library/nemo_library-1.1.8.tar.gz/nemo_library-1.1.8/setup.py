import os
from setuptools import setup, find_packages

# Absoluten Pfad zu requirements.txt ermitteln
base_dir = os.path.abspath(os.path.dirname(__file__))
requirements_path = os.path.join(base_dir, 'requirements.txt')

# Inhalte der requirements.txt lesen
with open(requirements_path) as f:
    required = f.read().splitlines()

setup(
    name='nemo_library',
    version='1.1.8',
    packages=find_packages(),
    install_requires=required,
    author='Gunnar Schug',
    author_email='GunnarSchug81@gmail.com',
    description='A library for uploading data to and downloading reports from NEMO cloud solution',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',    
    classifiers=[
        'Programming Language :: Python :: 3.12',
    ],
    project_urls={
        'Github': 'https://github.com/H3rm1nat0r/nemo_library',  
        'NEMO': 'https://enter.nemo-ai.com/nemo/'
    }
)