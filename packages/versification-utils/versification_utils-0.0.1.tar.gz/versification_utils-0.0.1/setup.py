from setuptools import find_packages, setup

setup(
    name="versification_utils",
    version="0.0.1",
    packages=find_packages(),
    author="James Cuénod",
    author_email="j3frea+github@gmail.com",
    description="Tools to detect and convert between Bible versifications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jcuenod/versification_utils",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    package_data={
        "": ["standard_mappings/*.json", "diagnostics/vrs_diffs.yaml", "vref.txt"]
    },
    include_package_data=True,
)
