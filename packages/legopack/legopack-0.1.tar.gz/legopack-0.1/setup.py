from setuptools import setup, find_packages


setup(
    name='legopack',
    version='0.1',
    author='Remi Prince',
    description='',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "streamad"
    ],
    zip_safe=False
)
