from setuptools import setup

installation_requirements = [
    "logtail-python==0.2.10",
]

setup(
    name="gravybox",
    description="A big box of gravy for all of your flask-sloshing itty-bits",
    version="0.1",
    url="https://github.com/clementinegroup/gravybox",
    author="(~)",
    package_dir={"": "packages"},
    packages=["gravybox"],
    install_requires=installation_requirements
)
