"""
" ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ████████╗██████╗  ██████╗ ███╗   ██╗
" ██║  ██║██║   ██║████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
" ███████║██║   ██║██╔████╔██║███████║   ██║   ██████╔╝██║   ██║██╔██╗ ██║
" ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║
" ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
" ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"
"                   Copyright (C) 2023 Humatron, Inc.
"                          All rights reserved.
"""

from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='humatron-python-sdk',
    version='1.0.1',
    author='Humatron',
    author_email='spec-support@humatron.ai',
    description='SDK library for Humatron developers',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://humatron.ai/build/api_reference',
    packages=[
        'humatron',
        'humatron/worker'
    ],
    install_requires=['locked-dict>=2023.10.22'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='Humatron python',
    python_requires='>=3.10'
)
