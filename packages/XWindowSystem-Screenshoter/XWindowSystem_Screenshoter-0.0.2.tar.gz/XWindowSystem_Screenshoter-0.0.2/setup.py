import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="XWindowSystem_Screenshoter",                     # This is the name of the package
    version="0.0.2",                        # The initial release version
    author="Matheus Verginio Fernandes",                     # Full name of the author
    description="A simple use to capture a screenshot of single window in linux Systems",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.0',                # Minimum version requirement of the package
    py_modules=["XWindowSystem_Screenshoter"],             # Name of the python package
    package_dir={'':'./src'},     # Directory of the source code of the package
    # install_requires=["numpy","threading", "Xlib"]                     # Install other dependencies if any
)