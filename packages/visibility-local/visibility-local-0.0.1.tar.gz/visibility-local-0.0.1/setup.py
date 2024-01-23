import setuptools
# Each Python project should have pyproject.toml or setup.py (if both exist, we use the setup.py)
# TODO: Please create pyproject.toml instead of setup.py (delete the setup.py)
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release) as we have moved away
#  from needing to generate a setup.py file to enable editable installs - We might able to delete this file soon

# Used by pypa/gh-action-pypi-publish

# TODO: Change the PACKAGE_NAME to the name of the package - Either xxx-local or xxx-remote
#   (without the -python-package suffix)
# Package Name in Pypi.org can also have underscore _ and point . but we decided not to use underscore and point, only hyphen
# Package Name should be identical to the inner directory name
PACKAGE_NAME = "visibility-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    # TODO: Please update the name and delete this line i.e. XXX-local or XXX-remote
    #  (without the -python-package suffix). Only lowercase, no underlines.
    name=PACKAGE_NAME,
    version='0.0.1',  # update only the minor version each time # https://pypi.org/project/<short-project-name-with-underscores>/
    author="Circles",
    author_email="info@circlez.ai",
    # TODO: Please update the description and long_description with no sensitive information as it is exposed in pypi.org
    description="PyPI Package for Circles visibility-local Python",
    long_description="PyPI Package for Circles visibility-local Python",
    long_description_content_type='text/markdown',
    # TODO: Please update the URL below
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",  # https://pypi.org/project/<project-name>/
    # packages=setuptools.find_packages(),
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TODO: Update which packages to include with this package
    install_requires=[
        'PyMySQL>=1.0.2',
        'pytest>=7.4.0',
        'mysql-connector>=2.2.9',
        'logzio-python-handler>= 4.1.0',
        'user-context-remote>=0.0.17',
        'python-sdk-local>=0.0.27'
    ],
)
