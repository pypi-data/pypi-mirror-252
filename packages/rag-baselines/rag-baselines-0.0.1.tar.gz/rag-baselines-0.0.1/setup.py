import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rag-baselines",
    version="0.0.1",
    author="Surya Dantuluri",
    author_email="s@sdan.io",
    description="Retrieval Augmented Generation Baselines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sdan/rag",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)