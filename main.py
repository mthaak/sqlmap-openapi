import json
import logging
import os
import tempfile
from dataclasses import dataclass
from typing import Iterator, Any, Union, List, Optional, Tuple
from urllib.parse import urlencode

import click
from prance import ResolvingParser

logger = logging.getLogger(__name__)

COMMAND_PREFIX = "python3 ./sqlmap-dev/sqlmap.py"
DEFAULT_RESULTS_FILE = "./results.txt"

# TODO allow a user to set these values
DEFAULT_HEADERS = {"Accept": "application/json"}
LEVEL = 1
RISK = 1
DBMS = "postgres"
TIME_SEC = 1


def insert_path_parameters_for_tampering(
    base_path: str, parameters: List[dict]
) -> Tuple[str, List[str]]:
    """
    Insert path parameters for tampering. The first path is a static path with all path parameters replaced by static
    values. The other paths are dynamic paths with one path parameter replaced by a wildcard.
    """

    paths = [base_path]

    def insert_path_parameter(name: str, static_value: str, tamper: bool = False):
        if tamper:
            # Append path with dynamic path parameter
            paths.append(paths[0].replace("{" + name + "}", "*", 1))

        for i in range(len(paths) - 1 if tamper else len(paths)):
            # Insert static path parameters
            paths[i] = paths[i].replace("{" + name + "}", static_value, 1)

    for parameter in parameters:
        if not parameter["in"] == "path":
            continue

        if parameter.get("schema") is None:
            logger.warning(f"Path parameter {parameter['name']} has no schema")
            continue
        schema = parameter["schema"]

        if schema["type"] == "string":
            # TODO make depend on format (e.g. date, date-time, email, etc.)
            static_value = parameter.get("default", "123")
            tamper = True
        elif schema["type"] == "number":
            static_value = parameter.get("default", "0")
            tamper = False
        elif schema["type"] == "integer":
            static_value = parameter.get("default", "0")
            tamper = False
        elif schema["type"] == "boolean":
            static_value = parameter.get("default", "false")
            tamper = False
        else:
            logger.warning(f"Parameter {parameter['name']} has unknown type")
            continue

        insert_path_parameter(parameter["name"], static_value, tamper)

    static_path, dynamic_paths = paths[0], paths[1:]

    return static_path, dynamic_paths


def create_queries_for_tampering(parameters: List[dict]) -> Tuple[str, List[str]]:
    """
    Create queries for tampering. The first query is a static query with all query parameters replaced by static
    values. The other queries are dynamic queries with one query parameter replaced by a wildcard.
    """

    query_params: List[dict] = [{}]

    def add_query_parameter(
        name: str, static_value: str, required: bool = False, tamper: bool = False
    ):
        if tamper:
            # Append query with dynamic query parameter
            query_params.append(query_params[0].copy())
            query_params[-1][name] = "*"

        if required:
            for i in range(len(query_params) - 1 if tamper else len(query_params)):
                # Insert static query parameters
                query_params[i][name] = static_value

    for parameter in parameters:
        if not parameter["in"] == "query":
            continue

        if parameter.get("schema") is None:
            logger.warning(f"Query parameter {parameter['name']} has no schema")
            continue
        schema = parameter["schema"]

        if schema["type"] == "string":
            # TODO make depend on format (e.g. date, date-time, email, etc.)
            static_value = parameter.get("default", "123")
            tamper = True
        elif schema["type"] == "number":
            static_value = parameter.get("default", "0")
            tamper = False
        elif schema["type"] == "integer":
            static_value = parameter.get("default", "0")
            tamper = False
        elif schema["type"] == "boolean":
            static_value = parameter.get("default", "false")
            tamper = False
        elif schema["type"] == "array":
            if schema.get("items") is None:
                logger.warning(f"Parameter {parameter['name']} has no items")
                continue
            static_value = parameter.get("default", "0")
            tamper = True
        else:
            logger.warning(f"Parameter {parameter['name']} has unknown type")
            continue

        add_query_parameter(
            parameter["name"], static_value, parameter.get("required", False), tamper
        )

    static_query_params, dynamic_query_params = query_params[0], query_params[1:]

    static_query = urlencode(query=static_query_params, doseq=True, safe="*")
    dynamic_queries = [
        urlencode(query=parameters, doseq=True, safe="*")
        for parameters in dynamic_query_params
    ]

    return static_query, dynamic_queries


