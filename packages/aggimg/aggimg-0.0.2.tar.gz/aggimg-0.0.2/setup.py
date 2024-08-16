from setuptools import setup, find_packages

# Distribute py wheels
# python3 setup.py bdist_wheel sdist
# twine check dist/*
# cd dist
# cat ~/.pypirc (to get token)
# twine upload * -u __token__ -p pypi-token


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("requirements.txt", "r") as r:
    install_requires = r.readlines()


setup(
    name="aggimg",
    version="0.0.2",
    description="Aggressive image optimizer cli!",
    url="https://github.com/ClimenteA/aggressive-image-optimizer-cli",
    author="Climente Alin",
    author_email="climente.alin@gmail.com",
    license="MIT",
    py_modules=["aggimg"],
    install_requires=install_requires,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    entry_points={"console_scripts": ["aggimg=aggimg:cli"]},
)