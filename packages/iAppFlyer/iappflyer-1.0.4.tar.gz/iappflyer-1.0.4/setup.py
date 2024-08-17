from setuptools import setup, find_packages

setup(
    name='iAppflyer',
    version='1.0.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'iAppFlyer = iAppflyer.app:main_function',
        ],
    },
)
