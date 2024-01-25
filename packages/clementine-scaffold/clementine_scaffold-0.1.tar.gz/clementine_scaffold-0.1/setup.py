from setuptools import setup

installation_requirements = [
    "logtail-python==0.2.10",
]

setup(
    name="clementine_scaffold",
    description="Scaffolding for all of your clementine-slugging, flask-sloshing itty-bits",
    version="0.1",
    url="https://github.com/clementinegroup/scaffold",
    author="The Clementine Group",
    package_dir={"": "packages"},
    packages=["clementine_scaffold"],
    install_requires=installation_requirements
)
