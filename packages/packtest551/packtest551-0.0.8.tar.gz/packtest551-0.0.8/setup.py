from setuptools import setup, find_packages

setup(
    author="asdf",
    description="asdfasdf",
    name="packtest551", # this is the name of the package when using "pip install test-package". when importing, "import test_pack" (the actual directory names). (refer to for_test_of_deployment)
    packages=find_packages(),
    version="0.0.8",
    package_data={'': ['LICENSE', 'README.md', 'MANIFEST.in']},
    #data_files=[('', ['LICENSE', 'README.md', 'MANIFEST.in'])],
    include_package_data=True,
    #include_package_data=True,
    #data_files=[('', ['LICENSE', 'README.md'])],
    #include_package_data=True,
    install_requires = ['numpy >=1.10', 'pandas'] # this better cover as many versions as possible (different from requirements.txt, which is "exact" version of installation via "pip freeze > requirements.txt", then install via "pip install -r requirements.txt")
)