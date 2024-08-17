from setuptools import setup

setup(
    name="infomedia-correlation-hash",
    version="0.2",
    description="A package to generate unique correlation hashes using UUID.",
    py_modules=["infomedia_correlation_hash"],
    package_dir={'': '.'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
