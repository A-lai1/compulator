from setuptools import setup, find_packages

setup(
    name="Compulator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "compulator=compulator.main:run_compulator",
        ],
    },
    author="Alvin Lai",
    description="A terminal-based calculator that evaluates expressions, stores and retrieves formulas and constants.",
    long_description=open("README.md").read() if __name__ == "__main__" else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
    ],
    python_requires=">=3.11.5",

    include_package_data=True,
    package_data={
        "compulator.helpers": ["*.json"],
    },
)