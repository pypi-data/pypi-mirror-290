from setuptools import setup, find_packages

setup(
    name='iAppflyer',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'iAppflyer = iAppflyer.app:main_function',
        ],
    },
)
