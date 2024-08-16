from setuptools import setup, find_packages

setup(
    name='easy-selenium-automation',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'selenium',
    ],
    description='A simple library to simplify Selenium automations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='TonDevPy',    
    url='https://github.com/tondevpy',  
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
