from flask import session
import docker
from docker.errors import APIError, DockerException, ImageNotFound

def push_docker_image(image, acr_login_server, acr_username, acr_password, tag='latest'):
        try:
            client = docker.from_env()
            client.login(username=acr_username, password=acr_password, registry=acr_login_server)
            full_image_name = image.tags[0]
            image_name = full_image_name.split('/')[-1].split(':')[0]
            print(f"Tagging image {image_name} with tag {tag}")
            image.tag(f"{acr_login_server}/{image_name}", tag=tag)
            client.images.push(f"{acr_login_server}/{image_name}", tag=tag)
            session['image_info'] = {
                'name': image_name,
                'tag': tag,
                'registry': acr_login_server
            }
            return session['image_info']
        except DockerException as login_err:
            print(f"Login error: {login_err}")
            return None
        except ImageNotFound as tag_err:
            print(f"Tagging error: {tag_err}")
            return None
        except IndexError as index_err:
            print(f"Index error: {index_err}")
            return None
        except APIError as push_err:
            print(f"Push error: {push_err}")
            return None