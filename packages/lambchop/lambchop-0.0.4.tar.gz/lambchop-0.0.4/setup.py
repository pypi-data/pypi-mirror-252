from setuptools import setup
from setuptools.command.install import install
import os
import shutil

# Custom install command to create a directory and add a file
class CustomInstallCommand(install):
    def run(self):
        print()
        print("RUNNING!!")
        print()
        install.run(self)
        target_directory = "/opt/extensions"
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        shutil.copy(
            "lambchop/server.py",
            target_directory
        )

# Package metadata
setup(
    # name='lambchop',
    # version='0.0.4',
    # packages=['lambchop'],
    cmdclass={'install': CustomInstallCommand}
)