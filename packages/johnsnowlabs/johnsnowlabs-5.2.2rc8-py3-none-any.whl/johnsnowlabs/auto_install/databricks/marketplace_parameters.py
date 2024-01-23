from johnsnowlabs.auto_install.databricks.endpoints import (
    create_secret_in_scope,
    setup_secrets,
)
from johnsnowlabs.auto_install.databricks.marketplace import create_endpoint
from databricks.sdk.runtime import *


def make_model_select_drop_down(models_df):
    models = models_df.NluRef.values.tolist()
    first_model = models[0]
    dbutils.widgets.dropdown("The model", first_model, models)


def get_selected_model_metadata(models_df):
    selected_model = dbutils.widgets.get("The model")
    model_data = models_df[models_df.NluRef == selected_model]
    return model_data


def query_endpoint(data, endpoint_name, db_host, db_token, base_name=None):
    url = f"{db_host}/serving-endpoints/{endpoint_name}/invocations"
    headers = {
        "Authorization": f"Bearer {db_token}",
        "Content-Type": "application/json",
    }
    response = requests.request(method="POST", headers=headers, url=url, data=data)
    if response.status_code != 200:
        raise Exception(
            f"Request failed with status {response.status_code}, {response.text}"
        )
    import pandas as pd

    return pd.DataFrame(json.loads(response.json()["predictions"]))


def make_ui(models_df=None):
    if models_df is None:
        from johnsnowlabs.auto_install.databricks.marketplace_offering import models_df
    dbutils.widgets.removeAll()
    dbutils.widgets.text("JSL-JSON-License", "")
    dbutils.widgets.text("Databricks access token", "")
    dbutils.widgets.text("Databricks host", "")
    # dbutils.widgets.text("Model to deploy", "")
    make_model_select_drop_down(models_df)
    dbutils.widgets.dropdown("hardware_target", "CPU", ["CPU", "GPU"])

    # avaiable_models = get_all_mm_models()
    # first_model = list(avaiable_models.keys())[0]
    # dbutils.widgets.dropdown("Model to Deploy", first_model,avaiable_models)


def get_db_token():
    return dbutils.widgets.get("Databricks access token")


def get_db_host():
    return dbutils.widgets.get("Databricks host")


# def get_model():return dbutils.widgets.get('Model to deploy')
def get_hardware_target():
    return dbutils.widgets.get("hardware_target")


def get_jsl_license():
    return dbutils.widgets.get("JSL-JSON-License")


def deploy(deployed_endpoint_name=None, models_df=None):
    if models_df is None:
        from johnsnowlabs.auto_install.databricks.marketplace_offering import models_df
    path_prefix = "john_snow_labs.test_models_v3"

    # models = get_all_mm_models()
    db_token = get_db_token()
    db_host = get_db_host()
    hardware_target = get_hardware_target()
    jsl_license = get_jsl_license()
    # model_name = get_model()
    model_data = get_selected_model_metadata(models_df)
    # full_path = f{path_prefix}.{model_name}_{hardware_target}
    # john_snow_labs_tiny_bert_test.test_models.en_classify_bert_tiny_gpu  # THIS WORKS!
    # model_path = f'john_snow_labs_{model_name}_{hardware_target}'.replace('.','_')

    model_path = (
        model_data.CpuModelPath.values[0]
        if hardware_target == "CPU"
        else model_data.GpuModelPath.values[0]
    )
    endpoint_name = (
        (model_path + "_endpoint")[:50].replace(".", "") + "_" + hardware_target.lower()
        if not deployed_endpoint_name
        else deployed_endpoint_name
    )
    setup_secrets(
        secret_name="JSL_SECRET_NAME",
        secret_value=jsl_license,
        scope_name="JSL_SCOPE",
        host=db_host,
        db_token=db_token,
    )

    print("creating model", model_path)
    print("creating endpoint", endpoint_name)

    endpoint_success = create_endpoint(
        endpoint_name,
        model_path,
        "2",
        db_token=db_token,
        db_host=db_host,
        workload_type=hardware_target,
    )
    if not endpoint_success:
        listing_id = model_data.PrivateListingId.values[0]
        try:
            displayHTML(
                f"""Could not import the model. <a href="marketplace/consumer/listings/{listing_id}" target="_blank">Please click this link and click on "get instant access" in the top right</a> """
            )
        except:
            print(
                f"""Could not import the model. Please visit  {db_host}/marketplace/consumer/listings/{listing_id} and click on "get instant access" in the top righ"""
            )

        return False
    return endpoint_name


# make_ui(models_df)
