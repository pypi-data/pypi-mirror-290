from setuptools import find_packages, setup

#with open("бібліотека/README.md", "r") as f:
#    long_description = f.read()
long_description = "..."

setup(
    name="dronarnya",
    version="0.1.0",
    description="An id generator that generated various types and lengths ids",
    package_dir={"": "бібліотека"},
    packages=find_packages(where="бібліотека"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeoUKR/Dronarnya.git",
    author="Коваленко Костянтин",
    author_email="neokkv@gmail.com",
    license="apache",
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
    install_requires=["uk-std-libraries>=0.0.13"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.9",
)
