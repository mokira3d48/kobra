from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="kobra",
    version="0.1.1",
    description=(
        "A custom server program based on the Django framework designed to allow a programmer "
        "to directly move to the implementation of an application's features without having "
        "to torture himself with other time-consuming configuration or installation."
    ),
    package_dir={"": "server"},
    packages=find_packages(where="server"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mokira3d48/kobra",
    author="DOCTOR MOKIRA",
    author_email="dr.mokira@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "django==5.2",
        "django-extensions",
        "django-cors-headers",
        "djangorestframework",
        "markdown",
        "django-filter",
        "djangorestframework-simplejwt",
        "drf-spectacular",
        "psycopg2",
        "python-dotenv",
        "gunicorn",
        "whitenoise==6.11.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "pytest-django>=4.5.2"],
    },
    python_requires=">=3.10",
)
