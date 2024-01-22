from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='backwards_regression',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'statsmodels',
    ],
    entry_points={
        'console_scripts': [
            'your-command = backwards_regression.module:main',  # Replace with actual command and module path
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords='statistics modeling regression feature elimination engineering',
    python_requires='>=3.7',
    description='Backwards Regression Python Library - Automated feature selection in linear and logistic regression models.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kwadwo Daddy Nyame Owusu - Boakye',
    author_email='kwadwo.owusuboakye@outlook.com',
    url='https://github.com/knowusuboaky/backwards_regression',
    license='MIT',
)
