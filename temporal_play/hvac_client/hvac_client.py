"""
hvac client
"""

import asyncio
import hvac


class HvacClient:  # pylint: disable=too-few-public-methods
    """Hashicorp Vault Client

    :param host: HVAC API host
    :type host: str
    :param port: HVAC API port
    :type port: int | str
    :param token: HVAC API token
    :type token: str
    """

    def __init__(self, host: str, port: int | str, token: str) -> None:
        self._client = hvac.Client(url=f"{host}:{port}", token=token)

    async def get_secret(self, path: str, key: str = None) -> str | dict | None:
        """Method to get secret key from a path

        :param path: Path to secret
        :type path: str
        :param key: The key name, if set to None will give back all keys
        :type key: str | None

        :rtype: str | dict
        :returns: The secret
        """
        data = await asyncio.to_thread(self._client.secrets.kv.v2.read_secret_version, path=path, mount_point="secret")

        if key is None:
            return data["data"]["data"]

        return data["data"]["data"].get(key)
