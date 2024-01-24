"""Setup."""

import setuptools

DIST_NAME = 'places_lk'
VERSION = "1.0.0"
DESCRIPTION = (
    "A utility library for returning the location of places in Sri Lanka."
)
INSTALL_REQUIRES = [
    'utils-nuuuwan',
]
setuptools.setup(
    name="%s-nuuuwan" % DIST_NAME,
    version=VERSION,
    author="Nuwan I. Senaratna",
    author_email="nuuuwan@gmail.com",
    description=DESCRIPTION,
    long_description="",
    long_description_content_type="text/markdown",
    url=f"https://github.com/nuuuwan/{DIST_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/nuuuwan/{DIST_NAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=INSTALL_REQUIRES,
    test_suite='nose.collector',
    tests_require=['nose'],
)
