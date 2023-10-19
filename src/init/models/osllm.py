# from init  import db


class OSLLM:
    def __init__(
        self,
        id,
        name,
        description,
        docker_image_url,
        type,
        uuid,
        version,
        is_active,
        tags,
        created_at,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.docker_image_url = docker_image_url
        self.type = type
        self.uuid = uuid
        self.version = version
        self.is_active = is_active
        self.tags = tags
        self.created_at = created_at

    def __str__(self):
        return f"OSLLM(id={self.id}, name={self.name}, description={self.description}, docker_image_url={self.docker_image_url}, type={self.type}, uuid={self.uuid}, version={self.version}, is_active={self.is_active}, tags={self.tags}, created_at={self.created_at})"
