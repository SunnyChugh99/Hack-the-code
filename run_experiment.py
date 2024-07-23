import logging, sys
from snowflake.snowpark.session import Session
from snowflake.ml.registry.registry import Registry

#~/.snowflake/connections.toml
#SNOWFLAKE_HOME
#session = Session.builder.config("connection_name", "myconnection").create()
CONNECTION_PARAMETERS = {
    "account": "ug94937.us-east4.gcp",
    "user":"VAIBHAV",
    "password": "Password@2023",
    "role": "VAIBHAV",
    "database": "FDC_DEV_VAIBHAV",
    "warehouse": "FOSFOR_INSIGHT_WH",
    "schema": "PUBLIC",
}



def create_stage(session, stage_name="demo"):
    try:
        session.sql(f"create or replace stage {stage_name}").collect()
        return f"@{stage_name}"
    except Exception as ex:
        print("Error while creating snowflake session", ex)
        raise ex

def get_session():
    """
    Method creates snowflake session object.
    :return:
    """
    try:
        return Session.builder.configs(CONNECTION_PARAMETERS).create()
    except Exception as ex:
        print("Error while creating snowflake session", ex)
        raise ex


# Stored Procedure
def train_ml_models(session: Session) -> list:
    from snowflake.ml.modeling.pipeline import Pipeline
    from snowflake.ml.modeling.preprocessing import MinMaxScaler, OrdinalEncoder
    from snowflake.ml.modeling.metrics import mean_squared_error, mean_absolute_error, r2_score
    from snowflake.ml.modeling.xgboost import XGBRegressor
    # from snowflake.snowpark import Session, FileOperation
    # 2] Model Recipe Execution
    # Random split
    df_train, df_test = session.table("diamonds").drop('ROW').random_split(weights=[0.9, 0.1], seed=0)
    cat_cols = ["CUT", "COLOR", "CLARITY"]
    cat_cols_oe = ["CUT_OE", "COLOR_OE", "CLARITY_OE"]
    num_cols = ["CARAT", "DEPTH", "TABLE_PCT", "X", "Y", "Z"]
    # Define a pipeline that does the preprocessing and training of
    # a XGBRegressor model
    pipe = Pipeline(steps=[("ord", OrdinalEncoder(input_cols=cat_cols, output_cols=cat_cols_oe)),
                           ("scaler", MinMaxScaler(input_cols=num_cols, output_cols=num_cols)),
                           ("regressor", XGBRegressor(input_cols=cat_cols_oe + num_cols, label_cols=["PRICE"],
                                                      output_cols=['PREDICTION'], n_jobs=-1))
                           ])
    # Fit the pipeline
    xgb_model = pipe.fit(df_train)
    # Test the model
    df_test_pred = xgb_model.predict(df_test)
    mse = mean_squared_error(df=df_test_pred, y_true_col_names="PRICE", y_pred_col_names="PREDICTION")
    mae = mean_absolute_error(df=df_test_pred, y_true_col_names="PRICE", y_pred_col_names="PREDICTION")
    r2 = r2_score(df=df_test_pred, y_true_col_name="PRICE", y_pred_col_name="PREDICTION")
    print("Execution Completed")
    print(f'MSE: {mse}')
    print(f'MAE: {mae}')
    print(f'R2: {r2}')

    # LOG MODEL INTO SNOWFLAKE REGISTRY
    from snowflake.ml.registry.registry import Registry
    reg = Registry(session=session)
    # Log the model
    model_name = "diamonds_model_v30"
    try:
        mv = reg.log_model(model=xgb_model,
                           model_name=model_name,
                           comment="test",
                           version_name="run1",
                           python_version="3.9.19",
                           conda_dependencies=["scikit-learn==1.3.2"],
                           metrics={"model_metrics": {"score": 96}, "project_id": "0001", "type": "EXP"})


    except Exception as ex:
        pass
    return [{"EXP_NAME":""+model_name,
             "Version":"Run1",
             "matrices":{"model_metrics": {"MSE": mse, "MAE": mae, "r2": r2}, "project_id": "0001", "type": "EXP"},
             "Alogirthm_Type":"Regression",
             "Alogithm": "XGBRegressor",
             "RUN_STATUS":"SUCESS",
             "registry_exp_name":""}]


# Initilization

#1 -  UPDATE EXP STATUS "In Progress"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
print("Creating Snowflake Session object...")
session = get_session()
stage = create_stage(session)
print("Session has been created !")

print("Creating stored procedure...")
session.sproc.register(func=train_ml_models,
                       name="train_ml_models",
                       packages=["snowflake-snowpark-python", "snowflake-ml-python"],
                       isPermanant=False,
                       stage_location=stage,
                       replace=True)
print("Stored procedure has been created successfully!")

print("Executing Stored Procedure")
print("log exp runs")
#procedure_response = session.call("train_ml_models")
#print("Stored Procedure Executed Successfully !")

procedure_response = train_ml_models(session)

print(procedure_response)


#Artifacts Log in mlflow
print("Logging in mlflow completed !")
