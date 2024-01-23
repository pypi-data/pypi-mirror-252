from setuptools import setup, find_packages

setup(
    author="practice1",
    description="for pactice",
    name="test-packageee111", # this is the name of the package when using "pip install test-package". when importing, "import test_pack" (the actual directory names). (refer to for_test_of_deployment)
    packages=find_packages(include=["test_pack", "test_pack.*"]),
    version="0.3.0",
    package_data={'': ['LICENSE', 'README.md']},
    include_package_data=True,
    install_requires = ['numpy >=1.10', 'pandas'] # this better cover as many versions as possible (different from requirements.txt, which is "exact" version of installation via "pip freeze > requirements.txt", then install via "pip install -r requirements.txt")
)