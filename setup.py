from setuptools import find_packages, setup


setup(
    name="reference-models",
    packages=find_packages(),
    version="0.1",
    install_requires=[
        "cmdstanpy",
        "pandas",
        "scikit-learn",
    ],
)
