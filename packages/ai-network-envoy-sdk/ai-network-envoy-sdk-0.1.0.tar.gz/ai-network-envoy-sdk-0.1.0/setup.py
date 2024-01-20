# setup.py
from setuptools import setup, find_packages

setup(
    name='ai-network-envoy-sdk',
    version='0.1.0',
    description='SDK for AI Network P2P message, dataset, mdoel, file sharing system',
    author='kmh4500',
    author_email='kimminhyun@comcom.ai',
    packages=find_packages(),
    install_requires=[
        'grpcio',
        'grpcio-tools'
        # Any other dependencies
    ],
)
