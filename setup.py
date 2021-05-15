from subprocess import call

from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        call(["pre-commit", "install"])


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    cmdclass={
        "install": PostInstallCommand,
    },
    install_requires=requirements
)
