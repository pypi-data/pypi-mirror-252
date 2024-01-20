from setuptools import setup, find_packages

setup(
    name='porte',
    version='0.0.2',
    description='handy python low level port scanner',
    author='LegacyObj',
    author_email='minjae@minj.ae',
    url='https://github.com/minj-ae/porte',
    install_requires=['asyncio', 'scapy',],
    packages=find_packages(exclude=[]),
    keywords=['porte', 'port scanner', 'LegacyObj', 'port', 'network'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': ['porte=porte.porte:__main__']
    },
)