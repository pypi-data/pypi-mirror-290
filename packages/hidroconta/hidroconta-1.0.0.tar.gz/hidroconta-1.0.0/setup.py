from setuptools import setup

setup(
    name='hidroconta',
    version='1.0.0',
    packages=['hidroconta'],
    install_requires=[
        'pandas',
        'requests',
        'datetime'
    ],
    author='JavierL',
    author_email='javier.lopez@hidroconta.com',
    description='API to easily access Demeter REST API provided by Hidroconta S.A.U.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)