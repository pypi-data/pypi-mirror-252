from setuptools import find_packages, setup

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="kedro-expectations",
    version="0.4.0",
    url="https://gitlab.com/anacision/kedro-expectations.git",
    author="Marcel Beining",
    author_email="marcel.beining@anacision.de",
    description="Combine Kedro and Great Expectations. Based on work from Joao Gabriel Pampanin de Abreu.",
    long_description="Combine Kedro and Great Expectations",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    license="MIT",
    install_requires=[
        "kedro~=0.19",
        "kedro-datasets~=2.0",
        "great_expectations>=0.18.1",
        "pandas"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "kedro.global_commands": ["kedro-expectations = kedro_expectations:commands"]
    }
)
