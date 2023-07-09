# SQLMAP-OpenAPI

This a project to show how an OpenAPI spec can be used to execute [sqlmap](https://github.com/sqlmapproject/sqlmap)
automatically against all endpoints of a target API. Parameters are replaced by wildcards which tell sqlmap where to
inject SQL payloads to detect vulnerabilities.


## Usage
```bash
make install
```

```bash
make run
```
