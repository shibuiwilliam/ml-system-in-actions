import os
from distutils.dir_util import copy_tree
from typing import Dict

import click
import yaml
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIRECTORY = "./template"
TEMPLATE_FILES_DIRECTORY = "./template_files"


def load_variable(
    variable_file: str,
) -> Dict:
    with open(variable_file, "r") as f:
        variables = yaml.load(
            f,
            Loader=yaml.SafeLoader,
        )
    return variables


def format_path(
    correspond_file_paths: Dict,
    name: str,
) -> Dict:
    formatted_correspond_file_paths: Dict = {}
    for k, v in correspond_file_paths.items():
        formatted_correspond_file_paths[k] = v.format(name)
    return formatted_correspond_file_paths


def copy_directory(name: str):
    copy_tree(TEMPLATE_DIRECTORY, name)


def build(
    template_file_name: str,
    output_file_path: str,
    variables: Dict,
):
    env = Environment(
        loader=FileSystemLoader("./", encoding="utf8"),
    )

    tmpl = env.get_template(
        os.path.join(
            TEMPLATE_FILES_DIRECTORY,
            template_file_name,
        ),
    )

    file = tmpl.render(**variables)

    with open(output_file_path, mode="w") as f:
        f.write(str(file))


@click.command(help="template pattern")
@click.option(
    "--name",
    type=str,
    required=True,
    help="name of project",
)
@click.option(
    "--variable_file",
    type=str,
    default="vars.yaml",
    required=True,
    help="path to variable file yaml",
)
@click.option(
    "--correspond_file_path",
    type=str,
    default="correspond_file_path.yaml",
    required=True,
    help="file defining corresponding file path",
)
def main(
    name: str,
    variable_file: str,
    correspond_file_path: str,
):
    variables = load_variable(
        variable_file=variable_file,
    )
    correspond_file_paths = load_variable(
        variable_file=correspond_file_path,
    )
    formatted_correspond_file_paths = format_path(
        correspond_file_paths=correspond_file_paths,
        name=name,
    )
    os.makedirs(name, exist_ok=True)
    copy_directory(name=name)
    for k, v in formatted_correspond_file_paths.items():
        build(
            template_file_name=k,
            output_file_path=v,
            variables=variables,
        )


if __name__ == "__main__":
    main()
