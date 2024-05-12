import os
import pprint
import yaml
from yaml import Loader

def load_ci_env(debug):
    print("> [Info] Gathering env variables")
    event = os.environ.get("GITHUB_EVENT_NAME", "")
    ref = os.environ.get("GITHUB_REF", "").replace("refs/heads/", "").replace("refs/tags/", "")
    build_info = {
        "branch": ref,
        "tag": ref if event == "release" else "",
        "event_type": event,
        "docker_reg_username": os.environ.get("DOCKER_USERNAME", ""),
        "docker_reg_password": os.environ.get("DOCKER_PASSWORD", ""),
    }
    if debug:
        print_debug_info(build_info)
    return build_info

def print_debug_info(build_info):
    pp = pprint.PrettyPrinter(indent=1)
    print(">> CI environment configuration: ")
    pp.pprint(build_info)
    print("\n")

def load_base_config():
    with open("base_config.yml") as base_config_file:
        base_config = base_config_file.read()
    return yaml.load(base_config, Loader=Loader)

def load_image_config(image_type, version):
    base_config_path = f"base_config.yml"
    image_config_path = f"{image_type}/config.yml"
    with open(base_config_path) as base_config_file:
        base_config = base_config_file.read()
    with open(image_config_path) as image_config_file:
        image_config = image_config_file.read()
    full_config = f"{base_config}\n{image_config}"
    config = yaml.load(full_config, Loader=Loader)

    validate_config(image_type, config, version)

    image_config = config["versions"][version] or dict()
    process_build_args(image_config)

    image_config["docker_hub_namespace"] = config["docker_hub_namespace"]

    return image_config

def validate_config(image_type, config, version):
    if "versions" not in config:
        raise KeyError(f"No configuration is set for this image - Image: {image_type}")
    if version not in config["versions"]:
        existing_versions = ", ".join(config["versions"].keys())
        raise KeyError(
            f"This version is not defined for {image_type} image - Defined versions: {existing_versions}"
        )

def process_build_args(image_config):
    if "build_args" in image_config:
        for arg, value in image_config["build_args"].items():
            image_config["build_args"][arg] = str(value)

def get_image_fullname(image_name, version, image_conf, env_conf):
    image_repo_name_base = f"{image_conf['docker_hub_namespace']}/ci-{image_name}"
    image_tag = get_image_tag(version, env_conf)
    return f"{image_repo_name_base}:{image_tag}"

def get_image_tag(version, env_conf):
    if env_conf["tag"]:
        return f'{version}-{env_conf["tag"]}'
    elif env_conf["event_type"] == "schedule":
        return f'{version}-nightly'
    elif env_conf["branch"] == "master":
        return f'{version}-latest'
    else:
        return f'{version}-latest'

def get_image_tags(image_name, version, image_conf, env_conf):
    image_repo_name_base = f"{image_conf['docker_hub_namespace']}/ci-{image_name}"
    local_repo_name_base = f"localhost:5000/ci-{image_name}"
    version_tag = get_image_tag(version, env_conf)

    tags = {
        "fullname": f"{image_repo_name_base}:{version_tag}",
        "localname": f"{local_repo_name_base}:{version_tag}",
        "platforms": {},
    }
    for platform in image_conf.get("platforms", []):
        _os, _arch, _variant = parse_platform(platform)
        tags["platforms"][platform] = f"{image_repo_name_base}-{_arch}:{version_tag}"
    return tags

def parse_platform(platform):
    parts = platform.split("/")
    parts.extend([None])
    return parts[:3]
