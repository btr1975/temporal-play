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


def get_private_data_dir(private_data_dir: str) -> Path:
    """Get the absolute full path to the private_data_dir create if it does not already exist

    :type private_data_dir: String
    :param private_data_dir: The path to the private data directory

    :rtype: Path
    :returns: The path to the private data directory
    """
    pd_path = Path(private_data_dir).absolute()

    pd_path.mkdir(parents=True, exist_ok=True)

    return pd_path


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
    private_data_dir = get_private_data_dir(private_data_dir="/tmp/ansible_runner")

    return ansible_runner.run_async(
        private_data_dir=str(private_data_dir),
        playbook=str(playbook_path),
        project_dir=str(project_path),
        inventory=inventory,
    )


def create_ansible_inventory_from_nautobot_gql(nautobot_query_result: dict) -> dict:
    """A simple example of creating an Ansible inventory from nautobot_gql response

    :type nautobot_query_result: dict
    :param nautobot_query_result: The nautobot_gql response

    :rtype: dict
    :returns: Ansible inventory from nautobot_gql response

    :raises: ValueError: If something fails
    """
    inventory_starter = {
        "all": {
            "vars": {
                "ansible_connection": "ansible.netcommon.network_cli",
                "ansible_become": True,
                "ansible_become_method": "enable",
            },
            "hosts": {},
        }
    }

    for device in nautobot_query_result["data"]["devices"]:
        device_data = device.copy()
        device_hostname = device["hostname"]

        try:
            created = {
                device_hostname: {
                    "ansible_network_os": device["platform"]["network_driver_mappings"]["ansible"],
                    "ansible_host": device["primary_ip4"]["host"],
                }
            }
            created[device_hostname].update(device_data)

        except Exception as e:
            raise ValueError(f"failed to create ansible inventory for device {device_hostname}") from e

        inventory_starter["all"]["hosts"].update(created)

    return inventory_starter
