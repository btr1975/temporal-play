"""
running ansible automations using ansible-runner
"""

from pathlib import Path
import ansible_runner
from ansible_runner.interface import Transmitter, Worker, Processor, Runner


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


def get_private_data_path(private_data_path: str) -> Path:
    """Get absolute path to the private data directory

    :type private_data_path: String
    :param private_data_path: The path to the Ansible project

    :rtype: Path
    :returns: The path to the folder

    :raises: FileNotFoundError: If the private data path does not exist
    """
    path = Path(private_data_path).absolute()

    if not path.is_dir():
        raise FileNotFoundError(f"directory '{path}' is not a found")

    return path


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


def run_playbook(playbook_name: str, path: str, private_data_path: str) -> Transmitter | Worker | Processor | Runner:
    """Function to run a playbook

    :type playbook_name: String
    :param playbook_name: The playbook name
    :type path: String
    :param path: The path to the Ansible project
    :type private_data_path: String
    :param private_data_path: The path to the private data directory

    :rtype: Transmitter | Worker | Processor | Runner
    :returns: Nothing it runs the playbook
    """
    project_path = get_project_path(path=path)
    playbook_path = get_playbook_path(path=path, playbook_name=playbook_name)
    pd_path = get_private_data_path(private_data_path=private_data_path)

    return ansible_runner.run(
        private_data_dir=pd_path,
        playbook=playbook_path,
        project_dir=project_path,
    )
