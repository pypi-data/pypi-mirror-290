from setuptools import setup, find_packages

setup(
    name='iAppFlyer',
    version='1.0.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'iAppFlyer = iAppFlyer.main:main_function',
        ],
    },
)
