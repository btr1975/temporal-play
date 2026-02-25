"""
A Git Client
"""

from shutil import rmtree
import asyncio
from pathlib import Path
import urllib.parse
from git import Repo


class GitClient:
    """A Git Client to clone repositories

    :param username: GitHub username
    :param password: GitHub password or token
    :param repository: A GitHub https repository
    :param clone_path: Path to clone to

    :returns: Nothing
    """

    def __init__(self, username: str, password: str, repository: str, clone_path: str) -> None:
        self._username = username
        self._password = password
        self._clone_path: Path = Path(clone_path)

        self._split_url = urllib.parse.urlsplit(repository)

        if self._split_url.scheme != "https":
            raise ValueError(f"invalid URL scheme the url must be https, but yours is {self._split_url.scheme}!")

        self._repository = repository

    def _get_auth_url(self) -> str:
        """Cleans up the auth url

        :returns: Auth url
        """
        safe_username = urllib.parse.quote(self._username)
        safe_password = urllib.parse.quote(self._password)
        return (
            f"{self._split_url.scheme}://{safe_username}:{safe_password}@{self._split_url.hostname}"
            f"{self._split_url.path}"
        )

    async def clone(self, branch_or_tag: str = None) -> None:
        """Clones the repository

        :param branch_or_tag: Branch or tag to clone default: None

        :returns: Nothing
        """
        url = self._get_auth_url()

        cloned_repo = await asyncio.to_thread(
            Repo.clone_from,
            url=url,
            to_path=self._clone_path.as_posix(),
        )

        await asyncio.to_thread(cloned_repo.git.fetch, "--all", "--tags")

        if branch_or_tag:
            await asyncio.to_thread(cloned_repo.git_checkout, branch_or_tag)

    async def remove_directory(self) -> None:
        """Removes the repository directory

        :returns: Nothing
        """
        if self._clone_path.is_dir():
            await asyncio.to_thread(rmtree, path=self._clone_path.as_posix(), ignore_errors=False, onerror=None)
