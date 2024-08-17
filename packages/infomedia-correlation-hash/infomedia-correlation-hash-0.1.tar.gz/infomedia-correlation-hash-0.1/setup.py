from setuptools import setup

setup(
    name="infomedia-correlation-hash",
    version="0.1",
    description="A package to generate unique hashes using UUID.",
    py_modules=["infomedia-correlation-hash"],
    package_dir={'': '.'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
