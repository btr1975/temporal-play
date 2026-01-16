"""
nautobot_gql_client
"""

import niquests


class NautobotGqlClient:  # pylint: disable=too-few-public-methods
    """A Natuobot client for gql

    :param host: Nautobot server host
    :type host: str
    :param port: Nautobot server port
    :type port: int
    :param token: Nautobot server token
    :type token: str
    :param ssl_verify: SSL verification
    :type ssl_verify: bool
    """

    def __init__(self, host: str, port: int, token: str, ssl_verify: bool | str = True) -> None:
        self._headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self._base_url = f"{host}:{port}/api"

        self._session = niquests.AsyncSession()
        self._session.headers.update(self._headers)
        self._session.verify = ssl_verify

    async def get_gql_data(self, query: str, variables: dict = None) -> dict:
        """Get data from Nautobot via GraphQL Query

        :param query: GraphQL query
        :type query: str
        :param variables: GraphQL variables
        :type variables: dict

        :rtype: dict
        :return: nautobot gql data
        """
        json_data = {
            "query": query,
        }
        if variables:
            json_data.update({"variables": variables})

        result = await self._session.post(url=f"{self._base_url}/graphql/", json=json_data, timeout=20, verify=False)

        if not result.ok:
            result.raise_for_status()

        return result.json()
