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
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Float64, Int64, String, UnixTimestamp
import numpy as np
from datetime import datetime, timedelta

# Define an entity for the Customer_id. You can think of an entity as a primary key used to
# fetch features.
customer = Entity(name="customer", join_keys=["CUSTOMER_ID"])

# Define an entity for the order_id. You can think of an entity as a primary key used to
# fetch features.
order = Entity(name="order", join_keys=["ORDER_ID"])

# Define an entity for the seller_id. You can think of an entity as a primary key used to
# fetch features.
#seller = Entity(name="seller", join_keys=["SELLER_ID"])

# Define an entity for the product_id. You can think of an entity as a primary key used to
# fetch features.
product = Entity(name="product", join_keys=["PRODUCT_ID"])

# Define an entity for the zip_code_prefix. You can think of an entity as a primary key used to
# fetch features.
#seller_zip_code_prefix = Entity(name="seller_zip_code_prefix", join_keys=["SELLER_ZIP_CODE_PREFIX"])

# Define an entity for the zip_code_prefix. You can think of an entity as a primary key used to
# fetch features.
#geolocation_zip_code_prefix = Entity(name="geolocation_zip_code_prefix", join_keys=["GEOLOCATION_ZIP_CODE_PREFIX"])

# Define an entity for the zip_code_prefix. You can think of an entity as a primary key used to
# fetch features.
#customer_zip_code_prefix = Entity(name="customer_zip_code_prefix", join_keys=["CUSTOMER_ZIP_CODE_PREFIX"])

# Defines a data source from which feature values can be retrieved. Sources are queried when building training
# datasets or materializing features into an online store.
project_name = yaml.safe_load(open("feature_store.yaml"))["project"]

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

# OLIST_GEOLOCATION data source
retail_stats_source = SnowflakeSource(
    database=yaml.safe_load(open("feature_store.yaml"))["offline_store"]["database"],
    schema=yaml.safe_load(open("feature_store.yaml"))["offline_store"]["schema"],
    timestamp_field="EVENT_TIMESTAMP",
    created_timestamp_column="CREATED_TIMESTAMP",
    table="Aggregated_Sales_Summary_Table"
)

customer_orders_fs = FeatureService(
    name="customer_orders_fs",
    features=[olist_customers_fv]
)


