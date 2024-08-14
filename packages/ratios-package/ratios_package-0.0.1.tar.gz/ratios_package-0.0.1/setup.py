from setuptools import setup, find_packages

setup(
    name='ratios_package',
    version='0.0.1',
    author='Bill Jiang',
    author_email='bcv0906@gmail.com',
    packages=find_packages(),  # Automatically find all packages in the current directory
    install_requires=[
        'pandas',
        'dash', 
    ],
    description='A package for calculating and analyzing financial ratios',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/billjiang-git/financial_ratios',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
