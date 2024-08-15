from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name='stemmer',
    version='0.0.4',
    author='semantic_solver',
    author_email='semanticsolver@gmail.com',
    description='This is my first module',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/semantic-search-az/stemmer-az',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
    include_package_data=True,
)