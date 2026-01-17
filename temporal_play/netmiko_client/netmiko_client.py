"""
Netmiko Client
"""

import asyncio
from netmiko import ConnectHandler


class NetmikoClient:
    """Client for Netmiko

    :param host: The host to connect to
    :type host: str
    :param username: The hosts username
    :type username: str
    :param password: The hosts password
    :type password: str
    :param device_type: The netmiko device type
    :type device_type: str

    """

    def __init__(self, host: str, username: str, password: str, device_type: str) -> None:
        self._client = ConnectHandler(host=host, username=username, password=password, device_type=device_type)

    async def send_command(self, command: str) -> str:
        """Sends command to a device

        :param command: The command to send
        :type command: str

        :rtype: str
        :return: The result of the command
        """
        result = await asyncio.to_thread(self._client.send_command, command_string=command)

        return result

    async def send_command_parse_ntc_templates(self, command: str) -> list[dict]:
        """Sends command to a device and parse with NTC-Templates

        :param command: The command to send
        :type command: str

        :rtype: list[dict]
        :return: The result of the command
        """
        result = await asyncio.to_thread(self._client.send_command, command_string=command, use_textfsm=True)

        return result

    async def send_command_parse_textfsm(self, command: str, textfsm_template: str) -> list[dict]:
        """Sends command to a device and parse with textfsm

        :param command: The command to send
        :type command: str
        :param textfsm_template: The textfsm template to use
        :type textfsm_template: str

        :rtype: list[dict]
        :return: The result of the command
        """
        result = await asyncio.to_thread(
            self._client.send_command, command_string=command, use_textfsm=True, textfsm_template=textfsm_template
        )

        return result

    async def send_command_parse_ttp(self, command: str, ttp_template: str) -> list[dict]:
        """Sends command to a device and parse with ttp

        :param command: The command to send
        :type command: str
        :param ttp_template: The ttp template to use
        :type ttp_template: str

        :rtype: list[dict]
        :return: The result of the command
        """
        result = await asyncio.to_thread(
            self._client.send_command, command_string=command, use_ttp=True, ttp_template=ttp_template
        )

        return result

    async def send_command_parse_genie(self, command: str) -> dict:
        """Sends command to a device and parse with Genie

        :param command: The command to send
        :type command: str

        :rtype: dict
        :return: The result of the command
        """
        result = await asyncio.to_thread(self._client.send_command, command_string=command, use_genie=True)

        return result
