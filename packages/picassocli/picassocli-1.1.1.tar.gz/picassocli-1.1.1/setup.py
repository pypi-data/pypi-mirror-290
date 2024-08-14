from setuptools import setup, find_packages
import subprocess

def get_version():
    try:
        # Fetch the latest Git tag
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], encoding='utf-8').strip()
        return tag
    except subprocess.CalledProcessError:
        # Return a default version if git fails
        return '0.0.0'

setup(
    name='picassocli', 
    version=get_version(),       
    description='A utility for constructing ANSI escape codes for terminal text styling.',
    long_description=open('README.md').read(),  # Long description from README file
    long_description_content_type='text/markdown',
    author='devinci-it',
    url='https://www.github.com/devinci-it/picassocli',  # Replace with your repo URL
    packages=find_packages(),  # List of packages to be included in the distribution),
    package_dir={'': '.'},  
    install_requires=[
        'huefy',  
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',  # Specify Python versions supported
)
