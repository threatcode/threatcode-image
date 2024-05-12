from os.path import exists

import click
from python_on_whales import docker

import src.config as config
import src.docker_tools as docker_tools


@click.command()
@click.option("--image", "-i", default="aws", help="image to build")
@click.option("--version", "-v", default="1", help="image version")
@click.option("--debug", "-d", is_flag=True, help="debug")
def build(image, version, debug):
    try:
        # Load environment variables
        env_conf = config.load_ci_env(debug)

        # Load image configuration
        image_conf = config.load_image_config(image, version)

        # Determine Dockerfile path
        dockerfile_directory = image
        prefixed_dockerfile_path = f"{version}/Dockerfile"
        dockerfile_path = prefixed_dockerfile_path if exists(
            f"{dockerfile_directory}/{prefixed_dockerfile_path}") else "Dockerfile"

        # Build image tags list (base tag + archs)
        image_tags = config.get_image_tags(image, version, image_conf, env_conf)

        with docker_tools.start_local_registry() as local_registry:
            # Build, tag, and push docker image to local registry
            docker_tools.build_image(image_conf, image_tags["localname"], dockerfile_directory, dockerfile_path, debug)

            # Run defined test command
            docker_tools.run_image(image_tags["localname"], image_conf, debug)

            # Push to registry if necessary
            if (
                env_conf["tag"] != ""
                or (env_conf["event_type"] != "pull_request" and env_conf["branch"] == "master")
                or env_conf["event_type"] == "schedule"
            ):
                # Login to registry and push
                docker_tools.login_to_registry(env_conf)
                # Build, tag, and push docker image to remote registry (Docker hub)
                docker_tools.build_image(image_conf, image_tags["fullname"], dockerfile_directory, dockerfile_path, debug)

    except KeyError as e:
        click.echo(f"Error: {e}")
        exit(1)


@click.group()
def cli():
    pass


cli.add_command(build)


if __name__ == "__main__":
    cli()
