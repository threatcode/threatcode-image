import json
import os
from git import Repo
import yaml

excluded_files = [
    '.gitignore',
    'CHANGELOG.md',
    'README.md',
    '.github/dependabot.yml',
]


def get_diff_files_list():
    repo = Repo('.')
    modified_files = repo.commit("origin/master").diff(repo.commit())
    changed_files = [item.a_path for item in modified_files]
    return changed_files


def filter_excluded_files(changed_files):
    return [file for file in changed_files if file not in excluded_files]


def get_paths(changed_files):
    paths = set()
    if not changed_files:
        return glob("*/") if not unfiltered_files else []

    for file in changed_files:
        if "/" not in file or "/src" in file or ".github" in file:
            return glob("*/")
        else:
            split_path = file.split("/")
            paths.add(split_path[0])
    return paths


def generate_matrix(paths):
    matrix = {"include": []}
    for image_folder in paths:
        config_path = os.path.join(image_folder, "config.yml")
        if os.path.exists(config_path):
            with open("base_config.yml", 'r') as base_config:
                with open(config_path, 'r') as config:
                    full_config = base_config.read() + config.read()
                    image_config = yaml.safe_load(full_config)

                    for version in image_config.get("versions", []):
                        matrix["include"].append({
                            "image": image_folder.replace("/", ""),
                            "version": str(version)
                        })
    print(json.dumps(matrix))


def main():
    changed_files = get_diff_files_list()
    filtered_files = filter_excluded_files(changed_files)
    paths = get_paths(filtered_files)
    generate_matrix(paths)


if __name__ == "__main__":
    main()
