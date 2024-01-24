import pathlib

import setuptools

setuptools.setup(
    name='igimf',
    version='0.1.0',
    description='Integrated Galaxy Wide IMF python package',
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    url="https://github.com/egjergo/pyIGIMF",
    author='Eda Gjergo',
    author_email='eda.gjergo@gmail.com',
    license='LICENSE',
    project_urls={
        "Documentation": "https://readthedocs.io/pyIGIMF",
        "Source": "https://github.com/egjergo/pyIGIMF",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">3.8,<3.12",
    install_requires=["requests", "pandas>1.0"],
    # extras_require={
        
    # }
    packages=setuptools.find_packages(),
    include_package_data=True,
)