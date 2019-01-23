import os

from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open('requirements.txt', 'r') as f:
    require_list = f.read().splitlines()

version = '1.0.0'

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-rest-client',
    version=version,
    description='Django rest client is a client to call other services.',
    author='lesliexlxiao',
    author_email='lesliexlxiao@163.com',
    url='https://github.com/lesliexlxiao/django-rest-client',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=require_list
)
