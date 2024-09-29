import setuptools

REQUIRED_PACKAGES = [
    "pytest==6.2.5",
    "requests==2.26.0",
    "pandas==2.2.3"
]

setuptools.setup(
    name="smhi",
    version="0.0.1",
    description="Data integration with SMHI",
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
    author="Trustly Data Engineering Team",
)
