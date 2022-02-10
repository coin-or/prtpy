import pathlib
import setuptools

NAME = "prtpy"
URL = "https://github.com/erelsgl/" + NAME
HERE = pathlib.Path(__file__).parent
print(f"\nHERE = {HERE.absolute()}\n")
README = (HERE / "README.md").read_text()
REQUIRES = (HERE / "requirements.txt").read_text().strip().split("\n")
REQUIRES = [lin.strip() for lin in REQUIRES]
print(f'\nVERSION = {(HERE / NAME / "VERSION").absolute()}\n')
VERSION = (HERE / NAME / "VERSION").read_text().strip()
# See https://packaging.python.org/en/latest/guides/single-sourcing-package-version/

setuptools.setup(
    name=NAME,
    packages=setuptools.find_packages(),
    version=VERSION,
    install_requires=REQUIRES,
    author="Erel Segal-Halevi",
    author_email="erelsgl@gmail.com",
    description="Number partitioning in Python",
    keywords="optimization, partition",
    license="MIT",
    license_files=("LICENSE",),
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    project_urls={"Bug Reports": URL + "/issues", "Source Code": URL},
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 1 - Planning",
    ],
)

# Build:
#   Delete old folders: build, dist, *.egg_info, .venv_test.
#   Then run:
#        python -m build
#   Or (old version):
#        python setup.py sdist bdist_wheel

# Publish to test PyPI:
#   twine upload --repository testpypi dist/*

# Publish to real PyPI:
#   twine upload --repository pypi dist/*
