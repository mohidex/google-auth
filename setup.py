from setuptools import setup, find_packages

setup(
    name='dj-google-auth',
    version='0.1',
    description='A simple library for working with google private data.',
    long_description=open('README.md').read(),
    author='Mohidul Islam',
    author_email='mohidul.cs@gmail.com',
    url='https://github.com/msi007/google-auth',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'google-auth-oauthlib',
        'requests',
        ],
    include_package_data=True,
    zip_safe=False,
)