from johnsnowlabs.auto_install.databricks.endpoints import *


def log_response_if_bad_status(response):
    try:
        response.raise_for_status()
    except Exception as err:
        print(response.text)
        raise err


from johnsnowlabs.auto_install.databricks.endpoints import *


def create_endpoint(
    endpoint_name,
    model_name,
    model_version,
    secret_scope_name="JSL_SCOPE",
    secret_name="JSL_SECRET_NAME",
    workload_size="Small",
    block_until_deployed=True,
    workload_type="CPU",
    db_token=None,
    db_host=None,
):
    """Create serving endpoint and wait for it to be ready
    maps name of your secret to an env variable with the same name in the container
    """

    print(f"Creating new serving endpoint: {endpoint_name}")
    endpoint_url = f"{db_host}/api/2.0/serving-endpoints"
    served_models = [
        {
            "name": "current",
            "model_name": model_name,
            "model_version": model_version,
            "workload_size": workload_size,
            "workload_type": workload_type,
            "scale_to_zero_enabled": "false"
            if "gpu" in workload_type.lower()
            else "true",
            "env_vars": [
                {
                    "env_var_name": "JOHNSNOWLABS_LICENSE_JSON",
                    "secret_scope": secret_scope_name,
                    "secret_key": secret_name,
                },
                {
                    "env_var_name": "spark.databricks.api.url",
                    "secret_scope": secret_scope_name,
                    "secret_key": "DB_API_URL",
                },
                {
                    "env_var_name": "DB_ENDPOINT_ENV",
                    "secret_scope": secret_scope_name,
                    "secret_key": "DB_ENDPOINT_ENV",
                },
            ],
        }
    ]

    request_data = {"name": endpoint_name, "config": {"served_models": served_models}}
    response = requests.post(
        endpoint_url,
        data=json.dumps(request_data).encode("utf-8"),
        headers=get_headers(db_token),
    )
    response_json = response.json()
    print(response.json())
    if (
        "error_code" in response_json
        and response_json["error_code"] == "RESOURCE_DOES_NOT_EXIST"
    ):
        # Mostl ikely model not imported from marketplace
        return False

    log_response_if_bad_status(response)
    if block_until_deployed:
        wait_for_endpoint(endpoint_name, db_host, db_token)

    try:
        displayHTML(
            f"""Created the <a href="/#mlflow/endpoints/{endpoint_name}" target="_blank">{endpoint_name}</a> serving endpoint"""
        )
    except:
        print(
            f"Created serving endpoint {endpoint_name} at {db_host}/#mlflow/endpoints/{endpoint_name}"
        )
    return True
