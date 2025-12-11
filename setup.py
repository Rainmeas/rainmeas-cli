from setuptools import setup, find_packages

setup(
    name="rainmeas",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "rainmeas=rainmeas.__main__:main",
        ]
    },
    install_requires=[],
    python_requires=">=3.6",
    author="Rainmeas Team",
    description="CLI tool for managing Rainmeter skin packages",
    keywords="rainmeter package manager cli",
)