import os
import pprint

from python_on_whales import docker
from python_on_whales.exceptions import DockerException
import src.docker_tools as docker_tools

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

# Modify other functions as needed

def build(image, version, debug):
    # Get env variables
    env_conf = config.load_ci_env(debug)

    # Get image configuration
    try:
        image_conf = config.load_image_config(image, version)
    except KeyError as e:
        print(e)
        exit(1)

    # Build dockerfile directory and path
    dockerfile_directory = image
    prefixed_dockerfile_path = f"{version}/Dockerfile"
    # Set the subdirectory in path because we want dockerfile_directory (aka the build context) to be the parent image directory
    dockerfile_path = prefixed_dockerfile_path if os.path.exists(
        f"{dockerfile_directory}/{prefixed_dockerfile_path}") else "Dockerfile"

    # Build image tags list (base tag + archs)
    image_tags = config.get_image_tags(image, version, image_conf, env_conf)

    with docker_tools.start_local_registry() as local_registry:
        # Build, tag and push docker image to local registry
        docker_tools.build_image(
            image_conf, image_tags["localname"], dockerfile_directory, dockerfile_path, debug)
        
        # Run defined test command
        docker_tools.run_image(image_tags["localname"], image_conf, debug)

        # Push to registry in case of:
        # - tag
        # - push to master
        # - nightly build
        if (
            env_conf["tag"] != ""
            or (env_conf["event_type"] != "pull_request" and env_conf["branch"] == "master")
            or env_conf["event_type"] == "schedule"
        ):
            # Login to registry and push
            docker_tools.login_to_registry("${{ github.actor }}", "${{ secrets.GITHUB_TOKEN }}")

            # Build, tag and push docker image to remote registry (Docker hub)
            docker_tools.build_image(
                image_conf, image_tags["fullname"], dockerfile_directory, dockerfile_path, debug)
