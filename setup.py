import setuptools

requirements = [
    "torchvision",
    "torch",
    "numpy",
    "pandas"
]

setuptools.setup(
    name='kaggle-protein-classification',
    description='source code for training',
    version="0.1",
    package_dir={'': 'src'},
    packages=setuptools.find_namespace_packages(where='src'))
    install_requires=requirements,
    author='Gordon MacMillan',
    author_email='gmacilla@ymail.com',
    license='BSD',
    platforms=['Linux'],
    python_requires='>=3.5.*',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
