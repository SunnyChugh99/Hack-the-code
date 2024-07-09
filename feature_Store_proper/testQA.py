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
        Field(name="TOTAL_SALES_AMOUNT", dtype=Float32),
        Field(name="TOTAL_PROFIT_PER_DAY", dtype=Float32),
        Field(name="AVERAGE_TRANSACTION_VALUE", dtype=Float32),
    ],
    source=olist_customers_source,
    tags={"team": "customers"},
)


customer_orders_fs = FeatureService(
    name="customer_orders_fs",
    features=[olist_customers_fv]
)


