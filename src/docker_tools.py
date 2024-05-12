import os
import pprint
from python_on_whales import docker
from python_on_whales.exceptions import DockerException

def build_image(image_conf, image_tag, dockerfile_directory, dockerfile_path, debug):
    print("> [Info] Building: " + image_tag)
    builder = None
    try:
        if debug:
            print_debug_info(image_conf, dockerfile_directory, dockerfile_path)

        # Create a buildx builder instance
        builder = docker.buildx.create(use=True, driver_options=dict(network="host"))

        # Build and push to local registry
        docker.buildx.build(
            builder=builder,
            file=os.path.join(dockerfile_directory, dockerfile_path),
            context_path=dockerfile_directory,
            tags=image_tag,
            cache=False,
            push=True,
            build_args=image_conf.get("build_args", {}),
            platforms=image_conf["platforms"]
        )  

    except DockerException as docker_exception:
        handle_exception("Build error", docker_exception)
    finally:
        if builder:
            builder.remove()
    print("Build successful")

def print_debug_info(image_conf, dockerfile_directory, dockerfile_path):
    pp = pprint.PrettyPrinter(indent=1)
    print(">> Building configuration: ")
    pp.pprint(image_conf)
    print("\n")
    print(">> Dockerfile directory: ")
    print(dockerfile_directory)
    print("\n")
    print(">> Dockerfile relative path: ")
    print(dockerfile_path)
    print("\n")

def handle_exception(message, exception):
    print(f"> [Error] {message} - {exception}")
    exit(1)

def run_image(image_name, image_conf, debug):
    volume = []
    print("> [Info] Testing " + image_name)
    try:
        if "test_config" in image_conf:
            test_config = image_conf["test_config"]
            volume = get_volume(test_config)
            run_tests(image_name, image_conf["platforms"], test_config["cmd"], volume, debug)
        print("Tests successful")
    except DockerException as e:
        handle_exception("Command test failed", e)
    finally:
        docker.container.prune()

def get_volume(test_config):
    volume = []
    if "volume" in test_config:
        src, dst = test_config["volume"].split(":")
        volume = [(f"{os.getcwd()}/{src}", dst, "ro")]
    return volume

def run_tests(image_name, platforms, commands, volume, debug):
    for cmd in commands:
        cmd_list = cmd.split(" ")
        if debug:
            print(f">> Running test: {cmd_list}")
        for platform in platforms:
            container_output = docker.container.run(
                image=image_name,
                platform=platform,
                command=cmd_list,
                volumes=volume
            )
            if debug:
                print(container_output)

def tag_image(image, tag):
    docker.image.tag(image, tag)

def start_local_registry():
    print("> [Info] Starting local registry")
    try:
        return docker.run("registry:2", detach=True, publish=[(5000, 5000)], restart='always', name='registry')
    except DockerException as e:
        handle_exception("Failed to start local registry", e)

def login_to_registry(env_conf):
    print("> [Info] Login to registry")
    try:
        docker.login(username=env_conf["docker_reg_username"], password=env_conf["docker_reg_password"])
        print("Login successful")
    except DockerException as e:
        handle_exception("Login failed", e)

def push_image(image_fullname):
    print("> [Info] Pushing " + image_fullname)
    try:
        docker.image.push(image_fullname)
        print("Push successful")
    except DockerException as e:
        handle_exception("Push failed", e)
