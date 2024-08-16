from setuptools import setup, find_packages

setup(
    name='fdds',
    version='0.1.0',
    author='Arif Hussain',
    author_email='starrvarse@gmail.com',
    description='Fast Dynamic Database System (FDDS)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/starrvarse/fdds-software',
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.2',
        'cryptography==41.0.3',
        'pytest==7.4.0',
        'pandas==2.0.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
