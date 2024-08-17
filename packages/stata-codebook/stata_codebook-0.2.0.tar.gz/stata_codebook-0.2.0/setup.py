from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='stata_codebook',
    version='0.2.0',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        'pandas',
        'scipy'
    ],
    author='Mohsen Askar',
    author_email='ceaser198511@gmail.com',
    description='A Python package for generating comprehensive data summaries and statistics, similar to Stata\'s codebook command.',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    url='https://github.com/MohsenAskar'
)

