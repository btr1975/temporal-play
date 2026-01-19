"""
running ansible automations using ansible-runner

See Source: https://docs.ansible.com/projects/runner/en/stable/_modules/ansible_runner/interface/#run
"""

from pathlib import Path
import ansible_runner
from ansible_runner.interface import Runner


def get_project_path(path: str) -> Path:
    """Get absolute path to Ansible project

    :type path: String
    :param path: The path to the Ansible project

    :rtype: Path
    :returns: The path to the folder

    :raises: FileNotFoundError: If the project path does not exist
    """
    project_path = Path(path).absolute()

    if not project_path.is_dir():
        raise FileNotFoundError(f"directory '{project_path}' is not a found")

    return project_path


def get_playbook_path(path: str, playbook_name: str) -> Path:
    """Get the absolute full path to the playbook

    :type path: String
    :param path: The path to the Ansible project
    :type playbook_name: String
    :param playbook_name: The playbook name

    :rtype: Path
    :returns: The path to the playbook

    :raises: FileNotFoundError: If the playbook path does not exist
    """
    playbook_path = get_project_path(path=path).joinpath(playbook_name).absolute()

    if not playbook_path.is_file():
        raise FileNotFoundError(f"playbook '{playbook_path}' is not found")

    return playbook_path


def run_playbook(path: str, playbook_name: str, inventory: dict = None) -> Runner:
    """Function to run a playbook

    :type path: String
    :param path: The path to the Ansible project
    :type playbook_name: String
    :param playbook_name: The playbook name
    :type inventory: dict
    :param inventory: Ansible Inventory defaults to None

    :rtype: Runner
    :returns: Nothing it runs the playbook

    :raises: FileNotFoundError: If the required paths are not found
    """
    project_path = get_project_path(path=path)
    playbook_path = get_playbook_path(path=path, playbook_name=playbook_name)

    return ansible_runner.run_async(
        playbook=str(playbook_path),
        project_dir=str(project_path),
        inventory=inventory,
    )
