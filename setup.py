from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Fusion360Tools',
    version='0.1.1',
    description='Fusion 360 Tools Collection - BackupTool and more',
    long_description=long_description,
    packages=['BackupTool', 'BackupTool.apper.apper', 'BackupTool.commands'],
    package_data={
        "": ["resources/*", "resources/**/*", "*.manifest"],
    },
    url='https://github.com/tapnair/Fusion360Tools',
    license='MIT',
    author='Patrick Rainsberry',
    author_email='patrick.rainsberry@autodesk.com',
)
