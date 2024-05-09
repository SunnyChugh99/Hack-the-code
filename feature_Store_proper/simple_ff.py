from datetime import timedelta

import pandas as pd
import yaml

from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    PushSource,
    RequestSource,
    SnowflakeSource,
    batch_feature_view,
    aggregation
)

from feast.types import Float32, Float64, Int64, String, UnixTimestamp
import numpy as np
from datetime import datetime, timedelta

customer = Entity(name="customer", join_keys=["CUSTOMER_ID"])


order = Entity(name="order", join_keys=["ORDER_ID"])

product = Entity(name="product", join_keys=["PRODUCT_ID"])

# project_name = yaml.safe_load(open("feature_store.yaml"))["project"]

# OLIST_CUSTOMERS data source
olist_customers_source = SnowflakeSource(
    database=yaml.safe_load(open("feature_store.yaml"))["offline_store"]["database"],
    schema=yaml.safe_load(open("feature_store.yaml"))["offline_store"]["schema"],
    timestamp_field="EVENT_TIMESTAMP",
    created_timestamp_column="CREATED_TIMESTAMP",
    table="Aggregated_Sales_Summary_Table"
)

olist_customers_fv = FeatureView(
    name="olist_customers_fv",
    entities=[customer],
    ttl=timedelta(weeks=52 * 10),
    schema=[
        Field(name="Customer_id", dtype=String),
        Field(name="Customer_name", dtype=String),
        Field(name="Quantity", dtype=Int64),
        Field(name="Max_sales_in_month", dtype=String),
        Field(name="Total_sales", dtype=String),
    ],
    source=olist_customers_source,
    tags={"team": "customers"},
)

# # OLIST_GEOLOCATION data source
# retail_stats_source = SnowflakeSource(
#     database=yaml.safe_load(open("feature_store.yaml"))["offline_store"]["database"],
#     schema=yaml.safe_load(open("feature_store.yaml"))["offline_store"]["schema"],
#     timestamp_field="EVENT_TIMESTAMP",
#     created_timestamp_column="CREATED_TIMESTAMP",
#     table="Aggregated_Sales_Summary_Table"
# )
#
# customer_orders_fs = FeatureService(
#     name="customer_orders_fs",
#     features=[olist_customers_fv]
# )
#

