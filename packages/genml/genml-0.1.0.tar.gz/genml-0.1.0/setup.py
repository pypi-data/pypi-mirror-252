from setuptools import setup, find_packages

setup(
    name='genml',
    version='0.1.0',
    description='A Python package for generating Mittag-Leffler noise',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.16.0',  
        'tqdm>=4.29.1',    
        'scipy>=1.2.0',    
        'matplotlib>=3.0.2' 
    ],
    python_requires='>=3.6', 
)