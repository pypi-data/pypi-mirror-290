from setuptools import setup, find_packages

setup(
    name="backprompt",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "httpx"
    ],
    python_requires=">=3.7",
)