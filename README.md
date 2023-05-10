# Kobra

![](https://img.shields.io/badge/Python-3.9.16-blue)
![](https://img.shields.io/badge/Django-4.1.5-%2344B78B)
![](https://img.shields.io/badge/REST%20Framework-3.14.0-%23A30000)
![](https://img.shields.io/badge/Swagger-OpenAPI%202.0-%23aaaa00)
![](https://img.shields.io/badge/LICENSE-MIT-%2300557f)
![](https://img.shields.io/badge/lastest-2023--05--09-success)
![](https://img.shields.io/badge/contact-dr.mokira%40gmail.com-blueviolet)

A custom server program based on the **Django framework** designed 
to allow a programmer to directly move to the implementation of 
an application's features without having to torture himself with other
time-consuming configuration or installation.

You can clone this repository everywhere you want in your machine,
with the following command lines:

###### `>_ cmd@01:~$`
```sh
git clone https://github.com/mokira3d48/cobra.git myapp && cd myapp
```

In this cloned directory, you will see the following structure:

```
.
├── LICENSE
├── README.md
├── requirements.txt
└── server
    ├── core
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── manage.py

2 directories, 9 files
```
<!--
This is the list of the installed features:
1. **Django REST Framework**: it's a powerful and flexible toolkit
for building Web APIs.
2. **drf-yasg**: for the generation of a documentation of the API in real
**Swagger/OpenAPI 2.0 specifications** from a **Django Rest Framework** API.
3. **Django CORS Headers**: it's a security mechanism that **allows one
domain to access** resources hosted on **another domain**.-->


<details id="table-content" open>
    <summary>Table of contents</summary>
    <ul>
        <li><a href="./docs/dev.md#1-dev-installation">1. Dev installation</a>
            <ul>
                <li><a href="./docs/dev.md#11-install-python3">1.1 Install python3</a></li>
                <li><a href="./docs/dev.md#12-install-venv">1.2 Install venv</a></li>
                <li><a href="./docs/dev.md#13-install-postgresql">1.3 Install PostgreSQL</a></li>
                <li><a href="./docs/dev.md#14-configuration">1.4 Configuration</a>
                    <ul>
                        <li><a href="./docs/dev.md#141-setting-virtual-environment">1.4.1 Setting virtual environment</a></li>
                        <li><a href="./docs/dev.md#142-creating-and-setting-of-postgresql-database">1.4.2 Creating and setting of PostgreSQL database</a>
                            <ul>
                                <li><a href="./docs/dev.md#a-env-settings">a. .env settings</a></li>
                                <li><a href="./docs/dev.md#b-launching-the-server">b. Server settings</a></li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <li><a href="./docs/dev.md#15-lauching-the-server">1.5 Launching the dev server</a></li>
            </ul>
        </li>
        <li><a href="./docs/cors.md#2-cross-origin-resource-sharing-cors">2. Cross Origin Resource Sharing (CORS)</a></li>
        <li><a href="./docs/postgis.md#3-spatial-database-with-postgis">3. Spatial database with PostGIS</a></li>
    </ul>
</details>


<!--## Usage
For the differents usages, you can consult the different documentation
available [here](./docs/README.md).

1. PostGIS
2. Cross Origin Resource Sharing
3. Usage example of Django REST Framework
4. JWT authentication with Django REST Framework
5. API documentation programming
6. Using cache with apiview and viewsets-->

<br>
