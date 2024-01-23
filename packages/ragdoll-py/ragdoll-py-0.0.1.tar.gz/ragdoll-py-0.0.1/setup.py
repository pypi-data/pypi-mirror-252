import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ragdoll-py",
    version="0.0.1",
    author="Surya Dantuluri",
    author_email="s@sdan.io",
    description="Retrieval Augmented Generation for Language Modeling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sdan/ragdoll",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)