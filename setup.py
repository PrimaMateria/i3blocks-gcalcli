from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="i3blocks_gcalcli",
    version="0.0.1",
    description="Shows upcoming event in the status bar and full month when clicked on.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Topic :: Office/Business :: Scheduling",
    ],
    url="https://github.com/PrimaMateria/i3blocks-gcalcli",
    author="Matus Benko",
    author_email="matus.benko@gmail.com",
    license="MIT",
    packages=["i3blocks_gcalcli"],
    install_requires=[
        "click",
        "python-dateutil",
    ],
    entry_points={"console_scripts": ["i3blocks-gcalcli=i3blocks_gcalcli.cli:main"]},
    zip_safe=False,
    include_package_data=True,
)
