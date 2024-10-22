import snowflake.connector
import requests

# Define Snowflake connection parameters
user = 'SAURABHKULKARNI'
password = 'Epsilon0*'
account = 'FYA62509.us-east-1'
role = 'SAURABHKULKARNI'
warehouse = 'FOSFOR_INSIGHT_WH'
database = 'INSIGHT_DESIGNER_SPCS'
schema = 'INSIGHT_SPCS_SCHEMA'

# Establish a connection to Snowflake
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    role=role,
    warehouse=warehouse,
    database=database,
    schema=schema
)
import base64

# # Generate an authentication token<your_warehouse>
auth_token = conn._rest._token
print(auth_token)
# Encode the token in Base64 format
base64_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
print("base64_token: ", base64_token)
#
# Print the generated token
print("Generated Snowflake Auth Token: ")
print(auth_token)
#
# # Close the connection
# conn.close()


# Get the access token
# cursor = conn.cursor()
# cursor.execute("CALL GET_ACCESS_TOKEN()")
# access_token = cursor.fetchone()[0]
#
# # Encode the access token as Base64
# base64_token = access_token.encode('utf-8').decode('base64')
#
# print("Base64-encoded token:", base64_token)


# Get the session ID
session_id = conn.session_id
#
print("Session ID:", session_id)


#
# # Encode the session ID as Base64
# base64_token = session_id.encode('utf-8').decode('base64')
# print("Base64-encoded session ID:", base64_token)


# Function to make a request to the Snowflake endpoint with the token
def access_snowflake_with_token():
    token = base64_token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # url = "https://zqiseam-ltimosaic.snowflakecomputing.com/oauth/authorize"
    url = "https://olzqgbof-zqiseam-ltimosaic.snowflakecomputing.app"

    # Skip the oauth/authorize step
    response = requests.get(url, headers=headers, allow_redirects=False)

    print(response.content)

    if response.status_code == 200:
        print("Access granted")
        # Handle the response as needed
    else:
        print(f"Failed to access Snowflake: {response.status_code}")
        # Handle the error as needed


# Call the function to access Snowflake
access_snowflake_with_token()
