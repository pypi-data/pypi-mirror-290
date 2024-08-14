# setup.py

from setuptools import setup, find_packages

setup(
    name="custom_linear_model",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mlflow>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "linear-model-predict=custom_model.linear_model:LinearModel",
        ],
    },
)
