"""
Setup file for PYPI
"""
from setuptools import setup, find_packages

setup(
    name='NeuralNetToolkit',
    version='1.0.0',
    author='Paul Walcher',
    author_email='paulwalcher12@gmail.com',
    description='NeuralNetwork toolkit',
    packages=["NeuralNet", "NeuralNet.Layers", "NeuralNet.MNIST",
                "NeuralNet.Networks",
                "NeuralNet.Layers.Activation",
                "NeuralNet.Layers.Loss",
                "NeuralNet.Layers.Initializers",
             ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy>=1.26.2"
    ]
)