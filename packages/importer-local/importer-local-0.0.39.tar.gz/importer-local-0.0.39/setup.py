import setuptools

PACKAGE_NAME = "importer-local"
# TODO Please use the function
package_dir = "circles_importer"

setuptools.setup(
    # TODO: Please update the name and delete this line i.e. XXX-local or XXX-remote (without the -python-package suffix)
    name=PACKAGE_NAME,  # https://pypi.org/project/importer-local
    version='0.0.39',
    author="Circlez",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles circles_importer Local/Remote Python",
    long_description="This is a package for sharing common importer function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles-zone/importer-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'logger-local>=0.0.75',
        'database-mysql-local>=0.0.134',
        'location-local>=0.0.60',
    ],
)
