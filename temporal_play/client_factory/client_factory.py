"""
Client factory
"""

from typing import Sequence, Any
import inspect
from concurrent.futures import ThreadPoolExecutor
import logging

from temporalio.client import Client
from temporalio.worker import Worker


class BasicClientFactory:
    """Basic client factory

    :param host: The Temporal host
    :param port: The Temporal hosts port
    :param namespace: The Temporal namespace

    :return: Nothing
    """

    def __init__(self, host: str, port: str | int, namespace: str) -> None:
        self._host = host
        self._port = port
        self._namespace = namespace

    @classmethod
    def create(cls, host: str, port: int, namespace: str = "default") -> "BasicClientFactory":
        """Create a basic client

        :param host: The Temporal host
        :param port: The Temporal hosts port
        :param namespace: The Temporal namespace

        :return: BasicClientFactory
        """
        return cls(host=host, port=port, namespace=namespace)

    async def get_client(self) -> Client:
        """Get the client

        :return: The Temporal client
        """
        client = await Client.connect(target_host=f"{self._host}:{self._port}", namespace=self._namespace)

        return client

    async def get_worker(self, task_queue: str, workflows: Sequence[type], activities: Sequence[Any]) -> Worker:
        """Get the worker

        :param task_queue: Temporal task queue name
        :param workflows: Temporal workflows the worker will work
        :param activities: Temporal activities the worker will use

        :return: The Temporal Worker
        """
        client = await self.get_client()

        logging.basicConfig(level=logging.INFO)
        if all(inspect.iscoroutinefunction(activity) for activity in activities):
            logging.info("Using Async Worker")
            worker = Worker(
                client=client,
                task_queue=task_queue,
                workflows=workflows,
                activities=activities,
            )

        else:
            logging.info("Using ThreadPoolExecutor Worker")
            worker = Worker(
                client=client,
                task_queue=task_queue,
                workflows=workflows,
                activities=activities,
                activity_executor=ThreadPoolExecutor(max_workers=50),
            )

        return worker

    async def get_nexus_worker(
        self, task_queue: str, workflows: Sequence[type], nexus_service_handlers: Sequence[Any]
    ) -> Worker:
        """Get the worker

        :param task_queue: Temporal task queue name
        :param workflows: Temporal workflows the worker will work
        :param nexus_service_handlers: Temporal Nexus service handlers this worker will use

        :return: The Temporal Nexus Worker
        """
        client = await self.get_client()

        logging.basicConfig(level=logging.INFO)

        logging.info("Starting Nexus Worker")
        worker = Worker(
            client=client,
            task_queue=task_queue,
            workflows=workflows,
            nexus_service_handlers=nexus_service_handlers,
        )

        return worker
