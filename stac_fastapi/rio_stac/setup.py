"""Setup stac_fastapi.rio_stac."""

from setuptools import find_namespace_packages, setup

with open("README.md") as f:
    long_description = f.read()

inst_reqs = [
    "stac_fastapi.api",
    "stac_fastapi.types",
    "stac_fastapi.extensions",
    "rio-stac",
    "pystac",
]
extra_reqs = {
    "pgstac": ["stac_fastapi.pgstac"],
    "sqlalchemy": ["stac_fastapi.sqlalchemy"],
    "test": ["pytest", "pytest-cov", "pytest-asyncio", "requests"],
}


setup(
    name="stac_fastapi.rio_stac",
    description=u"",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="COG STAC FastAPI",
    author=u"Vincent Sarago",
    author_email="vincent@developmentseed.org",
    url="https://github.com/developmentseed/stac-fastapi-rio-stac",
    license="MIT",
    packages=find_namespace_packages(exclude=["tests*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
