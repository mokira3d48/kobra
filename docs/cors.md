## 2. Cross Origin Resource Sharing (CORS)
![](https://img.shields.io/badge/lastest-2023--05--09-success)

You can define  a list of domains that will be allowed to access the resources
of your server, by defining `CORS_ALLOWED_ORIGINS` variable in
`server/core/settings.py` file as follows:

###### `</> PYTHON [01]`
```python
# ...

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://192.168.9.102:3000',
]

```

The above setting will permit the server to allow all application hosted at 
`http://localhost:4200` and `http://192.168.9.102:3000` 
to access to resources of your server. By default, 
we have the following configuration is already defined :

###### `</> PYTHON [02]`
```python
# ...

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

```

With this configuration, the server accepts all request from another any
server.

<div align="center">

[:house: **Retour à l'accueil**](../README.md)

</div>

<br/>
