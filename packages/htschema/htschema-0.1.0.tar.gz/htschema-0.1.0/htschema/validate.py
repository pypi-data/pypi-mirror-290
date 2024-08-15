from jsonschema import validate, ValidationError
import json
import yaml
import os
from datetime import datetime
import click


def convert_datetime_to_string(data):
    if isinstance(data, dict):
        return {k: convert_datetime_to_string(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_datetime_to_string(v) for v in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data


@click.group()
def cli() -> None:
    pass

@cli.command("validate", help="Validate a meta.yml or multiple meta.yml files versus the HathiTrust Schema")
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True, file_okay=False, readable=True),
    help="Path to directory containing meta.yml files",
)
def validate_files(path: str) -> None:
    schema_path = 'schemas/ht.json'

    try:
        with open(schema_path, 'r') as schema_file:
            schema = json.load(schema_file)
    except (IOError, json.JSONDecodeError) as e:
        click.echo(f"Error loading schema: {e}")
        return

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".yml") or file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as yaml_file:
                        current_map = yaml.safe_load(yaml_file)
                        current_map = convert_datetime_to_string(current_map)
                        validate(instance=current_map, schema=schema)
                        click.echo(f"{file_path} is valid.")
                except (IOError, yaml.YAMLError, ValidationError) as e:
                    click.echo(f"Validation error in {file_path}: {e}")
