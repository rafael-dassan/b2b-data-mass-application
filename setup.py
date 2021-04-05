import re
from os.path import dirname, join
from setuptools import find_packages, setup

with open(join(dirname(__file__), "data_mass", "__init__.py")) as fp:
    for line in fp:
        m = re.search(r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line)
        if m:
            version = m.group(2)
            break
    else:
        raise RuntimeError("Unable to find own __version__ string")

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

extras = {
    "testing": [
        "pytest>=4.4.0",
        "pytest-xdist==1.31.0",
        "pytest-cov==2.8.1",
        "flake8==3.7.9",
    ]
}

setup(
    name="data_mass",
    version=version,
    author="BEES Community",
    maintainer="Data Mass Team",
    description="Data generation.",
    long_description=long_description,
    project_urls={
        "Documentation": "https://ab-inbev.atlassian.net/wiki/spaces/PKB/pages/2175860865/Data+Mass",
        "Repository": "https://dev.azure.com/ab-inbev/GHQ_B2B_Delta/_git/b2b-data-mass-application",
        "Standards": "https://anheuserbuschinbev.sharepoint.com/sites/b2bengineering/architecture/SitePages/Data-Mass-Application.aspx",
        "Release Notes": "https://anheuserbuschinbev.sharepoint.com/:b:/s/b2bengineering/EaTlUWEzsp1EqdmKaqBclL4ByT6uvxDV1nF1erEOsD-stQ?e=QQyxU8",
    },
    packages=find_packages(),
    package_data={
        "data_mass": [
            "data/*.json",
            "mass_populator/country/data/*.csv",
            "mass_populator/country/data/ar/*.csv",
            "mass_populator/country/data/br/*.csv",
            "mass_populator/country/data/ca/*.csv",
            "mass_populator/country/data/co/*.csv",
            "mass_populator/country/data/do/*.csv",
            "mass_populator/country/data/ec/*.csv",
            "mass_populator/country/data/mx/*.csv",
            "mass_populator/country/data/pa/*.csv",
            "mass_populator/country/data/pe/*.csv",
            "mass_populator/country/data/py/*.csv",
            "mass_populator/country/data/ar/*.csv",
        ]
    },
    install_requires=requirements,
    extras_require=extras,
    python_requires=">=3.7.0",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
