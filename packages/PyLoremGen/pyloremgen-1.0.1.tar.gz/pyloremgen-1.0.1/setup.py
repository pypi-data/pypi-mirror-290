import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

README = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="PyLoremGen",
    version="1.0.1",
    url="https://github.com/oVitorio-ac/PyLoremGen/",
    license="MIT",
    author="Vitório Augusto Cavalheiro",
    description="A Python library for generating Lorem Ipsum text.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    zip_safe=False,
    python_requires=">=3.9.0, <4",
)
