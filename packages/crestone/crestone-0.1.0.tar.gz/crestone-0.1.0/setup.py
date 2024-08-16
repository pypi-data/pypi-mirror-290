from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='crestone',
    version='0.1.0',
    author='Jacob Weiss',
    author_email='jaweiss2305@gmail.com',
    description='A CLI app for Crestone',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jacobweiss2305/crestone',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'crestone=crestone.cli:cli',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)