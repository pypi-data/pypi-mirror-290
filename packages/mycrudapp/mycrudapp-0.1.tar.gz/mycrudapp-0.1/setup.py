from setuptools import setup, find_packages

setup(
    name='mycrudapp',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'djangorestframework',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Operating System :: OS Independent',
    ],
)