def create_json_datas_for_tampering(root_schema: dict) -> Tuple[bytes, List[bytes]]:
    """
    Create datas for tampering from schema. The first data is a static data with only static values. The other datas
    are dynamic datas with one value replaced by a wildcard.
    """

    @dataclass
    class DataParameter:
        name: str
        static_value: Any
        is_required: bool = False
        tamper: bool = False

    parameters: List[DataParameter] = []

    def build_parameterised_schema(
        name: str, path: str, is_required: bool, schema: dict
    ) -> Any:
        """
        Recursively builds parameterised schema and adds parameters to a list. The value of each parameter in the
        parameterised schema is a unique path from the root to the parameter. This is used to replace the parameter
        with a wildcard in the next step.
        """
        if schema.get("type") is None:
            logger.warning(f"Property {name} has no type")
        elif schema["type"] == "string":
            # TODO make depend on format (e.g. date, date-time, email, etc.)
            # TODO implement enums
            static_value = schema.get("default", "123")
            parameters.append(DataParameter(path, static_value, is_required, True))
            return "{" + path + "}"
        elif schema["type"] == "number":
            static_value = schema.get("default", 0)
            # TODO take into account min and max
            parameters.append(DataParameter(path, static_value, is_required, False))
            return "{" + path + "}"
        elif schema["type"] == "integer":
            static_value = schema.get("default", 0)
            parameters.append(DataParameter(path, static_value, is_required, False))
            return "{" + path + "}"
        elif schema["type"] == "boolean":
            static_value = schema.get("default", False)
            parameters.append(DataParameter(path, static_value, is_required))
            return "{" + path + "}"
        elif schema["type"] == "array":
            if schema.get("items") is None:
                logger.warning(f"Property {name} has no items")
                return None
            return [
                build_parameterised_schema(
                    name, path + "[0]", is_required, schema["items"]
                )
            ]
        elif schema["type"] == "object":
            props = {}
            if schema.get("properties") is not None:
                for name, prop in schema["properties"].items():
                    props[name] = build_parameterised_schema(
                        name,
                        path + "." + name,
                        is_required and name in schema.get("required", []),
                        prop,
                    )
            if schema.get("additionalProperties") is not None:
                # TODO make depend on key format?
                key_name = path + "->" + "prop1/key"
                parameters.append(DataParameter(key_name, "123", is_required, True))
                props["{" + key_name + "}"] = build_parameterised_schema(
                    name,
                    path + "." + "prop1",
                    is_required,
                    schema["additionalProperties"],
                )
            return props
        else:
            logger.warning(f"Unknown type {schema['type']}")

    # Build parameterised schema and collect parameters
    parameterised_schema = build_parameterised_schema("root", "root", True, root_schema)

    parameterised_schema_json = json.dumps(parameterised_schema)

    schemas = [parameterised_schema_json]

    def insert_parameter(parameter: DataParameter):
        if parameter.tamper:
            # Append a new schema with the parameter replaced with a wildcard
            schemas.append(schemas[0].replace('"{' + parameter.name + '}"', '"*"'))

        # TODO use is_required field on DataParameter to decide whether to add parameter to schemas
        for i in range(len(schemas) - 1 if parameter.tamper else len(schemas)):
            # Replace parameter with static value in all schemas
            schemas[i] = schemas[i].replace(
                '"{' + parameter.name + '}"', json.dumps(parameter.static_value)
            )

    # Generate datas for tampering
    for parameter in parameters:
        insert_parameter(parameter)

    static_schema, dynamic_schemas = schemas[0], schemas[1:]

    return static_schema.encode(), [schema.encode() for schema in dynamic_schemas]


def create_raw_data_for_tampering() -> Tuple[bytes, List[bytes]]:
    return b"abc", [b"*"]


def merge_parameters(
    parameters_parent: List[dict], parameters_child: List[dict]
) -> List[dict]:
    """
    Merges two lists of parameters, keeping only the child parameter if there is a parent parameter with the same name.
    """
    parameters_by_name = {}
    for parameter in parameters_parent:
        parameters_by_name[parameter["name"]] = parameter
    for parameter in parameters_child:
        parameters_by_name[parameter["name"]] = parameter
    return list(parameters_by_name.values())


@dataclass
class Task:
    """
    A task to be performed by sqlmap.
    """

    method: str
    path: str
    query: str
    data: Optional[bytes] = None


