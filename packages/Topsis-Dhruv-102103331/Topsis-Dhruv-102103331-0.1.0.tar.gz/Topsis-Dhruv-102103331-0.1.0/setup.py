from setuptools import setup, find_packages

setup(
    name='Topsis-Dhruv-102103331',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'topsis-dhruv-102103331=Topsis_Dhruv_102103331.cli:main',
        ],
    },
)
