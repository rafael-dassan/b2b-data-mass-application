from subprocess import call

from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        call(["pre-commit", "install"])


setup(
    cmdclass={
        "install": PostInstallCommand,
    }
)
