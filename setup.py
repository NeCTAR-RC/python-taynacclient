#!/usr/bin/env python

import setuptools

from pbr.packaging import parse_requirements

entry_points = {
    'openstack.cli.extension':
    ['taynac = taynacclient.osc.plugin'],
    'openstack.taynac.v1':
    [
        'message send = taynacclient.osc.v1.messages:SendMessage',
    ]
}


setuptools.setup(
    name='taynacclient',
    version='1.0.0',
    description=('Client for the taynac system'),
    author='Sam Morrison',
    author_email='sorrison@gmail.com',
    url='https://github.com/NeCTAR-RC/python-taynacclient',
    packages=[
        'taynacclient',
    ],
    include_package_data=True,
    setup_requires=['pbr>=3.0.0'],
    install_requires=parse_requirements(),
    license="Apache",
    zip_safe=False,
    classifiers=(
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ),
    entry_points=entry_points,
)
