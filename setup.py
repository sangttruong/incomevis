from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='incomevis',
    version='0.1',
    description='Visualization toolbox for income distribution',
    py_modules=['incomevis'],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires = [
        'matplotlib >= 3.0',
        'numpy >= 1.0',
        'pandas >= 1.0',
        'multiprocess >= 0.7',
        'ipython >= 5.5.0',
        'statsmodels >= 0.12.0'
    ],

    packages=find_packages("src"),  # include all packages under src
    package_dir={"": "src"},   # tell distutils packages are under src

    include_package_data=True,    # include everything in source control
    # extras_require = {
    #     'dev': [
    #         'pytest >= 3.7',
    #     ],
    # },

    url='https://github.com/sangttruong/incomevis',
    author='Sang T. Truong',
    author_email='sangtruong_2021@depauw.edu'
)

# python setup.py bdist_wheel sdist
# pip install --user -e .
# pip install twine
# twine upload dist/*
