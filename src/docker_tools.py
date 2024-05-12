import os
import pprint
import subprocess
from python_on_whales import docker
from python_on_whales.exceptions import DockerException

def login_to_ghcr(username, token):
    print("> [Info] Login to GitHub Container Registry (ghcr.io)")
    try:
        # Run the docker login command with subprocess
        login_command = f"docker login ghcr.io -u {username} -p {token}"
        subprocess.run(login_command, shell=True, check=True)
        print("Login successful")
    except subprocess.CalledProcessError as error:
        print("> [Error] Login failed - " + str(error))
        exit(1)

def build_image(image_conf, image_tag, dockerfile_directory, dockerfile_path, debug):
    print("> [Info] Building: " + image_tag)
    try:
        if debug:
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

        # Create a buildx builder instance
        builder = docker.buildx.create(
            use=True, driver_options=dict(network="host"))

        # Build and push to local registry
        docker.buildx.build(
            builder=builder,
            file=os.path.join(dockerfile_directory, dockerfile_path),
            context_path=dockerfile_directory,
            tags=image_tag,
            cache=False,
            push=True,
            build_args=image_conf["build_args"] if "build_args" in image_conf else {},
            platforms=image_conf["platforms"]
        )  

    except DockerException as docker_exception:
        print("> [Error] Build error - " + str(docker_exception))
        exit(1)
    finally:
        builder.remove()

    print("Build successful")

def run_image(image_name, image_conf, debug):
    volume = []

    print("> [Info] Testing " + image_name)

    try:
        if "test_config" in image_conf:
            test_config = image_conf["test_config"]
            if "volume" in test_config:
                # Split path:directory string and build volume dict
                splitted_volume = test_config["volume"].split(":")
                volume = [(f"{os.getcwd()}/{splitted_volume[0]}",
                          splitted_volume[1],
                          "ro")]
            for cmd in test_config["cmd"]:
                cmd_list = cmd.split(" ")
                if debug:
                    print(">> Running test: " + str(cmd_list))
                for platform in image_conf["platforms"]:
                    container_output = docker.container.run(
                        image=image_name,
                        platform=platform,
                        command=cmd_list,
                        volumes=volume
                    )
                    if debug:
                        print(container_output)
        print("Tests successful")
    except DockerException as e:
        print("> [Error] Command test failed - " + str(e))
        exit(1)
    finally:
        docker.container.prune()

def tag_image(image, tag):
    docker.image.tag(image, tag)

def start_local_registry():
    return docker.run("registry:2", detach=True, publish=[(5000, 5000)], restart='always', name='registry')

def push_image(image_fullname):
    print("> [Info] Pushing " + image_fullname)
    try:
        docker.image.push(image_fullname)
        print("Push successful")
    except DockerException as docker_exception:
        print("> [Error] Push failed - " + str(docker_exception))
        exit(1))
