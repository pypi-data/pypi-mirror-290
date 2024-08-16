from setuptools import setup, find_packages

setup(
    name='cymulate-oauth2-client',
    version='1.0.0',
    description='A Python client for OAuth2 authentication with Cymulate API',
    author='Cymulate',
    author_email='roys@cymulate.com',
    url='https://github.com/royscymulate/Cymulate-Oauth2-Client',
    packages=find_packages(),
    install_requires=[
        'requests>=2.20.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
