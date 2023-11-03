from flask import session
import docker
from docker.errors import APIError, DockerException, ImageNotFound

def push_docker_image(image, acr_login_server, acr_username, acr_password, tag='latest'):
    client = docker.from_env()
    try:
        client.login(username=acr_username, password=acr_password, registry=acr_login_server)
        print(f"Tagging image {image} with tag {tag}")
        client.images.push(f"{acr_login_server}/{image}", tag=tag)
        session['image_info'] = {
            'name': image,
            'tag': tag,
            'registry': acr_login_server
        }
        return session['image_info']
    except DockerException as login_err:
        print(f"Login error: {login_err}")
    except ImageNotFound as tag_err:
        print(f"Tagging error: {tag_err}")
    except IndexError as index_err:
        print(f"Index error: {index_err}")
    except APIError as push_err:
        print(f"Push error: {push_err}")
    return None
