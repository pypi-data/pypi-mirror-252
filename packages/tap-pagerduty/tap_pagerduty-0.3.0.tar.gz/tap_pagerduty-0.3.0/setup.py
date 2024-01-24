import setuptools


setuptools.setup(
    name='tap_pagerduty',
    author='David Wallace',
    author_email='david.wallace@goodeggs.com',
    version='0.3.0',
    url='https://github.com/goodeggs/tap-pagerduty',
    description='Singer.io tap for extracting data from Pagerduty v2 API',
    long_description='',
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords="singer tap python pagerduty",
    license='GPLv3',
    packages=setuptools.find_packages(exclude=['tests']),
    package_data={
        'tap_pagerduty': ['schemas/*.json']
    },
    install_requires=[
        'requests==2.31.0',
        'singer-python==6.0.0'
    ],
    extras_require={
        'dev': [
            'pylint',
            'ipdb'
        ]
    },
    entry_points={
        'console_scripts': ['tap-pagerduty = tap_pagerduty:main']
    }
)
