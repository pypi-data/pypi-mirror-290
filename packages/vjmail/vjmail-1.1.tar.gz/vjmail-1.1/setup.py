from setuptools import setup, find_packages

setup(
    name='vjmail',
    version='1.1',
    description='A simple library to centralize VJBots e-mails sendings.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Fioruci',
    author_email='fiorucit@example.com',
    url='https://github.com/Fioruci/vjmail',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
