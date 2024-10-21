import docker
import pandas as pd

DOCKER_CLIENT = docker.from_env()
IMAGE_NAME = "IMAGE_NAME" # electronic-python
VERSION_IMAGE = "VERSION_IMAGE" # 1.0.0
CONTAINER_NAME = "CONTAINER_NAME" # electronic-python
AUTO = True

def get_docker_images() -> list:

    docker_images = [x.tags[0] for x in DOCKER_CLIENT.images.list()]

    return docker_images

def get_data_frame_docker_images(docker_images: list = None) -> pd.DataFrame:

    if not docker_images:

        docker_images = get_docker_images()

    data_frame_docker_images = pd.DataFrame(data=docker_images, columns=["images"])

    return data_frame_docker_images

def print_data_frame_docker_images(data_frame_docker_images: pd.DataFrame = None) -> None:

    if not data_frame_docker_images:

        data_frame_docker_images = get_data_frame_docker_images()

    print(data_frame_docker_images)

def exist_docker_image(docker_image: str = None) -> bool:

    docker_images = get_docker_images()

    return docker_image in docker_images

def remove_docker_image(docker_image: str = IMAGE_NAME, version_image: str = VERSION_IMAGE) -> bool:

    if exist_docker_image(f"{docker_image}:{version_image}"):

        DOCKER_CLIENT.images.remove(f"{docker_image}:{version_image}", noprune=False)

        DOCKER_CLIENT.images.prune(filters={"dangling": True})

        print(f"{docker_image}:{version_image} was removed")

        return True

    else:

        print(f"{docker_image}:{version_image} was not found")

        return False

def create_docker_image(docker_image: str = IMAGE_NAME, version_image: str = VERSION_IMAGE) -> bool:

    if not exist_docker_image(f"{docker_image}:{version_image}"):

        print(f"{docker_image}:{version_image} is being created....")

        DOCKER_CLIENT.images.build(path=".", tag=f"{docker_image}:{version_image}", rm=True, forcerm=True)

        print(f"{docker_image}:{version_image} was created")

        return True

    else:

        print(f"{docker_image}:{version_image} already exist")

        return False

try:

    print_data_frame_docker_images()

    remove_docker_image()

    create_docker_image()

    print_data_frame_docker_images()

except Exception as e:

    print(e)
