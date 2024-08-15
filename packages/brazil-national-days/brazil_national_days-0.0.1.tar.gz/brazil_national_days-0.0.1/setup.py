from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name="brazil_national_days",
    version="0.0.1",
    license="MIT License",
    author="Leonardo Alves Francisco",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="leonardoalves294@gmail.com",
    keywords="holidays brazil national",
    description="Is a package that simplifies accessing and managing Brazilian national holidays. It fetches holiday data directly from ANBIMA, allowing you to easily retrieve holiday dates, names, and weekdays, as well as check if a specific date is a holiday. The package offers a straightforward interface for querying and interacting with holiday information.",
    packages=["brazil_national_days"],
    install_requires=["requests", "pandas"],
)
