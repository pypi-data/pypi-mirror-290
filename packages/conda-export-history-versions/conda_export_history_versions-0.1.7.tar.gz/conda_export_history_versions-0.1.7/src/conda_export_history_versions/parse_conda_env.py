import argparse
import json
import subprocess
from typing import Dict, List, Optional

import yaml


def run_command(command: List[str]) -> str:
    """
    Run a shell command and return its output.

    Args:
        command (List[str]): The command to run as a list of strings.

    Returns:
        str: The output of the command.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Error message: {e.stderr}")
        raise


def get_conda_env_export(env_name: Optional[str] = None) -> Dict:
    """
    Get the conda environment export as a dictionary.

    Args:
        env_name (Optional[str]): The name of the conda environment.

    Returns:
        Dict: The conda environment export as a dictionary.
    """
    command = ["conda", "env", "export", "--from-history"]
    if env_name:
        command.extend(["-n", env_name])
    env_yaml = run_command(command)
    return yaml.safe_load(env_yaml)


def get_conda_list(env_name: Optional[str] = None) -> List[Dict]:
    """
    Get the conda list as a list of dictionaries.

    Args:
        env_name (Optional[str]): The name of the conda environment.

    Returns:
        List[Dict]: The conda list as a list of dictionaries.
    """
    command = ["conda", "list", "--json"]
    if env_name:
        command.extend(["-n", env_name])
    conda_list_json = run_command(command)
    return json.loads(conda_list_json)


def update_dependencies(env_dict: Dict, conda_list: List[Dict]) -> Dict:
    """
    Update the dependencies in the environment dictionary with version information.

    Args:
        env_dict (Dict): The environment dictionary.
        conda_list (List[Dict]): The conda list.

    Returns:
        Dict: The updated environment dictionary.
    """
    dependencies = env_dict.get("dependencies", [])
    package_dict = {package["name"]: package["version"] for package in conda_list}

    updated_dependencies = [
        f"{package}=={package_dict[package]}" if package in package_dict else package
        for package in dependencies
    ]

    env_dict["dependencies"] = sorted(updated_dependencies)
    env_dict.pop("prefix", None)
    return env_dict


def export_yaml(data: Dict, file_path: Optional[str] = None) -> None:
    """
    Export the data as YAML to a file or print to console.

    Args:
        data (Dict): The data to export.
        file_path (Optional[str]): The file path to write the YAML. If None, print to console.
    """
    yaml_output = yaml.dump(data, default_flow_style=False, sort_keys=False)
    yaml_output = yaml_output.replace("- ", "  - ")  # Improve indentation

    if file_path:
        with open(file_path, "w") as f:
            f.write(yaml_output)
    else:
        print(yaml_output)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Export conda environment with version information."
    )
    parser.add_argument("-f", "--file", help="Export the modified yml into a file")
    parser.add_argument("-n", "--name", help="Name of the conda environment")
    return parser.parse_args()


def main() -> None:
    """
    Main function to export conda environment with version information.
    """
    args = parse_arguments()

    env_dict = get_conda_env_export(args.name)
    conda_list = get_conda_list(args.name)
    updated_env_dict = update_dependencies(env_dict, conda_list)
    export_yaml(updated_env_dict, args.file)


if __name__ == "__main__":
    main()
