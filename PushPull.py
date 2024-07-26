import docker
client = docker.from_env()


registry1_username = "SAURABHKULKARNI"
registry1_password = "Epsilon0*"
registry1_url = "zqiseam-ltifosforscsaws.registry.snowflakecomputing.com"
registry2_url = "zqiseam-ltimosaic.registry.snowflakecomputing.com"
registry2_username = "SAURABHKULKARNI"
registry2_password = "Epsilon0*"
image_name = "/insight_designer_spcs/insight_spcs_schema/insight_spcs_repository:py39_V1"
image_name2 = "/insight_designer_spcs/insight_spcs_schema/spcs_test:py39_V1"


def pull_and_push_image(registry1_url, registry1_username, registry1_password, registry2_url, registry2_username,
                        registry2_password, image_name):
    try:
        # Login to the first Docker registry
        start_time = time.time()
        client.login(registry=registry1_url, username=registry1_username, password=registry1_password)

        # Pull the image from the first registry
        response = client.api.pull(f"{registry1_url}{image_name}")
        print(response)

        # Rename the image
        image = client.images.get(f"{registry1_url}{image_name}")
        image.tag(f"{registry2_url}{image_name2}")
        print(f'image tagged')

        # Logout from the first registry
        # client.auth.logout(registry=registry1_url)

        # Login to the second Docker registry
        client.login(registry=registry2_url, username=registry2_username, password=registry2_password)

        # Push the image to the second registry
        response = client.images.push(repository=f"{registry2_url}{image_name2}", stream=True, decode=True)
        for line in response:
            print(line)
            if 'errorDetail' in line:
                raise Exception(f"Failed to push image: {line['errorDetail']}")

        # Logout from the second registry
        # client.auth.logout(registry=registry2_url)

        # Delete the image from the local storage
        client.images.remove(f"{registry2_url}{image_name}")
        client.images.remove(f"{registry1_url}{image_name}")

        print(f"Successfully pulled and pushed {image_name} from {registry1_url} to {registry2_url}")
        end_time = time.time()
        tt = end_time - start_time
        print(f'time taken = {tt}')
    except docker.errors.APIError as e:
        print(f"Failed to pull and push image: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


pull_and_push_image(registry1_url, registry1_username, registry1_password, registry2_url, registry2_username,
                    registry2_password, image_name)
