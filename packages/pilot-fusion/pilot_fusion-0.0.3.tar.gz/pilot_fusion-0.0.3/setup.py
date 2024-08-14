from setuptools import setup, find_packages

setup(
    name='pilot-fusion',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'google-generativeai',
        'PyPDF2',
        'pandas',
        'openai',
        'anthropic',
        'mistralai',


    ],
    author='Piyush Kumar',
    author_email='piyush@pilot-tech.co',
    description='A package for generating code using various AI models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lishu-gupta-pilot-tech/pilot-py-hub',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
