from setuptools import setup, find_packages

setup(
    name='iAppFlyer',
    version='1.0.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'iAppFlyer = iAppFlyer.app:main_function',
        ],
    },
)
