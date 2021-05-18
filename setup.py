from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as input_file:
    long_description = input_file.read()

setup(
    name='python-stopwatch',
    version='1.0.3',
    author='Jonghwan Hyeon',
    author_email='hyeon0145@gmail.com',
    description='A simple stopwatch for measuring code performance',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jonghwanhyeon/python-stopwatch',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='stopwatch profile',
    packages=find_packages(),
    install_requires=['termcolor'],
    python_requires='>=3.4',
)