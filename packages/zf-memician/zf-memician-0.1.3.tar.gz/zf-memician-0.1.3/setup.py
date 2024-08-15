from os import path as os_path

import setuptools

PACKAGE_NAME = "zf-memician"
AUTHOR_NAME = "Zeff Muks"
AUTHOR_EMAIL = "zeffmuks@gmail.com"

with open("README.md", "r") as f:
    readme = f.read()


def read_version():
    version_file = os_path.join(os_path.dirname(__file__), "memician", "version.py")
    with open(version_file) as file:
        exec(file.read())
    version = locals()["__version__"]
    print(f"Building {PACKAGE_NAME} v{version}")
    return version


setuptools.setup(
    name=PACKAGE_NAME,
    version=read_version(),
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="Memician is a state of the art Memelord",
    license="PROPRIETARY",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=open("requirements.txt").read().splitlines(),
    package_data={"memician": ["Resources/*/*"]},
    packages=setuptools.find_packages(include=["memician", "memician.*"], exclude=["venv", "venv.*"]),
    entry_points={"console_scripts": ["memician = memician.__main__:main"]},
)
