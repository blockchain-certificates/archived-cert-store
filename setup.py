import os

from pip.req import parse_requirements
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='cert-store',
    version='0.0.27',
    url='https://github.com/blockchain-certificates/cert-store',
    license='MIT',
    author='MIT Media Lab Blockchain Certificates',
    author_email='info@blockcerts.org',
    description='A library for retrieving blockchain certificates',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs
)
