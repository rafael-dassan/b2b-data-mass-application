"""Package Installation."""
import re
from os.path import dirname, join
from subprocess import call

from setuptools import find_packages, setup
from setuptools.command.install import install

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

with open("README.md") as f:
    long_description = f.read()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        call(["pre-commit", "install"], shell=True)


extras = {
    "testing": [
        "pytest>=4.4.0",
        "pytest-xdist==1.31.0",
        "pytest-cov==2.8.1",
    ]
}

setup(
    name="data_mass",
    version=version,
    author="BEES Community",
    maintainer="Data Mass Team",
    maintainer_email="qcoe.data@ab-inbev.com",
    description="Data generation.",
    long_description=long_description,
    project_urls={
        "Documentation": (
            "https://ab-inbev.atlassian.net"
            "/wiki/spaces/PKB/pages/2175860865/Data+Mass"
        ),
        "Repository": (
            "https://dev.azure.com/ab-inbev/"
            "GHQ_B2B_Delta/_git/b2b-data-mass-application"
        ),
        "Standards": (
            "https://anheuserbuschinbev.sharepoint.com/"
            "sites/b2bengineering/architecture/SitePages/"
            "Data-Mass-Application.aspx"
        ),
        "Release Notes": (
            "https://anheuserbuschinbev.sharepoint.com/:b:/s"
            "/b2bengineering/"
            "EaTlUWEzsp1EqdmKaqBclL4ByT6uvxDV1nF1erEOsD-stQ?e=QQyxU8"
        ),
    },
    packages=find_packages(),
    package_data={
        "data_mass": [
            "data/*.json",
            "populator/country/data/*.csv",
            "populator/country/data/ar/*.csv",
            "populator/country/data/br/*.csv",
            "populator/country/data/ca/*.csv",
            "populator/country/data/co/*.csv",
            "populator/country/data/do/*.csv",
            "populator/country/data/ec/*.csv",
            "populator/country/data/mx/*.csv",
            "populator/country/data/pa/*.csv",
            "populator/country/data/pe/*.csv",
            "populator/country/data/py/*.csv",
            "populator/country/data/ar/*.csv",
        ]
    },
    install_requires=requirements,
    extras_require=extras,
    python_requires=">=3.7.0",
    cmdclass={
        "install": PostInstallCommand,
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)
