# _*_ coding: utf-8 _*_
# @Time : 2023/5/19
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :

from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).resolve().parent
README = (here / "README.md").read_text(encoding="utf-8")

excluded_packages = ["tests", "tests.*"]

# this module can be zip-safe if the zipimporter implements iter_modules or if
# pkgutil.iter_importer_modules has registered a dispatch for the zipimporter.
try:
    import pkgutil
    import zipimport

    zip_safe = (
            hasattr(zipimport.zipimporter, "iter_modules")
            or zipimport.zipimporter in pkgutil.iter_importer_modules.registry.keys()
    )
except AttributeError:
    zip_safe = False

requires = [
    "aiohappyeyeballs==2.3.4",
    "aiohttp==3.10.0",
    "aiosignal==1.3.1",
    "annotated-types==0.7.0",
    "async-timeout==4.0.3",
    "attrs==23.2.0",
    "certifi==2024.7.4",
    "cffi==1.16.0",
    "chardet==5.2.0",
    "charset-normalizer==3.3.2",
    "crypto==1.4.1",
    "DBUtils==3.1.0",
    "dnspython==2.6.1",
    "frozenlist==1.4.1",
    "idna==3.7",
    "loguru==0.7.2",
    "multidict==6.0.5",
    "Naked==0.1.32",
    "numpy==2.0.1",
    "orjson==3.10.6",
    "pandas==2.2.2",
    "pycparser==2.22",
    "pycryptodome==3.20.0",
    "pydantic==2.8.2",
    "pydantic_core==2.20.1",
    "pymongo==4.8.0",
    "PyMySQL==1.1.1",
    "python-dateutil==2.9.0.post0",
    "pytz==2024.1",
    "PyYAML==6.0.1",
    "redis==5.0.8",
    "requests==2.32.3",
    "shellescape==3.8.1",
    "six==1.16.0",
    "typing_extensions==4.12.2",
    "tzdata==2024.1",
    "urllib3==2.2.2",
    "yarl==1.9.4",
    "pdfplumber==0.11.2",
    "beautifulsoup4==4.12.3",
    "pysmb==1.2.9.1",
    "setuptools==68.2.0"
]

setup(
    name="DigiCore",
    version="1.1.9",
    description="DigiCore是一个基于Python的数字化支持部第三方库，旨在为数据处理和开发提供完备的工具集和服务。",
    long_description=README,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="digicore是服务于道诚集团数字化支持部的自建第三方库项目",
    author="yarm",
    author_email="yangyang@doocn.com",
    license="MIT License",
    packages=find_packages(exclude=excluded_packages),
    install_requires=requires,
    platforms=["any"],
    zip_safe=zip_safe,
    python_requires=">=3.8",
)
