# Trying to create a package from a repo that includes both local and serverless.com 

import setuptools

# TODO: Change the PACKAGE_NAME to the package's name - Either xxx-local or xxx-remote (without the -python-package suffix). Only lowercase, no underlines.
# Used by pypa/gh-action-pypi-publish
# Package Name should be identical to the inner directory name
# Changing the package name here, will cause changing the package directory name as well
# PACKAGE_NAME should be singular if handling only one instance
# PACKAGE_NAME should not include the word "main"
PACKAGE_NAME = "event-local"  # e.g.: queue-local, without python-package suffix

package_dir = PACKAGE_NAME.replace("-", "_")
# If we need backward-compatible:
# old_package_dir = "old_package_name"
    
setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.7',  # increase this number every time you make a change you want to publish. After 0.0.9 switch to 0.0.10 and not 0.1.0
                      # https://pypi.org/project/event-local/
    author="Circles",
    author_email="info@circlez.ai",
    description=f"PyPI Package for Circles {PACKAGE_NAME} Python",
    long_description=f"PyPI Package for Circles {PACKAGE_NAME} Python",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    # packages=[package_dir, old_package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    # package_dir={package_dir: f'{package_dir}/src', old_package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TODO: Update which packages to include with this package in production (dependencies) - Not for development/testing
    install_requires=[
        'logger-local',  # TODO: in -remote package please use logger-remote instead.
        'database-sql-local',  # TODO: In -remote package please delete this line.
        'python-sdk-remote'
    ]
)
