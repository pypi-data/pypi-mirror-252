from setuptools import setup, find_packages

setup(
    name='pydemography',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.26.3',
        'pandas>=2.2.0',
        'seaborn>=0.13.1',
        'matplotlib>=3.8.2',
        'patsy>=0.5.6',
        'statsmodels>=0.14.1',
        'scipy>=1.12.0',
        'statsmodels>=0.14.1'
    ]
)