def crawl_openapi(root_openapi: dict) -> Iterator[Task]:
    """
    Crawls an OpenAPI specification and yields tasks to be performed by sqlmap.
    """

    for path, endpoints in root_openapi["paths"].items():
        for method, endpoint in endpoints.items():
            if method not in ["get", "post", "put", "patch", "delete"]:
                continue

            parameters = merge_parameters(
                endpoints.get("parameters", []), endpoint.get("parameters", [])
            )

            static_path, dynamic_paths = insert_path_parameters_for_tampering(
                path, parameters
            )

            static_query, dynamic_queries = create_queries_for_tampering(parameters)

            static_data: Union[bytes, None] = None
            dynamic_datas: Union[List[bytes], None] = None
            if "requestBody" in endpoint:
                if endpoint["requestBody"].get("content") is None:
                    logger.warning(f"Unknown content {endpoint['requestBody']}")
                    continue

                content = endpoint["requestBody"]["content"]

                if content.get("application/octet-stream") is not None:
                    static_data, dynamic_datas = create_raw_data_for_tampering()
                elif content.get("application/json") is not None:
                    if content["application/json"].get("schema") is None:
                        logger.warning(
                            f"Missing schema {endpoint['requestBody']['content']}"
                        )
                        continue

                    schema = content["application/json"]["schema"]
                    static_data, dynamic_datas = create_json_datas_for_tampering(schema)
                else:
                    logger.warning(
                        f"Unknown content {endpoint['requestBody']['content']}"
                    )
                    continue

            # Yield task for tampering each dynamic path parameter
            if dynamic_paths:
                for dynamic_path in dynamic_paths:
                    yield Task(
                        method,
                        dynamic_path,
                        static_query,
                        static_data,
                    )

            # Yield task for tampering each dynamic query parameter
            if dynamic_queries:
                for dynamic_query in dynamic_queries:
                    yield Task(
                        method,
                        static_path,
                        dynamic_query,
                        static_data,
                    )

            # Yield task for tampering each dynamic data parameter
            if dynamic_datas:
                for dynamic_data in dynamic_datas:
                    yield Task(method, static_path, static_query, dynamic_data)


def execute_sqlmap(
    base_url: str,
    method: str,
    path: str,
    query: str,
    headers: Optional[dict] = None,
    data: Optional[bytes] = None,
    level: Optional[int] = None,
    risk: Optional[int] = None,
    dbms: Optional[str] = None,
    time_sec: Optional[int] = None,
    results_file: Optional[str] = None,
    dry_run: bool = False,
):
    """
    Executes sqlmap on a given request.
    """

    command = f"{COMMAND_PREFIX} --batch"
    url = base_url + path + ("?" + query if query else "")
    command += f' --method={method} --url="{url}"'
    if level:
        command += f" --level={level}"
    if risk:
        command += f" --risk={risk}"
    if dbms:
        command += f" --dbms={dbms}"
    if time_sec:
        command += f" --time-sec={time_sec}"
    if results_file:
        command += f' --results-file="{results_file}"'
    if data:
        command += str.format(' --data "{}"', data.replace(b'"', b'\\"').decode())
    if headers:
        for key, value in headers.items():
            command += f' -H "{key}: {value}"'
    if dry_run:
        print(command)
    else:
        os.system(command)


def merge_results(results_filepath: str, batch_results_filepath: str, is_temp: bool):
    """
    Merges the results of a batch into the results file.
    """
    results_file_exists = os.path.isfile(results_filepath)
    with open(results_filepath, "a") as results_file:
        with open(batch_results_filepath, "r") as batch_file:
            if results_file_exists and not is_temp:
                batch_file.readline()  # skip header
            results_file.write(batch_file.read())


def main(url: str, openapi_url: str, results_file: str, dry_run: bool):
    with open(results_file, "w") as f:
        f.write("Target URL,Place,Parameter,Technique(s),Note(s)\n")

    parser = ResolvingParser(openapi_url)
    if not parser.valid:
        raise Exception("Invalid OpenAPI specification")

    tasks = crawl_openapi(parser.specification)
    for task in tasks:
        with tempfile.NamedTemporaryFile(suffix=".txt") as f:
            execute_sqlmap(
                base_url=url,
                method=task.method,
                path=task.path,
                query=task.query,
                headers=DEFAULT_HEADERS,
                data=task.data,
                level=LEVEL,
                risk=RISK,
                dbms=DBMS,
                time_sec=TIME_SEC,
                results_file=f.name,
                dry_run=dry_run,
            )
            merge_results(results_file, f.name, True)


@click.command()
@click.option("--url", type=str, help="Base URL to target", required=True)
@click.option(
    "--openapi", type=str, help="URL to the OpenAPI specification file", required=True
)
@click.option(
    "--results-file",
    type=str,
    help="File to write results to",
    default=DEFAULT_RESULTS_FILE,
)
@click.option(
    "--dry-run",
    type=bool,
    flag_value=True,
    help="Print commands instead of executing them",
)
def command(url, openapi, results_file, dry_run):
    main(url, openapi, results_file, dry_run)


if __name__ == "__main__":
    command()
