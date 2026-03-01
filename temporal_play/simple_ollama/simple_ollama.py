"""
Yes I know there is an official client, I felt like writing one
"""

import json
from niquests import AsyncSession, Response


class SimpleOllamaClient:
    """Simple Ollama Client

    :param host: Host address
    :param port: Port number

    :returns: Nothing
    """

    def __init__(self, host: str, port: str | int) -> None:
        self._host = host
        self._port = port
        self._base_url = f"http://{self._host}:{self._port}"
        self._client = AsyncSession()
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def _get(self, url: str, params: dict | None = None) -> Response:
        """GET request

        :param url: URL
        :param params: URL parameters

        :returns: Response object
        """
        result = await self._client.get(url=url, headers=self._headers, params=params, timeout=5)

        if not result.ok:
            result.raise_for_status()

        return result

    async def _post(self, url: str, json_data: dict, params: dict | None = None) -> Response:
        """POST request

        :param url: URL
        :param json_data: JSON data
        :param params: URL parameters

        :returns: Response object
        """
        result = await self._client.post(url=url, headers=self._headers, params=params, json=json_data, timeout=60)

        if not result.ok:
            result.raise_for_status()

        return result

    async def chat(self, model: str, user_prompt: str, system_prompt: str = "") -> dict:
        """CHAT request

        :param model: The name of the model to run
        :param user_prompt: User prompt
        :param system_prompt: System prompt

        :returns: Dictionary of results
        """
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
        }
        result = await self._post(url=f"{self._base_url}/api/chat", json_data=data)

        return json.loads(result.text)

    async def get_models(self) -> dict:
        """Get models available

        :returns: Dictionary of models
        """
        result = await self._get(url=f"{self._base_url}/api/tags")

        return result.json()

    async def get_running_models(self) -> dict:
        """Get models that are currently running

        :returns: Dictionary of models
        """
        result = await self._get(url=f"{self._base_url}/api/ps")

        return result.json()
